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
    def test_browser_excerpt_sources_disclose_digest_scope(self):
        name = "electrical"
        folder = ROOT / name
        catalog = json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
        sources = json.loads((folder / "sources.json").read_text(encoding="utf-8"))
        rendered = builder.sources_page(name, builder.load_meta(name), catalog, sources)
        self.assertIn("SHA-256 binds only the exact excerpt shown below", rendered)
        self.assertIn("SHA-256 `61ddfd52e3a1a0c3…` (covers the recorded excerpt)", rendered)
        self.assertIn("> Ground fault protection is integrated into GFCI receptacles and GFCI circuit breakers.", rendered)
        self.assertIn("> AFCIs are intended to address fire hazards; GFCIs address shock hazards.", rendered)
        self.assertNotIn("binds the page text as fetched", rendered)

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

    def test_kernel_reference_modules_do_not_claim_consumer_preflight_is_implemented(self):
        references = ROOT / "skills/jev-question-kernel-catalog/references"
        for path in sorted(references.glob("*.md")):
            with self.subTest(reference=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertNotRegex(
                    content,
                    r"(?im)Before inference, code validates `required_state_fields`",
                )
        grading = (references / "grading.md").read_text(encoding="utf-8")
        self.assertIn("The consuming application must validate `required_state_fields`", grading)
        self.assertIn("do not implement or verify that preflight", grading)

    def test_flat_and_versioned_summaries_resolve_to_current_selection(self):
        flat = json.loads((ROOT / "executive/results/summary.json").read_text(encoding="utf-8"))
        self.assertIs(builder.current_summary(flat), flat)
        for name in ("auto-performance", "construction", "motorsport"):
            with self.subTest(collection=name):
                outer = json.loads((ROOT / name / "results/summary.json").read_text(encoding="utf-8"))
                current = builder.current_summary(outer)
                self.assertIs(current, outer["current"])
                self.assertIn("splits", current)
                self.assertIn("provisional_patterns", current)

    def test_versioned_pages_disclose_reviewer_regressions_and_current_receipts(self):
        for name, pattern_id in (("executive", "CE03"), ("auto-performance", "AP03"),
                                 ("construction", "CN05"), ("motorsport", "MR04")):
            with self.subTest(collection=name):
                folder = ROOT / name
                catalog = json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
                fixtures = json.loads((folder / "fixtures.json").read_text(encoding="utf-8"))
                sources = json.loads((folder / "sources.json").read_text(encoding="utf-8"))
                summary = json.loads((folder / "results/summary.json").read_text(encoding="utf-8"))
                pattern = next(p for p in catalog["patterns"] if p["id"] == pattern_id)
                meta = builder.load_meta(name)
                rendered = builder.pattern_page(name, meta, pattern, fixtures, sources,
                                                builder.all_titles(), summary)
                self.assertIn("Exact question JSON", rendered)
                self.assertIn("development regressions, not independent or held-out examples", rendered)
                evaluation = builder.evaluation_page(
                    name, meta, catalog, fixtures, summary,
                    json.loads((folder / "results/screening.json").read_text(encoding="utf-8")),
                    json.loads((folder / "results/recovery.json").read_text(encoding="utf-8")),
                )
                self.assertIn("Versioned refinement receipts", evaluation)
                self.assertIn("Preserved version-1 disagreements", evaluation)

    def test_versioned_evaluation_does_not_assume_one_challenge_per_pattern(self):
        name = "human-resources"
        folder = ROOT / name
        catalog = json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
        fixtures = json.loads((folder / "fixtures.json").read_text(encoding="utf-8"))
        summary = json.loads((folder / "results/summary.json").read_text(encoding="utf-8"))
        rendered = builder.evaluation_page(
            name,
            builder.load_meta(name),
            catalog,
            fixtures,
            summary,
            json.loads((folder / "results/screening.json").read_text(encoding="utf-8")),
            json.loads((folder / "results/recovery.json").read_text(encoding="utf-8")),
        )
        self.assertIn("The synthetic screen is small and targeted", rendered)
        self.assertNotIn("one small synthetic challenge per pattern", rendered)
        self.assertIn("Current answers below the recorded review threshold", rendered)
        index = builder.index_page(
            name, builder.load_meta(name), catalog, fixtures, summary, builder.all_titles()
        )
        self.assertIn("HR06 remains provisional", index)


if __name__ == "__main__":
    unittest.main()
