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
        self.assertEqual(result["final_contract_acceptance"], {
            "fixtures": 61,
            "fixture_matches": 61,
            "questions": 84,
            "question_matches": 84,
        })

    def test_catalog_domain_counts_and_versioned_refinements(self):
        self.assertEqual(len(PATTERNS), 30)
        self.assertEqual(
            {domain: sum(pattern["domain"] == domain for pattern in PATTERNS.values())
             for domain in ("business", "engineering", "llm", "harness")},
            {"business": 7, "engineering": 7, "llm": 6, "harness": 10},
        )
        self.assertEqual(PATTERNS["E16"]["contract_version"], 2)
        self.assertEqual(PATTERNS["L14"]["contract_version"], 2)

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


if __name__ == "__main__":
    unittest.main()
