import copy
import json
from pathlib import Path
import unittest
from check_contract import provider_request, validate

ASSETS = Path(__file__).resolve().parents[1] / "assets"


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ASSETS / "contract-example.json").read_text())
        self.suite = json.loads((ASSETS / "fixtures-example.json").read_text())

    def test_example_is_structurally_valid(self):
        self.assertEqual(validate(self.contract, self.suite)["fixtures"], 4)

    def test_transport_excludes_expectations_and_is_independent(self):
        fixture = self.suite["fixtures"][0]
        original = copy.deepcopy(fixture)
        request = provider_request(self.contract, fixture)
        self.assertEqual(set(request), {"state", "questions"})
        self.assertEqual(request["state"], fixture["state"])
        request["state"]["message"] = "changed"
        self.assertEqual(fixture, original)

    def test_stale_fixture_version_rejected(self):
        self.suite["version"] = 2
        with self.assertRaises(ValueError):
            validate(self.contract, self.suite)

    def test_omitted_required_state_rejected(self):
        self.suite["fixtures"][0]["state"] = {}
        with self.assertRaises(ValueError):
            validate(self.contract, self.suite)

    def test_unsupported_choice_rejected(self):
        self.suite["fixtures"][0]["expected"]["request_kind"] = "invented"
        with self.assertRaises(ValueError):
            validate(self.contract, self.suite)

    def test_missing_question_expectation_rejected(self):
        self.suite["fixtures"][0]["expected"] = {}
        with self.assertRaises(ValueError):
            validate(self.contract, self.suite)

    def test_duplicate_fixture_rejected(self):
        self.suite["fixtures"].append(copy.deepcopy(self.suite["fixtures"][0]))
        with self.assertRaises(ValueError):
            validate(self.contract, self.suite)

    def test_noul_and_score_intervals(self):
        for primitive, upper in (("noul", 1), ("score", 2)):
            self.contract["request"]["questions"] = {"signal": {
                "type": primitive, "instructions": "Assess the stated signal.",
                **({"criteria": ["Absent", "Moderate", "Strong"]} if primitive == "score" else {})}}
            for fixture in self.suite["fixtures"]:
                fixture["expected"] = {"signal": {"min": 0, "max": upper}}
            validate(self.contract, self.suite)
            for bad in (True, float("nan"), float("inf"), upper + 1):
                self.suite["fixtures"][0]["expected"]["signal"]["max"] = bad
                with self.assertRaises(ValueError):
                    validate(self.contract, self.suite)
            self.suite["fixtures"][0]["expected"]["signal"]["max"] = upper

    def test_label_envelope_cannot_be_request_field(self):
        self.contract["request"]["expected"] = "refund_requested"
        with self.assertRaises(ValueError):
            validate(self.contract, self.suite)


if __name__ == "__main__":
    unittest.main()
