import copy
import json
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate import read, report, score, validate_fixture_history, validate_receipt


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
        self.assertEqual(
            result["em10_v2_first_pass"],
            {"matched": 6, "total": 7, "misses": ["EM10-7"]},
        )
        self.assertEqual(result["refinement"], {"matched": 13, "total": 13, "misses": []})
        self.assertEqual(result["current"], {"matched": 40, "total": 40, "misses": []})
        self.assertEqual(result["request_digests_verified"], 56)

    def test_em10_v2_miss_expectation_is_frozen_in_v3(self):
        first_pass = read("results/em10-v2-first-pass.json")
        current = [f for f in read("fixtures.json") if f["pattern_id"] == "EM10"]
        next(f for f in current if f["id"] == "EM10-7")["expected"] = "substantive_reply"
        with self.assertRaisesRegex(ValueError, "frozen fixture was rewritten"):
            validate_fixture_history(
                first_pass["fixtures"], current,
                [first_pass["pattern"]],
                [next(p for p in read("catalog.json")["patterns"] if p["id"] == "EM10")],
            )

    def test_fixture_history_allows_versioned_regression_additions(self):
        validate_fixture_history(
            read("results/initial-fixtures.json"),
            read("fixtures.json"),
            read("results/initial-catalog.json")["patterns"],
            read("catalog.json")["patterns"],
        )

    def test_fixture_history_rejects_rewriting_frozen_state(self):
        current = read("fixtures.json")
        current[0]["state"]["current_body"] = "Rewritten fixture"
        with self.assertRaisesRegex(ValueError, "frozen fixture was rewritten"):
            validate_fixture_history(
                read("results/initial-fixtures.json"), current,
                read("results/initial-catalog.json")["patterns"],
                read("catalog.json")["patterns"],
            )

    def test_fixture_history_rejects_removed_original(self):
        current = read("fixtures.json")
        current = [fixture for fixture in current if fixture["id"] != "EM01-1"]
        with self.assertRaisesRegex(ValueError, "frozen fixture removed"):
            validate_fixture_history(
                read("results/initial-fixtures.json"), current,
                read("results/initial-catalog.json")["patterns"],
                read("catalog.json")["patterns"],
            )

    def test_fixture_history_rejects_new_case_on_unrevised_contract(self):
        current = read("fixtures.json")
        current.append({
            "id": "EM01-4", "pattern_id": "EM01", "version": 1,
            "state": {"owner": "Morgan", "current_body": "Hello.", "recipients": "To Morgan"},
            "expected": "nobody",
        })
        with self.assertRaisesRegex(ValueError, "new fixture must target a revised contract"):
            validate_fixture_history(
                read("results/initial-fixtures.json"), current,
                read("results/initial-catalog.json")["patterns"],
                read("catalog.json")["patterns"],
            )

    def test_fixture_history_rejects_case_on_wrong_version(self):
        current = read("fixtures.json")
        next(fixture for fixture in current if fixture["id"] == "EM10-4")["version"] = 1
        with self.assertRaisesRegex(ValueError, "fixture version does not match current contract"):
            validate_fixture_history(
                read("results/initial-fixtures.json"), current,
                read("results/initial-catalog.json")["patterns"],
                read("catalog.json")["patterns"],
            )

    def test_em10_page_matches_current_contract_and_fixtures(self):
        pattern = next(p for p in read("catalog.json")["patterns"] if p["id"] == "EM10")
        page = (Path(__file__).resolve().parent / "patterns/em10.md").read_text()
        self.assertIn("Email profile · contract v3", page)
        match = re.search(
            r"Exact version-3 question configuration:\s*```json\s*(.*?)\s*```",
            page,
            re.S,
        )
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)), pattern["questions"])
        for fixture in read("fixtures.json"):
            if fixture["pattern_id"] == "EM10":
                self.assertIn(f"| {fixture['id']} | `{fixture['expected']}` |", page)

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

    def test_versions_are_exact_positive_integers(self):
        for target in ("receipt", "fixture", "pattern"):
            with self.subTest(target=target):
                receipt = copy.deepcopy(self.receipt)
                fixture = copy.deepcopy(self.fixture)
                pattern = copy.deepcopy(self.pattern)
                objects = {"receipt": receipt, "fixture": fixture, "pattern": pattern}
                objects[target]["version"] = True
                with self.assertRaisesRegex(ValueError, "invalid contract version"):
                    validate_receipt(receipt, fixture, pattern)

    def test_fixture_history_rejects_boolean_version(self):
        current = read("fixtures.json")
        next(fixture for fixture in current if fixture["id"] == "EM01-1")["version"] = True
        with self.assertRaisesRegex(ValueError, "invalid fixture version"):
            validate_fixture_history(
                read("results/initial-fixtures.json"), current,
                read("results/initial-catalog.json")["patterns"],
                read("catalog.json")["patterns"],
            )

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

    def test_probability_sum_tolerance_matches_bridge(self):
        answer = self.receipt["response"]["answers"]["decision"]
        others = [k for k in answer["probabilities"] if k != answer["choice"]]
        answer["probabilities"] = {k: 0 for k in answer["probabilities"]}
        answer["probabilities"].update({answer["choice"]: 0.93, others[0]: 0.05, others[1]: 0.01})  # sum 0.99
        self.check()
        answer["probabilities"][answer["choice"]] = 0.90  # sum 0.96 is a real gap
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
