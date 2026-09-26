import json
from pathlib import Path
import tempfile
import unittest

from review_all_patterns import inventory


class ReviewInventoryTests(unittest.TestCase):
    def test_current_catalog_coverage_and_unique_keys(self):
        rows = inventory()
        self.assertEqual(len(rows), 390)
        self.assertEqual(len({r["catalog"] for r in rows}), 30)
        self.assertEqual(len({r["key"] for r in rows}), len(rows))
        self.assertTrue(all(r["semantic_review"] == "pending" for r in rows))

    def write_catalog(self, root, patterns):
        folder = root / "sample"
        folder.mkdir(exist_ok=True)
        (folder / "catalog.json").write_text(json.dumps({"patterns": patterns}))

    def test_historical_version_supported_and_hash_binds_questions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            p = {"id": "P1", "contract_version": 2, "questions": {"q": {"type": "noul"}}}
            self.write_catalog(root, [p])
            first = inventory(root)[0]
            self.assertEqual(first["version"], 2)
            p["questions"]["q"]["instructions"] = "changed"
            self.write_catalog(root, [p])
            self.assertNotEqual(first["pattern_sha256"], inventory(root)[0]["pattern_sha256"])

    def test_invalid_versions_and_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for version in (None, True, 0, "1"):
                self.write_catalog(root, [{"id": "P1", "version": version, "questions": {}}])
                with self.assertRaises(ValueError):
                    inventory(root)
            p = {"id": "P1", "version": 1, "questions": {}}
            self.write_catalog(root, [p, p])
            with self.assertRaises(ValueError):
                inventory(root)


if __name__ == "__main__":
    unittest.main()
