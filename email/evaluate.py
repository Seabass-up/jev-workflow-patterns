"""Replay synthetic email receipts; no network or mailbox operations."""
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


def report():
    catalog, fixtures = read("catalog.json"), read("fixtures.json")
    old_catalog, old_fixtures = read("results/initial-catalog.json"), read("results/initial-fixtures.json")
    initial, refinement = read("results/initial.json"), read("results/refinement.json")
    revised_ids = {p["id"] for p in catalog["patterns"] if p["version"] > 1}
    revised_fixtures = [f for f in fixtures if f["pattern_id"] in revised_ids]
    selected = [r for r in initial if r["pattern_id"] not in revised_ids] + refinement
    # A revision may change its contract, but not silently rewrite the frozen test.
    before, after = unique(old_fixtures, "id"), unique(fixtures, "id")
    if set(before) != set(after):
        raise ValueError("fixture identity changed")
    for fid in before:
        if {k: v for k, v in before[fid].items() if k != "version"} != {k: v for k, v in after[fid].items() if k != "version"}:
            raise ValueError("frozen fixture was rewritten")
    runs = initial + refinement
    return {
        "initial": score(initial, old_fixtures, old_catalog["patterns"]),
        "refinement": score(refinement, revised_fixtures, catalog["patterns"]),
        "current": score(selected, fixtures, catalog["patterns"]),
        "request_digests_verified": len(runs),
        "provider_input_tokens": sum(r["response"]["usage"]["input_tokens"] for r in runs),
        "provider_output_tokens": sum(r["response"]["usage"]["output_tokens"] for r in runs),
        "bridge_estimated_cost_usd": round(sum(r["response"]["estimated_cost_usd"] for r in runs), 10),
        "models": sorted({r["response"]["model"] for r in runs}),
        "scope": "Synthetic author-labelled design screening, not held-out production accuracy.",
    }


if __name__ == "__main__":
    result = report()
    print(json.dumps(result, indent=2))
    if result["current"]["misses"]:
        raise SystemExit("current fixtures did not all match")
    summary_path = ROOT / "results/summary.json"
    if summary_path.exists() and result != read("results/summary.json"):
        raise SystemExit("saved summary differs from replay")
