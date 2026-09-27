"""Guard generated collection pages against unsupported runtime claims."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "build_collection_pages", Path(__file__).with_name("build_collection_pages.py")
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class CollectionPageBuilderTests(unittest.TestCase):
    def test_data_quality_pages_describe_preflight_as_consumer_requirement(self):
        name = "data-quality"
        folder = ROOT / name
        catalog = json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
        fixtures = json.loads((folder / "fixtures.json").read_text(encoding="utf-8"))
        sources = json.loads((folder / "sources.json").read_text(encoding="utf-8"))
        summary = json.loads((folder / "results/summary.json").read_text(encoding="utf-8"))
        meta = builder.load_meta(name)

        for pattern in catalog["patterns"]:
            with self.subTest(pattern=pattern["id"]):
                rendered = builder.pattern_page(
                    name, meta, pattern, fixtures, sources, builder.all_titles(), summary
                )
                self.assertIn("Consumer code must deterministically return", rendered)
                self.assertIn("this collection does not implement or verify that gate", rendered)
                self.assertNotIn("Code deterministically returns `unknown`", rendered)


if __name__ == "__main__":
    unittest.main()
