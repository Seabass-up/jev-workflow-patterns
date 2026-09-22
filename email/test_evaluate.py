import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate import read, report, score, validate_receipt


class EmailReplayTests(unittest.TestCase):
    def setUp(self):
        self.receipt = copy.deepcopy(read("results/initial.json")[0])
        self.fixture = read("results/initial-fixtures.json")[0]
        self.pattern = read("results/initial-catalog.json")["patterns"][0]

    def check(self):
        return validate_receipt(self.receipt, self.fixture, self.pattern)

    def test_original_receipt(self):
        self.assertTrue(self.check())
        # Confidence is a distribution statistic, not chosen-option probability.
        receipts = read("results/initial.json")
        fixtures = read("results/initial-fixtures.json")
        patterns = read("results/initial-catalog.json")["patterns"]
        miss = next(r for r in receipts if r["fixture_id"] == "EM07-3")
        fixture = next(f for f in fixtures if f["id"] == "EM07-3")
        pattern = next(p for p in patterns if p["id"] == "EM07")
        self.assertFalse(validate_receipt(miss, fixture, pattern))

    def test_full_replay_preserves_misses(self):
        result = report()
        self.assertEqual(result["initial"]["misses"], ["EM07-3", "EM08-3"])
        self.assertEqual(result["current"]["matched"], 36)
        self.assertEqual(result["request_digests_verified"], 42)

    def test_changed_state(self):
        self.receipt["request"]["state"]["current_body"] = "Changed evidence"
        with self.assertRaises(ValueError):
            self.check()

    def test_changed_question(self):
        self.receipt["request"]["questions"]["decision"]["instructions"] = "Changed contract"
        with self.assertRaises(ValueError):
            self.check()

    def test_digest(self):
        self.receipt["response"]["request_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.check()

    def test_version(self):
        self.receipt["version"] = 99
        with self.assertRaises(ValueError):
            self.check()

    def test_choice_membership(self):
        self.receipt["response"]["answers"]["decision"]["choice"] = "send_now"
        with self.assertRaises(ValueError):
            self.check()

    def test_invalid_probabilities(self):
        for value in (None, True, -0.1, 1.1, float("nan"), float("inf")):
            with self.subTest(value=value):
                self.receipt["response"]["answers"]["decision"]["confidence"] = value
                with self.assertRaises(ValueError):
                    self.check()

    def test_probability_coverage(self):
        del self.receipt["response"]["answers"]["decision"]["probabilities"]["unknown"]
        with self.assertRaises(ValueError):
            self.check()

    def test_failed_provider(self):
        self.receipt["response"]["ok"] = False
        with self.assertRaises(ValueError):
            self.check()

    def test_missing_receipt(self):
        with self.assertRaises(ValueError):
            score([], [self.fixture], [self.pattern])

    def test_duplicate_receipt(self):
        with self.assertRaises(ValueError):
            score([self.receipt, self.receipt], [self.fixture], [self.pattern])

    def test_fixture_expectation_excluded_from_transport(self):
        self.receipt["request"]["expected"] = self.fixture["expected"]
        with self.assertRaises(ValueError):
            self.check()


if __name__ == "__main__":
    unittest.main()
