#!/usr/bin/env python3
"""Offline receipt verification and side-effect-free advisory controllers.

No production action is executed. --live explicitly sends one synthetic fixture
through an already-configured Jev bridge; no credentials are read by this script.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
SCREENS = ("core-initial", "core-refinement", "harness-screen")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":")).encode("utf-8")


def probability(value):
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1


def valid_answers(questions, response):
    if not isinstance(response, dict) or response.get("ok") is not True:
        return False
    answers = response.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        return False
    for key, question in questions.items():
        answer = answers[key]
        if not isinstance(answer, dict) or answer.get("type") != question["type"]:
            return False
        kind = question["type"]
        if kind == "noul":
            if not probability(answer.get("noul")):
                return False
        elif kind in ("choice", "score"):
            if not probability(answer.get("confidence")):
                return False
            if kind == "choice":
                if (not isinstance(answer.get("choice"), str)
                        or answer["choice"] not in question["criteria"]):
                    return False
            else:
                value = answer.get("score")
                if (type(value) not in (int, float) or not math.isfinite(value)
                        or not 0 <= value <= len(question["criteria"]) - 1):
                    return False
        else:
            return False
    return True


def ready(answer):
    if answer["type"] == "noul":
        return answer["noul"] <= 0.2 or answer["noul"] >= 0.8
    return answer["confidence"] >= 0.8


def checks_for(fixture, response):
    result = []
    for key, expected in fixture["expected"].items():
        answer = response.get("answers", {}).get(key, {})
        value = answer.get("choice", answer.get("noul", answer.get("score")))
        match = (value == expected["choice"] if "choice" in expected else
                 type(value) in (int, float) and math.isfinite(value)
                 and expected["range"][0] <= value <= expected["range"][1])
        result.append({"question_id": key, "value": value, "match": match})
    return result


def plan(pattern, response, control=None):
    """Return a proposal, never perform a tool call, write, merge or notification.

    control is trusted host metadata, not model output or extracted source text.
    Fresh source/authority checks and an external permission layer remain required.
    """
    control = control or {}
    if pattern["id"] == "H07" and control.get("mandatory_alert") is True:
        return {"next": "mandatory_policy_review"}
    if not valid_answers(pattern["questions"], response):
        return {"next": "review", "reason": "provider_or_schema_failure"}
    answers = response["answers"]
    pid = pattern["id"]
    if pid == "E01":
        evidence = answers["evidence"]
        if not ready(evidence) or evidence["choice"] != "enough":
            return {"next": "request_impact_evidence"}  # Ignore unused score.
        if not ready(answers["impact"]):
            return {"next": "review", "reason": "uncertain_impact"}
        return {"next": "review_priority", "score": answers["impact"]["score"]}
    if pid == "L01":
        if (control.get("required") is True
                or answers["premise_conflict"]["noul"] > 0.2
                or not all(ready(a) for a in answers.values())):
            return {"next": "retain_passage"}
        return {"next": "rank_passage", "score": answers["relevance"]["score"]}
    if pid == "H01":
        if not (control.get("request_target_bound") is True
                and control.get("candidates_complete") is True):
            return {"next": "clarify", "reason": "unbound_target_or_incomplete_candidates"}
        # A middle probability remains possible, not silently dropped.
        plausible = [k for k, a in answers.items() if a["noul"] > 0.2]
        operations = control.get("operations", {})
        if not plausible:
            return {"next": "clarify", "reason": "no_matching_interpretation"}
        selected = []
        for key in plausible:
            op = operations.get(key)
            if (not isinstance(op, dict) or not isinstance(op.get("tool"), str)
                    or not isinstance(op.get("args"), dict)
                    or op.get("authorized") is not True
                    or op.get("read_only") is not True):
                return {"next": "review", "reason": "unapproved_or_nonread_operation"}
            selected.append({"tool": op["tool"], "args": op["args"]})
        try:
            identical = len({canonical(op) for op in selected}) == 1
        except (TypeError, ValueError):
            return {"next": "review", "reason": "invalid_operation"}
        if not identical:
            return {"next": "clarify", "reason": "different_next_reads"}
        return {"next": "propose_same_authorized_read", "operation": selected[0]}
    if pid == "L05":
        # A known conflict takes priority; unused missing-detail signals do not block it.
        if answers["constraint_conflict"]["noul"] >= 0.8:
            return {"next": "ask_constraint_priority"}
        if not ready(answers["constraint_conflict"]):
            return {"next": "review", "reason": "uncertain_constraint"}
        for key, action in (("target_clear", "ask_target"), ("success_clear", "ask_success")):
            if not ready(answers[key]):
                return {"next": "review", "reason": "uncertain_" + key}
            if answers[key]["noul"] <= 0.2:
                return {"next": action}
        return {"next": "normal_planning"}
    if pid == "B02":
        for key in ("location", "symptom", "access"):
            if not ready(answers[key]):
                return {"next": "review", "reason": "uncertain_" + key}
            if answers[key]["noul"] <= 0.2:
                return {"next": "ask_" + key}
        return {"next": "verify_dispatch_details"}  # Not authority to dispatch.
    if not all(ready(a) for a in answers.values()):
        return {"next": "review", "reason": "uncertain_consumed_answer"}
    decision = answers.get("decision", {}).get("choice")
    if pid == "H02":
        if decision in ("restates", "irrelevant"):
            count = control.get("stall_count", 0)
            limit = control.get("stall_limit", 2)
            if (type(count) is not int or count < 0 or type(limit) is not int or limit < 1):
                return {"next": "review", "reason": "invalid_stall_budget"}
            count += 1
            return {"next": "change_evidence_plan" if count >= limit else "retain_and_continue",
                    "stall_count": count}
        if decision == "adds_evidence":
            return {"next": "inspect_new_evidence", "stall_count": 0}
        return {"next": "preserve_conflict" if decision == "contradicts" else "review"}
    if pid == "H03":
        return {"next": "branch_check_passed" if decision == "preserved" else "retain_original_context"}
    if pid == "H04":
        return {"next": {"subject_mismatch": "rebind_subject", "fact_gap": "retrieve_disputed_fact",
                         "rubric_tradeoff": "ask_criterion_priority",
                         "no_disagreement": "record_agreement"}.get(decision, "review")}
    if pid == "H05":
        used = control.get("repair_attempts", 0)
        if type(used) is not int or used < 0 or used >= 1 or decision == "not_established":
            return {"next": "retain_failure_for_review"}
        return {"next": "propose_one_targeted_repair", "defect": decision}
    if pid == "H06":
        if decision == "task_value" and control.get("source_binding_verified") is True:
            return {"next": "normal_tool_preflight"}  # Still not execution.
        return {"next": "hold_argument"}
    if pid == "H07":
        if decision == "completion" and control.get("completion_verified") is not True:
            return {"next": "verify_completion"}
        return {"next": "no_notification_proposal" if decision == "noise" else "draft_status_for_review"}
    if pid == "H08":
        return {"next": "candidate_for_safe_cost_ranking" if decision == "discriminating"
                else "seek_discriminating_check"}
    if pid == "H09":
        return {"next": {"direct_goal": "normal_scope_preflight",
                         "necessary_prerequisite": "verify_prerequisite_and_permission",
                         "optional_extension": "backlog_pending_user_choice",
                         "unrelated": "exclude_from_this_run"}.get(decision, "review")}
    if pid == "H10":
        return {"next": "reopen_recommendation_for_review" if decision == "undermines"
                else "retain_recommendation_history"}
    return {"next": "review_typed_signal", "answers": answers}


def replay(root=ROOT):
    screens = json.loads((root / "screens.json").read_text())
    summary = {}
    for name in SCREENS:
        screen = screens[name]
        fixtures = {f["id"]: f for f in screen["fixtures"]}
        rows = json.loads((root / "results" / (name + ".json")).read_text())
        if len(rows) != len(fixtures) or {r["fixture_id"] for r in rows} != set(fixtures):
            raise ValueError("receipt coverage mismatch: " + name)
        matching = accepted = accepted_matches = questions_count = question_matches = 0
        for row in rows:
            fixture = fixtures[row["fixture_id"]]
            if row["pattern_id"] != fixture["pattern_id"]:
                raise ValueError("pattern mismatch")
            qs = screen["contracts"][fixture["pattern_id"]]["questions"]
            response = row["response"]
            if not valid_answers(qs, response):
                raise ValueError("invalid successful receipt: " + fixture["id"])
            request = {"model": response["model"], "state": fixture["state"], "questions": qs}
            if hashlib.sha256(canonical(request)).hexdigest() != response["request_sha256"]:
                raise ValueError("request digest mismatch: " + fixture["id"])
            checks = checks_for(fixture, response)
            match = all(c["match"] for c in checks)
            if row["match"] != match:
                raise ValueError("stored match differs from recomputed match")
            stored = {c["question_id"]: c for c in row["checks"]}
            for check in checks:
                if any(stored[check["question_id"]].get(k) != check[k] for k in ("value", "match")):
                    raise ValueError("stored check differs from recomputed check")
                answer = response["answers"][check["question_id"]]
                if ready(answer):
                    accepted += 1
                    accepted_matches += int(check["match"])
            matching += int(match)
            questions_count += len(checks)
            question_matches += sum(c["match"] for c in checks)
        summary[name] = {"requests": len(rows), "fixture_matches": matching,
                         "questions": questions_count, "question_matches": question_matches,
                         "threshold_decided_questions": accepted,
                         "threshold_decided_matches": accepted_matches,
                         "request_digests_verified": len(rows)}
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Explicitly send one synthetic fixture to TypeSafe")
    parser.add_argument("--screen", choices=SCREENS)
    parser.add_argument("--fixture")
    parser.add_argument("--bridge", default="jev-workflows", help="Existing configured bridge executable")
    args = parser.parse_args()
    if not args.live:
        print(json.dumps(replay(), indent=2))
        return
    if not args.screen or not args.fixture:
        parser.error("--live requires --screen and --fixture; no implicit batch spend")
    screens = json.loads((ROOT / "screens.json").read_text())
    screen = screens[args.screen]
    fixture = next((f for f in screen["fixtures"] if f["id"] == args.fixture), None)
    if fixture is None:
        parser.error("fixture not present in selected screen")
    qs = screen["contracts"][fixture["pattern_id"]]["questions"]
    request = {"state": fixture["state"], "questions": qs, "use_cache": False}
    try:
        run = subprocess.run([args.bridge, "decide"], input=json.dumps(request), text=True,
                             capture_output=True, timeout=15, check=True)
        response = json.loads(run.stdout)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise SystemExit("Live bridge unavailable or invalid response (" + type(exc).__name__ + ")")
    # No expected labels or fixture IDs were sent to the model.
    print(json.dumps({"fixture_id": fixture["id"], "pattern_id": fixture["pattern_id"],
                      "response": response, "checks": checks_for(fixture, response)}, indent=2))


if __name__ == "__main__":
    main()
