#!/usr/bin/env python3
"""Verify synthetic Jev receipts and return side-effect-free workflow proposals.

This module never sends messages, changes records, invokes operational tools, or
reads credentials. The --live switch is deliberately explicit and sends exactly
one synthetic final fixture to an already configured local bridge.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
from typing import Any

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SCREEN_NAMES = (
    "core-initial",
    "harness-screen",
    "core-refinement",
    "harness-refinement",
    "core-refinement-v3",
    "harness-refinement-v3",
)


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
    if not isinstance(values, dict) or set(values) != keys:
        return False
    if not all(probability(value) for value in values.values()):
        return False
    return abs(sum(values.values()) - 1) <= 0.000001


def valid_answers(questions: Any, response: Any) -> bool:
    """Validate typed Jev answers without treating them as trusted actions."""
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
        kind = question.get("type")
        answer = answers.get(question_id)
        if not isinstance(answer, dict) or answer.get("type") != kind:
            return False
        if kind == "noul":
            if not probability(answer.get("noul")):
                return False
        elif kind == "choice":
            criteria = question.get("criteria")
            if not isinstance(criteria, dict):
                return False
            if not isinstance(answer.get("choice"), str) or answer["choice"] not in criteria:
                return False
            if not probability(answer.get("confidence")):
                return False
            if not probability_distribution(answer.get("probabilities"), set(criteria)):
                return False
        elif kind == "score":
            criteria = question.get("criteria")
            value = answer.get("score")
            if (not isinstance(criteria, list)
                    or not finite_number(value)
                    or not 0 <= value <= len(criteria) - 1
                    or not probability(answer.get("confidence"))):
                return False
            score_keys = {str(index) for index in range(len(criteria))}
            if not probability_distribution(answer.get("probabilities"), score_keys):
                return False
        else:
            return False
    return True


def expected_match(answer: dict[str, Any], expected: dict[str, Any]) -> bool:
    value = answer_value(answer)
    if "choice" in expected:
        return value == expected["choice"]
    bounds = expected.get("range")
    return (
        isinstance(bounds, list)
        and len(bounds) == 2
        and finite_number(value)
        and bounds[0] <= value <= bounds[1]
    )


def contains_expected(value: Any) -> bool:
    if isinstance(value, dict):
        return "expected" in value or any(contains_expected(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_expected(item) for item in value)
    return False


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text())


def check_receipt(row: dict[str, Any], screen_name: str) -> dict[str, int]:
    if row.get("screen") != screen_name:
        raise ValueError("wrong screen on " + str(row.get("fixture_id")))
    request = row.get("request")
    response = row.get("response")
    if not isinstance(request, dict) or not isinstance(response, dict):
        raise ValueError("missing request/response receipt")
    if contains_expected(request.get("state")):
        raise ValueError("expected label leaked into state: " + str(row.get("fixture_id")))
    model = request.get("model")
    questions = request.get("questions")
    if not isinstance(model, str) or response.get("model") != model:
        raise ValueError("model binding mismatch: " + str(row.get("fixture_id")))
    if not valid_answers(questions, response):
        raise ValueError("invalid typed response: " + str(row.get("fixture_id")))
    signed = {"model": model, "state": request.get("state"), "questions": questions}
    if hashlib.sha256(canonical(signed)).hexdigest() != response.get("request_sha256"):
        raise ValueError("request digest mismatch: " + str(row.get("fixture_id")))
    checks = row.get("checks")
    if not isinstance(checks, list) or {check.get("question_id") for check in checks} != set(questions):
        raise ValueError("incomplete check set: " + str(row.get("fixture_id")))
    recomputed = []
    for check in checks:
        question_id = check["question_id"]
        expected = check.get("expected")
        if not isinstance(expected, dict):
            raise ValueError("missing expectation: " + str(row.get("fixture_id")))
        observed = answer_value(response["answers"][question_id])
        matched = expected_match(response["answers"][question_id], expected)
        if check.get("observed") != observed or check.get("match") is not matched:
            raise ValueError("stored check differs: " + str(row.get("fixture_id")))
        recomputed.append(matched)
    if row.get("match") is not all(recomputed):
        raise ValueError("stored request match differs: " + str(row.get("fixture_id")))
    return {
        "questions": len(checks),
        "question_matches": sum(recomputed),
        "fixture_match": int(all(recomputed)),
    }


def validate_final_catalog() -> tuple[dict[str, Any], dict[str, Any]]:
    catalog = load_json("catalog.json")
    fixtures = load_json("fixtures.json")
    patterns = catalog.get("patterns")
    if not isinstance(patterns, list) or len(patterns) != 30:
        raise ValueError("expected 30 final patterns")
    by_id = {pattern.get("id"): pattern for pattern in patterns}
    if len(by_id) != 30 or None in by_id:
        raise ValueError("pattern IDs must be unique")
    expected_domains = {"business": 7, "engineering": 7, "llm": 6, "harness": 10}
    domains = {key: sum(p.get("domain") == key for p in patterns) for key in expected_domains}
    if domains != expected_domains:
        raise ValueError("unexpected domain counts")
    if not isinstance(fixtures, list) or len(fixtures) != 134:
        raise ValueError("expected 134 final fixtures")
    if len({fixture.get("id") for fixture in fixtures}) != len(fixtures):
        raise ValueError("fixture IDs must be unique")
    for fixture in fixtures:
        pattern = by_id.get(fixture.get("pattern_id"))
        if pattern is None:
            raise ValueError("fixture references unknown pattern")
        state = fixture.get("state")
        if not isinstance(state, dict) or contains_expected(state):
            raise ValueError("invalid or label-contaminated final fixture state")
        required = pattern.get("required_state_fields")
        if not isinstance(required, list) or not set(required) <= set(state):
            raise ValueError("missing required state field: " + str(fixture.get("id")))
        questions = pattern.get("questions")
        expected = fixture.get("expected")
        if not isinstance(expected, dict) or set(expected) != set(questions):
            raise ValueError("fixture does not label every question: " + str(fixture.get("id")))
    return by_id, {fixture["id"]: fixture for fixture in fixtures}


def replay(root: Path = ROOT) -> dict[str, Any]:
    """Replay every saved receipt without a network call or state mutation."""
    if root != ROOT:
        old_root = ROOT
        raise ValueError("root override is unsupported; use the published iteration directory")
    screens = load_json("screens.json").get("screens")
    if not isinstance(screens, dict) or set(screens) != set(SCREEN_NAMES):
        raise ValueError("screen manifest mismatch")
    receipts: dict[str, dict[str, Any]] = {}
    metrics: dict[str, dict[str, int]] = {}
    for name in SCREEN_NAMES:
        meta = screens[name]
        relative = meta.get("result_file")
        rows = load_json(relative)
        if not isinstance(rows, list) or len(rows) != meta.get("fixture_count"):
            raise ValueError("receipt coverage mismatch: " + name)
        if len({row.get("fixture_id") for row in rows}) != len(rows):
            raise ValueError("duplicate fixture receipt: " + name)
        total = {"requests": len(rows), "fixture_matches": 0, "questions": 0, "question_matches": 0,
                 "request_digests_verified": 0}
        for row in rows:
            checked = check_receipt(row, name)
            total["fixture_matches"] += checked["fixture_match"]
            total["questions"] += checked["questions"]
            total["question_matches"] += checked["question_matches"]
            total["request_digests_verified"] += 1
            receipts[f"{name}:{row['fixture_id']}"] = row
        metrics[name] = total

    patterns, fixtures = validate_final_catalog()
    acceptance = load_json("results/final-acceptance.json").get("receipts")
    if not isinstance(acceptance, list) or len(acceptance) != len(fixtures):
        raise ValueError("final acceptance coverage mismatch")
    selected = {item.get("fixture_id"): item for item in acceptance}
    if set(selected) != set(fixtures):
        raise ValueError("final acceptance fixture IDs mismatch")
    final_matches = final_questions = final_question_matches = 0
    for fixture_id, fixture in fixtures.items():
        item = selected[fixture_id]
        screen = item.get("result_screen")
        receipt = receipts.get(f"{screen}:{fixture_id}")
        if receipt is None:
            raise ValueError("selected final receipt missing: " + fixture_id)
        pattern = patterns[fixture["pattern_id"]]
        if receipt.get("pattern_id") != fixture["pattern_id"]:
            raise ValueError("final receipt pattern mismatch")
        if item.get("contract_version") != pattern.get("contract_version"):
            raise ValueError("final receipt contract version mismatch")
        if canonical(receipt["request"]["state"]) != canonical(fixture["state"]):
            raise ValueError("final receipt state mismatch")
        if canonical(receipt["request"]["questions"]) != canonical(pattern["questions"]):
            raise ValueError("final receipt question contract mismatch")
        expected = {key: value for key, value in fixture["expected"].items()}
        receipt_expected = {check["question_id"]: check["expected"] for check in receipt["checks"]}
        if canonical(expected) != canonical(receipt_expected):
            raise ValueError("final receipt expectation mismatch")
        if item.get("request_sha256") != receipt["response"].get("request_sha256"):
            raise ValueError("final acceptance digest mismatch")
        if item.get("match") is not receipt.get("match"):
            raise ValueError("final acceptance match mismatch")
        final_matches += int(receipt["match"])
        final_questions += len(receipt["checks"])
        final_question_matches += sum(check["match"] for check in receipt["checks"])

    return {
        "screens": metrics,
        "final_contract_acceptance": {
            "fixtures": len(fixtures),
            "fixture_matches": final_matches,
            "questions": final_questions,
            "question_matches": final_question_matches,
        },
    }


def ready(pattern: dict[str, Any], answer: dict[str, Any]) -> bool:
    policy = pattern.get("policy", {})
    if answer.get("type") == "noul":
        return (
            answer.get("noul", 0.5) >= policy.get("noul_yes_floor", 0.8)
            or answer.get("noul", 0.5) <= policy.get("noul_no_ceiling", 0.2)
        )
    return answer.get("confidence", 0.0) >= policy.get("choice_score_confidence_floor", 0.8)


def plan(pattern: dict[str, Any], response: dict[str, Any], control: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a non-executing next-step proposal.

    Trusted control metadata is supplied and validated by caller-owned code. A
    Jev answer can choose only a review/proposal path; it never grants authority.
    """
    control = control or {}
    if not valid_answers(pattern.get("questions"), response):
        return {"next": "review", "reason": "provider_or_schema_failure"}
    answers = response["answers"]
    if not all(ready(pattern, answer) for answer in answers.values()):
        return {"next": "review", "reason": "uncertain_consumed_answer"}
    decision = answer_value(answers.get("decision"))
    pid = pattern.get("id")

    if pid == "B08":
        return {"next": {
            "within_policy": "propose_standard_policy_route",
            "exception_review": "request_designated_policy_review",
            "prohibited": "hold_and_surface_policy_clause",
            "insufficient": "ask_for_controlling_policy_condition",
        }.get(decision, "review")}
    if pid == "E13":
        return {"next": {
            "direct": "record_direct_signal_candidate",
            "proxy_only": "propose_observability_gap_review",
            "unobservable": "request_observability_design",
            "insufficient": "clarify_measurement_relationship",
        }.get(decision, "review")}
    if pid == "L09":
        if decision in ("no_match", "uncertain"):
            return {"next": "retain_current_taxonomy_node"}
        return {"next": "propose_taxonomy_child", "child": decision,
                "taxonomy_version_must_match": True}
    if pid == "L11":
        score = answers["coverage"]["score"]
        if score < 2:
            return {"next": "hold_answer_plan_for_missing_obligations"}
        return {"next": "propose_evidence_plan_review", "coverage_score": score}
    if pid == "H11":
        if decision in ("no_match", "uncertain"):
            return {"next": "retain_broader_taxonomy_node"}
        return {"next": "propose_taxonomy_child_for_review", "child": decision}
    if pid == "H12":
        samples = control.get("samples", [])
        if (decision == "automatic"
                and control.get("low_stakes_rule_verified") is True
                and isinstance(samples, list)
                and len(samples) == 3
                and samples == ["automatic", "automatic", "automatic"]):
            return {"next": "propose_low_stakes_route_for_independent_authorization"}
        return {"next": "review_repeated_decision"}
    if pid == "H13":
        mode = answers["mode"]["choice"]
        candidate = answers["candidate"]["choice"]
        if candidate in ("not_stated", "ambiguous") or mode in ("not_stated", "ambiguous"):
            return {"next": "clarify_date_expression"}
        if mode == "relative_to_reference" and control.get("reference_date_verified") is not True:
            return {"next": "await_verified_reference_date"}
        if mode == "relative_to_event" and control.get("event_date_verified") is not True:
            return {"next": "await_verified_event_date"}
        return {"next": "propose_deterministic_date_resolution", "candidate": candidate,
                "mode": mode}
    if pid == "H14":
        if decision in ("not_found", "ambiguous"):
            return {"next": "expand_or_preserve_candidate_search"}
        spans = control.get("candidate_spans")
        document = control.get("document")
        span = spans.get(decision) if isinstance(spans, dict) else None
        offset = span.get("offset") if isinstance(span, dict) else None
        text = span.get("text") if isinstance(span, dict) else None
        if (control.get("source_revision_verified") is not True
                or type(offset) is not int
                or not isinstance(text, str)
                or not isinstance(document, str)
                or document[offset:offset + len(text)] != text):
            return {"next": "hold_unverified_candidate_span"}
        return {"next": "propose_normalize_verified_span", "span_id": decision}
    if pid == "H15":
        if decision == "consistent" and control.get("binding_sources_verified") is True:
            return {"next": "propose_role_separated_assembly"}
        return {"next": "hold_prompt_assembly_for_review"}
    if pid == "H16":
        if decision == "unchanged" and control.get("state_revision_match") is True:
            return {"next": "propose_continue_pending_plan"}
        return {"next": "discard_pending_proposal_and_replan"}
    if pid == "H17":
        if decision == "verified" and control.get("source_identity_verified") is True:
            return {"next": "propose_field_as_verified"}
        return {"next": {
            "contradicted": "preserve_conflict_for_verifier",
            "not_evidenced": "request_field_evidence",
            "insufficient": "review_field_mapping",
        }.get(decision, "review")}
    if pid == "H18":
        if decision == "complete" and control.get("obligation_ids_complete") is True:
            return {"next": "propose_evidence_complete_answer_for_review"}
        return {"next": "hold_answer_release"}
    if pid == "H19":
        hazard = answers["hazard"]["noul"]
        severity = answers["severity"]["score"]
        policy = pattern["policy"]
        if hazard >= policy["noul_yes_floor"]:
            return {"next": ("request_material_policy_review" if severity >= 2
                             else "request_limited_policy_review"),
                    "severity": severity}
        if hazard <= policy["noul_no_ceiling"]:
            return {"next": "no_policy_hazard_route_proposed"}
        return {"next": "review", "reason": "uncertain_policy_hazard"}
    if pid == "H20":
        return {"next": "record_for_independent_human_adjudication",
                "probability": answers["eligible"]["noul"],
                "automatic_threshold_change": False}
    return {"next": "review_typed_signal", "answers": answers}


def live_one(bridge: str, fixture_id: str) -> Any:
    patterns, fixtures = validate_final_catalog()
    fixture = fixtures.get(fixture_id)
    if fixture is None:
        raise ValueError("unknown final fixture")
    pattern = patterns[fixture["pattern_id"]]
    request = {"state": fixture["state"], "questions": pattern["questions"], "use_cache": False}
    run = subprocess.run(
        [bridge, "decide"],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        timeout=20,
        check=True,
    )
    return json.loads(run.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true",
                        help="explicitly send one synthetic final fixture; never a batch")
    parser.add_argument("--fixture", help="final fixture ID required with --live")
    parser.add_argument("--bridge", default="jev-workflows",
                        help="existing configured bridge executable")
    args = parser.parse_args()
    if args.live:
        if not args.fixture:
            parser.error("--live requires --fixture; no implicit provider spend")
        print(json.dumps(live_one(args.bridge, args.fixture), indent=2))
        return
    print(json.dumps(replay(), indent=2))


if __name__ == "__main__":
    main()
