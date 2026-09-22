import copy
import json
import unittest

from evaluate import ROOT, contains_expected, plan, replay, valid_answers


CATALOG = json.loads((ROOT / "catalog.json").read_text())
PATTERNS = {pattern["id"]: pattern for pattern in CATALOG["patterns"]}


def response(pattern_id, values=None, confidence=1.0):
    """Build a schema-valid synthetic response, never a provider receipt."""
    values = values or {}
    answers = {}
    for key, question in PATTERNS[pattern_id]["questions"].items():
        kind = question["type"]
        value = values.get(key)
        if kind == "choice":
            selected = value if value is not None else next(iter(question["criteria"]))
            probabilities = {label: float(label == selected) for label in question["criteria"]}
            answers[key] = {
                "type": "choice",
                "choice": selected,
                "confidence": confidence,
                "probabilities": probabilities,
            }
        elif kind == "score":
            selected = 1 if value is None else value
            bucket = min(len(question["criteria"]) - 1, max(0, round(selected)))
            probabilities = {str(index): float(index == bucket)
                             for index in range(len(question["criteria"]))}
            answers[key] = {
                "type": "score",
                "score": selected,
                "confidence": confidence,
                "probabilities": probabilities,
            }
        else:
            answers[key] = {"type": "noul", "noul": 0.95 if value is None else value}
    return {"ok": True, "answers": answers}


