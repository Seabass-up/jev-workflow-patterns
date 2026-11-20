import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import evaluate

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import ROOT, contains_expected, plan as raw_plan, replay, valid_answers


CATALOG = json.loads((ROOT / "catalog.json").read_text())
PATTERNS = {pattern["id"]: pattern for pattern in CATALOG["patterns"]}


def plan(pattern, signal):
    # Pure branch tests provide nonempty synthetic evidence, not provider proof.
    state = {field: "synthetic branch-test evidence" for field in pattern["required_state_fields"]}
    return raw_plan(pattern, signal, state=state)


def response(pattern_id, values=None, confidence=1.0):
    """Build a schema-valid local synthetic response; this is not a provider receipt."""
    values = values or {}
    answers = {}
    for key, question in PATTERNS[pattern_id]["questions"].items():
        kind = question["type"]
        value = values.get(key)
        if kind == "choice":
            selected = value if value is not None else next(iter(question["criteria"]))
            answers[key] = {
                "type": "choice",
                "choice": selected,
                "confidence": confidence,
                "probabilities": {label: float(label == selected) for label in question["criteria"]},
            }
        elif kind == "score":
            selected = 1 if value is None else value
            bucket = min(len(question["criteria"]) - 1, max(0, round(selected)))
            answers[key] = {
                "type": "score",
                "score": selected,
                "confidence": confidence,
                "probabilities": {
                    str(index): float(index == bucket) for index in range(len(question["criteria"]))
                },
            }
        else:
            answers[key] = {"type": "noul", "noul": 0.95 if value is None else value}
    return {"ok": True, "answers": answers}


