"""Replay research-inspired human-AI question scenarios; no human benefit is inferred."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads((ROOT / path).read_text())


def digest(request):
    return hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False, separators=(",", ":")).encode()).hexdigest()


def unique(items, key):
    result = {}
    for item in items:
        value = item[key]
        if value in result:
            raise ValueError("duplicate " + key + ": " + str(value))
        result[value] = item
    return result


def validate_receipt(receipt, fixture, pattern):
    if any(type(item["version"]) is not int or item["version"] < 1
           for item in (receipt, fixture, pattern)):
        raise ValueError("invalid version")
    if receipt["fixture_id"] != fixture["id"] or receipt["pattern_id"] != pattern["id"]:
        raise ValueError("identity mismatch")
    if fixture["pattern_id"] != pattern["id"]:
        raise ValueError("fixture pattern mismatch")
    if receipt["version"] != fixture["version"] or fixture["version"] != pattern["version"]:
        raise ValueError("stale contract version")
    request, response = receipt["request"], receipt["response"]
    if set(request) != {"state", "questions", "model"}:
        raise ValueError("unexpected transport fields")
    if request["state"] != fixture["state"] or request["questions"] != pattern["questions"]:
        raise ValueError("state or question binding mismatch")
    if response.get("request_sha256") != digest(request):
        raise ValueError("request digest mismatch")
    if response.get("ok") is not True or response.get("advisory_only") is not True:
        raise ValueError("unsuccessful or non-advisory response")
    if response.get("model") != request["model"]:
        raise ValueError("model binding mismatch")
    if set(response.get("answers", {})) != {"decision"}:
        raise ValueError("answer coverage mismatch")
    answer = response["answers"]["decision"]
    labels = set(pattern["questions"]["decision"]["criteria"])
    if fixture["expected"] not in labels or answer.get("choice") not in labels:
        raise ValueError("unknown choice label")
    if answer.get("type") != "choice":
        raise ValueError("wrong primitive")
    probabilities = answer.get("probabilities", {})
    if set(probabilities) != labels:
        raise ValueError("probability label mismatch")
    for value in [answer.get("confidence"), *probabilities.values()]:
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("invalid probability")
    if not math.isclose(sum(probabilities.values()), 1, abs_tol=1e-6):
        raise ValueError("probabilities do not sum to one")
    # TypeSafe confidence summarizes distribution shape; it is not defined
    # as the probability of the selected option. Validate it independently.
    if probabilities[answer["choice"]] < max(probabilities.values()):
        raise ValueError("choice is not a maximum")
    return answer["choice"] == fixture["expected"]


def score(receipts, fixtures, patterns):
    rmap = unique(receipts, "fixture_id")
    fmap = unique(fixtures, "id")
    pmap = unique(patterns, "id")
    if set(rmap) != set(fmap):
        raise ValueError("receipt coverage mismatch")
    misses = []
    for fid, fixture in fmap.items():
        if not validate_receipt(rmap[fid], fixture, pmap[fixture["pattern_id"]]):
            misses.append(fid)
    return {"matched": len(fixtures) - len(misses), "total": len(fixtures), "misses": misses}


def validate_collection(catalog, fixtures, sources):
    patterns = unique(catalog["patterns"], "id")
    smap = unique(sources, "id")
    fmap = unique(fixtures, "id")
    if not patterns or not smap:
        raise ValueError("empty catalog or source register")
    for p in patterns.values():
        if type(p["version"]) is not int or p["version"] < 1:
            raise ValueError("invalid version")
        if set(p["questions"]) != {"decision"}:
            raise ValueError("single decision handle required for this catalog")
        question = p["questions"]["decision"]
        if question["type"] != "choice" or "unknown" not in question["criteria"]:
            raise ValueError("Choice with explicit unknown required")
        if not p["source_ids"] or set(p["source_ids"]) - smap.keys():
            raise ValueError("unbound research source")
        cases = [f for f in fixtures if f["pattern_id"] == p["id"]]
        if len(cases) != 4 or sum(f["split"] == "challenge" for f in cases) != 1:
            raise ValueError("each profile needs three design and one challenge case")
        if {f["split"] for f in cases} != {"design", "challenge"}:
            raise ValueError("invalid fixture split")
        for f in cases:
            if type(f["version"]) is not int or f["version"] < 1:
                raise ValueError("invalid fixture version")
            if f["version"] != p["version"] or f["expected"] not in question["criteria"]:
                raise ValueError("invalid fixture contract")
            if not isinstance(f["state"], dict):
                raise ValueError("named state required")
        if not any(f["expected"] == "unknown" for f in cases):
            raise ValueError("missing unknown probe")
    if set(f["pattern_id"] for f in fixtures) != set(patterns):
        raise ValueError("unbound fixture")
    return patterns, fmap


def replay(catalog, fixtures, sources, initial, recovery):
    patterns, fmap = validate_collection(catalog, fixtures, sources)
    first, retries = unique(initial, "fixture_id"), unique(recovery, "fixture_id")
    if set(first) != set(fmap):
        raise ValueError("initial coverage mismatch")
    failures = {fid for fid, r in first.items() if r["response"].get("ok") is False}
    if set(retries) - failures:
        raise ValueError("recovery may not replace a semantic miss or add a fixture")
    for r in [*first.values(), *retries.values()]:
        f = fmap[r["fixture_id"]]
        p = patterns[f["pattern_id"]]
        if type(r["version"]) is not int or r["version"] < 1:
            raise ValueError("invalid receipt version")
        if r["pattern_id"] != p["id"] or r["version"] != p["version"] or r["version"] != f["version"]:
            raise ValueError("identity/version mismatch")
        req = r["request"]
        if set(req) != {"state", "questions", "model"} or req["state"] != f["state"] or req["questions"] != p["questions"]:
            raise ValueError("request binding mismatch")
        if r["response"].get("ok") is True:
            validate_receipt(r, f, p)
        elif r["response"].get("ok") is not False or not r["response"].get("error") or r["response"].get("answers"):
            raise ValueError("invalid failure receipt")
    selected = {**first, **retries}
    successful = [r for r in [*first.values(), *retries.values()] if r["response"].get("ok") is True]
    splits = {}
    provisional = set()
    for split in ("design", "challenge"):
        subset = [f for f in fixtures if f["split"] == split]
        mismatches, errors = [], []
        for f in subset:
            r = selected[f["id"]]
            if not r["response"].get("ok"):
                errors.append(f["id"])
                provisional.add(f["pattern_id"])
            elif r["response"]["answers"]["decision"]["choice"] != f["expected"]:
                a = r["response"]["answers"]["decision"]
                mismatches.append({"fixture_id": f["id"], "expected": f["expected"],
                                   "observed": a["choice"], "confidence": a["confidence"]})
                provisional.add(f["pattern_id"])
        splits[split] = {"cases": len(subset), "label_matches": len(subset) - len(mismatches) - len(errors),
                         "disagreements": mismatches, "provider_unresolved": errors}
    return {
        "patterns": len(patterns), "sources": len(sources), "fixtures": len(fixtures),
        "initial_attempts": len(first), "initial_provider_failures": sorted(failures),
        "recovery_attempts": len(retries), "successful_request_digests_verified": len(successful),
        "splits": splits, "provisional_patterns": sorted(provisional),
        "reported_input_tokens": sum(r["response"]["usage"]["input_tokens"] for r in successful),
        "reported_output_tokens": sum(r["response"]["usage"]["output_tokens"] for r in successful),
        "reported_bridge_estimated_cost_usd": round(sum(r["response"]["estimated_cost_usd"] for r in successful), 10),
        "models": sorted({r["response"]["model"] for r in successful}),
        "scope": "Synthetic design and separately authored challenge cases; no human study, efficacy or production accuracy claim. Research calls and failed-call billing excluded from cost."
    }


def report():
    return replay(read("catalog.json"), read("fixtures.json"), read("sources.json"),
                  read("results/screening.json"), read("results/recovery.json"))


if __name__ == "__main__":
    result = report()
    print(json.dumps(result, indent=2))
    if (ROOT / "results/summary.json").exists() and result != read("results/summary.json"):
        raise SystemExit("saved summary differs from replay; preserve disagreement rather than relabel")
