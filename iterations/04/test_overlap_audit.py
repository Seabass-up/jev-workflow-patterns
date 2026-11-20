import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import ROOT, canonical, replay, valid_answers


CATALOG = json.loads((ROOT / "catalog.json").read_text())
PATTERNS = {item["id"]: item for item in CATALOG["patterns"]}
AUDIT = json.loads((ROOT / "results/overlap-audit.json").read_text())


def check_request_receipt(batch):
    request, response = batch["request"], batch["response"]
    if not isinstance(request, dict) or not isinstance(response, dict):
        return False
    model, questions = request.get("model"), request.get("questions")
    if model != response.get("model") or response.get("ok") is not True or response.get("cached") is not False:
        return False
    digest = hashlib.sha256(canonical({"model": model, "state": request.get("state"), "questions": questions})).hexdigest()
    return response.get("request_sha256") == digest and valid_answers(questions, response)


class OverlapAuditTests(unittest.TestCase):
    def test_original_whole_contract_batches_are_request_bound(self):
        batches = AUDIT["whole_contract_review_v1"]
        self.assertEqual(len(batches), 3)
        self.assertTrue(all(check_request_receipt(batch) for batch in batches))
        self.assertEqual(sum(len(batch["response"]["answers"]) for batch in batches), 13)
        self.assertEqual(set(AUDIT["scope"]["label_overlap_not_applicable"]), {"B23", "B26", "H33"})
        for pattern_id in AUDIT["scope"]["label_overlap_not_applicable"]:
            self.assertFalse(any(question["type"] == "choice" for question in PATTERNS[pattern_id]["questions"].values()))

    def test_v1_pair_review_receipts_cover_original_pairs(self):
        batches = AUDIT["choice_pair_review_v1"]
        self.assertEqual(len(batches), 3)
        self.assertTrue(all(check_request_receipt(batch) for batch in batches))
        self.assertEqual(sum(len(batch["request"]["questions"]) for batch in batches), 64)

    def test_current_pair_review_covers_every_v2_label_pair(self):
        batches = AUDIT["choice_pair_review_v2"]
        target_ids = set(AUDIT["scope"]["choice_contracts_revised"])
        self.assertEqual({batch["pattern_id"] for batch in batches}, target_ids)
        self.assertTrue(all(check_request_receipt(batch) for batch in batches))
        total = 0
        for batch in batches:
            pattern = PATTERNS[batch["pattern_id"]]
            question = next(iter(pattern["questions"].values()))
            self.assertEqual(batch["request"]["state"]["question_contract"], question)
            labels = list(question["criteria"])
            expected_pairs = [[labels[i], labels[j]] for i in range(len(labels)) for j in range(i + 1, len(labels))]
            pairs = batch["pairs"]
            self.assertEqual(pairs, expected_pairs)
            total += len(pairs)
            for answer in batch["response"]["answers"].values():
                self.assertIn(answer["choice"], {"disjoint", "precedence_resolved"})
        self.assertEqual(total, 77)

    def test_superseded_l20_overlap_is_preserved_and_resolved(self):
        receipt = AUDIT["refinement_history"]["superseded_pair_receipt"]
        self.assertTrue(check_request_receipt(receipt))
        answers = receipt["response"]["answers"]
        unresolved = [
            (receipt["pairs"][int(key.split("_")[1])], answer["choice"])
            for key, answer in answers.items()
            if answer["choice"] == "overlap_unresolved"
        ]
        self.assertIn((["verbatim_source", "typed_value"], "overlap_unresolved"), unresolved)
        current = next(batch for batch in AUDIT["choice_pair_review_v2"] if batch["pattern_id"] == "L20")
        self.assertTrue(all(answer["choice"] != "overlap_unresolved" for answer in current["response"]["answers"].values()))

    def test_public_pattern_pages_mirror_current_question_json(self):
        for pattern_id in AUDIT["scope"]["choice_contracts_revised"]:
            with self.subTest(pattern=pattern_id):
                page = (ROOT / "patterns" / (pattern_id.lower() + ".md")).read_text()
                blocks = re.findall(r"~~~json\n(.*?)\n~~~", page, re.S)
                self.assertEqual(len(blocks), 1)
                self.assertEqual(json.loads(blocks[0]), PATTERNS[pattern_id]["questions"])
                self.assertIn("Contract version 2", page)

    def test_first_pass_misses_remain_and_current_screen_is_clean(self):
        result = replay()["screens"]
        self.assertEqual(result["overlap-v2-first-pass"]["fixture_matches"], 41)
        self.assertEqual(result["overlap-v2"]["fixture_matches"], 46)
        first = json.loads((ROOT / "results/overlap-v2-first-pass.json").read_text())
        misses = {row["fixture_id"] for row in first if not row["match"]}
        self.assertEqual(misses, {"B22-procurement", "B25-unclear", "E24-insufficient", "L21-ambiguous"})
        audit_usage = AUDIT["usage"]
        self.assertEqual(audit_usage["requests"], 17)
        self.assertEqual(result["overlap-v2"]["request_digests_verified"], 46)


if __name__ == "__main__":
    unittest.main()
