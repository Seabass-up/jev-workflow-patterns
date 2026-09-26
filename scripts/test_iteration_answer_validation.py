"""Cross-iteration interface regressions; synthetic responses, no provider calls."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IterationAnswerValidationTests(unittest.TestCase):
    def validators(self):
        for iteration in range(1, 5):
            spec = importlib.util.spec_from_file_location(
                f"answer_validation_{iteration}", ROOT / f"iterations/{iteration:02}/evaluate.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            yield iteration, module.valid_answers

    def test_rounded_choice_and_score_are_accepted(self):
        for iteration, validate in self.validators():
            for kind in ("choice", "score"):
                with self.subTest(iteration=iteration, kind=kind):
                    criteria = {"a": "A", "b": "B", "c": "C"} if kind == "choice" else ["A", "B", "C"]
                    keys = list(criteria) if kind == "choice" else ["0", "1", "2"]
                    question = {"x": {"type": kind, "criteria": criteria}}
                    for values in ([.66, .22, .11], [.66, .23, .12], [.66, .23, .11]):
                        answer = {"type": kind, "confidence": .49,
                                  "probabilities": dict(zip(keys, values))}
                        answer["choice" if kind == "choice" else "score"] = "a" if kind == "choice" else .45
                        self.assertTrue(validate(question, {"ok": True, "answers": {"x": answer}}))

    def test_malformed_and_nonmaximum_choices_are_rejected(self):
        question = {"x": {"type": "choice", "criteria": {"a": "A", "b": "B", "c": "C"}}}
        good = {"type": "choice", "choice": "a", "confidence": .49,
                "probabilities": {"a": .66, "b": .23, "c": .11}}
        for iteration, validate in self.validators():
            mutations = [("choice", "b"), ("probabilities", None),
                         ("probabilities", {"a": .66, "b": .23}),
                         ("probabilities", {"a": .7, "b": .25, "c": .1}),
                         ("probabilities", {"a": .7, "b": .15, "c": .1}),
                         ("probabilities", {"a": True, "b": 0, "c": 0}),
                         ("probabilities", {"a": float("nan"), "b": .23, "c": .11})]
            for key, value in mutations:
                with self.subTest(iteration=iteration, mutation=key, value=value):
                    bad = copy.deepcopy(good)
                    bad[key] = value
                    self.assertFalse(validate(question, {"ok": True, "answers": {"x": bad}}))

    def test_tied_maximum_is_not_rejected(self):
        question = {"x": {"type": "choice", "criteria": {"a": "A", "b": "B"}}}
        answer = {"type": "choice", "choice": "b", "confidence": 0,
                  "probabilities": {"a": .5, "b": .5}}
        for iteration, validate in self.validators():
            with self.subTest(iteration=iteration):
                self.assertTrue(validate(question, {"ok": True, "answers": {"x": answer}}))

    def test_wave04_consumer_replays_remain_review(self):
        spec = importlib.util.spec_from_file_location("wave04_consumer", ROOT / "iterations/03/evaluate.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        folder = ROOT / "reviews/2026-09-26"
        patterns = {p["id"]: p for p in json.loads((ROOT / "iterations/03/catalog.json").read_text())["patterns"]}
        fixtures = {f["id"]: f for f in json.loads((folder / "boundary-fixtures-wave04.json").read_text())["cases"]}
        receipts = json.loads((folder / "boundary-receipts-wave04.json").read_text())
        self.assertEqual(len(receipts), 5)
        for row in receipts:
            with self.subTest(fixture=row["fixture_id"]):
                pattern = patterns[row["pattern_key"].split("/")[-1]]
                outcome = module.plan(pattern, row["response"], state=fixtures[row["fixture_id"]]["state"])
                self.assertEqual(outcome["next"], "review")


if __name__ == "__main__":
    unittest.main()
