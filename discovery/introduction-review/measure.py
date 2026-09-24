"""Replay offline measurements over preserved receipts; no network or model calls."""
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "skills/jev-question-kernel-catalog/scripts"))
from check_confidence import answers, choice_confidence, required_top_probability  # noqa: E402

RECEIPT_DIRS = [REPO / "iterations", REPO / "email"]
SAVED = ROOT / "measurements.json"


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_all():
    """Pin inputs to the saved snapshot so later receipts cannot silently change it."""
    if SAVED.exists():
        pinned = json.loads(SAVED.read_text())["input_files"]
        for name, digest in pinned.items():
            if sha256(REPO / name) != digest:
                raise SystemExit("pinned input changed: " + name)
        paths = [REPO / name for name in pinned]
    else:
        paths = [p for folder in RECEIPT_DIRS for p in sorted(folder.rglob("*.json"))]
    documents = [(p.relative_to(REPO).as_posix(), json.loads(p.read_text())) for p in paths]
    return [(name, doc) for name, doc in documents
            if is_catalog(name) or any(True for _ in answers(doc))
            or any("elapsed_ms" in n for n in walk(doc))]


def is_catalog(name):
    parts = name.split("/")
    return len(parts) == 3 and parts[0] == "iterations" and parts[1].isdigit() and parts[2] == "catalog.json"


def confidence_fit(documents):
    choice, beyond_rounding, score = [], 0, {}
    for _, document in documents:
        for _, answer in answers(document):
            if answer["type"] == "choice":
                n = len(answer["probabilities"])
                difference = abs(choice_confidence(answer["probabilities"]) - answer["confidence"])
                choice.append(difference)
                # Both confidence and top probability are stored to two decimals.
                beyond_rounding += difference > 0.005 + 0.005 * n / (n - 1) + 1e-9
            else:
                ordered = tuple(answer["probabilities"][k] for k in sorted(answer["probabilities"], key=float))
                score[(ordered, answer["confidence"])] = None
    score_differences = [abs(choice_confidence(p) - c) for p, c in score]
    extreme = [{"ordered_probabilities": list(p), "confidence": c} for p, c in score
               if len(p) >= 3 and p[0] + p[-1] >= 0.95 and min(p[0], p[-1]) >= 0.4]
    return {
        "choice_answers": len(choice),
        "choice_max_abs_difference": round(max(choice), 4),
        "choice_consistent_with_two_decimal_rounding": sum(d <= 0.005 + 1e-9 for d in choice),
        "choice_within_0_01": sum(d <= 0.01 + 1e-9 for d in choice),
        "choice_beyond_combined_rounding_bound": beyond_rounding,
        "score_unique_answers": len(score),
        "score_max_abs_difference_from_choice_formula": round(max(score_differences), 4),
        "score_extreme_split_examples": extreme,
    }


def latency(documents):
    receipts = {}
    for _, document in documents:
        for node in walk(document):
            if isinstance(node.get("answers"), dict) and "elapsed_ms" in node and not node.get("cached"):
                # Repeated calls share a digest but not an observation time; copies of one
                # response across files share both and are counted once.
                key = (node.get("request_sha256"), node.get("observed_at")) if node.get("observed_at") else id(node)
                receipts[key] = (
                    len(node["answers"]), float(node["elapsed_ms"]),
                    (node.get("usage") or {}).get("input_tokens"))
    rows = list(receipts.values())
    groups = {}
    for questions, ms, tokens in rows:
        groups.setdefault(questions, []).append((ms, tokens))
    by_count = {}
    for questions in sorted(groups):
        values = groups[questions]
        tokens = [t for _, t in values if t]
        by_count[str(questions)] = {"calls": len(values),
                                    "median_ms": round(statistics.median(ms for ms, _ in values), 1),
                                    "median_input_tokens": statistics.median(tokens) if tokens else None}
    q = [r[0] for r in rows]
    ms = [r[1] for r in rows]
    mq, mm = statistics.mean(q), statistics.mean(ms)
    correlation = sum((a - mq) * (b - mm) for a, b in zip(q, ms)) / math.sqrt(
        sum((a - mq) ** 2 for a in q) * sum((b - mm) ** 2 for b in ms))
    return {"uncached_calls": len(rows),
            "single_question_calls": sum(1 for r in rows if r[0] == 1),
            "median_ms": round(statistics.median(ms), 1),
            "p90_ms": round(sorted(ms)[int(0.9 * (len(ms) - 1))], 1),
            "correlation_ms_vs_question_count": round(correlation, 2),
            "by_question_count": by_count,
            "timing_scope": "Client-observed bridge elapsed time including network; not server time."}