class IterationThreeTests(unittest.TestCase):
    def test_replay_preserves_initial_misses_and_final_selection(self):
        result = replay()
        self.assertEqual(result["screens"]["initial"], {
            "requests": 61,
            "fixture_matches": 58,
            "questions": 84,
            "question_matches": 81,
            "request_digests_verified": 61,
        })
        self.assertEqual(result["screens"]["refinement"], {
            "requests": 6,
            "fixture_matches": 6,
            "questions": 17,
            "question_matches": 17,
            "request_digests_verified": 6,
        })
        self.assertEqual(result["final_contract_acceptance"]["fixtures"], 73)
        self.assertEqual(result["final_contract_acceptance"]["questions"], 98)

    def test_catalog_domain_counts_and_versioned_refinements(self):
        self.assertEqual(len(PATTERNS), 30)
        self.assertEqual(
            {domain: sum(pattern["domain"] == domain for pattern in PATTERNS.values())
             for domain in ("business", "engineering", "llm", "harness")},
            {"business": 7, "engineering": 7, "llm": 6, "harness": 10},
        )
        self.assertEqual(PATTERNS["E16"]["contract_version"], 2)
        self.assertEqual(PATTERNS["L14"]["contract_version"], 2)
        self.assertEqual(PATTERNS["L17"]["contract_version"], 3)
        self.assertEqual(PATTERNS["L18"]["contract_version"], 2)
        self.assertEqual(PATTERNS["H28"]["contract_version"], 2)

    def test_frozen_expectations_do_not_enter_provider_state(self):
        fixtures = json.loads((ROOT / "fixtures.json").read_text())
        for fixture in fixtures:
            with self.subTest(fixture=fixture["id"]):
                self.assertFalse(contains_expected(fixture["state"]))
                self.assertEqual(set(fixture["expected"]), set(PATTERNS[fixture["pattern_id"]]["questions"]))

    def test_invalid_choice_and_probability_shapes_fail_closed(self):
        invalid = response("B16", {"pricing_basis": "make_up_a_price"})
        self.assertFalse(valid_answers(PATTERNS["B16"]["questions"], invalid))
        invalid = response("H24")
        invalid["answers"]["named_veto"]["noul"] = True
        self.assertFalse(valid_answers(PATTERNS["H24"]["questions"], invalid))
        invalid = response("L13")
        invalid["answers"]["alignment"]["score"] = float("nan")
        self.assertFalse(valid_answers(PATTERNS["L13"]["questions"], invalid))

    def test_provider_failure_never_has_a_default_action(self):
        for pattern in PATTERNS.values():
            with self.subTest(pattern=pattern["id"]):
                self.assertEqual(plan(pattern, {"ok": False})["next"], "review")

    def test_h21_discards_noncurrent_snapshot(self):
        signal = response("H21", {"snapshot_relation": "stale_after_change"})
        outcome = plan(PATTERNS["H21"], signal)
        self.assertEqual(outcome["next"], "discard_or_rerun_on_fresh_snapshot")
        self.assertNotIn("use", outcome["next"])

    def test_h22_requires_code_manifest_verification(self):
        signal = response("H22", {"coverage": "exhaustive_with_provenance"})
        self.assertEqual(plan(PATTERNS["H22"], signal)["next"], "verify_manifest_in_code")

    def test_h24_veto_cannot_be_compensated_by_scores(self):
        signal = response("H24", {"fit": 2, "operational_burden": 0, "named_veto": 0.95})
        self.assertEqual(plan(PATTERNS["H24"], signal)["next"], "review_named_veto")

    def test_h29_routes_calculation_out_of_semantic_controller(self):
        signal = response("H29", {"precision_route": "deterministic_calculation_only"})
        self.assertEqual(plan(PATTERNS["H29"], signal)["next"], "deterministic_calculation_or_review")

    def test_l17_l18_h28_consumers_route_every_label_without_actions(self):
        routes = {
            "L17": {
                "document_editor": "inspect_one_offered_skill",
                "data_analysis": "inspect_one_offered_skill",
                "browser_test": "inspect_one_offered_skill",
                "multiple_required": "sequence_multiple_skills",
                "no_skill": "expand_or_review_candidate_search",
                "insufficient": "review_or_expand_shortlist",
            },
            "L18": {
                "direct_stated_judgment": "single_system_one_judgment",
                "single_bounded_comparison": "bounded_comparison",
                "multistep_or_indirect_derivation": "route_to_reasoning_or_retrieval",
                "insufficient": "review_task_shape",
            },
            "H28": {
                "batchable": "verify_budget_and_snapshot_in_code",
                "dependent_sequence_required": "sequence_dependencies_before_batching",
                "over_budget_or_oversized": "split_or_review_budget",
                "stale_or_unverifiable_snapshot": "refresh_snapshot_and_rebuild_manifest",
                "insufficient": "review_manifest_and_budget_evidence",
            },
        }
        question_id = {"L17": "skill", "L18": "decision_depth", "H28": "batch_status"}
        for pattern_id, label_routes in routes.items():
            for label, expected_next in label_routes.items():
                with self.subTest(pattern=pattern_id, label=label):
                    signal = response(pattern_id, {question_id[pattern_id]: label})
                    outcome = raw_plan(PATTERNS[pattern_id], signal, state={
                        field: "synthetic branch evidence"
                        for field in PATTERNS[pattern_id]["required_state_fields"]
                    })
                    self.assertEqual(outcome["next"], expected_next)
                    self.assertEqual(outcome["reason"], label)
                    self.assertIsInstance(outcome["next"], str)

    def test_l17_l18_h28_preflight_missing_or_empty_state_fails_closed(self):
        for pattern_id in ("L17", "L18", "H28"):
            p = PATTERNS[pattern_id]
            signal = response(pattern_id)
            for field in p["required_state_fields"]:
                state = {name: "present" for name in p["required_state_fields"]}
                state[field] = ""
                with self.subTest(pattern=pattern_id, field=field):
                    result = raw_plan(p, signal, state=state)
                    self.assertEqual(result["next"], "review")
                    self.assertEqual(result["reason"], "missing_required_state")

    def test_precedence_revision_receipts_and_pair_results(self):
        result = replay()
        self.assertEqual(result["screens"]["precedence-review-v2"]["requests"], 24)
        self.assertEqual(result["screens"]["precedence-review-v2"]["fixture_matches"], 24)
        rows = evaluate.load("results/precedence-pair-review-v2.json")
        self.assertEqual(sum(len(row["response"]["answers"]) for row in rows), 30)
        self.assertTrue(all(a["choice"] == "disjoint" for row in rows for a in row["response"]["answers"].values()))

    def test_revision_refuses_changed_originals_and_frozen_cases(self):
        original_load = evaluate.load
        for path, mutate in (
            ("results/precedence-pre-review-contracts.json", lambda d: d["fixtures"][0]["state"].update({"support_bundle": "changed"})),
            ("results/precedence-revision-fixtures.json", lambda d: d["cases"][0]["expected"]["support_status"].update({"choice": "insufficient"})),
            ("results/precedence-revision-fixtures.json", lambda d: d["patterns"][0]["questions"]["support_status"].update({"instructions": "changed"})),
            ("results/precedence-pair-review-v2.json", lambda d: d[0]["request"]["state"]["pair0"].update({"question_instructions": "changed"})),
            ("results/pattern-review-pre-review-contracts.json", lambda d: d["fixtures"][0]["state"].update({"user_task": "changed"})),
            ("results/pattern-review-revision-v2.json", lambda d: d["cases"][6]["expected"]["skill"].update({"choice": "no_skill"})),
            ("results/pattern-review-revision-v2.json", lambda d: d["patterns"][0]["questions"]["skill"].update({"instructions": "changed"})),
            ("results/pattern-review-pair-review-v2.json", lambda d: d["final_reviews"][0]["request"]["state"]["pairs"]["pair0"].update({"option_a_label": "changed"})),
            ("results/l17-v3-pre-review-v2.json", lambda d: d["cases"][0]["state"].update({"user_task": "changed"})),
            ("results/l17-v3-revision-fixtures.json", lambda d: d["cases"][0]["expected"]["skill"].update({"choice": "no_skill"})),
            ("results/pattern-review-pair-review-v3.json", lambda d: d["final_reviews"][0]["request"]["state"]["pairs"]["pair0"].update({"option_a_label": "changed"})),
        ):
            with self.subTest(path=path):
                data = copy.deepcopy(original_load(path))
                mutate(data)
                with patch.object(evaluate, "load", side_effect=lambda name: data if name == path else original_load(name)):
                    with self.assertRaises(ValueError):
                        replay()

    def test_revised_missing_inputs_remain_consumer_review(self):
        cases = {f["id"]: f for f in evaluate.load("results/precedence-revision-fixtures.json")["cases"]}
        rows = evaluate.load("results/precedence-review-v2.json")
        for row in rows:
            if row["fixture_id"].endswith("missing-input"):
                with self.subTest(fixture=row["fixture_id"]):
                    self.assertEqual(raw_plan(PATTERNS[row["pattern_id"]], row["response"], state=cases[row["fixture_id"]]["state"])["next"], "review")

    def test_h24_preserves_both_screens_and_conservative_mismatch(self):
        result = replay()
        self.assertEqual(result["screens"]["h24-review-v2"]["fixture_matches"], 4)
        self.assertEqual(result["screens"]["h24-review-v3"]["fixture_matches"], 6)
        self.assertEqual(result["screens"]["h24-review-v3"]["question_matches"], 27)
        held = next(c for c in result["h24_availability_revision"]["consumer_cases"] if not c["match"])
        self.assertEqual(held["fixture_id"], "H24-review-negated-extra-resources")
        self.assertEqual(held["observed"], "review_missing_or_uncertain_burden")

    def test_h24_unavailable_burden_score_is_ignored(self):
        for score in (0, 1, 2):
            for availability in (0, .5, .799):
                with self.subTest(score=score, availability=availability):
                    signal = response("H24", {"fit": 2, "operational_burden": score,
                                              "named_veto": .05, "burden_available": availability})
                    self.assertEqual(plan(PATTERNS["H24"], signal)["next"], "review_missing_or_uncertain_burden")
                    signal["answers"]["named_veto"]["noul"] = .95
                    self.assertEqual(plan(PATTERNS["H24"], signal)["next"], "review_named_veto")

    def test_h24_provisional_gate_and_bad_configuration(self):
        signal = response("H24", {"fit": 2, "operational_burden": 0,
                                  "named_veto": .05, "burden_available": .8})
        self.assertEqual(plan(PATTERNS["H24"], signal)["next"], "compute_versioned_score_in_code")
        for bad_minimum in (None, True, float("nan"), 1.01):
            p = copy.deepcopy(PATTERNS["H24"])
            p["policy"]["burden_available_min"] = bad_minimum
            self.assertEqual(plan(p, signal)["next"], "review_missing_or_uncertain_burden")

    def test_pattern_review_pair_receipts_and_low_confidence_are_retained(self):
        revision = replay()["pattern_review_revision"]
        self.assertEqual(revision["patterns"], 3)
        self.assertEqual(revision["unchanged_regressions"], 6)
        self.assertEqual(revision["development_cases"], 12)
        self.assertEqual(revision["pairs"], 31)
        self.assertTrue(any(item["pattern_id"] == "H28" and item["confidence"] < 0.8
                            for item in revision["low_confidence_pairs"]))
        v2_misses = [item for item in revision["consumer_cases"] if not item["match"]]
        self.assertEqual(len(v2_misses), 1)
        self.assertEqual(v2_misses[0]["fixture_id"], "L17-v2-incomplete-description")
        self.assertEqual(v2_misses[0]["observed"], "inspect_one_offered_skill")
        self.assertEqual(len(revision["consumer_cases"]), 18)
        l17_v3 = replay()["l17_v3_revision"]
        self.assertEqual(l17_v3["fixture_matches"], 6)
        self.assertEqual(l17_v3["pairs"], 15)
        self.assertEqual(len(l17_v3["low_confidence_pairs"]), 6)
        self.assertTrue(all(item["match"] for item in l17_v3["consumer_cases"]))

    def test_h24_refinement_cannot_change_states_or_expected_intervals(self):
        original_load = evaluate.load
        for path, mutate in (
            ("results/h24-pre-review-contract.json", lambda d: d["fixtures"][0]["state"].update({"candidate": "changed"})),
            ("results/h24-v3-revision-fixtures.json", lambda d: d["cases"][0]["expected"]["burden_available"].update({"range": [0, 1]})),
            ("results/h24-v3-revision-fixtures.json", lambda d: d["cases"][2]["state"].update({"candidate": "changed"})),
        ):
            with self.subTest(path=path):
                data = copy.deepcopy(original_load(path))
                mutate(data)
                with patch.object(evaluate, "load", side_effect=lambda name: data if name == path else original_load(name)):
                    with self.assertRaises(ValueError):
                        replay()


if __name__ == "__main__":
    unittest.main()
