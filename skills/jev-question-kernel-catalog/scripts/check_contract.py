"""Local authoring-envelope checks; no network, inference, or semantic certification."""
import copy
import json
import math
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def meaningful(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return bool(value) and all(isinstance(k, str) and meaningful(v) for k, v in value.items())
    if isinstance(value, list):
        return bool(value) and all(meaningful(v) for v in value)
    return False


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def provider_request(contract, fixture):
    """Build a fresh transport subset; expected labels/authoring metadata never copied."""
    return {"state": copy.deepcopy(fixture["state"]),
            "questions": copy.deepcopy(contract["request"]["questions"])}


def validate(contract, suite):
    require(isinstance(contract, dict) and isinstance(suite, dict), "envelopes must be objects")
    require(isinstance(contract.get("contract_id"), str) and meaningful(contract["contract_id"]), "contract_id required")
    require(type(contract.get("version")) is int and contract["version"] > 0, "positive integer version required")
    for key in ("consumer", "uncertainty_policy", "evaluation_scope"):
        require(isinstance(contract.get(key), str) and meaningful(contract[key]), key + " required")
    checks = contract.get("code_owned_checks")
    require(isinstance(checks, list) and meaningful(checks), "code_owned_checks required")
    follow = contract.get("follow_up")
    require(isinstance(follow, dict), "follow_up required")
    require(type(follow.get("max_calls")) is int and follow["max_calls"] >= 0, "nonnegative follow-up budget required")
    for key in ("trigger", "new_evidence", "stop_condition"):
        require(isinstance(follow.get(key), str) and meaningful(follow[key]), "follow_up." + key + " required")
    fields = contract.get("required_state_fields")
    require(isinstance(fields, list) and all(isinstance(k, str) and k for k in fields), "top-level state field list required")
    require(len(fields) == len(set(fields)), "duplicate state fields")
    request = contract.get("request")
    require(isinstance(request, dict) and set(request) == {"state", "questions"}, "request must contain only state and questions")
    questions = request["questions"]
    require(isinstance(questions, dict) and bool(questions), "questions required")
    for qid, q in questions.items():
        require(isinstance(qid, str) and bool(qid) and isinstance(q, dict), "question ID/object invalid")
        require(q.get("type") in ("choice", "score", "noul"), "unknown primitive")
        require(meaningful(q.get("instructions")), "complete instructions required")
        criteria = q.get("criteria")
        if q["type"] == "choice":
            require(isinstance(criteria, dict) and len(criteria) >= 2 and meaningful(criteria), "Choice requires at least two described labels")
            require(all(bool(k.strip()) for k in criteria), "empty Choice label")
        elif q["type"] == "score":
            require(isinstance(criteria, list) and len(criteria) >= 2 and meaningful(criteria), "Score requires ordered described levels")
        elif criteria is not None:
            require(meaningful(criteria), "Noul criteria must be meaningful")

    def state_check(state):
        require(isinstance(state, (str, dict, list)), "state must be text, object, or array")
        if fields:
            require(isinstance(state, dict) and set(fields) <= set(state), "missing required state fields")
        # Strict JSON rejects NaN/Infinity, but does not inspect prose for label leakage.
        json.dumps(state, allow_nan=False)

    state_check(request["state"])
    require(suite.get("contract_id") == contract["contract_id"] and type(suite.get("version")) is int
            and suite["version"] == contract["version"], "fixture contract/version mismatch")
    fixtures = suite.get("fixtures")
    require(isinstance(fixtures, list) and bool(fixtures), "fixtures required")
    ids = set()
    for fixture in fixtures:
        require(isinstance(fixture, dict) and set(fixture) == {"id", "state", "expected"}, "fixture requires id/state/expected siblings")
        fid = fixture["id"]
        require(isinstance(fid, str) and bool(fid) and fid not in ids, "duplicate or invalid fixture ID")
        ids.add(fid)
        state_check(fixture["state"])
        expected = fixture["expected"]
        require(isinstance(expected, dict) and set(expected) == set(questions), "expected question coverage mismatch")
        for qid, value in expected.items():
            q = questions[qid]
            if q["type"] == "choice":
                require(isinstance(value, str) and value in q["criteria"], "unknown expected Choice")
            else:
                require(isinstance(value, dict) and set(value) == {"min", "max"}, "expected interval required")
                lo, hi = value["min"], value["max"]
                upper = 1 if q["type"] == "noul" else len(q["criteria"]) - 1
                require(finite(lo) and finite(hi) and 0 <= lo <= hi <= upper, "invalid expected interval")
        json.dumps(provider_request(contract, fixture), allow_nan=False)
    return {"structural_check": "passed", "fixtures": len(fixtures),
            "questions": len(questions), "semantic_quality_assessed": False}


if __name__ == "__main__":
    try:
        require(len(sys.argv) == 3, "usage: check_contract.py CONTRACT.json FIXTURES.json")
        print(json.dumps(validate(json.loads(Path(sys.argv[1]).read_text()),
                                  json.loads(Path(sys.argv[2]).read_text()))))
    except (ValueError, TypeError, OSError, KeyError) as error:
        print(json.dumps({"structural_check": "failed", "error": str(error)}))
        sys.exit(1)
