import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_confidence import check, check_answer, choice_confidence, required_top_probability


class ConfidenceTests(unittest.TestCase):
    def test_documented_quickstart_answer_is_consistent(self):
        # docs.typesafe.ai/introduction/quickstart: technical 0.85, billing 0.15, sales 0.0 -> 0.78
        answer = {"type": "choice", "choice": "technical", "confidence": 0.78,
                  "probabilities": {"technical": 0.85, "sales": 0.0, "billing": 0.15}}
        self.assertAlmostEqual(choice_confidence(answer["probabilities"]), 0.775)
        self.assertIsNone(check_answer(answer))

    def test_endpoints(self):
        self.assertEqual(choice_confidence([1.0, 0.0, 0.0]), 1.0)
        self.assertAlmostEqual(choice_confidence([1 / 3, 1 / 3, 1 / 3]), 0.0)

    def test_same_top_probability_gains_confidence_with_more_options(self):
        self.assertAlmostEqual(choice_confidence([0.85, 0.15, 0.0]), 0.775)
        self.assertAlmostEqual(choice_confidence([0.85, 0.15, 0.0, 0.0]), 0.8)

    def test_fixed_threshold_needs_different_top_probability(self):
        expected = {2: 0.9, 3: 0.8666667, 4: 0.85, 6: 0.8333333, 255: 0.8007843}
        for n, top in expected.items():
            self.assertAlmostEqual(required_top_probability(0.8, n), top, places=6)
            probabilities = [top] + [(1 - top) / (n - 1)] * (n - 1)
            self.assertAlmostEqual(choice_confidence(probabilities), 0.8, places=6)

    def test_inconsistent_confidence_reported(self):
        answer = {"type": "choice", "confidence": 0.95, "probabilities": {"a": 0.6, "b": 0.4}}
        self.assertIn("differs", check_answer(answer))

    def test_invalid_values_rejected(self):
        for probabilities, confidence in (({"a": 1.0}, 1.0), ({"a": True, "b": 0.0}, 1.0),
                                          ({"a": float("nan"), "b": 0.5}, 0.5),
                                          ({"a": 0.5, "b": 0.5}, None)):
            self.assertIsNotNone(check_answer({"type": "choice", "confidence": confidence,
                                               "probabilities": probabilities}))
        with self.assertRaises(ValueError):
            required_top_probability(0.8, 1)

    def test_scan_counts_scores_without_checking_them(self):
        receipt = {"answers": {
            "c": {"type": "choice", "confidence": 0.5, "probabilities": {"a": 0.75, "b": 0.25}},
            "s": {"type": "score", "score": 1.5, "confidence": 0.0,
                  "probabilities": {"0": 0.5, "1": 0.0, "2": 0.0, "3": 0.5}},
            "n": {"type": "noul", "noul": 0.4}}}
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "receipt.json").write_text(json.dumps(receipt))
            report = check([folder])
        self.assertEqual(report["choice_answers_checked"], 1)
        self.assertEqual(report["score_answers_not_checked"], 1)
        self.assertEqual(report["by_option_count"], {"2": 1})
        self.assertEqual(report["failures"], [])

    def test_scan_reports_failure_location(self):
        receipt = [{"answers": {"c": {"type": "choice", "confidence": 0.9,
                                      "probabilities": {"a": 0.5, "b": 0.5}}}}]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder, "bad.json")
            path.write_text(json.dumps(receipt))
            report = check([path])
        self.assertEqual(report["failures"][0]["path"], "$[0].answers.c")


if __name__ == "__main__":
    unittest.main()
