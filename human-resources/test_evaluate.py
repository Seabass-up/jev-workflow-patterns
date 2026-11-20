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
        self.old_catalog = ev.read("results/initial-catalog.json")
        self.old_fixtures = ev.read("results/initial-fixtures.json")
        self.old_sources = ev.read("results/initial-sources.json")
        self.catalog = ev.read("catalog.json")
        self.fixtures = ev.read("fixtures.json")
        self.sources = ev.read("sources.json")
        self.initial = ev.read("results/screening.json")
        self.refinement = ev.read("results/refinement.json")
        self.recovery = ev.read("results/recovery.json")
        self.r = copy.deepcopy(next(r for r in self.refinement if r["fixture_id"] == "HR06-4"))
        self.f = next(f for f in self.fixtures if f["id"] == self.r["fixture_id"])
        self.p = next(p for p in self.catalog["patterns"] if p["id"] == self.f["pattern_id"])

    def validate(self):
        return ev.validate_receipt(self.r, self.f, self.p)

    def replay(self):
        return ev.report()

    def test_preserved_summary(self):
        self.assertEqual(self.replay(), ev.read("results/summary.json"))

    def test_two_evaluation_splits(self):
        result = self.replay()
        self.assertEqual(result["splits"]["design"]["cases"], 24)
        self.assertEqual(result["splits"]["challenge"]["cases"], 13)
        self.assertEqual(result["fixtures"], 37)
        self.assertEqual(result["splits"]["design"]["label_matches"], 23)
        self.assertEqual(result["splits"]["challenge"]["label_matches"], 13)
        self.assertEqual(result["provisional_patterns"], ["HR06"])

    def test_v1_history_and_v2_regressions_are_separate(self):
        result = self.replay()
        initial_disagreements = {
            item["fixture_id"]
            for split in result["initial"]["splits"].values()
            for item in split["disagreements"]
        }
        self.assertEqual(initial_disagreements, {"HR06-3", "HR06-4", "HR07-4"})
        self.assertEqual(result["initial"]["successful_request_digests_verified"], 32)
        self.assertEqual(result["refinement"]["successful_request_digests_verified"], 17)
        self.assertEqual(result["refinement"]["splits"]["design"]["label_matches"], 8)
        self.assertEqual(result["refinement"]["splits"]["challenge"]["label_matches"], 8)
        self.assertEqual(result["request_digests_verified"], 49)
        self.assertEqual(result["revision"]["patterns"], ["HR05", "HR06", "HR07"])
        self.assertEqual(result["revision"]["preserved_initial_receipts"], 32)

    def test_review_threshold_is_reported_for_matches_and_disagreements(self):
        review = self.replay()["review_required"]
        self.assertEqual(
            [item["fixture_id"] for item in review],
            ["HR01-4", "HR03-2", "HR06-3"],
        )
        self.assertTrue(all(item["confidence"] < item["review_below"] for item in review))
        page = (Path(__file__).resolve().parent / "evaluation.md").read_text()
        self.assertIn("Current answers below the recorded review threshold", page)
        for fixture_id in ("HR01-4", "HR03-2", "HR06-3"):
            self.assertIn(fixture_id, page)

    def test_v1_summary_stays_bound_to_frozen_files(self):
        old_summary = ev.replay_collection(
            self.old_catalog, self.old_fixtures, self.old_sources, self.initial, []
        )
        self.assertEqual(old_summary, ev.read("results/initial-summary.json"))

    def test_fixture_history_preserves_old_content_and_versions_new_cases(self):
        ev.validate_fixture_history(
            self.old_fixtures, self.fixtures,
            self.old_catalog["patterns"], self.catalog["patterns"],
        )
        fixtures = copy.deepcopy(self.fixtures)
        next(f for f in fixtures if f["id"] == "HR06-4")["state"]["offer_letter_text"] = "rewritten"
        with self.assertRaisesRegex(ValueError, "frozen fixture was rewritten"):
            ev.validate_fixture_history(
                self.old_fixtures, fixtures,
                self.old_catalog["patterns"], self.catalog["patterns"],
            )

    def test_policy_option_counts_match_contracts(self):
        for p in self.catalog["patterns"]:
            self.assertEqual(p["policy"]["option_count"], len(p["questions"]["decision"]["criteria"]))

    def test_revised_multi_reason_and_example_rules_are_explicit(self):
        patterns = {p["id"]: p for p in self.catalog["patterns"]}
        hr05 = patterns["HR05"]["questions"]["decision"]
        self.assertIn("select the first actual reason mentioned", hr05["instructions"])
        self.assertIn("Do not use a fixed category-priority order", hr05["instructions"])
        hr06 = patterns["HR06"]["questions"]["decision"]
        self.assertIn("whether or not another listed element is missing", hr06["instructions"])
        self.assertIn("whether or not another listed element is given no value", hr06["criteria"]["inconsistent_elements"])
        self.assertIn("and no listed element is given two different values", hr06["criteria"]["missing_elements"])
        hr07 = patterns["HR07"]["questions"]["decision"]
        self.assertIn("merely naming a period or event", hr07["instructions"])
        self.assertIn("does not make it an instance", hr07["criteria"]["generalization_only"])
        self.assertIn("what the employee did or produced", hr07["criteria"]["generalization_with_example"])

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

    def test_relabeled_expectation_changes_summary(self):
        fixtures = copy.deepcopy(self.old_fixtures)
        old_pattern = next(p for p in self.old_catalog["patterns"] if p["id"] == "HR01")
        labels = list(old_pattern["questions"]["decision"]["criteria"])
        target = next(f for f in fixtures if f["id"] == "HR01-1")
        target["expected"] = next(l for l in labels if l != target["expected"])
        result = ev.replay_collection(
            self.old_catalog, fixtures, self.old_sources, self.initial, []
        )
        self.assertNotEqual(result, ev.read("results/initial-summary.json"))

    def test_recovery_cannot_replace_semantic_miss(self):
        recovery = copy.deepcopy(self.recovery)
        semantic_miss = next(r for r in self.initial if r["fixture_id"] == "HR06-3")
        recovery.append(copy.deepcopy(semantic_miss))
        with self.assertRaises(ValueError):
            ev.replay_collection(
                self.old_catalog, self.old_fixtures, self.old_sources, self.initial, recovery
            )

    def test_all_pages_match_current_questions_fields_and_fixture_labels(self):
        patterns = {p["id"]: p for p in self.catalog["patterns"]}
        mark = chr(96)
        fence = mark * 3
        for pattern in self.catalog["patterns"]:
            page = (
                Path(__file__).resolve().parent
                / "patterns"
                / f"{pattern['id'].lower()}.md"
            ).read_text()
            with self.subTest(pattern=pattern["id"]):
                match = re.search(
                    r"## Exact question JSON\s+Reproduced from contract v\d+.*?"
                    + fence + r"json\s*(.*?)\s*" + fence,
                    page,
                    re.S,
                )
                self.assertIsNotNone(match)
                self.assertEqual(json.loads(match.group(1)), patterns[pattern["id"]]["questions"])
                for field in pattern["required_state_fields"]:
                    self.assertIn(field, page)
                for fixture in self.fixtures:
                    if fixture["pattern_id"] == pattern["id"]:
                        self.assertIn(
                            f"| {mark}{fixture['id']}{mark} | {fixture['split']} | "
                            f"{mark}{fixture['expected']}{mark} |",
                            page,
                        )

    def test_versioned_evaluation_preserves_old_misses_and_limits(self):
        page = (Path(__file__).resolve().parent / "evaluation.md").read_text()
        self.assertIn("Preserved version-1 disagreements", page)
        self.assertIn("HR06-4", page)
        self.assertIn("HR07-4", page)
        self.assertIn("Versioned refinement receipts (17)", page)
        self.assertIn("no random sample", page)


if __name__ == "__main__":
    unittest.main()
