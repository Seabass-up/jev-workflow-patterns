"""Offline drift, status, path and packaging regression tests for the import."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_research_import as research


class ResearchImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.bundle = Path(self.temp.name) / "bundle"
        shutil.copytree(research.DEFAULT_BUNDLE, self.bundle)
        self.manifest_path = self.bundle / "manifest.json"
        self.manifest = json.loads(self.manifest_path.read_text())

    def save_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest))

    def reject(self, message):
        with self.assertRaisesRegex(ValueError, message):
            research.load_bundle(self.bundle)

    def test_exact_ten_and_unchanged_mixed_contract(self):
        manifest, contracts = research.load_bundle(self.bundle)
        self.assertEqual(set(contracts), set(research.VERSIONS))
        self.assertEqual(len(manifest["excluded"]), 4)
        self.assertEqual(contracts["JP-011"]["version"], 2)
        self.assertEqual({q["type"] for q in contracts["JP-011"]["request"]["questions"].values()}, {"choice", "score"})
        self.assertNotIn("state", contracts["JP-013"]["request"])

    def test_held_pending_and_unknown_cannot_be_loaded(self):
        for key in (*research.EXCLUDED, "JP-017", "JP-999"):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "Not in this admitted snapshot"):
                research.load_contract(key, self.bundle)

    def test_contract_wording_change_is_detected(self):
        path = self.bundle / self.manifest["patterns"][0]["contract"]
        path.write_text(path.read_text().replace("explicit acceptance", "implied acceptance"))
        self.reject("hash mismatch")

    def test_missing_contract_is_rejected(self):
        (self.bundle / self.manifest["patterns"][0]["contract"]).unlink()
        self.reject("Missing regular file")

    def test_unregistered_contract_is_rejected(self):
        (self.bundle / "contracts/JP-017.v1.json").write_text("{}")
        self.reject("Unregistered")

    def test_duplicate_admission_is_rejected(self):
        self.manifest["patterns"].append(self.manifest["patterns"][0])
        self.save_manifest()
        self.reject("Duplicate admissions ID")

    def test_held_entry_cannot_replace_admission(self):
        self.manifest["patterns"][0]["id"] = "JP-001"
        self.save_manifest()
        self.reject("ID coverage")

    def test_pending_addition_cannot_be_promoted(self):
        self.manifest["working_additions"][0]["included"] = True
        self.save_manifest()
        self.reject("silently promoted")

    def test_qualification_claim_cannot_be_promoted(self):
        self.manifest["production_qualified"] = True
        self.save_manifest()
        self.reject("Unwarranted import claim")

    def test_old_jp011_version_is_rejected(self):
        next(row for row in self.manifest["patterns"] if row["id"] == "JP-011")["version"] = 1
        self.save_manifest()
        self.reject("Version changed")

    def test_discovery_routes_cannot_be_counted_as_domain_validation(self):
        self.manifest["coverage_at_checkpoint"]["individual_domain_validation"] = 22
        self.save_manifest()
        self.reject("discovery/domain distinction")

    def test_historical_transfer_counts_cannot_silently_change(self):
        self.manifest["jp002_public_transfer"]["public_previews"] = 6
        self.save_manifest()
        self.reject("Historical transfer summary")

    def test_path_traversal_is_rejected(self):
        self.manifest["source"]["files"]["../outside"] = "a" * 64
        self.save_manifest()
        self.reject("normalized relative path")

    def test_contract_symlink_is_rejected_even_when_content_matches(self):
        path = self.bundle / self.manifest["patterns"][0]["contract"]
        original = Path(self.temp.name) / "original.json"
        path.rename(original)
        path.symlink_to(original)
        self.reject("Symlink")

    def test_duplicate_json_key_is_rejected(self):
        self.manifest_path.write_text('{"schema_version": 1, "schema_version": 1}')
        self.reject("Duplicate JSON key")

    def test_nonfinite_json_is_rejected(self):
        self.manifest_path.write_text('{"schema_version": NaN}')
        self.reject("Non-finite")

    def test_source_verification_rejects_wrong_object_bytes(self):
        wrong = subprocess.CompletedProcess([], 0, stdout=b"wrong", stderr=b"")
        with patch.object(research.subprocess, "run", return_value=wrong):
            with self.assertRaisesRegex(ValueError, "Pinned source hash mismatch"):
                research.load_bundle(self.bundle, source_root=self.temp.name)

    def test_show_is_read_only_and_rejects_pending_pattern(self):
        result = subprocess.run([sys.executable, research.__file__, "--bundle", str(self.bundle),
                                 "--show", "JP-017"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Not in this admitted snapshot", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
