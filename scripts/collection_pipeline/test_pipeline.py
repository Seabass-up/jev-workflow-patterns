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


import finish_collection  # noqa: E402
import screen  # noqa: E402

QUESTION = {"decision": {"type": "choice", "instructions": "Pick.", "criteria": {"a": "A", "b": "B", "unknown": "U"}}}


def answer(choice, ok=True):
    if not ok:
        return {"ok": False, "advisory_only": True, "error": "deadline_exceeded"}
    return {"ok": True, "advisory_only": True, "model": "jev-1.13.0",
            "answers": {"decision": {"type": "choice", "choice": choice, "confidence": 1.0,
                                     "probabilities": {"a": 1.0 if choice == "a" else 0.0,
                                                       "b": 1.0 if choice == "b" else 0.0, "unknown": 0.0}}}}


def make_collection(n_fixtures):
    root = Path(tempfile.mkdtemp(prefix="collection-test-"))
    (root / "catalog.json").write_text(json.dumps({"patterns": [{"id": "ZZ01", "version": 1, "questions": QUESTION}]}))
    fixtures = [{"id": "ZZ01-%d" % i, "pattern_id": "ZZ01", "version": 1, "state": {"text": "case %d" % i},
                 "expected": "a"} for i in range(1, n_fixtures + 1)]
    (root / "fixtures.json").write_text(json.dumps(fixtures))
    (root / "results").mkdir()
    return root, fixtures


class Caller:
    def __init__(self, response, fail_after=None):
        self.response, self.fail_after, self.calls = response, fail_after, 0

    def __call__(self, state, questions):
        self.calls += 1
        if self.fail_after is not None and self.calls > self.fail_after:
            raise KeyboardInterrupt("simulated interruption")
        return self.response


class ScreenAppendOnlyTests(unittest.TestCase):
    def test_rerun_never_replaces_a_stored_receipt(self):
        root, fixtures = make_collection(2)
        original = {"fixture_id": "ZZ01-1", "pattern_id": "ZZ01", "version": 1,
                    "request": {"state": fixtures[0]["state"], "questions": QUESTION, "model": "jev-1.13.0"},
                    "response": answer("b")}
        (root / "results/screening.json").write_text(json.dumps([original]))
        caller = Caller(answer("a"))
        self.assertEqual(screen.screen("zz", "initial", root=root, caller=caller), 1)
        stored = json.loads((root / "results/screening.json").read_text())
        self.assertEqual(stored[0], original)
        self.assertEqual([r["fixture_id"] for r in stored], ["ZZ01-1", "ZZ01-2"])
        self.assertEqual(screen.screen("zz", "initial", root=root, caller=caller), 0)
        self.assertEqual(caller.calls, 1)
        self.assertEqual(json.loads((root / "results/screening.json").read_text()), stored)

    def test_interrupted_batch_keeps_completed_calls(self):
        root, _ = make_collection(3)
        with self.assertRaises(KeyboardInterrupt):
            screen.screen("zz", "initial", root=root, caller=Caller(answer("a"), fail_after=1))
        self.assertEqual(len(json.loads((root / "results/screening.json").read_text())), 1)

    def test_changed_fixture_stops_the_run(self):
        root, fixtures = make_collection(1)
        screen.screen("zz", "initial", root=root, caller=Caller(answer("a")))
        fixtures[0]["state"] = {"text": "edited after screening"}
        (root / "fixtures.json").write_text(json.dumps(fixtures))
        with self.assertRaises(SystemExit):
            screen.screen("zz", "initial", root=root, caller=Caller(answer("a")))

    def test_recovery_screens_each_failure_once(self):
        root, _ = make_collection(2)
        screen.screen("zz", "initial", root=root, caller=Caller(answer("a", ok=False)))
        caller = Caller(answer("a"))
        self.assertEqual(screen.screen("zz", "recovery", root=root, caller=caller), 2)
        self.assertEqual(screen.screen("zz", "recovery", root=root, caller=caller), 0)

    def test_fixtures_frozen_once_screened(self):
        root, fixtures = make_collection(1)
        self.assertIsNone(finish_collection.frozen_fixture_problem(root, fixtures))
        screen.screen("zz", "initial", root=root, caller=Caller(answer("a")))
        self.assertIsNone(finish_collection.frozen_fixture_problem(root, fixtures))
        relabeled = [dict(fixtures[0], expected="b")]
        self.assertIsNotNone(finish_collection.frozen_fixture_problem(root, relabeled))


class SourceDriftTests(unittest.TestCase):
    RAW = source_support.RAW_BYTES
    TEXT = source_support.DISPLAYED_TEXT

    def test_drift_needs_matching_representations(self):
        self.assertIs(source_support.drift_status("aa", self.TEXT, "bb", self.TEXT), True)
        self.assertIs(source_support.drift_status("aa", self.TEXT, "aa", self.TEXT), False)
        self.assertIsNone(source_support.drift_status("aa", self.RAW, "aa", self.TEXT))
        self.assertIsNone(source_support.drift_status("aa", self.RAW, None, self.RAW))

    def test_recorded_representation_follows_fetch_method(self):
        browser = {"fetch_method": "Read in the built-in browser; sha256 is of the page's main text as displayed."}
        self.assertEqual(source_support.recorded_representation(browser), self.TEXT)
        self.assertEqual(source_support.recorded_representation({}), self.RAW)

    def run_review(self, sources, browser_pages, fetcher=None, run_id=None, root=None):
        root = root or Path(tempfile.mkdtemp(prefix="review-test-"))
        (root / "results").mkdir(exist_ok=True)
        (root / "sources.json").write_text(json.dumps(sources))
        asker = lambda state: {"ok": True, "model": "jev-1.13.0",
                               "answers": {"support": {"choice": "supported_as_written", "confidence": 0.9}}}
        source_support.run("zz", browser_pages, run_id=run_id, asker=asker, fetcher=fetcher, root=root)
        name = "source-review-%s.json" % run_id if run_id else "source-review.json"
        return root, json.loads((root / "results" / name).read_text())["receipts"]

    def test_browser_read_with_different_hash_is_reported_changed(self):
        source = {"id": "S1", "title": "T", "url": "https://page.example/", "sha256": "a" * 64, "summary": "s",
                  "fetch_method": "Read in the browser; hash of the text as displayed."}
        pages = {"https://page.example/": {"excerpt": "text", "sha256_of_text": "b" * 64}}
        _, receipts = self.run_review([source], pages)
        self.assertIs(receipts[0]["page_changed_since_record"], True)

    def test_browser_read_against_raw_byte_record_is_unknown(self):
        source = {"id": "S1", "title": "T", "url": "https://page.example/", "sha256": "a" * 64, "summary": "s"}
        pages = {"https://page.example/": {"excerpt": "text", "sha256_of_text": "a" * 64}}
        _, receipts = self.run_review([source], pages)
        self.assertIsNone(receipts[0]["page_changed_since_record"])

    def test_failed_fetch_is_unknown_and_reviews_are_immutable(self):
        source = {"id": "S1", "title": "T", "url": "https://page.example/", "sha256": "a" * 64, "summary": "s"}
        root, receipts = self.run_review([source], {}, fetcher=lambda url: ("403", b"blocked"))
        self.assertIsNone(receipts[0]["page_changed_since_record"])
        with self.assertRaises(SystemExit):
            source_support.run("zz", {}, fetcher=lambda url: ("403", b""), root=root)
        _, second = self.run_review([source], {}, fetcher=lambda url: ("403", b""), run_id="rerun", root=root)
        self.assertEqual(len(second), 1)
        self.assertTrue((root / "results/source-review.json").exists())


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
