"""Replay authored bug-hunting scenarios; no code-under-review is executed."""
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


def classify_for_review(answer, *, binding_current):
    """Pure advisory routing; never establishes a finding or grants an action."""
    if not binding_current:
        return "unresolved_stale_evidence"
    if not answer or answer.get("choice") not in {"risk_supported", "counterevidence", "insufficient"}:
        return "unresolved"
    if answer["choice"] == "risk_supported":
        return "candidate_requires_verification"
    if answer["choice"] == "counterevidence":
        return "counterevidence_only"
    return "unresolved"


def disagreements(selected, fixtures, pending):
    result = []
    for fid, r in selected.items():
        if fid not in pending and r["response"]["answers"]["decision"]["choice"] != fixtures[fid]["expected"]:
            a = r["response"]["answers"]["decision"]
            result.append({"fixture_id": fid, "expected": fixtures[fid]["expected"],
                           "observed": a["choice"], "confidence": a["confidence"]})
    return result


def check_attempts(attempts, fixtures, patterns):
    """Every initial attempt binds to its fixture; failures carry an error and no answers."""
    failed = set()
    for fid, r in attempts.items():
        f = fixtures[fid]
        p = patterns[f["pattern_id"]]
        if r["pattern_id"] != p["id"] or r["version"] != p["version"] or r["version"] != f["version"]:
            raise ValueError("identity/version mismatch")
        if set(r["request"]) != {"model", "state", "questions"} or r["request"]["state"] != f["state"] or r["request"]["questions"] != p["questions"]:
            raise ValueError("request binding mismatch")
        if r["response"].get("ok") is False:
            if not r["response"].get("error") or r["response"].get("answers"):
                raise ValueError("invalid provider failure receipt")
            failed.add(fid)
    return failed


def report():
    patterns = unique(read("catalog.json")["patterns"], "id")
    fixtures = unique(read("fixtures.json"), "id")
    old_patterns = unique(read("results/initial-catalog.json")["patterns"], "id")
    old_fixtures = unique(read("results/initial-fixtures.json"), "id")
    initial = unique(read("results/screening.json"), "fixture_id")
    recovery = unique(read("results/recovery.json"), "fixture_id")
    refinement_log = read("results/refinement-attempts.json")
    refinement_attempts = unique(refinement_log["attempts"], "fixture_id")
    refinement_recovery = unique(refinement_log["recovery"], "fixture_id")
    refinement = unique(read("results/refinement.json"), "fixture_id")
    if len(patterns) != 48 or len(fixtures) != 144 or set(initial) != set(fixtures):
        raise ValueError("catalog or initial coverage mismatch")
    for pattern in patterns.values():
        cases = [f for f in fixtures.values() if f["pattern_id"] == pattern["id"]]
        if len(cases) != 3 or {f["expected"] for f in cases} != {"risk_supported", "counterevidence", "insufficient"}:
            raise ValueError("missing pattern contrast")
    if len({p["hypothesis"] for p in patterns.values()}) != len(patterns):
        raise ValueError("identical hypotheses")
    # A revision may change its contract, but not silently rewrite the frozen test.
    if set(old_fixtures) != set(fixtures) or set(old_patterns) != set(patterns):
        raise ValueError("fixture or pattern identity changed")
    for fid, before in old_fixtures.items():
        if {k: v for k, v in before.items() if k != "version"} != {k: v for k, v in fixtures[fid].items() if k != "version"}:
            raise ValueError("frozen fixture was rewritten")
    if any(p["version"] <= old_patterns[pid]["version"] for pid, p in patterns.items()):
        raise ValueError("revised catalog must carry a higher version for every pattern")
    # Initial screen: version-1 receipts validate against the preserved version-1 contract.
    failed = check_attempts(initial, old_fixtures, old_patterns)
    if set(recovery) != failed:
        raise ValueError("recovery must cover only original provider failures once")
    initial_selected = {**initial, **recovery}
    initial_successful = [r for r in [*initial.values(), *recovery.values()] if r["response"].get("ok") is True]
    for r in initial_successful:
        f = old_fixtures[r["fixture_id"]]
        validate_receipt(r, f, old_patterns[f["pattern_id"]])
    initial_pending = [fid for fid, r in initial_selected.items() if r["response"].get("ok") is not True]
    initial_disagreements = disagreements(initial_selected, old_fixtures, initial_pending)
    initial_matches = sum(r["response"]["answers"]["decision"]["choice"] == old_fixtures[fid]["expected"]
                          for fid, r in initial.items() if fid not in failed)
    # Revision: every fixture re-screened once against the version-2 contract, with one bounded recovery.
    if set(refinement_attempts) != set(fixtures):
        raise ValueError("refinement coverage mismatch")
    refinement_failed = check_attempts(refinement_attempts, fixtures, patterns)
    if set(refinement_recovery) != refinement_failed:
        raise ValueError("refinement recovery must cover only its provider failures once")
    if set(refinement) != set(fixtures):
        raise ValueError("refinement selection must cover every fixture")
    for fid, r in refinement.items():
        source = refinement_recovery.get(fid) if fid in refinement_failed else refinement_attempts[fid]
        if r != source:
            raise ValueError("refinement selection does not match its logged attempt")
        validate_receipt(r, fixtures[fid], patterns[fixtures[fid]["pattern_id"]])
    current_disagreements = disagreements(refinement, fixtures, [])
    successful = initial_successful + list(refinement.values())
    return {
        "patterns": len(patterns),
        "fixtures": len(fixtures),
        "contract_version": 2,
        "initial_attempts": len(initial),
        "initial_successful_responses": len(initial) - len(failed),
        "initial_label_matches": initial_matches,
        "initial_provider_failures": sorted(failed),
        "recovery_attempts": len(recovery),
        "initial_selected_label_matches": len(fixtures) - len(initial_pending) - len(initial_disagreements),
        "initial_provider_unresolved": initial_pending,
        "initial_disagreements": initial_disagreements,
        "refinement_attempts": len(refinement_attempts),
        "refinement_provider_failures": sorted(refinement_failed),
        "refinement_recovery_attempts": len(refinement_recovery),
        "current_label_matches": len(fixtures) - len(current_disagreements),
        "current_provider_unresolved": [],
        "current_disagreements": current_disagreements,
        "successful_request_digests_verified": len(successful),
        "models": sorted({r["response"]["model"] for r in successful}),
        "reported_input_tokens": sum(r["response"]["usage"]["input_tokens"] for r in successful),
        "reported_output_tokens": sum(r["response"]["usage"]["output_tokens"] for r in successful),
        "reported_bridge_estimated_cost_usd": round(sum(r["response"]["estimated_cost_usd"] for r in successful), 10),
        "cost_scope": "Successful screening, recovery and refinement receipts only; failed-call billing unknown; separate design consultations excluded.",
        "qualification": "Authored textual scenarios, not executed reproductions or held-out production accuracy.",
    }


if __name__ == "__main__":
    result = report()
    print(json.dumps(result, indent=2))
    if (ROOT / "results/summary.json").exists() and result != read("results/summary.json"):
        raise SystemExit("saved summary differs from replay; inspect rather than silently relabel")
