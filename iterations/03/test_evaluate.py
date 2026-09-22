import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import ROOT, contains_expected, plan, replay, valid_answers


CATALOG = json.loads((ROOT / "catalog.json").read_text())
PATTERNS = {pattern["id"]: pattern for pattern in CATALOG["patterns"]}


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


if __name__ == "__main__":
    unittest.main()
