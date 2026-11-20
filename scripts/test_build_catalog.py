"""Guard the pattern finder against supported collection summary shapes."""

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_catalog", Path(__file__).with_name("build_catalog.py")
)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class CatalogBuilderTests(unittest.TestCase):
    def test_versioned_collection_summaries_use_current_provisional_list(self):
        groups = {group["slug"]: group for group in builder.source_groups()}

        for name in ("auto-performance", "construction", "motorsport"):
            with self.subTest(collection=name):
                summary = json.loads(
                    (ROOT / name / "results/summary.json").read_text(encoding="utf-8")
                )
                current = builder.current_summary(summary)
                self.assertEqual(groups[name]["provisional"], set(current["provisional_patterns"]))

    def test_provisional_flags_remain_scoped_to_each_catalog(self):
        groups = {group["slug"]: group for group in builder.source_groups()}

        self.assertEqual(groups["construction"]["provisional"], {"CN05"})
        self.assertEqual(groups["bug-hunting"]["provisional"], {"BH41"})
        self.assertEqual(groups["auto-performance"]["provisional"], set())
        self.assertEqual(groups["motorsport"]["provisional"], set())
        self.assertEqual(groups["executive"]["provisional"], set())
        self.assertEqual(groups["human-resources"]["provisional"], {"HR06"})


if __name__ == "__main__":
    unittest.main()
