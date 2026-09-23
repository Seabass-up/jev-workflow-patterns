import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("human_catalog_evaluate", Path(__file__).with_name("evaluate.py"))
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


class HumanPatternTests(unittest.TestCase):
    def setUp(self):
        self.catalog = ev.read("catalog.json")
        self.fixtures = ev.read("fixtures.json")
        self.sources = ev.read("sources.json")
        self.initial = ev.read("results/screening.json")
        self.recovery = ev.read("results/recovery.json")
        self.r = copy.deepcopy(next(r for r in self.initial if r["response"]["ok"]))
        self.f = next(f for f in self.fixtures if f["id"] == self.r["fixture_id"])
        self.p = next(p for p in self.catalog["patterns"] if p["id"] == self.f["pattern_id"])

    def validate(self):
        return ev.validate_receipt(self.r, self.f, self.p)

    def replay(self):
        return ev.replay(self.catalog, self.fixtures, self.sources, self.initial, self.recovery)

    def test_preserved_summary(self):
        self.assertEqual(self.replay(), ev.read("results/summary.json"))

    def test_two_evaluation_splits(self):
        result = self.replay()
        self.assertEqual(result["splits"]["design"]["cases"], 3 * result["patterns"])
        self.assertEqual(result["splits"]["challenge"]["cases"], result["patterns"])

    def test_changed_state(self):
        self.r["request"]["state"] = {"unrelated": "replacement"}
        with self.assertRaises(ValueError):
            self.validate()

    def test_changed_question(self):
        self.r["request"]["questions"]["decision"]["instructions"] = "Changed meaning"
        with self.assertRaises(ValueError):
            self.validate()

    def test_stale_version(self):
        self.r["version"] += 1
        with self.assertRaises(ValueError):
            self.validate()

    def test_tampered_digest(self):
        self.r["response"]["request_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.validate()

    def test_wrong_model(self):
        self.r["response"]["model"] = "unrelated-model"
        with self.assertRaises(ValueError):
            self.validate()

    def test_unknown_output_label(self):
        self.r["response"]["answers"]["decision"]["choice"] = "act_without_permission"
        with self.assertRaises(ValueError):
            self.validate()

    def test_invalid_confidence(self):
        for value in (None, True, -0.1, 1.1, float("nan"), float("inf")):
            with self.subTest(value=value):
                self.r["response"]["answers"]["decision"]["confidence"] = value
                with self.assertRaises(ValueError):
                    self.validate()

    def test_probability_coverage(self):
        self.r["response"]["answers"]["decision"]["probabilities"].pop("unknown")
        with self.assertRaises(ValueError):
            self.validate()

    def test_no_expectations_in_transport(self):
        self.r["request"]["expected"] = self.f["expected"]
        with self.assertRaises(ValueError):
            self.validate()

    def test_missing_receipt(self):
        self.initial.pop()
        with self.assertRaises(ValueError):
            self.replay()

    def test_duplicate_receipt(self):
        self.initial.append(copy.deepcopy(self.initial[0]))
        with self.assertRaises(ValueError):
            self.replay()

    def test_recovery_cannot_replace_semantic_judgment(self):
        self.recovery.append(self.r)
        with self.assertRaises(ValueError):
            self.replay()

    def test_missing_source(self):
        self.sources = []
        with self.assertRaises(ValueError):
            self.replay()

    def test_unbound_source_reference(self):
        self.catalog["patterns"][0]["source_ids"] = ["invented_source"]
        with self.assertRaises(ValueError):
            self.replay()

    def test_missing_challenge(self):
        self.fixtures = [f for f in self.fixtures if not (f["pattern_id"] == self.p["id"] and f["split"] == "challenge")]
        with self.assertRaises(ValueError):
            self.replay()

    def test_fixture_label_must_be_in_contract(self):
        self.fixtures[0]["expected"] = "not_a_label"
        with self.assertRaises(ValueError):
            self.replay()

    def test_version_must_not_be_boolean(self):
        self.catalog["patterns"][0]["version"] = True
        with self.assertRaises(ValueError):
            self.replay()

    def test_fixture_version_requires_exact_integer(self):
        for value in (True, 1.0, 0, None):
            with self.subTest(value=value):
                self.f["version"] = value
                with self.assertRaises(ValueError):
                    self.validate()
                with self.assertRaises(ValueError):
                    self.replay()

    def test_receipt_version_requires_exact_integer(self):
        for value in (True, 1.0, 0, None):
            with self.subTest(value=value):
                self.r["version"] = value
                with self.assertRaises(ValueError):
                    self.validate()
                self.initial[0]["version"] = value
                with self.assertRaises(ValueError):
                    self.replay()


if __name__ == "__main__":
    unittest.main()