def flat_threshold_audit(documents):
    rows = []
    for _, catalog in [(n, d) for n, d in documents if is_catalog(n)]:
        for pattern in catalog["patterns"]:
            floor = (pattern.get("policy") or {}).get("choice_score_confidence_floor")
            counts = sorted({len(node["criteria"]) for node in walk(pattern.get("questions", {}))
                             if node.get("type") == "choice" and isinstance(node.get("criteria"), dict)})
            if floor is not None and counts:
                rows.append((pattern["id"], floor, counts))
    floors = sorted({floor for _, floor, _ in rows})
    counts = sorted({n for _, _, c in rows for n in c})
    return {"patterns_with_choice_and_numeric_floor": len(rows),
            "floors": floors,
            "choice_option_counts": counts,
            "pattern_ids": [pid for pid, _, _ in rows],
            "required_top_probability": {str(n): round(required_top_probability(floors[0], n), 4)
                                         for n in counts} if len(floors) == 1 else None}


def duplicate_screen():
    """Replay the discovery screen's request binding and answer coverage."""
    receipt = json.loads((ROOT / "duplicate-screen.json").read_text())
    request, response = receipt["request"], receipt["response"]
    digest = hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False, allow_nan=False,
                                       separators=(",", ":")).encode()).hexdigest()
    if digest != response["request_sha256"] or response["model"] != request["model"]:
        raise SystemExit("duplicate screen request binding mismatch")
    if set(response["answers"]) != set(request["questions"]) or response.get("ok") is not True:
        raise SystemExit("duplicate screen answer coverage mismatch")
    candidates = set(request["state"]["candidates"])
    if set(receipt["host_review"]["dispositions"]) != candidates:
        raise SystemExit("duplicate screen disposition coverage mismatch")
    choices = {k: v["choice"] for k, v in response["answers"].items() if v["type"] == "choice"}
    return {"request_digest_verified": True,
            "model": response["model"],
            "questions": len(request["questions"]),
            "jev_nearest": dict(sorted(choices.items())),
            "host_decisions": {k: v["decision"] for k, v in sorted(receipt["host_review"]["dispositions"].items())}}


def source_comparison():
    """Check the recorded Iteration 4 digests and their refetched values."""
    sources = json.loads((ROOT / "sources.json").read_text())
    recorded = (REPO / "iterations/04/sources.md").read_text()
    fetched = {s["url"]: s["sha256"] for s in sources["sources"]}
    rows = sources["iteration_4_comparison"]
    for row in rows:
        if row["iteration_4_sha256"] not in recorded:
            raise SystemExit("Iteration 4 digest not found in its source record: " + row["url"])
        if row["match"] != (row["iteration_4_sha256"] == row["fetched_sha256"]):
            raise SystemExit("inconsistent match flag: " + row["url"])
        if fetched.get(row["url"], row["fetched_sha256"]) != row["fetched_sha256"]:
            raise SystemExit("conflicting fetched digest: " + row["url"])
    return {"iteration_4_pages": len(rows), "unchanged": sum(r["match"] for r in rows)}


def report():
    documents = load_all()
    return {"schema_version": 1,
            "inputs": "Preserved iteration and email receipts in this repository; offline replay.",
            "input_files": {name: sha256(REPO / name) for name, _ in documents},
            "confidence_fit": confidence_fit(documents),
            "latency": latency(documents),
            "flat_threshold_audit": flat_threshold_audit(documents),
            "duplicate_screen": duplicate_screen(),
            "iteration_4_source_comparison": source_comparison(),
            "scope": ("Measurements of stored synthetic screening receipts from jev-1.13.0. "
                      "They are not accuracy, calibration, or production latency claims.")}


if __name__ == "__main__":
    result = report()
    print(json.dumps(result, indent=2))
    if SAVED.exists() and json.loads(SAVED.read_text()) != result:
        raise SystemExit("saved measurements differ from replay")
