import copy
import hashlib
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

    def test_policy_option_counts_match_contracts(self):
        for p in self.catalog["patterns"]:
            self.assertEqual(p["policy"]["option_count"], len(p["questions"]["decision"]["criteria"]))

    def test_el07_has_primary_cpsc_device_function_sources(self):
        source_map = {source["id"]: source for source in self.sources}
        el07 = next(pattern for pattern in self.catalog["patterns"] if pattern["id"] == "EL07")
        self.assertIn("ES-7", el07["source_ids"])
        self.assertIn("ES-8", el07["source_ids"])
        for source_id in ("ES-7", "ES-8"):
            source = source_map[source_id]
            with self.subTest(source=source_id):
                self.assertIn("CPSC", source["title"])
                self.assertEqual(source["representation"], "browser_excerpt")
                self.assertEqual(hashlib.sha256(source["excerpt"].encode("utf-8")).hexdigest(), source["sha256"])
                self.assertIn("not current installation requirements", source["summary"])

    def test_all_electrical_pages_match_catalog_question_and_preflight_boundary(self):
        patterns = {pattern["id"]: pattern for pattern in self.catalog["patterns"]}
        for pattern_id, pattern in patterns.items():
            page_path = Path(__file__).resolve().parent / "patterns" / (pattern_id.lower() + ".md")
            page = page_path.read_text(encoding="utf-8")
            with self.subTest(pattern=pattern_id):
                match = re.search(r"## Exact question JSON\s+Reproduced from contract v\d+.*?```json\s*(.*?)\s*```", page, re.S)
                self.assertIsNotNone(match)
                self.assertEqual(json.loads(match.group(1)), pattern["questions"])
                self.assertIn("Consumer code must deterministically return `unknown`", page)
                self.assertIn("this collection does not implement or verify that gate", page)
                self.assertNotIn("Code deterministically returns `unknown`", page)

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
        fixtures = copy.deepcopy(self.fixtures)
        labels = list(self.p["questions"]["decision"]["criteria"])
        target = next(f for f in fixtures if f["id"] == self.f["id"])
        target["expected"] = next(l for l in labels if l != target["expected"])
        result = ev.replay(self.catalog, fixtures, self.sources, self.initial, self.recovery)
        self.assertNotEqual(result, ev.read("results/summary.json"))

    def test_recovery_cannot_replace_semantic_miss(self):
        recovery = copy.deepcopy(self.recovery)
        recovery.append(copy.deepcopy(self.r))
        with self.assertRaises(ValueError):
            ev.replay(self.catalog, self.fixtures, self.sources, self.initial, recovery)


if __name__ == "__main__":
    unittest.main()
