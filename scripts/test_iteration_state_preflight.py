"""Exercise evidence preflight across every historical iteration profile."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_iteration(number):
    path = ROOT / "iterations" / number / "evaluate.py"
    spec = importlib.util.spec_from_file_location("iteration_preflight_" + number, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def signal(pattern):
    answers = {}
    for key, q in pattern["questions"].items():
        if q["type"] == "choice":
            first = next(iter(q["criteria"]))
            answers[key] = {"type": "choice", "choice": first, "confidence": 1,
                            "probabilities": {label: int(label == first) for label in q["criteria"]}}
        elif q["type"] == "score":
            answers[key] = {"type": "score", "score": 0, "confidence": 1,
                            "probabilities": {str(i): int(i == 0) for i in range(len(q["criteria"]))}}
        else:
            answers[key] = {"type": "noul", "noul": .01}
    return {"ok": True, "answers": answers}


class IterationPreflightTests(unittest.TestCase):
    def test_all_120_profiles_require_nonempty_state(self):
        total = 0
        for number in ("01", "02", "03", "04"):
            module = load_iteration(number)
            patterns = json.loads((module.ROOT / "catalog.json").read_text())["patterns"]
            for p in patterns:
                total += 1
                good = {field: "supplied synthetic evidence" for field in p["required_state_fields"]}
                response = signal(p)
                self.assertTrue(module.valid_answers(p["questions"], response))
                self.assertTrue(module.state_ready(p, good))
                self.assertNotEqual(module.plan(p, response, state=good).get("reason"), "missing_required_state")
                self.assertEqual(module.plan(p, response)["reason"], "missing_required_state")
                for field in p["required_state_fields"]:
                    for empty in (None, "", "  \n", [], {}):
                        with self.subTest(iteration=number, pattern=p["id"], field=field, value=empty):
                            bad = {**good, field: empty}
                            self.assertEqual(module.plan(p, response, state=bad)["reason"], "missing_required_state")
                    bad = dict(good)
                    del bad[field]
                    self.assertEqual(module.plan(p, response, state=bad)["reason"], "missing_required_state")
        self.assertEqual(total, 120)

    def test_preflight_shape_is_not_truth_or_authority(self):
        for number in ("01", "02", "03", "04"):
            m = load_iteration(number)
            p = {"required_state_fields": ["a", "b"]}
            self.assertTrue(m.state_ready(p, {"a": 0, "b": False}))
            self.assertTrue(m.state_ready(p, {"a": {"text": ""}, "b": "present"}))
            for required in (None, [], "a", [None]):
                self.assertFalse(m.state_ready({"required_state_fields": required}, {"a": "present"}))


if __name__ == "__main__":
    unittest.main()
