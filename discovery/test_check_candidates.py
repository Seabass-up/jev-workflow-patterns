import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_candidates import ROOT, prior_ids, validate  # noqa: E402


class CandidateRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "candidates.json").read_text())
        self.known = prior_ids()

    def check(self):
        return validate(self.registry, self.known)

    def rejects(self, message):
        with self.assertRaisesRegex(ValueError, message):
            self.check()

    def test_registry_is_valid(self):
        self.assertEqual(self.check()["next_id"], "C" + str(len(self.registry["candidates"]) + 1))

    def test_duplicate_id_rejected(self):
        self.registry["candidates"].append(copy.deepcopy(self.registry["candidates"][0]))
        self.registry["candidates"][-1]["title"] = "A different title"
        self.rejects("unique and ascending")

    def test_renamed_title_duplicate_rejected(self):
        extra = copy.deepcopy(self.registry["candidates"][0])
        extra["id"] = "C99"
        extra["title"] = extra["title"].upper()
        self.registry["candidates"].append(extra)
        self.rejects("repeats a title")

    def test_unknown_prior_rejected(self):
        self.registry["candidates"][0]["nearest_prior"] = ["Z99"]
        self.rejects("unknown prior")

    def test_missing_evidence_path_rejected(self):
        self.registry["candidates"][0]["evidence"] = ["discovery/missing-receipt.json"]
        self.rejects("evidence path missing")

    def test_closed_status_needs_resolution(self):
        self.registry["candidates"][0]["status"] = "rejected"
        self.rejects("resolution")
        self.registry["candidates"][0]["resolution"] = "Duplicate of H32."
        self.check()

    def test_open_status_must_not_claim_resolution(self):
        self.registry["candidates"][0]["resolution"] = "Promoted early."
        self.rejects("resolution")

    def test_private_material_tripwires(self):
        for value in ("Reply to ops@example.com first", "Account 4334111056416644 was late",
                      "Uses sk-ABCDEFGHIJKLMNOP to call"):
            registry = copy.deepcopy(self.registry)
            registry["candidates"][0]["mechanism"] = value
            with self.assertRaises(ValueError):
                validate(registry, self.known)
        self.registry["candidates"][0]["found"]["context"] = "Found in ops@example.com thread"
        self.rejects("context contains")

    def test_private_material_in_evidence_rejected(self):
        for value in ("Thread from ops@example.com", "token_ABCDEFGHIJKLMNOP"):
            registry = copy.deepcopy(self.registry)
            registry["candidates"][0]["evidence"] = [value]
            with self.assertRaisesRegex(ValueError, "evidence contains"):
                validate(registry, self.known)


if __name__ == "__main__":
    unittest.main()
