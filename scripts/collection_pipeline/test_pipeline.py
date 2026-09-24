"""Offline tests for the collection pipeline; no network or Jev calls."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WORK = Path(tempfile.mkdtemp(prefix="pipeline-test-"))
os.environ["JEV_PATTERNS_WORKDIR"] = str(WORK)
sys.path.insert(0, str(HERE))
import check_authoring  # noqa: E402
import overlap_check  # noqa: E402
import source_support  # noqa: E402


class WindowTests(unittest.TestCase):
    def test_window_prefers_distinct_non_title_keywords(self):
        filler = "Project management overview. " * 400
        target = "The register lists each risk with an owner, a trigger condition, and a mitigation step."
        text = filler + target + " " + filler
        summary = "Describes risk registers that record an owner, trigger, and mitigation for each entry."
        excerpt = source_support.window(text, summary, title="Wikipedia: Project management", size=600)
        self.assertIn("mitigation", excerpt)

    def test_short_text_returned_whole(self):
        self.assertEqual(source_support.window("short page", "any summary", "t"), "short page")


class OverlapQuestionTests(unittest.TestCase):
    def test_question_names_both_options_and_keeps_unknown(self):
        q = overlap_check.question("XX01", "alpha", "beta")
        self.assertIn("`contracts.XX01.options.alpha`", q["instructions"])
        self.assertIn("`contracts.XX01.options.beta`", q["instructions"])
        self.assertEqual(set(q["criteria"]), {"disjoint", "overlapping", "unknown"})


class AuthoringCheckTests(unittest.TestCase):
    """The electrical collection, with its design split and module staged in the work directory."""

    @classmethod
    def setUpClass(cls):
        fixtures = json.loads((REPO / "electrical/fixtures.json").read_text())
        (WORK / "design_electrical.json").write_text(json.dumps([f for f in fixtures if f["split"] == "design"]))
        shutil.copy(REPO / "skills/jev-question-kernel-catalog/references/electrical.md", WORK / "module_electrical.md")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(WORK, ignore_errors=True)

    def test_exemplar_passes_at_its_own_version(self):
        import io
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            code = check_authoring.main("electrical", expected_version="2.5.0")
        report = json.loads(out.getvalue())
        self.assertEqual(report["problems"], [])
        self.assertEqual(code, 0)

    def test_version_mismatch_reported(self):
        import io
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            check_authoring.main("electrical", expected_version="9.9.9")
        self.assertIn("kernel_skill_version must be 9.9.9", json.loads(out.getvalue())["problems"])


if __name__ == "__main__":
    unittest.main()
