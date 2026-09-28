"""Offline packaging and explicit-selection regressions; no model-quality claim."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_research_import as previous
import check_research_working_import as working


class WorkingImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.bundle = Path(self.tmp.name) / "bundle"
        shutil.copytree(working.DEFAULT_BUNDLE, self.bundle)

    def test_exact_inventory_and_historical_bundle_unchanged(self):
        manifest, assets = working.inspect_bundle(self.bundle)
        old, _ = previous.load_bundle()
        self.assertEqual(len(manifest["patterns"]), 19)
        self.assertEqual(len(manifest["compositions"]), 1)
        self.assertEqual(len(old["patterns"]), 10)
        self.assertFalse(set(working.VERSIONS) & set(previous.VERSIONS))
        self.assertEqual(manifest["audit_counts"]["unassessed_pairs"], 252)
        self.assertEqual(assets["inventory.json"]["requalified_from_held"]["historical_held_versions"], [2, 3])

    def test_all_nineteen_load_only_as_marked_research(self):
        for pid, version in working.VERSIONS.items():
            with self.subTest(pid=pid):
                result = working.load_contract(f"{pid}@{version}", allow_audit_pending=True, bundle=self.bundle)
                self.assertEqual(result["contract"]["version"], version)
                self.assertEqual(result["audit_status"], "AUDIT_PENDING")
                self.assertFalse(result["production_qualified"])
                self.assertEqual(result["source_admission"]["status"], "ACCEPTED_RESEARCH")
                self.assertEqual(result["action"], "none")
                self.assertEqual(result["provider_calls"], 0)

    def test_pending_acknowledgement_must_be_literal_true(self):
        for value in (False, None, 1, "true"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "Explicit"):
                working.load_contract("JP-001@4", allow_audit_pending=value, bundle=self.bundle)

    def test_bare_ids_held_versions_unknown_and_old_bundle_ids_refused(self):
        for selector in ("JP-001", "JP-001@1", "JP-001@2", "JP-001@3", "JP-001@04",
                         "JP-017", "JP-023@1", "JP-046@2", "JP-006@1", "JP-002@1", "CA03@1", None):
            with self.subTest(selector=selector), self.assertRaisesRegex(ValueError, "exact selectable"):
                working.load_contract(selector, allow_audit_pending=True, bundle=self.bundle)

    def test_composition_is_not_a_twentieth_primitive(self):
        result = working.load_contract("AP-C01@1", allow_audit_pending=True,
                                       composition=True, bundle=self.bundle)
        self.assertEqual(result["kind"], "composition_not_new_primitive")
        self.assertEqual(result["contract"]["component_contracts"], ["JP-025@1", "JP-023@2"])
        with self.assertRaises(ValueError):
            working.load_contract("AP-C01@1", allow_audit_pending=True, bundle=self.bundle)
        with self.assertRaises(ValueError):
            working.load_contract("JP-025@1", composition=True, allow_audit_pending=True, bundle=self.bundle)

    def test_original_candidate_status_and_distinct_title_preserved(self):
        result = working.load_contract("JP-017@1", allow_audit_pending=True, bundle=self.bundle)
        self.assertEqual(result["contract"]["status"], "CANDIDATE")
        self.assertNotEqual(result["contract"]["title"], result["source_admission"]["title"])
        self.assertEqual(working.question_for(result["contract"])["type"], "choice")

    def test_thresholds_preserved_per_contract(self):
        _, assets = working.inspect_bundle(self.bundle)
        self.assertEqual(assets["contracts/JP-027.v1.json"]["minimum_top_probability"], .8)
        self.assertEqual(assets["contracts/JP-028.v1.json"]["minimum_top_probability"], .8)
        self.assertEqual(assets["contracts/JP-001.v4.json"]["minimum_top_probability"], .85)
        self.assertEqual(assets["contracts/JP-017.v1.json"]["follow_up"]["maximum_calls"], 0)

    def test_any_contract_byte_change_refused(self):
        path = self.bundle / "contracts/JP-001.v4.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            working.inspect_bundle(self.bundle)

    def test_receipt_or_status_promotion_refused(self):
        path = self.bundle / "admissions.json"
        path.write_text(path.read_text().replace('"PENDING"', '"COMPLETE"'))
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            working.inspect_bundle(self.bundle)

    def test_manifest_cannot_rehash_its_own_changes(self):
        path = self.bundle / "manifest.json"
        manifest = json.loads(path.read_text())
        for mutation in (lambda d: d.update(production_qualified=True),
                         lambda d: d["patterns"][0].update(audit_status="AUDITED"),
                         lambda d: d["patterns"].append(copy.deepcopy(d["patterns"][0])),
                         lambda d: d["source"].update(commit="f" * 40),
                         lambda d: d["bundled_files"].update({"../outside": "0" * 64})):
            changed = copy.deepcopy(manifest)
            mutation(changed)
            path.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, "Frozen manifest changed"):
                working.inspect_bundle(self.bundle)

    def test_duplicate_and_nonfinite_json_refused(self):
        path = self.bundle / "manifest.json"
        for payload in ('{"a":1,"a":2}', '{"x":NaN}'):
            path.write_text(payload)
            with self.assertRaises(ValueError):
                working.inspect_bundle(self.bundle)

    def test_unregistered_file_refused(self):
        (self.bundle / "contracts/JP-001.v3.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Unregistered"):
            working.inspect_bundle(self.bundle)

    def test_missing_and_symlinked_files_refused(self):
        path = self.bundle / "contracts/JP-001.v4.json"
        path.unlink()
        with self.assertRaisesRegex(ValueError, "Missing regular file"):
            working.inspect_bundle(self.bundle)
        path.symlink_to(working.DEFAULT_BUNDLE / "contracts/JP-001.v4.json")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            working.inspect_bundle(self.bundle)

    def test_git_check_uses_pinned_commit_and_rejects_mismatch(self):
        manifest, _ = working.inspect_bundle(self.bundle)
        called = []
        def run(argv, **kwargs):
            called.append(argv)
            return subprocess.CompletedProcess(argv, 0, b"unexpected bytes", b"")
        with patch.object(working.subprocess, "run", side_effect=run):
            with self.assertRaisesRegex(ValueError, "Pinned source hash mismatch"):
                working.verify_source(manifest, self.bundle)
        self.assertTrue(called[0][2].startswith(working.SOURCE_COMMIT + ":"))
        self.assertEqual(called[0][:2], ["git", "show"])

    def test_missing_source_commit_refused(self):
        manifest, _ = working.inspect_bundle(self.bundle)
        with patch.object(working.subprocess, "run", return_value=subprocess.CompletedProcess([], 128, b"", b"")):
            with self.assertRaisesRegex(ValueError, "Cannot read pinned source object"):
                working.verify_source(manifest, self.bundle)

    def test_cli_default_is_metadata_only_and_selection_requires_opt_in(self):
        script = Path(working.__file__)
        base = [sys.executable, str(script), "--bundle", str(self.bundle)]
        result = subprocess.run(base, text=True, capture_output=True, check=True)
        self.assertNotIn("contract", json.loads(result.stdout))
        refused = subprocess.run(base + ["--show", "JP-001@4"], text=True, capture_output=True)
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(refused.stdout, "")
        self.assertIn("Explicit", refused.stderr)
        shown = subprocess.run(base + ["--show", "JP-001@4", "--allow-audit-pending"],
                               text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(shown.stdout)["audit_status"], "AUDIT_PENDING")


if __name__ == "__main__":
    unittest.main()
