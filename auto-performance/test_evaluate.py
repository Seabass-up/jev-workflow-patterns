import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest

spec = importlib.util.spec_from_file_location("collection_evaluate", Path(__file__).with_name("evaluate.py"))
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = ev.read("catalog.json")
        self.fixtures = ev.read("fixtures.json")
        self.sources = ev.read("sources.json")
        self.initial_catalog = ev.read("results/initial-catalog.json")
        self.initial_fixtures = ev.read("results/initial-fixtures.json")
        self.initial = ev.read("results/screening.json")
        self.initial_recovery = ev.read("results/recovery.json")
        self.refinement = ev.read("results/refinement.json")
        self.refinement_recovery = ev.read("results/refinement-recovery.json")
        self.r = copy.deepcopy(next(r for r in self.refinement if r["fixture_id"] == "AP03-5"))
        self.f = next(f for f in self.fixtures if f["id"] == self.r["fixture_id"])
        self.p = next(p for p in self.catalog["patterns"] if p["id"] == self.f["pattern_id"])

    def selected(self, initial=None, refinement=None):
        revised = ev.validate_pattern_history(self.initial_catalog["patterns"], self.catalog["patterns"])
        initial = self.initial if initial is None else initial
        refinement = self.refinement if refinement is None else refinement
        return [r for r in initial if r["pattern_id"] not in revised] + refinement

    def validate(self):
        return ev.validate_receipt(self.r, self.f, self.p)

    def test_preserved_summary(self):
        self.assertEqual(ev.report(), ev.read("results/summary.json"))

    def test_initial_and_refinement_summaries(self):
        report = ev.report()
        self.assertEqual(report["initial"]["fixtures"], 32)
        self.assertEqual(report["initial"]["splits"]["design"]["label_matches"], 24)
        self.assertEqual(report["refinement"]["fixtures"], 6)
        self.assertEqual(report["refinement"]["splits"]["challenge"]["label_matches"], 3)
        self.assertEqual(report["current"]["fixtures"], 34)
        self.assertEqual(report["current"]["provisional_patterns"], [])

    def test_two_evaluation_splits(self):
        result = ev.report()["current"]
        self.assertEqual(result["splits"]["design"]["cases"], 24)
        self.assertEqual(result["splits"]["challenge"]["cases"], 10)

    def test_policy_option_counts_match_contracts(self):
        for p in self.catalog["patterns"]:
            self.assertEqual(p["policy"]["option_count"], len(p["questions"]["decision"]["criteria"]))

    def test_versioned_fixture_history_is_additive(self):
        revised = ev.validate_pattern_history(self.initial_catalog["patterns"], self.catalog["patterns"])
        self.assertEqual(revised, {"AP03"})
        ev.validate_fixture_history(self.initial_fixtures, self.fixtures, revised, self.catalog["patterns"])
        self.assertEqual(set(f["id"] for f in self.fixtures) - set(f["id"] for f in self.initial_fixtures), {"AP03-5", "AP03-6"})
        new_cases = [f for f in self.fixtures if f["id"] in {"AP03-5", "AP03-6"}]
        self.assertTrue(all(f["author_origin"] == "versioned_contract_reviewer" for f in new_cases))

    def test_each_revised_pattern_needs_a_new_boundary_case(self):
        with self.assertRaisesRegex(ValueError, "each revised pattern"):
            ev.validate_fixture_history(
                self.initial_fixtures,
                self.fixtures,
                {"AP03", "AP04"},
                self.catalog["patterns"],
            )

    def test_frozen_fixture_state_cannot_change(self):
        revised = {"AP03"}
        fixtures = copy.deepcopy(self.fixtures)
        next(f for f in fixtures if f["id"] == "AP03-1")["state"]["fitment_text"] += " AWD only."
        with self.assertRaises(ValueError):
            ev.validate_fixture_history(self.initial_fixtures, fixtures, revised, self.catalog["patterns"])

    def test_frozen_fixture_expectation_cannot_change(self):
        fixtures = copy.deepcopy(self.fixtures)
        next(f for f in fixtures if f["id"] == "AP03-1")["expected"] = "unknown"
        with self.assertRaises(ValueError):
            ev.validate_fixture_history(self.initial_fixtures, fixtures, {"AP03"}, self.catalog["patterns"])

    def test_frozen_fixture_cannot_be_removed(self):
        fixtures = [f for f in self.fixtures if f["id"] != "AP03-1"]
        with self.assertRaises(ValueError):
            ev.validate_fixture_history(self.initial_fixtures, fixtures, {"AP03"}, self.catalog["patterns"])

    def test_pattern_cannot_change_without_version_increment(self):
        patterns = copy.deepcopy(self.catalog["patterns"])
        next(p for p in patterns if p["id"] == "AP01")["title"] += " changed"
        with self.assertRaises(ValueError):
            ev.validate_pattern_history(self.initial_catalog["patterns"], patterns)

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

    def test_boolean_version_rejected(self):
        self.r["version"] = True
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

    def test_inconsistent_confidence_rejected(self):
        answer = self.r["response"]["answers"]["decision"]
        answer["confidence"] = 0.0 if answer["confidence"] > 0.5 else 1.0
        with self.assertRaises(ValueError):
            self.validate()

    def test_recovery_cannot_replace_semantic_miss(self):
        recovery = copy.deepcopy(self.refinement_recovery)
        recovery.append(copy.deepcopy(self.r))
        with self.assertRaises(ValueError):
            ev.replay_collection(
                self.catalog,
                self.fixtures,
                self.sources,
                self.selected(),
                recovery,
            )

    def test_pattern_page_question_json_matches_catalog(self):
        page = (Path(__file__).parent / "patterns" / "ap03.md").read_text()
        match = re.search(r"## Exact question JSON.*?```json\s*(.*?)```", page, re.S)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)), self.p["questions"])


if __name__ == "__main__":
    unittest.main()
