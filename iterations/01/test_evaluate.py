import copy
import json
import unittest

from evaluate import ROOT, plan, replay, valid_answers


CATALOG = json.loads((ROOT / "catalog.json").read_text())
PATTERNS = {p["id"]: p for p in CATALOG["patterns"]}


def response(pid, values=None, confidence=1.0):
    values = values or {}
    answers = {}
    for key, q in PATTERNS[pid]["questions"].items():
        kind = q["type"]
        value = values.get(key)
        if kind == "choice":
            answers[key] = {"type": kind, "choice": value or next(iter(q["criteria"])),
                            "confidence": confidence}
        elif kind == "noul":
            answers[key] = {"type": kind, "noul": 0.95 if value is None else value}
        else:
            answers[key] = {"type": kind, "score": 1 if value is None else value,
                            "confidence": confidence}
    return {"ok": True, "answers": answers}


def op(tool="read_log", record="sample"):
    return {"tool": tool, "args": {"record": record}, "authorized": True, "read_only": True}


class ReceiptTests(unittest.TestCase):
    def test_all_receipts_bind_exact_state_and_question(self):
        result = replay()
        self.assertEqual(sum(s["request_digests_verified"] for s in result.values()), 136)
        self.assertEqual(result["core-initial"]["fixture_matches"], 76)
        self.assertEqual(result["core-refinement"]["fixture_matches"], 15)
        self.assertEqual(result["harness-screen"]["fixture_matches"], 38)

    def test_catalog_domain_counts_and_unique_ids(self):
        self.assertEqual(len(PATTERNS), 30)
        self.assertEqual({d: sum(p["domain"] == d for p in PATTERNS.values())
                          for d in ("business", "engineering", "llm", "harness")},
                         {"business": 7, "engineering": 7, "llm": 6, "harness": 10})

    def test_model_failure_has_no_default_acceptance(self):
        for p in PATTERNS.values():
            with self.subTest(pattern=p["id"]):
                self.assertEqual(plan(p, {"ok": False})["next"], "review")

    def test_unknown_label_is_rejected(self):
        r = response("B01", {"decision": "delete_everything"})
        self.assertFalse(valid_answers(PATTERNS["B01"]["questions"], r))

    def test_non_scalar_label_fails_closed(self):
        r = response("B01")
        r["answers"]["decision"]["choice"] = ["billing"]
        self.assertFalse(valid_answers(PATTERNS["B01"]["questions"], r))

    def test_nan_and_boolean_are_not_probabilities(self):
        for bad in (float("nan"), float("inf"), True, -0.1, 1.1, "0.99", None):
            with self.subTest(value=bad):
                r = response("B02")
                r["answers"]["access"]["noul"] = bad
                self.assertFalse(valid_answers(PATTERNS["B02"]["questions"], r))

    def test_missing_answer_fails_closed(self):
        r = response("B02")
        del r["answers"]["access"]
        self.assertEqual(plan(PATTERNS["B02"], r)["next"], "review")

    def test_low_confidence_is_review(self):
        self.assertEqual(plan(PATTERNS["E02"], response("E02", confidence=0.79))["next"], "review")

    def test_dispatch_asks_first_missing_dimension(self):
        r = response("B02", {"location": 0.01, "symptom": 0.99, "access": 0.99})
        self.assertEqual(plan(PATTERNS["B02"], r)["next"], "ask_location")

    def test_dispatch_ready_still_requires_verification(self):
        self.assertEqual(plan(PATTERNS["B02"], response("B02"))["next"], "verify_dispatch_details")

    def test_unused_impact_confidence_does_not_block_evidence_request(self):
        r = response("E01", {"evidence": "missing"})
        r["answers"]["impact"]["confidence"] = 0.01
        self.assertEqual(plan(PATTERNS["E01"], r)["next"], "request_impact_evidence")

    def test_constraint_conflict_takes_priority_over_unknown_target(self):
        r = response("L05", {"constraint_conflict": 0.95, "target_clear": 0.5})
        self.assertEqual(plan(PATTERNS["L05"], r)["next"], "ask_constraint_priority")

    def test_required_or_uncertain_counterevidence_is_retained(self):
        for values, control in (({"premise_conflict": 0.5}, {}),
                                ({"premise_conflict": 0.01}, {"required": True})):
            r = response("L01", values)
            self.assertEqual(plan(PATTERNS["L01"], r, control)["next"], "retain_passage")

    def test_h01_same_authorized_read_is_only_a_proposal(self):
        c = {"request_target_bound": True, "candidates_complete": True,
             "operations": {"a_plausible": op(), "b_plausible": op()}}
        result = plan(PATTERNS["H01"], response("H01"), c)
        self.assertEqual(result["next"], "propose_same_authorized_read")
        self.assertEqual(result["operation"], {"tool": "read_log", "args": {"record": "sample"}})

    def test_h01_same_tool_different_arguments_requires_clarification(self):
        c = {"request_target_bound": True, "candidates_complete": True,
             "operations": {"a_plausible": op(record="one"), "b_plausible": op(record="two")}}
        self.assertEqual(plan(PATTERNS["H01"], response("H01"), c)["next"], "clarify")

    def test_h01_ambiguous_probability_is_not_dropped(self):
        c = {"request_target_bound": True, "candidates_complete": True,
             "operations": {"a_plausible": op(record="one"), "b_plausible": op(record="two")}}
        r = response("H01", {"a_plausible": 0.95, "b_plausible": 0.5})
        self.assertEqual(plan(PATTERNS["H01"], r, c)["next"], "clarify")

    def test_h01_unbound_target_blocks_actual_high_probability_failure(self):
        rows = json.loads((ROOT / "results/harness-screen.json").read_text())
        failed = next(r for r in rows if r["fixture_id"] == "H01-4")
        self.assertGreaterEqual(failed["response"]["answers"]["a_plausible"]["noul"], 0.8)
        c = {"request_target_bound": False, "candidates_complete": True,
             "operations": {"a_plausible": op(), "b_plausible": op()}}
        self.assertEqual(plan(PATTERNS["H01"], failed["response"], c)["next"], "clarify")

    def test_h01_does_not_approve_write_or_unapproved_read(self):
        for flag in ("authorized", "read_only"):
            one = op()
            one[flag] = False
            c = {"request_target_bound": True, "candidates_complete": True,
                 "operations": {"a_plausible": one, "b_plausible": op()}}
            self.assertEqual(plan(PATTERNS["H01"], response("H01"), c)["next"], "review")

    def test_semantic_stall_budget(self):
        r = response("H02", {"decision": "restates"})
        self.assertEqual(plan(PATTERNS["H02"], r, {"stall_count": 1})["next"], "change_evidence_plan")

    def test_conflict_is_not_counted_as_repetition(self):
        r = response("H02", {"decision": "contradicts"})
        self.assertEqual(plan(PATTERNS["H02"], r)["next"], "preserve_conflict")

    def test_handoff_cannot_close_a_branch(self):
        r = response("H03", {"decision": "prematurely_resolved"})
        self.assertEqual(plan(PATTERNS["H03"], r)["next"], "retain_original_context")

    def test_disagreement_routes_to_relevant_recovery(self):
        for choice, expected in (("fact_gap", "retrieve_disputed_fact"),
                                 ("rubric_tradeoff", "ask_criterion_priority"),
                                 ("subject_mismatch", "rebind_subject")):
            self.assertEqual(plan(PATTERNS["H04"], response("H04", {"decision": choice}))["next"], expected)

    def test_repair_loop_is_bounded(self):
        r = response("H05", {"decision": "criterion_ambiguity"})
        self.assertEqual(plan(PATTERNS["H05"], r, {"repair_attempts": 1})["next"], "retain_failure_for_review")

    def test_example_or_unverified_argument_is_held(self):
        for choice in ("example_only", "unknown", "conflict", "task_value"):
            self.assertEqual(plan(PATTERNS["H06"], response("H06", {"decision": choice}))["next"], "hold_argument")

    def test_model_completion_is_not_verified_completion(self):
        r = response("H07", {"decision": "completion"})
        self.assertEqual(plan(PATTERNS["H07"], r)["next"], "verify_completion")

    def test_provider_failure_cannot_suppress_mandatory_alert(self):
        self.assertEqual(plan(PATTERNS["H07"], {"ok": False}, {"mandatory_alert": True})["next"],
                         "mandatory_policy_review")

    def test_non_discriminating_diagnostic_is_not_recommended(self):
        r = response("H08", {"decision": "non_discriminating"})
        self.assertEqual(plan(PATTERNS["H08"], r)["next"], "seek_discriminating_check")

    def test_optional_scope_is_not_authorized(self):
        r = response("H09", {"decision": "optional_extension"})
        self.assertEqual(plan(PATTERNS["H09"], r)["next"], "backlog_pending_user_choice")

    def test_retraction_is_review_not_message_delivery(self):
        r = response("H10", {"decision": "undermines"})
        self.assertEqual(plan(PATTERNS["H10"], r)["next"], "reopen_recommendation_for_review")

    def test_planning_does_not_mutate_input(self):
        r = response("H02", {"decision": "restates"})
        c = {"stall_count": 1}
        old = copy.deepcopy((r, c))
        plan(PATTERNS["H02"], r, c)
        self.assertEqual((r, c), old)

    def test_expected_label_never_in_live_state(self):
        screens = json.loads((ROOT / "screens.json").read_text())
        for screen in screens.values():
            for fixture in screen["fixtures"]:
                self.assertNotIn("expected", fixture["state"])
                asked = set(screen["contracts"][fixture["pattern_id"]]["questions"])
                labeled = set(fixture["expected"])
                self.assertTrue(labeled <= asked)
                if asked != labeled:
                    self.assertEqual(fixture["pattern_id"], "E01")
                    self.assertEqual(asked - labeled, {"impact"})
                    self.assertIn(fixture["expected"]["evidence"]["choice"], ("missing", "conflict"))


if __name__ == "__main__":
    unittest.main()
