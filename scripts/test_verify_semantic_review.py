import copy
from pathlib import Path
import unittest

from verify_semantic_review import ROOT, validate_answer, verify, verify_boundaries


class SemanticReviewTests(unittest.TestCase):
    def test_all_current_contracts_and_receipts_bind(self):
        result = verify(ROOT / "reviews/2026-09-26")
        self.assertEqual(result["profiles"], 390)
        self.assertEqual(result["batches"], 113)

    def test_live_boundary_receipts_bind_and_match(self):
        rows = verify_boundaries(ROOT / "reviews/2026-09-26")
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(r["match"] for r in rows))

    def test_wave02_and_versioned_screen_are_explicit(self):
        rows = verify_boundaries(ROOT / "reviews/2026-09-26", wave="02")
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r["match"] for r in rows))
        result = verify(ROOT / "reviews/2026-09-26")
        h18 = next(r for r in result["patterns"] if r["key"] == "iterations/02/H18")
        self.assertFalse(h18["current_contract_match"])
        self.assertNotEqual(h18["pattern_sha256"], h18["screened_pattern_sha256"])

    def test_malformed_screen_answers_rejected(self):
        q = {"criteria": {"a": "A", "b": "B"}}
        good = {"type": "choice", "choice": "a", "confidence": 1,
                "probabilities": {"a": 1, "b": 0}}
        validate_answer(q, good)
        for key, value in (("choice", []), ("choice", "b"), ("confidence", True),
                           ("confidence", float("nan")), ("probabilities", {}),
                           ("probabilities", {"a": .3, "b": .3})):
            with self.subTest(field=key, value=value):
                bad = copy.deepcopy(good)
                bad[key] = value
                with self.assertRaises(ValueError):
                    validate_answer(q, bad)


if __name__ == "__main__":
    unittest.main()
