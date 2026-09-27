import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest

spec = importlib.util.spec_from_file_location("executive_evaluate", Path(__file__).with_name("evaluate.py"))
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


class ExecutiveReplayTests(unittest.TestCase):
    def setUp(self):
        self.old_catalog = ev.read("results/initial-catalog.json")
        self.old_fixtures = ev.read("results/initial-fixtures.json")
        self.old_sources = ev.read("results/initial-sources.json")
        self.catalog = ev.read("catalog.json")
        self.fixtures = ev.read("fixtures.json")
        self.sources = ev.read("sources.json")
        self.initial = ev.read("results/screening.json")
        self.refinement = ev.read("results/refinement.json")

    def test_saved_versioned_summary_replays(self):
        self.assertEqual(ev.report(), ev.read("results/summary.json"))

    def test_v1_disagreements_are_preserved_and_v2_is_version_bound(self):
        result = ev.report()
        self.assertEqual(
            [x["fixture_id"] for x in result["initial"]["splits"]["challenge"]["disagreements"]],
            ["CE02-4", "CE06-4"],
        )
        self.assertEqual(result["initial"]["splits"]["challenge"]["label_matches"], 6)
        self.assertEqual(result["refinement"]["successful_request_digests_verified"], 15)
        self.assertEqual(result["refinement"]["splits"]["design"]["label_matches"], 9)
        self.assertEqual(result["refinement"]["splits"]["challenge"]["label_matches"], 6)
        self.assertEqual(result["fixtures"], 35)
        self.assertEqual(result["successful_request_digests_verified"], 35)
        self.assertEqual(result["splits"]["design"]["label_matches"], 24)
        self.assertEqual(result["splits"]["challenge"]["label_matches"], 11)
        self.assertEqual(result["request_digests_verified"], 47)
        self.assertEqual(result["revision"]["patterns"], ["CE02", "CE03", "CE06"])

    def test_low_confidence_match_still_requires_policy_review(self):
        result = ev.report()
        self.assertEqual(result["review_required"], [
            {
                "fixture_id": "CE01-4",
                "pattern_id": "CE01",
                "expected": "no_decision_requested",
                "observed": "no_decision_requested",
                "confidence": 0.67,
                "review_below": 0.8,
            },
            {
                "fixture_id": "CE07-2",
                "pattern_id": "CE07",
                "expected": "qualitative_outcome",
                "observed": "qualitative_outcome",
                "confidence": 0.59,
                "review_below": 0.8,
            },
            {
                "fixture_id": "CE02-5",
                "pattern_id": "CE02",
                "expected": "reversibility_not_addressed",
                "observed": "reversibility_not_addressed",
                "confidence": 0.56,
                "review_below": 0.8,
            },
        ])

    def test_v1_summary_stays_bound_to_v1_files(self):
        from collection_tools import replay
        replayed = replay(self.old_catalog, self.old_fixtures, self.old_sources, self.initial, [])
        self.assertEqual(replayed, ev.read("results/initial-summary.json"))

    def test_historical_fixture_state_and_expectation_cannot_be_rewritten(self):
        fixtures = copy.deepcopy(self.fixtures)
        next(f for f in fixtures if f["id"] == "CE02-4")["state"]["proposal_text"] = "rewritten"
        with self.assertRaisesRegex(ValueError, "frozen fixture was rewritten"):
            ev.validate_fixture_history(self.old_fixtures, fixtures, self.old_catalog["patterns"], self.catalog["patterns"])
        fixtures = copy.deepcopy(self.fixtures)
        next(f for f in fixtures if f["id"] == "CE06-4")["expected"] = "upside_only"
        with self.assertRaisesRegex(ValueError, "frozen fixture was rewritten"):
            ev.validate_fixture_history(self.old_fixtures, fixtures, self.old_catalog["patterns"], self.catalog["patterns"])

    def test_historical_fixture_cannot_be_removed(self):
        fixtures = [f for f in self.fixtures if f["id"] != "CE01-1"]
        with self.assertRaisesRegex(ValueError, "frozen fixture removed"):
            ev.validate_fixture_history(self.old_fixtures, fixtures, self.old_catalog["patterns"], self.catalog["patterns"])

    def test_new_fixture_requires_a_revised_contract(self):
        fixtures = copy.deepcopy(self.fixtures)
        added = copy.deepcopy(next(f for f in fixtures if f["id"] == "CE01-1"))
        added["id"] = "CE01-5"
        fixtures.append(added)
        with self.assertRaisesRegex(ValueError, "new fixture must target a revised contract"):
            ev.validate_fixture_history(self.old_fixtures, fixtures, self.old_catalog["patterns"], self.catalog["patterns"])

    def test_contract_cannot_change_without_version_increment(self):
        patterns = copy.deepcopy(self.catalog["patterns"])
        next(p for p in patterns if p["id"] == "CE04")["purpose"] = "changed without bump"
        with self.assertRaisesRegex(ValueError, "contract changed without version increment"):
            ev.validate_fixture_history(self.old_fixtures, self.fixtures, self.old_catalog["patterns"], patterns)

    def test_version_skip_and_boolean_version_rejected(self):
        patterns = copy.deepcopy(self.catalog["patterns"])
        next(p for p in patterns if p["id"] == "CE02")["version"] = 4
        with self.assertRaisesRegex(ValueError, "pattern version skipped"):
            ev.validate_fixture_history(self.old_fixtures, self.fixtures, self.old_catalog["patterns"], patterns)
        patterns = copy.deepcopy(self.catalog["patterns"])
        next(p for p in patterns if p["id"] == "CE02")["version"] = True
        with self.assertRaisesRegex(ValueError, "invalid pattern version"):
            ev.validate_fixture_history(self.old_fixtures, self.fixtures, self.old_catalog["patterns"], patterns)

    def test_fixture_version_must_match_current_pattern(self):
        fixtures = copy.deepcopy(self.fixtures)
        next(f for f in fixtures if f["id"] == "CE02-5")["version"] = 1
        with self.assertRaisesRegex(ValueError, "fixture version does not match current contract"):
            ev.validate_fixture_history(self.old_fixtures, fixtures, self.old_catalog["patterns"], self.catalog["patterns"])

    def test_fixture_version_must_be_exact_positive_integer(self):
        for invalid in (True, 1.0, 0, None):
            with self.subTest(version=invalid):
                fixtures = copy.deepcopy(self.fixtures)
                next(f for f in fixtures if f["id"] == "CE01-1")["version"] = invalid
                with self.assertRaisesRegex(ValueError, "invalid fixture version"):
                    ev.validate_fixture_history(self.old_fixtures, fixtures, self.old_catalog["patterns"], self.catalog["patterns"])

    def test_eight_pages_embed_exact_current_questions_and_fixture_expectations(self):
        patterns = {p["id"]: p for p in self.catalog["patterns"]}
        for pattern in self.catalog["patterns"]:
            page = (Path(__file__).resolve().parent / "patterns" / (pattern["id"].lower() + ".md")).read_text()
            with self.subTest(pattern=pattern["id"]):
                match = re.search(r"## Exact question JSON\s+Reproduced from contract v\d+.*?```json\s*(.*?)\s*```", page, re.S)
                self.assertIsNotNone(match)
                self.assertEqual(json.loads(match.group(1)), pattern["questions"])
                for fixture in self.fixtures:
                    if fixture["pattern_id"] == pattern["id"]:
                        self.assertIn("| `%s` | %s | `%s` |" % (fixture["id"], fixture["split"], fixture["expected"]), page)
        self.assertIn("confidence 0.56 below 0.8 review threshold", (Path(__file__).resolve().parent / "patterns/ce02.md").read_text())

    def test_evaluation_page_keeps_v1_misses_and_low_confidence_review(self):
        page = (Path(__file__).resolve().parent / "evaluation.md").read_text()
        self.assertIn("Preserved version-1 disagreements", page)
        self.assertIn("CE02-4", page)
        self.assertIn("CE06-4", page)
        self.assertIn("CE02-5", page)
        self.assertIn("0.56", page)

    def test_source_refresh_is_current_and_motivates_ce02_only(self):
        sources = {source["id"]: source for source in self.sources}
        self.assertEqual(sources["CE-S6"]["checked"], "2026-09-27")
        self.assertIn("CE-S6", next(p for p in self.catalog["patterns"] if p["id"] == "CE02")["source_ids"])
        self.assertNotIn("CE-S6", next(p for p in self.catalog["patterns"] if p["id"] == "CE06")["source_ids"])


if __name__ == "__main__":
    unittest.main()
