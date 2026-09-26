"""Verify whole-contract review receipts; screening is not pattern qualification."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

from review_all_patterns import ROOT, catalogs, inventory

sys.path.insert(0, str(ROOT / "skills/jev-question-kernel-catalog/scripts"))
from check_confidence import check_answer


def canonical(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode()


def validate_answer(question, answer):
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        raise ValueError("invalid screening primitive")
    labels = question["criteria"]
    p = answer.get("probabilities")
    if not isinstance(p, dict) or set(p) != set(labels):
        raise ValueError("screening probability coverage")
    values = [answer.get("confidence"), *p.values()]
    if not all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 1 for v in values):
        raise ValueError("invalid screening probability")
    if not math.isclose(sum(p.values()), 1, rel_tol=0, abs_tol=.005 * len(p) + 1e-12):
        raise ValueError("screening probability sum")
    choice = answer.get("choice")
    if not isinstance(choice, str) or choice not in labels or p[choice] < max(p.values()):
        raise ValueError("invalid screening selection")
    problem = check_answer(answer)
    if problem:
        raise ValueError("screening confidence: " + problem)


def verify(folder, root=ROOT):
    folder, root = folder.resolve(), root.resolve()
    contract = json.loads((folder / "semantic-screen-contract.json").read_text())
    patterns = {str(path.parent.relative_to(root)) + "/" + p["id"]: p
                for path in catalogs(root)
                for p in json.loads(path.read_text())["patterns"]}
    seen = {}
    counts = {}
    batches = set()
    files = sorted(folder.glob("semantic-screen-[0-9][0-9][0-9].json"))
    for path in files:
        for receipt in json.loads(path.read_text()):
            if receipt["batch"] in batches:
                raise ValueError("duplicate screening batch")
            batches.add(receipt["batch"])
            req, resp = receipt["request"], receipt["response"]
            if resp.get("ok") is not True or resp.get("advisory_only") is not True:
                raise ValueError("provider failure or non-advisory receipt")
            if req.get("use_cache") is not False or resp.get("cached") is not False:
                raise ValueError("cached screening")
            if req["state"]["source_commit"] != contract["source_commit"]:
                raise ValueError("screen source mismatch")
            signed = {"state": req["state"], "questions": req["questions"], "model": resp["model"]}
            if hashlib.sha256(canonical(signed)).hexdigest() != resp.get("request_sha256"):
                raise ValueError("screen request digest mismatch")
            expected_questions = {}
            for slot, row in req["state"]["patterns"].items():
                key = row["key"]
                if key in seen or patterns.get(key) != row["pattern"]:
                    raise ValueError("duplicate or stale screened pattern: " + key)
                answers = {}
                for dimension, q in contract["dimensions"].items():
                    qid = slot + "_" + dimension
                    question = {**q, "instructions": "Evaluate ONLY patterns." + slot
                                + ".pattern; its key is " + key + ". " + q["instructions"]}
                    expected_questions[qid] = question
                    answer = resp["answers"][qid]
                    validate_answer(question, answer)
                    answers[dimension] = answer
                    label = dimension + ":" + answer["choice"]
                    counts[label] = counts.get(label, 0) + 1
                seen[key] = {"screen_answers": answers, "screen_receipt": str(path.relative_to(root)),
                             "batch": receipt["batch"], "host_review": "pending"}
            if req["questions"] != expected_questions or set(resp["answers"]) != set(expected_questions):
                raise ValueError("screen question or answer coverage mismatch")
    if set(seen) != set(patterns):
        raise ValueError("screen profile coverage incomplete")
    rows = [{**row, **seen[row["key"]]} for row in inventory(root)]
    return {"profiles": len(rows), "batches": len(batches), "counts": counts, "patterns": rows,
            "scope": "Verified advisory screen only. Host review, live behavior boundaries, and qualification are not implied."}


def verify_boundaries(folder, root=ROOT):
    fixtures = json.loads((folder / "boundary-fixtures-wave01.json").read_text())["cases"]
    receipts = json.loads((folder / "boundary-receipts-wave01.json").read_text())
    patterns = {str(path.parent.relative_to(root)) + "/" + p["id"]: p
                for path in catalogs(root)
                for p in json.loads(path.read_text())["patterns"]}
    by_id = {r["fixture_id"]: r for r in receipts}
    if len(by_id) != len(receipts) or set(by_id) != {f["id"] for f in fixtures}:
        raise ValueError("boundary receipt coverage")
    result = []
    for f in fixtures:
        r = by_id[f["id"]]
        p = patterns[f["key"]]
        req, resp = r["request"], r["response"]
        if (r["pattern_key"] != f["key"] or r["contract_version"] != p.get("version", p.get("contract_version"))
                or req["state"] != f["state"] or req["questions"] != p["questions"]
                or resp.get("ok") is not True or resp.get("advisory_only") is not True
                or req.get("use_cache") is not False or resp.get("cached") is not False):
            raise ValueError("boundary binding or provider failure")
        signed = {"state": req["state"], "questions": req["questions"], "model": resp["model"]}
        if hashlib.sha256(canonical(signed)).hexdigest() != resp.get("request_sha256"):
            raise ValueError("boundary digest mismatch")
        if set(resp["answers"]) != set(p["questions"]):
            raise ValueError("boundary answer coverage")
        for qid, question in p["questions"].items():
            validate_answer(question, resp["answers"][qid])
        answer = resp["answers"]["decision"]
        result.append({"id": f["id"], "key": f["key"], "expected": f["expected"],
                       "observed": answer["choice"], "match": f["expected"] == answer["choice"],
                       "confidence": answer["confidence"]})
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    report = verify(args.folder)
    report["boundary_wave01"] = verify_boundaries(args.folder.resolve())
    if args.output:
        with args.output.open("x") as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
    print(json.dumps({key: report[key] for key in ("profiles", "batches", "counts")}))


if __name__ == "__main__":
    main()
