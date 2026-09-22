#!/usr/bin/env python3
"""Replay Iteration 4 synthetic Jev receipts without provider or operational calls.

The evaluator verifies only the typed, request-bound public receipt contract.  It does
not infer truth, grant authority, run an action, or claim a frozen synthetic label is a
production benchmark.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def finite_number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def probability(value: Any) -> bool:
    return finite_number(value) and 0 <= value <= 1


def answer_value(answer: Any) -> Any:
    if not isinstance(answer, dict):
        return None
    for key in ("choice", "score", "noul"):
        if key in answer:
            return answer[key]
    return None


def probability_distribution(values: Any, keys: set[str]) -> bool:
    return isinstance(values, dict) and set(values) == keys and all(probability(v) for v in values.values()) and abs(sum(values.values()) - 1) <= 0.000001


def valid_answers(questions: Any, response: Any) -> bool:
    """Check interface shape only; a typed response is never evidence of truth."""
    if not isinstance(questions, dict) or not isinstance(response, dict) or response.get("ok") is not True:
        return False
    answers = response.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        return False
    for question_id, question in questions.items():
        answer = answers.get(question_id)
        if not isinstance(question, dict) or not isinstance(answer, dict) or answer.get("type") != question.get("type"):
            return False
        kind = question["type"]
        if kind == "choice":
            criteria = question.get("criteria")
            if not isinstance(criteria, dict) or not isinstance(answer.get("choice"), str) or answer["choice"] not in criteria:
                return False
            if not probability(answer.get("confidence")) or not probability_distribution(answer.get("probabilities"), set(criteria)):
                return False
        elif kind == "score":
            criteria = question.get("criteria")
            if not isinstance(criteria, list) or not finite_number(answer.get("score")) or not 0 <= answer["score"] <= len(criteria) - 1:
                return False
            if not probability(answer.get("confidence")) or not probability_distribution(answer.get("probabilities"), {str(i) for i in range(len(criteria))}):
                return False
        elif kind == "noul":
            if not probability(answer.get("noul")):
                return False
        else:
            return False
    return True


def expected_match(answer: Any, expected: Any) -> bool:
    if not isinstance(expected, dict):
        return False
    observed = answer_value(answer)
    if "choice" in expected:
        return observed == expected["choice"]
    bounds = expected.get("range")
    return isinstance(bounds, list) and len(bounds) == 2 and all(finite_number(item) for item in bounds) and finite_number(observed) and bounds[0] <= observed <= bounds[1]


def contains_expected(value: Any) -> bool:
    if isinstance(value, dict):
        return "expected" in value or any(contains_expected(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_expected(item) for item in value)
    return False


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate_catalog_and_fixtures() -> tuple[dict[str, dict], dict[str, dict]]:
    catalog = load("catalog.json")
    fixtures = load("fixtures.json")
    patterns = catalog.get("patterns")
    if not isinstance(patterns, list) or len(patterns) != 30:
        raise ValueError("expected exactly 30 patterns")
    by_pattern = {item.get("id"): item for item in patterns}
    if len(by_pattern) != 30 or None in by_pattern:
        raise ValueError("pattern IDs must be unique")
    wanted = {"business": 7, "engineering": 7, "llm": 6, "harness": 10}
    got = {domain: sum(item.get("domain") == domain for item in patterns) for domain in wanted}
    if got != wanted:
        raise ValueError(f"unexpected domain counts: {got}")
    if not isinstance(fixtures, list) or len(fixtures) != 60:
        raise ValueError("expected exactly 60 frozen fixtures")
    by_fixture = {item.get("id"): item for item in fixtures}
    if len(by_fixture) != 60 or None in by_fixture:
        raise ValueError("fixture IDs must be unique")
    for item in fixtures:
        pattern = by_pattern.get(item.get("pattern_id"))
        state = item.get("state")
        expected = item.get("expected")
        if pattern is None or not isinstance(state, dict) or contains_expected(state):
            raise ValueError("invalid fixture state: " + str(item.get("id")))
        if not set(pattern.get("required_state_fields", [])) <= set(state):
            raise ValueError("missing state field: " + str(item.get("id")))
        if not isinstance(expected, dict) or set(expected) != set(pattern.get("questions", {})):
            raise ValueError("incomplete frozen expectations: " + str(item.get("id")))
    return by_pattern, by_fixture


def check_receipt(row: dict[str, Any], screen: str) -> dict[str, int]:
    if row.get("screen") != screen:
        raise ValueError("wrong screen for " + str(row.get("fixture_id")))
    request, response = row.get("request"), row.get("response")
    if not isinstance(request, dict) or not isinstance(response, dict) or contains_expected(request.get("state")):
        raise ValueError("invalid request/response for " + str(row.get("fixture_id")))
    model, questions = request.get("model"), request.get("questions")
    if not isinstance(model, str) or response.get("model") != model or not valid_answers(questions, response):
        raise ValueError("invalid typed response for " + str(row.get("fixture_id")))
    digest = hashlib.sha256(canonical({"model": model, "state": request.get("state"), "questions": questions})).hexdigest()
    if response.get("request_sha256") != digest:
        raise ValueError("request digest mismatch for " + str(row.get("fixture_id")))
    checks = row.get("checks")
    if not isinstance(checks, list) or {item.get("question_id") for item in checks} != set(questions):
        raise ValueError("incomplete checks for " + str(row.get("fixture_id")))
    matches = []
    for check in checks:
        qid = check["question_id"]
        observed = answer_value(response["answers"][qid])
        match = expected_match(response["answers"][qid], check.get("expected"))
        if check.get("observed") != observed or check.get("match") is not match:
            raise ValueError("stored check mismatch for " + str(row.get("fixture_id")))
        matches.append(match)
    if row.get("match") is not all(matches):
        raise ValueError("stored fixture match mismatch for " + str(row.get("fixture_id")))
    return {"requests": 1, "fixture_matches": int(all(matches)), "questions": len(checks), "question_matches": sum(matches), "request_digests_verified": 1}


def plan(pattern: dict[str, Any], response: dict[str, Any]) -> dict[str, str]:
    """A deliberately non-actioning controller used only by pure tests."""
    if not valid_answers(pattern.get("questions"), response):
        return {"next": "review"}
    return {"next": "review_or_code_owned_branch"}


def replay() -> dict[str, Any]:
    patterns, fixtures = validate_catalog_and_fixtures()
    manifest = load("screens.json").get("screens")
    if not isinstance(manifest, dict) or "initial" not in manifest:
        raise ValueError("initial screen manifest is required")
    rows_by_screen: dict[str, dict[str, dict]] = {}
    metrics: dict[str, dict[str, int]] = {}
    for screen, metadata in manifest.items():
        rows = load(metadata["result_file"])
        if not isinstance(rows, list) or len(rows) != metadata.get("fixture_count"):
            raise ValueError("screen receipt coverage mismatch: " + screen)
        table = {row.get("fixture_id"): row for row in rows}
        if len(table) != len(rows) or None in table:
            raise ValueError("duplicate receipt in screen: " + screen)
        total = {"requests": 0, "fixture_matches": 0, "questions": 0, "question_matches": 0, "request_digests_verified": 0}
        for row in rows:
            result = check_receipt(row, screen)
            for key, value in result.items():
                total[key] += value
        rows_by_screen[screen] = table
        metrics[screen] = total
    selected_rows = load("results/final-acceptance.json").get("receipts")
    if not isinstance(selected_rows, list) or len(selected_rows) != len(fixtures):
        raise ValueError("final acceptance receipt coverage mismatch")
    selected = {row.get("fixture_id"): row for row in selected_rows}
    if set(selected) != set(fixtures) or len(selected) != len(selected_rows):
        raise ValueError("final acceptance fixture IDs mismatch")
    final = {"fixtures": 0, "fixture_matches": 0, "questions": 0, "question_matches": 0}
    for fixture_id, fixture in fixtures.items():
        item = selected[fixture_id]
        screen = item.get("result_screen")
        row = rows_by_screen.get(screen, {}).get(fixture_id)
        if row is None or item.get("pattern_id") != fixture["pattern_id"]:
            raise ValueError("selected receipt missing/mismatched: " + fixture_id)
        pattern = patterns[fixture["pattern_id"]]
        if item.get("contract_version") != pattern.get("contract_version"):
            raise ValueError("selected contract version mismatch: " + fixture_id)
        if canonical(row["request"]["state"]) != canonical(fixture["state"]) or canonical(row["request"]["questions"]) != canonical(pattern["questions"]):
            raise ValueError("selected receipt not bound to current fixture/contract: " + fixture_id)
        if item.get("request_sha256") != row["response"].get("request_sha256"):
            raise ValueError("selected digest mismatch: " + fixture_id)
        final["fixtures"] += 1
        final["fixture_matches"] += int(row["match"])
        final["questions"] += len(row["checks"])
        final["question_matches"] += sum(int(check["match"]) for check in row["checks"])
    return {"screens": metrics, "final_contract_acceptance": final}


if __name__ == "__main__":
    print(json.dumps(replay(), sort_keys=True))
