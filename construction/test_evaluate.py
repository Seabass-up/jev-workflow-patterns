import copy
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("construction_evaluate", Path(__file__).with_name("evaluate.py"))
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


class ConstructionTests(unittest.TestCase):
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
        self.r = copy.deepcopy(next(r for r in self.refinement if r["fixture_id"] == "CN05-8"))
        self.f = next(f for f in self.fixtures if f["id"] == self.r["fixture_id"])
        self.p = next(p for p in self.catalog["patterns"] if p["id"] == self.f["pattern_id"])

    def validate(self):
        return ev.validate_receipt(self.r, self.f, self.p)

    def revised(self):
        return ev.validate_pattern_history(self.initial_catalog["patterns"], self.catalog["patterns"])

    def test_saved_summary_replays(self):
        self.assertEqual(ev.report(), ev.read("results/summary.json"))

    def test_initial_refinement_and_current_screens_remain_distinct(self):
        result = ev.report()
        self.assertEqual(result["initial"]["fixtures"], 32)
        self.assertEqual(result["initial"]["splits"]["design"]["label_matches"], 24)
        self.assertEqual(result["initial"]["splits"]["challenge"]["label_matches"], 7)
        self.assertEqual(result["initial"]["splits"]["challenge"]["disagreements"][0]["fixture_id"], "CN05-4")
        self.assertEqual(result["refinement"]["fixtures"], 7)
        self.assertEqual(result["refinement"]["splits"]["design"]["cases"], 3)
        self.assertEqual(result["refinement"]["splits"]["challenge"]["cases"], 4)
        self.assertEqual(result["current"]["fixtures"], 35)
        self.assertEqual(result["current"]["splits"]["design"]["cases"], 24)
        self.assertEqual(result["current"]["splits"]["challenge"]["cases"], 11)

    def test_only_cn05_is_versioned_and_original_expectations_stay_immutable(self):
        self.assertEqual(self.revised(), {"CN05"})
        old = ev.unique(self.initial_fixtures, "id")
        current = ev.unique(self.fixtures, "id")
        self.assertTrue(set(old).issubset(current))
        for fixture_id, fixture in old.items():
            self.assertEqual(current[fixture_id], fixture)
        self.assertEqual(
            set(current) - set(old),
            {"CN05-5", "CN05-6", "CN05-7", "CN05-8", "CN05-9", "CN05-10", "CN05-11"},
        )

    def test_v1_miss_is_preserved_and_v2_has_each_label(self):
        current = ev.current_fixtures(self.catalog, self.fixtures)
        initial_cn05 = next(f for f in self.initial_fixtures if f["id"] == "CN05-4")
        self.assertEqual(initial_cn05["expected"], "stop_work_condition")
        self.assertEqual(initial_cn05["version"], 1)
        v2 = [f for f in current if f["pattern_id"] == "CN05"]
        self.assertEqual({f["expected"] for f in v2}, set(self.p["questions"]["decision"]["criteria"]))
        active_case = next(f for f in v2 if f["id"] == "CN05-8")
        self.assertEqual(active_case["expected"], "hazard_to_correct")
        self.assertIn("continued cutting", active_case["state"]["observation_text"])

    def test_versioned_cases_are_reviewer_authored_and_not_held_out(self):
        added = [f for f in self.fixtures if f["id"].startswith("CN05-") and f["version"] == 2]
        self.assertEqual(len(added), 7)
        self.assertTrue(all(f["author_origin"] == "versioned_contract_reviewer" for f in added))
        self.assertEqual(sum(f["split"] == "design" for f in added), 3)
        self.assertEqual(sum(f["split"] == "challenge" for f in added), 4)
        self.assertIn("not independently labeled or held out", ev.report()["refinement"]["scope"])

    def test_versioned_fixture_history_is_additive_without_relabeling_old_cases(self):
        added = ev.validate_fixture_history(
            self.initial_fixtures, self.fixtures, self.revised(),
            self.initial_catalog["patterns"], self.catalog["patterns"],
        )
        self.assertEqual(added, {"CN05-5", "CN05-6", "CN05-7", "CN05-8", "CN05-9", "CN05-10", "CN05-11"})

    def test_removed_superseded_fixture_is_rejected(self):
        fixtures = [f for f in self.fixtures if f["id"] != "CN05-4"]
        with self.assertRaisesRegex(ValueError, "frozen fixture removed"):
            ev.validate_fixture_history(
                self.initial_fixtures, fixtures, self.revised(),
                self.initial_catalog["patterns"], self.catalog["patterns"],
            )

    def test_relabelled_or_rewritten_v1_fixture_is_rejected(self):
        for field, value in (("expected", "hazard_to_correct"), ("version", 2)):
            fixtures = copy.deepcopy(self.fixtures)
            next(f for f in fixtures if f["id"] == "CN05-4")[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "frozen fixture was rewritten"):
                ev.validate_fixture_history(
                    self.initial_fixtures, fixtures, self.revised(),
                    self.initial_catalog["patterns"], self.catalog["patterns"],
                )

    def test_revised_contract_requires_new_current_version_cases(self):
        fixtures = [f for f in self.fixtures if f["id"] not in {"CN05-8", "CN05-9", "CN05-10", "CN05-11"}]
        with self.assertRaisesRegex(ValueError, "needs three design and one challenge"):
            ev.validate_fixture_history(
                self.initial_fixtures, fixtures, self.revised(),
                self.initial_catalog["patterns"], self.catalog["patterns"],
            )

    def test_new_fixture_cannot_target_an_unchanged_contract(self):
        fixtures = copy.deepcopy(self.fixtures)
        fixture = copy.deepcopy(next(f for f in fixtures if f["id"] == "CN01-1"))
        fixture["id"] = "CN01-5"
        fixtures.append(fixture)
        with self.assertRaisesRegex(ValueError, "new fixture must target a revised pattern"):
            ev.validate_fixture_history(
                self.initial_fixtures, fixtures, self.revised(),
                self.initial_catalog["patterns"], self.catalog["patterns"],
            )

    def test_contract_changes_require_one_exact_version_increment(self):
        patterns = copy.deepcopy(self.catalog["patterns"])
        next(p for p in patterns if p["id"] == "CN05")["version"] = 3
        with self.assertRaisesRegex(ValueError, "increment exactly once"):
            ev.validate_pattern_history(self.initial_catalog["patterns"], patterns)

    def test_pattern_cannot_change_without_a_version_increment(self):
        patterns = copy.deepcopy(self.catalog["patterns"])
        next(p for p in patterns if p["id"] == "CN01")["title"] += " changed"
        with self.assertRaisesRegex(ValueError, "without a version increment"):
            ev.validate_pattern_history(self.initial_catalog["patterns"], patterns)

    def test_version_cannot_change_without_contract_content_change(self):
        patterns = copy.deepcopy(self.initial_catalog["patterns"])
        next(p for p in patterns if p["id"] == "CN05")["version"] = 2
        with self.assertRaisesRegex(ValueError, "without a content change"):
            ev.validate_pattern_history(self.initial_catalog["patterns"], patterns)

    def test_contract_policy_option_counts_match_questions(self):
        for pattern in self.catalog["patterns"]:
            self.assertEqual(pattern["policy"]["option_count"], len(pattern["questions"]["decision"]["criteria"]))

    def test_all_eight_question_pages_match_catalog_json(self):
        for pattern in self.catalog["patterns"]:
            page = (Path(__file__).parent / "patterns" / f"{pattern['id'].lower()}.md").read_text()
            section = page.split("## Exact question JSON", 1)[1]
            block = section.split("```json", 1)[1].split("```", 1)[0]
            with self.subTest(pattern_id=pattern["id"]):
                self.assertEqual(json.loads(block), pattern["questions"])

    def test_revised_request_binds_the_v2_state_and_question(self):
        ev.validate_receipt(self.r, self.f, self.p)
        self.assertEqual(self.r["version"], 2)
        self.assertEqual(self.r["request"]["state"], self.f["state"])
        self.assertEqual(self.r["request"]["questions"], self.p["questions"])

    def test_changed_v2_state_is_rejected(self):
        self.r["request"]["state"] = {"replacement": True}
        with self.assertRaisesRegex(ValueError, "state or question binding mismatch"):
            self.validate()

    def test_changed_v2_question_is_rejected(self):
        self.r["request"]["questions"]["decision"]["instructions"] = "Changed meaning"
        with self.assertRaisesRegex(ValueError, "state or question binding mismatch"):
            self.validate()

    def test_stale_receipt_version_is_rejected(self):
        self.r["version"] = 1
        with self.assertRaisesRegex(ValueError, "stale contract version"):
            self.validate()

    def test_boolean_version_is_rejected(self):
        self.r["version"] = True
        with self.assertRaisesRegex(ValueError, "invalid version"):
            self.validate()

    def test_tampered_request_digest_is_rejected(self):
        self.r["response"]["request_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "request digest mismatch"):
            self.validate()

    def test_wrong_model_is_rejected(self):
        self.r["response"]["model"] = "unrelated-model"
        with self.assertRaisesRegex(ValueError, "model binding mismatch"):
            self.validate()

    def test_inconsistent_confidence_is_rejected(self):
        answer = self.r["response"]["answers"]["decision"]
        answer["confidence"] = 0.0 if answer["confidence"] > 0.5 else 1.0
        with self.assertRaisesRegex(ValueError, "confidence inconsistent"):
            self.validate()

    def test_recovery_cannot_replace_a_semantic_miss(self):
        recovery = copy.deepcopy(self.refinement_recovery)
        recovery.append(copy.deepcopy(self.r))
        with self.assertRaisesRegex(ValueError, "recovery may not replace a semantic miss"):
            ev.replay_collection(
                {**self.catalog, "patterns": [self.p]},
                [f for f in ev.current_fixtures(self.catalog, self.fixtures) if f["pattern_id"] == "CN05"],
                self.sources,
                self.refinement,
                recovery,
            )


if __name__ == "__main__":
    unittest.main()
