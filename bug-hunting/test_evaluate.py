import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("bug_catalog_evaluate", Path(__file__).with_name("evaluate.py"))
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


class BugCatalogTests(unittest.TestCase):
    def setUp(self):
        self.r = copy.deepcopy(ev.read("results/refinement.json")[0])
        self.f = next(f for f in ev.read("fixtures.json") if f["id"] == self.r["fixture_id"])
        self.p = next(p for p in ev.read("catalog.json")["patterns"] if p["id"] == self.f["pattern_id"])

    def validate(self):
        return ev.validate_receipt(self.r, self.f, self.p)

    def test_replay_preserves_unresolved_case(self):
        result = ev.report()
        self.assertEqual(result["contract_version"], 2)
        self.assertEqual(result["initial_selected_label_matches"], 143)
        self.assertEqual([x["fixture_id"] for x in result["initial_disagreements"]], ["BH41-2"])
        self.assertEqual(result["initial_provider_failures"], ["BH09-2", "BH39-1"])
        self.assertEqual(result["refinement_attempts"], 144)
        self.assertEqual(result["refinement_provider_failures"], [])
        self.assertEqual(result["current_label_matches"], 143)
        self.assertEqual([x["fixture_id"] for x in result["current_disagreements"]], ["BH41-2"])
        self.assertEqual(result["successful_request_digests_verified"], 288)

    def test_initial_receipt_still_binds_to_preserved_contract(self):
        r = ev.read("results/screening.json")[0]
        f = next(f for f in ev.read("results/initial-fixtures.json") if f["id"] == r["fixture_id"])
        p = next(p for p in ev.read("results/initial-catalog.json")["patterns"] if p["id"] == f["pattern_id"])
        self.assertTrue(ev.validate_receipt(r, f, p))
        with self.assertRaises(ValueError):
            ev.validate_receipt(r, self.f, self.p)  # version-1 receipt against the version-2 contract

    def test_good_receipt(self):
        self.assertTrue(self.validate())

    def test_changed_evidence(self):
        self.r["request"]["state"]["evidence"] = "different revision"
        with self.assertRaises(ValueError):
            self.validate()

    def test_changed_question(self):
        self.r["request"]["questions"]["decision"]["instructions"] = "different meaning"
        with self.assertRaises(ValueError):
            self.validate()

    def test_stale_version(self):
        self.r["version"] = 7
        with self.assertRaises(ValueError):
            self.validate()

    def test_tampered_digest(self):
        self.r["response"]["request_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.validate()

    def test_invented_label(self):
        self.r["response"]["answers"]["decision"]["choice"] = "verified_fixed"
        with self.assertRaises(ValueError):
            self.validate()

    def test_invalid_confidence(self):
        for value in (None, True, -1, 2, float("nan"), float("inf")):
            with self.subTest(value=value):
                self.r["response"]["answers"]["decision"]["confidence"] = value
                with self.assertRaises(ValueError):
                    self.validate()

    def test_probability_sum_tolerance_matches_bridge(self):
        a = self.r["response"]["answers"]["decision"]
        others = [k for k in a["probabilities"] if k != a["choice"]]
        a["probabilities"] = {a["choice"]: 0.93, others[0]: 0.05, others[1]: 0.01}  # rounding drift, sum 0.99
        self.validate()
        a["probabilities"][a["choice"]] = 0.90  # sum 0.96 is a real gap
        with self.assertRaises(ValueError):
            self.validate()

    def test_missing_probability(self):
        del self.r["response"]["answers"]["decision"]["probabilities"]["insufficient"]
        with self.assertRaises(ValueError):
            self.validate()

    def test_duplicate_receipt(self):
        with self.assertRaises(ValueError):
            ev.unique([self.r, self.r], "fixture_id")

    def test_missing_receipt(self):
        with self.assertRaises(ValueError):
            ev.score([], [self.f], [self.p])

    def test_expected_label_not_transport(self):
        self.r["request"]["expected"] = self.f["expected"]
        with self.assertRaises(ValueError):
            self.validate()

    def test_low_confidence_lead_is_retained(self):
        self.assertEqual(ev.classify_for_review({"choice": "risk_supported", "confidence": 0.1}, binding_current=True),
                         "candidate_requires_verification")

    def test_counterevidence_is_not_bug_free(self):
        self.assertEqual(ev.classify_for_review({"choice": "counterevidence", "confidence": 1}, binding_current=True),
                         "counterevidence_only")

    def test_stale_evidence_never_promotes(self):
        self.assertEqual(ev.classify_for_review({"choice": "risk_supported"}, binding_current=False),
                         "unresolved_stale_evidence")

    def test_failure_and_unknown_stay_unresolved(self):
        for answer in (None, {}, {"choice": "insufficient"}, {"choice": "verified_fixed"}):
            with self.subTest(answer=answer):
                self.assertEqual(ev.classify_for_review(answer, binding_current=True), "unresolved")


if __name__ == "__main__":
    unittest.main()
