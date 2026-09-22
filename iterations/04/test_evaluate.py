import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import ROOT, contains_expected, plan, replay, valid_answers


CATALOG = json.loads((ROOT / "catalog.json").read_text())
PATTERNS = {item["id"]: item for item in CATALOG["patterns"]}


def response(pattern_id, values=None, confidence=1.0):
    values = values or {}
    answers = {}
    for key, question in PATTERNS[pattern_id]["questions"].items():
        kind, value = question["type"], values.get(key)
        if kind == "choice":
            picked = value if value is not None else next(iter(question["criteria"]))
            answers[key] = {"type": "choice", "choice": picked, "confidence": confidence, "probabilities": {label: float(label == picked) for label in question["criteria"]}}
        elif kind == "score":
            picked = 1 if value is None else value
            bucket = min(len(question["criteria"]) - 1, max(0, round(picked)))
            answers[key] = {"type": "score", "score": picked, "confidence": confidence, "probabilities": {str(index): float(index == bucket) for index in range(len(question["criteria"]))}}
        else:
            answers[key] = {"type": "noul", "noul": 0.95 if value is None else value}
    return {"ok": True, "answers": answers}


class IterationFourTests(unittest.TestCase):
    def test_catalog_counts_and_ids(self):
        self.assertEqual(len(PATTERNS), 30)
        self.assertEqual({name: sum(p["domain"] == name for p in PATTERNS.values()) for name in ("business", "engineering", "llm", "harness")}, {"business": 7, "engineering": 7, "llm": 6, "harness": 10})
        self.assertEqual(set(PATTERNS), {f"B{i}" for i in range(22, 29)} | {f"E{i}" for i in range(22, 29)} | {f"L{i}" for i in range(19, 25)} | {f"H{i}" for i in range(31, 41)})

    def test_frozen_labels_never_enter_provider_state(self):
        fixtures = json.loads((ROOT / "fixtures.json").read_text())
        self.assertEqual(len(fixtures), 60)
        for item in fixtures:
            with self.subTest(fixture=item["id"]):
                self.assertFalse(contains_expected(item["state"]))
                self.assertEqual(set(item["expected"]), set(PATTERNS[item["pattern_id"]]["questions"]))

    def test_invalid_answer_shapes_fail_closed(self):
        invalid = response("B22", {"buyer_role": "invented"})
        self.assertFalse(valid_answers(PATTERNS["B22"]["questions"], invalid))
        invalid = response("B23")
        invalid["answers"]["intent_strength"]["score"] = float("nan")
        self.assertFalse(valid_answers(PATTERNS["B23"]["questions"], invalid))
        invalid = response("H33", {"field_problem": True})
        self.assertFalse(valid_answers(PATTERNS["H33"]["questions"], invalid))

    def test_provider_failure_never_selects_an_action(self):
        for item in PATTERNS.values():
            with self.subTest(pattern=item["id"]):
                self.assertEqual(plan(item, {"ok": False})["next"], "review")

    def test_h34_rejects_unlisted_candidate(self):
        invalid = response("H34", {"selected_candidate": "candidate_3"})
        self.assertFalse(valid_answers(PATTERNS["H34"]["questions"], invalid))

    def test_final_selection_covers_every_current_fixture(self):
        result = replay()
        self.assertEqual(result["final_contract_acceptance"]["fixtures"], 60)
        self.assertEqual(result["final_contract_acceptance"]["questions"], 60)
        self.assertEqual(result["final_contract_acceptance"]["fixture_matches"], 60)
        self.assertEqual(result["final_contract_acceptance"]["question_matches"], 60)


if __name__ == "__main__":
    unittest.main()
