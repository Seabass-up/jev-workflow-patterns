#!/usr/bin/env python3
"""Replay Iteration 3 synthetic Jev receipts without provider or operational calls.

The evaluator verifies request-bound receipt integrity, frozen-label separation, and
the final versioned contract selection. Its tiny controllers only propose a next
review/calculation branch; they never write a record, send a message, or execute an
external action.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def finite_number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def probability(value: Any) -> bool:
    return finite_number(value) and 0 <= value <= 1


def answer_value(answer: Any) -> Any:
    if not isinstance(answer, dict):
        return None
    for name in ("choice", "noul", "score"):
        if name in answer:
            return answer[name]
    return None


def probability_distribution(values: Any, keys: set[str]) -> bool:
    return (
        isinstance(values, dict)
        and set(values) == keys
        and all(probability(value) for value in values.values())
        # Each provider probability is rounded to two decimal places.
        and abs(sum(values.values()) - 1) <= .005 * len(keys) + 1e-12
    )


def valid_answers(questions: Any, response: Any) -> bool:
    """Validate only the typed response contract, never its real-world truth."""
    if not isinstance(questions, dict) or not isinstance(response, dict):
        return False
    if response.get("ok") is not True:
        return False
    answers = response.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        return False
    for question_id, question in questions.items():
        if not isinstance(question, dict):
            return False
        answer = answers.get(question_id)
        kind = question.get("type")
        if not isinstance(answer, dict) or answer.get("type") != kind:
            return False
        if kind == "noul":
            if not probability(answer.get("noul")):
                return False
        elif kind == "choice":
            criteria = question.get("criteria")
            if (
                not isinstance(criteria, dict)
                or not isinstance(answer.get("choice"), str)
                or answer["choice"] not in criteria
                or not probability(answer.get("confidence"))
                or not probability_distribution(answer.get("probabilities"), set(criteria))
            ):
                return False
            if answer["probabilities"][answer["choice"]] < max(answer["probabilities"].values()):
                return False
        elif kind == "score":
            criteria = question.get("criteria")
            score = answer.get("score")
            if (
                not isinstance(criteria, list)
                or not finite_number(score)
                or not 0 <= score <= len(criteria) - 1
                or not probability(answer.get("confidence"))
                or not probability_distribution(
                    answer.get("probabilities"),
                    {str(index) for index in range(len(criteria))},
                )
            ):
                return False
        else:
            return False
    return True


def expected_match(answer: Any, expected: Any) -> bool:
    if not isinstance(expected, dict):
        return False
    value = answer_value(answer)
    if "choice" in expected:
        return value == expected["choice"]
    bounds = expected.get("range")
    return (
        isinstance(bounds, list)
        and len(bounds) == 2
        and all(finite_number(item) for item in bounds)
        and finite_number(value)
        and bounds[0] <= value <= bounds[1]
    )


def contains_expected(value: Any) -> bool:
    if isinstance(value, dict):
        return "expected" in value or any(contains_expected(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_expected(item) for item in value)
    return False


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def check_receipt(row: dict[str, Any], screen: str) -> dict[str, int]:
    if row.get("screen") != screen:
        raise ValueError("wrong screen on " + str(row.get("fixture_id")))
    request = row.get("request")
    response = row.get("response")
    if not isinstance(request, dict) or not isinstance(response, dict):
        raise ValueError("missing request or response")
    if contains_expected(request.get("state")):
        raise ValueError("expected label leaked into state: " + str(row.get("fixture_id")))
    model = request.get("model")
    questions = request.get("questions")
    if not isinstance(model, str) or response.get("model") != model:
        raise ValueError("model binding mismatch: " + str(row.get("fixture_id")))
    if not valid_answers(questions, response):
        raise ValueError("invalid typed response: " + str(row.get("fixture_id")))
    signed = {"model": model, "state": request.get("state"), "questions": questions}
    digest = hashlib.sha256(canonical(signed)).hexdigest()
    if digest != response.get("request_sha256"):
        raise ValueError("request digest mismatch: " + str(row.get("fixture_id")))
    checks = row.get("checks")
    if not isinstance(checks, list) or {item.get("question_id") for item in checks} != set(questions):
        raise ValueError("incomplete checks: " + str(row.get("fixture_id")))
    matches = []
    for check in checks:
        question_id = check["question_id"]
        observed = answer_value(response["answers"][question_id])
        matched = expected_match(response["answers"][question_id], check.get("expected"))
        if check.get("observed") != observed or check.get("match") is not matched:
            raise ValueError("stored check mismatch: " + str(row.get("fixture_id")))
        matches.append(matched)
    if row.get("match") is not all(matches):
        raise ValueError("stored fixture mismatch: " + str(row.get("fixture_id")))
    return {
        "requests": 1,
        "fixture_matches": int(all(matches)),
        "questions": len(checks),
        "question_matches": sum(matches),
        "request_digests_verified": 1,
    }


def validate_catalog_and_fixtures() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    catalog = load("catalog.json")
    fixtures = load("fixtures.json")
    patterns = catalog.get("patterns")
    if not isinstance(patterns, list) or len(patterns) != 30:
        raise ValueError("expected 30 patterns")
    by_id = {pattern.get("id"): pattern for pattern in patterns}
    if len(by_id) != 30 or None in by_id:
        raise ValueError("pattern IDs must be unique")
    expected_domains = {"business": 7, "engineering": 7, "llm": 6, "harness": 10}
    domain_counts = {
        name: sum(pattern.get("domain") == name for pattern in patterns)
        for name in expected_domains
    }
    if domain_counts != expected_domains:
        raise ValueError("unexpected domain distribution")
    if not isinstance(fixtures, list) or len(fixtures) != 61:
        raise ValueError("expected 61 frozen fixtures")
    by_fixture = {fixture.get("id"): fixture for fixture in fixtures}
    if len(by_fixture) != len(fixtures) or None in by_fixture:
        raise ValueError("fixture IDs must be unique")
    for fixture in fixtures:
        pattern = by_id.get(fixture.get("pattern_id"))
        if pattern is None:
            raise ValueError("unknown pattern on " + str(fixture.get("id")))
        state = fixture.get("state")
        if not isinstance(state, dict) or contains_expected(state):
            raise ValueError("invalid fixture state: " + str(fixture.get("id")))
        required = pattern.get("required_state_fields")
        if not isinstance(required, list) or not set(required) <= set(state):
            raise ValueError("missing required state field: " + str(fixture.get("id")))
        expected = fixture.get("expected")
        if not isinstance(expected, dict) or set(expected) != set(pattern.get("questions", {})):
            raise ValueError("incomplete frozen expectation: " + str(fixture.get("id")))
    return by_id, by_fixture


def verify_precedence_revision(patterns, fixtures, rows_by_screen):
    """Bind preserved originals to Git and the one frozen v2 screen to current source."""
    archived = load("results/precedence-pre-review-contracts.json")
    revised = load("results/precedence-revision-fixtures.json")
    source = archived["source_commit"]
    repo = ROOT.parents[1]
    def original(path):
        return json.loads(subprocess.check_output(["git", "show", source + ":" + path], cwd=repo))
    old_patterns = {p["id"]: p for p in original("iterations/03/catalog.json")["patterns"]}
    old_fixtures = {f["id"]: f for f in original("iterations/03/fixtures.json")}
    ids = {"B19", "E18", "H22", "H26", "H27"}
    if {p["id"] for p in archived["patterns"]} != ids or len(archived["patterns"]) != 5:
        raise ValueError("revision archive pattern coverage")
    for p in archived["patterns"]:
        if p != old_patterns[p["id"]]:
            raise ValueError("revision archive differs from Git source")
    expected_old = [f for f in old_fixtures.values() if f["pattern_id"] in ids]
    if archived["fixtures"] != expected_old:
        raise ValueError("revision archive fixture changed")
    for f in archived["fixtures"]:
        current = {k: v for k, v in fixtures[f["id"]].items() if k != "contract_version"}
        if current != f or fixtures[f["id"]].get("contract_version") != 2:
            raise ValueError("original revision fixture changed")
        receipt = rows_by_screen["initial"][f["id"]]
        if (receipt["request"]["state"] != f["state"]
                or receipt["request"]["questions"] != old_patterns[f["pattern_id"]]["questions"]
                or {c["question_id"]: c["expected"] for c in receipt["checks"]} != f["expected"]):
            raise ValueError("original revision receipt binding")
    if revised["patterns"] != [patterns[p["id"]] for p in archived["patterns"]]:
        raise ValueError("revision current contract binding")
    cases = revised["cases"]
    by_id = {f["id"]: f for f in cases}
    rows = rows_by_screen["precedence-review-v2"]
    if len(cases) != 24 or len(by_id) != len(cases) or set(by_id) != set(rows):
        raise ValueError("revision case coverage")
    for f in archived["fixtures"]:
        case = by_id[f["id"]]
        if (case["state"] != f["state"] or case["expected"] != f["expected"]
                or case["split"] != "unchanged_regression"):
            raise ValueError("revision regression changed")
    for f in cases:
        row = rows[f["id"]]
        p = patterns[f["pattern_id"]]
        if (f["pattern_id"] not in ids or p["contract_version"] != 2
                or f["contract_version"] != 2 or row["contract_version"] != 2
                or row["pattern_id"] != f["pattern_id"] or row["split"] != f["split"]
                or row["request"]["state"] != f["state"]
                or row["request"]["questions"] != p["questions"]
                or row["request"].get("use_cache") is not False
                or row["response"].get("cached") is not False
                or row["response"].get("advisory_only") is not True
                or {c["question_id"]: c["expected"] for c in row["checks"]} != f["expected"]):
            raise ValueError("revision receipt binding")
    # CT08 remains advisory; low confidence is retained, not retried until passing.
    ct08 = next(p for p in original("controls/catalog.json")["patterns"] if p["id"] == "CT08")
    pair_rows = load("results/precedence-pair-review-v2.json")
    if len(pair_rows) != 5 or {r["pattern_id"] for r in pair_rows} != ids:
        raise ValueError("revision pair coverage")
    for row in pair_rows:
        p = patterns[row["pattern_id"]]
        question = next(iter(p["questions"].values()))
        labels = list(question["criteria"])
        state, questions = {}, {}
        for a in range(len(labels)):
            for b in range(a + 1, len(labels)):
                slot = "pair" + str(len(state))
                state[slot] = {"question_instructions": question["instructions"],
                               "option_a_label": labels[a], "option_a_description": question["criteria"][labels[a]],
                               "option_b_label": labels[b], "option_b_description": question["criteria"][labels[b]]}
                q = dict(ct08["questions"]["decision"])
                q["instructions"] = "Evaluate only state." + slot + ". " + q["instructions"]
                questions[slot] = q
        req, resp = row["request"], row["response"]
        digest = hashlib.sha256(canonical({"model": resp["model"], "state": state, "questions": questions})).hexdigest()
        if (row["contract_version"] != 2 or req["state"] != state or req["questions"] != questions
                or req.get("use_cache") is not False or resp.get("cached") is not False
                or resp.get("advisory_only") is not True or resp.get("request_sha256") != digest
                or not valid_answers(questions, resp)):
            raise ValueError("revision pair binding")
    return {"patterns": 5, "unchanged_regressions": 10, "development_cases": 14,
            "pairs": 30, "scope": "Synthetic revision evidence, not production qualification."}


def replay() -> dict[str, Any]:
    """Verify all raw screens and selected final receipts without a network call."""
    patterns, fixtures = validate_catalog_and_fixtures()
    screen_manifest = load("screens.json").get("screens")
    if not isinstance(screen_manifest, dict) or set(screen_manifest) != {"initial", "refinement", "precedence-review-v2"}:
        raise ValueError("unexpected screen manifest")
    rows_by_screen: dict[str, dict[str, dict[str, Any]]] = {}
    metrics: dict[str, dict[str, int]] = {}
    for screen, metadata in screen_manifest.items():
        rows = load(metadata["result_file"])
        if not isinstance(rows, list) or len(rows) != metadata.get("fixture_count"):
            raise ValueError("receipt coverage mismatch: " + screen)
        table = {row.get("fixture_id"): row for row in rows}
        if len(table) != len(rows) or None in table:
            raise ValueError("duplicate fixture receipt: " + screen)
        total = {"requests": 0, "fixture_matches": 0, "questions": 0,
                 "question_matches": 0, "request_digests_verified": 0}
        for row in rows:
            checked = check_receipt(row, screen)
            for key, value in checked.items():
                total[key] += value
        rows_by_screen[screen] = table
        metrics[screen] = total

    revision = verify_precedence_revision(patterns, fixtures, rows_by_screen)

    selections = load("results/final-acceptance.json").get("receipts")
    if not isinstance(selections, list) or len(selections) != len(fixtures):
        raise ValueError("final acceptance coverage mismatch")
    selected = {item.get("fixture_id"): item for item in selections}
    if set(selected) != set(fixtures) or len(selected) != len(selections):
        raise ValueError("final acceptance fixture IDs mismatch")

    final_matches = 0
    final_questions = 0
    final_question_matches = 0
    for fixture_id, fixture in fixtures.items():
        item = selected[fixture_id]
        screen = item.get("result_screen")
        receipt = rows_by_screen.get(screen, {}).get(fixture_id)
        if receipt is None:
            raise ValueError("selected receipt missing: " + fixture_id)
        pattern = patterns[fixture["pattern_id"]]
        if item.get("pattern_id") != fixture["pattern_id"]:
            raise ValueError("selected pattern mismatch: " + fixture_id)
        if item.get("contract_version") != pattern.get("contract_version"):
            raise ValueError("selected contract version mismatch: " + fixture_id)
        if canonical(receipt["request"]["state"]) != canonical(fixture["state"]):
            raise ValueError("selected state mismatch: " + fixture_id)
        if canonical(receipt["request"]["questions"]) != canonical(pattern["questions"]):
            raise ValueError("selected contract mismatch: " + fixture_id)
        receipt_expected = {check["question_id"]: check["expected"] for check in receipt["checks"]}
        if canonical(receipt_expected) != canonical(fixture["expected"]):
            raise ValueError("selected expectation mismatch: " + fixture_id)
        if item.get("request_sha256") != receipt["response"].get("request_sha256"):
            raise ValueError("selected digest mismatch: " + fixture_id)
        if item.get("match") is not receipt.get("match"):
            raise ValueError("selected match mismatch: " + fixture_id)
        final_matches += int(receipt["match"])
        final_questions += len(receipt["checks"])
        final_question_matches += sum(check["match"] for check in receipt["checks"])

    return {
        "screens": metrics,
        "precedence_revision": revision,
        "final_contract_acceptance": {
            "fixtures": len(fixtures),
            "fixture_matches": final_matches,
            "questions": final_questions,
            "question_matches": final_question_matches,
        },
    }


def state_ready(pattern, state):
    """Check top-level evidence presence, not truth, freshness or authority."""
    required = pattern.get("required_state_fields")
    if (not isinstance(state, dict) or not isinstance(required, list) or not required
            or any(not isinstance(field, str) or not field for field in required)):
        return False
    for field in required:
        if field not in state or state[field] is None:
            return False
        value = state[field]
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, (list, dict)) and not value:
            return False
    return True


def plan(pattern: dict[str, Any], response: dict[str, Any], *, state=None) -> dict[str, str]:
    """Return a non-executing proposal; malformed/provider-failed signals fail closed."""
    if not state_ready(pattern, state):
        return {"next": "review", "reason": "missing_required_state"}
    questions = pattern.get("questions", {})
    if not valid_answers(questions, response):
        return {"next": "review", "reason": "invalid_or_failed_typed_response"}
    pattern_id = pattern.get("id")
    answers = response["answers"]
    if pattern_id == "H21":
        route = answers["snapshot_relation"]["choice"]
        return {
            "next": "verify_exact_snapshot_fingerprint" if route == "current_match" else "discard_or_rerun_on_fresh_snapshot",
            "reason": route,
        }
    if pattern_id == "H22":
        route = answers["coverage"]["choice"]
        return {
            "next": "verify_manifest_in_code" if route == "exhaustive_with_provenance" else "expand_or_review_candidate_universe",
            "reason": route,
        }
    if pattern_id == "H24":
        veto = answers["named_veto"]["noul"]
        return {
            "next": "review_named_veto" if veto >= 0.5 else "compute_versioned_score_in_code",
            "reason": "veto_signal" if veto >= 0.5 else "no_high_veto_signal",
        }
    if pattern_id == "H29":
        route = answers["precision_route"]["choice"]
        return {
            "next": "deterministic_calculation_or_review" if route != "semantic_judgment_only" else "bounded_semantic_review",
            "reason": route,
        }
    return {"next": "review", "reason": "advisory_result_requires_controller_policy"}


if __name__ == "__main__":
    print(json.dumps(replay(), sort_keys=True))