class ReceiptTests(unittest.TestCase):
    def test_receipts_are_replayable_and_final_contracts_pass(self):
        result = replay()
        self.assertEqual(
            sum(item["request_digests_verified"] for item in result["screens"].values()),
            168,
        )
        self.assertEqual(result["screens"]["core-initial"]["fixture_matches"], 80)
        self.assertEqual(result["screens"]["harness-screen"]["fixture_matches"], 44)
        self.assertEqual(result["screens"]["core-refinement"]["fixture_matches"], 15)
        self.assertEqual(result["screens"]["harness-refinement"]["fixture_matches"], 8)
        self.assertEqual(result["screens"]["core-refinement-v3"]["fixture_matches"], 5)
        self.assertEqual(result["screens"]["harness-refinement-v3"]["fixture_matches"], 4)
        self.assertEqual(result["final_contract_acceptance"], {
            "fixtures": 134,
            "fixture_matches": 134,
            "questions": 147,
            "question_matches": 147,
        })

    def test_catalog_has_expected_domain_counts(self):
        self.assertEqual(len(PATTERNS), 30)
        self.assertEqual(
            {domain: sum(pattern["domain"] == domain for pattern in PATTERNS.values())
             for domain in ("business", "engineering", "llm", "harness")},
            {"business": 7, "engineering": 7, "llm": 6, "harness": 10},
        )

    def test_final_states_keep_expected_labels_out_of_provider_input(self):
        fixtures = json.loads((ROOT / "fixtures.json").read_text())
        for fixture in fixtures:
            with self.subTest(fixture=fixture["id"]):
                self.assertFalse(contains_expected(fixture["state"]))
                self.assertEqual(set(fixture["expected"]),
                                 set(PATTERNS[fixture["pattern_id"]]["questions"]))

    def test_unknown_choice_and_non_scalar_value_fail_closed(self):
        invalid = response("B08", {"decision": "perform_action"})
        self.assertFalse(valid_answers(PATTERNS["B08"]["questions"], invalid))
        invalid = response("B08")
        invalid["answers"]["decision"]["choice"] = ["within_policy"]
        self.assertFalse(valid_answers(PATTERNS["B08"]["questions"], invalid))

    def test_bad_probability_forms_fail_closed(self):
        for value in (True, float("nan"), float("inf"), -0.01, 1.01, "0.9", None):
            with self.subTest(value=value):
                invalid = response("H20")
                invalid["answers"]["eligible"]["noul"] = value
                self.assertFalse(valid_answers(PATTERNS["H20"]["questions"], invalid))

    def test_provider_failure_never_has_a_default_action(self):
        for pattern in PATTERNS.values():
            with self.subTest(pattern=pattern["id"]):
                self.assertEqual(plan(pattern, {"ok": False})["next"], "review")

    def test_low_confidence_choice_is_reviewed(self):
        signal = response("B08", {"decision": "within_policy"}, confidence=0.79)
        self.assertEqual(plan(PATTERNS["B08"], signal)["next"], "review")

    def test_policy_exception_result_never_authorizes_action(self):
        next_step = plan(PATTERNS["B08"], response("B08", {"decision": "exception_review"}))
        self.assertEqual(next_step["next"], "request_designated_policy_review")
        self.assertNotIn("approve", next_step["next"])

    def test_h11_retains_broader_category_on_no_match(self):
        signal = response("H11", {"decision": "no_match"})
        self.assertEqual(plan(PATTERNS["H11"], signal)["next"], "retain_broader_taxonomy_node")

    def test_h12_requires_exact_stable_low_stakes_samples(self):
        signal = response("H12", {"decision": "automatic"})
        self.assertEqual(
            plan(PATTERNS["H12"], signal, {
                "low_stakes_rule_verified": True,
                "samples": ["automatic", "automatic", "automatic"],
            })["next"],
            "propose_low_stakes_route_for_independent_authorization",
        )
        self.assertEqual(
            plan(PATTERNS["H12"], signal, {
                "low_stakes_rule_verified": True,
                "samples": ["automatic", "review", "automatic"],
            })["next"],
            "review_repeated_decision",
        )

    def test_h13_never_resolves_relative_date_without_verified_reference(self):
        signal = response("H13", {"mode": "relative_to_event", "candidate": "c1"})
        self.assertEqual(
            plan(PATTERNS["H13"], signal, {"event_date_verified": False})["next"],
            "await_verified_event_date",
        )
        self.assertEqual(
            plan(PATTERNS["H13"], signal, {"event_date_verified": True})["next"],
            "propose_deterministic_date_resolution",
        )

    def test_h14_requires_exact_verified_offset(self):
        signal = response("H14", {"decision": "s1"})
        control = {
            "source_revision_verified": True,
            "document": "Send invoice to billing@example.test.",
            "candidate_spans": {"s1": {"text": "billing@example.test", "offset": 16}},
        }
        self.assertEqual(
            plan(PATTERNS["H14"], signal, control)["next"],
            "propose_normalize_verified_span",
        )
        control["candidate_spans"]["s1"]["offset"] = 17
        self.assertEqual(
            plan(PATTERNS["H14"], signal, control)["next"],
            "hold_unverified_candidate_span",
        )

    def test_h15_does_not_promote_reference_without_binding_verification(self):
        signal = response("H15", {"decision": "consistent"})
        self.assertEqual(plan(PATTERNS["H15"], signal)["next"], "hold_prompt_assembly_for_review")
        self.assertEqual(
            plan(PATTERNS["H15"], signal, {"binding_sources_verified": True})["next"],
            "propose_role_separated_assembly",
        )

    def test_h16_drops_pending_proposal_after_material_change(self):
        signal = response("H16", {"decision": "replan_required"})
        self.assertEqual(plan(PATTERNS["H16"], signal)["next"],
                         "discard_pending_proposal_and_replan")
        unchanged = response("H16", {"decision": "unchanged"})
        self.assertEqual(plan(PATTERNS["H16"], unchanged)["next"],
                         "discard_pending_proposal_and_replan")

    def test_h17_field_verification_requires_source_identity(self):
        signal = response("H17", {"decision": "verified"})
        self.assertEqual(plan(PATTERNS["H17"], signal)["next"], "review")
        self.assertEqual(
            plan(PATTERNS["H17"], signal, {"source_identity_verified": True})["next"],
            "propose_field_as_verified",
        )

    def test_h18_evidence_release_requires_deterministic_ids(self):
        signal = response("H18", {"decision": "complete"})
        self.assertEqual(plan(PATTERNS["H18"], signal)["next"], "hold_answer_release")
        self.assertEqual(
            plan(PATTERNS["H18"], signal, {"obligation_ids_complete": True})["next"],
            "propose_evidence_complete_answer_for_review",
        )

    def test_h19_always_routes_to_review_not_an_action(self):
        signal = response("H19", {"hazard": 0.95, "severity": 2.4})
        result = plan(PATTERNS["H19"], signal)
        self.assertEqual(result["next"], "request_material_policy_review")
        self.assertNotIn("execute", result["next"])

    def test_h20_records_for_later_adjudication_without_threshold_change(self):
        result = plan(PATTERNS["H20"], response("H20", {"eligible": 0.99}))
        self.assertEqual(result["next"], "record_for_independent_human_adjudication")
        self.assertFalse(result["automatic_threshold_change"])

    def test_latest_contract_mapping_uses_l09_v3(self):
        acceptance = json.loads((ROOT / "results/final-acceptance.json").read_text())["receipts"]
        by_fixture = {item["fixture_id"]: item for item in acceptance}
        self.assertEqual(by_fixture["L09-1"]["contract_version"], 3)
        self.assertEqual(by_fixture["L09-1"]["result_screen"], "core-refinement-v3")
        self.assertEqual(by_fixture["B08-1"]["contract_version"], 2)
        self.assertEqual(by_fixture["H19-1"]["contract_version"], 3)
        self.assertEqual(by_fixture["H19-1"]["result_screen"], "harness-refinement-v3")

    def test_planning_does_not_mutate_response_or_control(self):
        signal = response("H14", {"decision": "s1"})
        control = {
            "source_revision_verified": True,
            "document": "abc",
            "candidate_spans": {"s1": {"text": "a", "offset": 0}},
        }
        before = copy.deepcopy((signal, control))
        plan(PATTERNS["H14"], signal, control)
        self.assertEqual((signal, control), before)


if __name__ == "__main__":
    unittest.main()
