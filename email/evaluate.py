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


def valid_version(value):
    return type(value) is int and value > 0


def validate_fixture_history(old_fixtures, fixtures, old_patterns, patterns):
    before, after = unique(old_fixtures, "id"), unique(fixtures, "id")
    old_pattern_map = unique(old_patterns, "id")
    pattern_map = unique(patterns, "id")
    if any(not valid_version(item.get("version")) for item in old_fixtures + fixtures):
        raise ValueError("invalid fixture version")
    if any(not valid_version(item.get("version")) for item in old_patterns + patterns):
        raise ValueError("invalid pattern version")
    if not set(before).issubset(after):
        raise ValueError("frozen fixture removed")
    for fid, original in before.items():
        current = after[fid]
        old_content = {k: v for k, v in original.items() if k != "version"}
        current_content = {k: v for k, v in current.items() if k != "version"}
        if old_content != current_content:
            raise ValueError("frozen fixture was rewritten")
    for fid, fixture in after.items():
        pattern = pattern_map.get(fixture["pattern_id"])
        if pattern is None or fixture["version"] != pattern["version"]:
            raise ValueError("fixture version does not match current contract")
        if fid not in before:
            old_pattern = old_pattern_map.get(fixture["pattern_id"])
            if old_pattern is None or pattern["version"] <= old_pattern["version"]:
                raise ValueError("new fixture must target a revised contract")


def validate_receipt(receipt, fixture, pattern):
    if any(not valid_version(item.get("version")) for item in (receipt, fixture, pattern)):
        raise ValueError("invalid contract version")
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
    # Provider probabilities are rounded to two decimals; accept the bridge's 0.02 tolerance.
    if not math.isclose(sum(probabilities.values()), 1, abs_tol=0.02):
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
    em10_v2 = read("results/em10-v2-first-pass.json")
    revised_ids = {p["id"] for p in catalog["patterns"] if p["version"] > 1}
    revised_fixtures = [f for f in fixtures if f["pattern_id"] in revised_ids]
    selected = [r for r in initial if r["pattern_id"] not in revised_ids] + refinement
    # Revisions may add version-matched regression cases, but cannot remove or
    # rewrite any original state/expectation. New cases must target a revised
    # contract so their receipts cannot silently alter a baseline pattern.
    validate_fixture_history(old_fixtures, fixtures, old_catalog["patterns"], catalog["patterns"])
    current_em10 = next(pattern for pattern in catalog["patterns"] if pattern["id"] == "EM10")
    validate_fixture_history(
        em10_v2["fixtures"],
        [fixture for fixture in fixtures if fixture["pattern_id"] == "EM10"],
        [em10_v2["pattern"]],
        [current_em10],
    )
    em10_v2_first_pass = score(em10_v2["receipts"], em10_v2["fixtures"], [em10_v2["pattern"]])
    runs = initial + refinement + em10_v2["receipts"]
    return {
        "initial": score(initial, old_fixtures, old_catalog["patterns"]),
        "em10_v2_first_pass": em10_v2_first_pass,
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
