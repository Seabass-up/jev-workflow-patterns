"""Offline receipt-validation tests for the shared pattern collection replay."""
import unittest

from collection_tools import digest, validate_receipt


def receipt_fixture(option_count, probabilities):
    labels = ["option-%d" % index for index in range(option_count)]
    question = {"type": "choice", "instructions": "Choose the supported option.",
                "criteria": {label: label for label in labels}}
    pattern = {"id": "TST01", "version": 1, "questions": {"decision": question}}
    fixture = {"id": "TST01-1", "pattern_id": "TST01", "version": 1,
               "expected": labels[0], "state": {"text": "synthetic test"}}
    request = {"state": fixture["state"], "questions": pattern["questions"],
               "model": "jev-1.13.0"}
    answer = {"type": "choice", "choice": labels[0], "confidence": 0.05555555555555555,
              "probabilities": dict(zip(labels, probabilities))}
    response = {"ok": True, "advisory_only": True, "model": request["model"],
                "request_sha256": digest(request), "answers": {"decision": answer}}
    receipt = {"version": 1, "fixture_id": fixture["id"], "pattern_id": pattern["id"],
               "request": request, "response": response}
    return receipt, fixture, pattern


class CollectionReceiptTests(unittest.TestCase):
    def test_rounding_bound_accepts_ten_option_two_decimal_sum(self):
        values = [0.15] + [0.10] * 9
        receipt, fixture, pattern = receipt_fixture(10, values)
        self.assertTrue(validate_receipt(receipt, fixture, pattern))

    def test_rounding_bound_rejects_two_option_sum_outside_rounding_error(self):
        receipt, fixture, pattern = receipt_fixture(2, [0.50, 0.48])
        with self.assertRaisesRegex(ValueError, "probabilities do not sum"):
            validate_receipt(receipt, fixture, pattern)


if __name__ == "__main__":
    unittest.main()
