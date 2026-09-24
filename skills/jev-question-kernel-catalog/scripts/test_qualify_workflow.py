"""Offline tests for the shadow qualification replay; no provider or action calls."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

from check_contract import missing_required_fields
from qualify_workflow import evaluate


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CONTRACT = json.loads((ASSETS / "mixed-contract-example.json").read_text())
PILOT = json.loads((ASSETS / "mixed-pilot-example.json").read_text())
SPEC = importlib.util.spec_from_file_location("demo_consumer", ASSETS / "mixed-consumer-example.py")
CONSUMER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONSUMER)


class QualificationTests(unittest.TestCase):
    def test_demo_replays_but_cannot_claim_held_out_qualification(self):
        result = evaluate(CONTRACT, PILOT, CONSUMER.decide)
        self.assertEqual(result["evidence_scope"], "synthetic_demo_only")
        self.assertNotIn("checks_met", result["sample"])
        self.assertEqual(result["sample"]["matched"], 4)
        self.assertEqual(result["sample"]["automatic_errors"], 0)
        self.assertEqual(result["sample"]["review_fraction"], 0.5)
        self.assertEqual(result["sample"]["by_disposition"]["billing_review"]["true_positive"], 1)
        self.assertEqual(result["cases"][-1]["status"], "preflight_missing")

    def test_empty_and_blank_required_fields_are_code_owned(self):
        self.assertEqual(missing_required_fields(CONTRACT, {"message": "  "}), ["message"])
        self.assertEqual(missing_required_fields(CONTRACT, {}), ["message"])
        self.assertEqual(missing_required_fields(CONTRACT, {"message": "hello"}), [])

    def test_tampered_request_binding_fails_closed(self):
        pilot = copy.deepcopy(PILOT)
        pilot["cases"][0]["state"]["message"] = "changed after inference"
        result = evaluate(CONTRACT, pilot, CONSUMER.decide)
        self.assertEqual(result["cases"][0]["status"], "invalid_receipt")
        self.assertEqual(result["cases"][0]["selected"], "human_review")
        self.assertIn("digest", result["cases"][0]["problem"])

    def test_wrong_answer_type_and_score_inconsistency_fail_closed(self):
        pilot = copy.deepcopy(PILOT)
        pilot["cases"][0]["receipt"]["response"]["answers"]["refund_requested"]["type"] = "choice"
        pilot["cases"][1]["receipt"]["response"]["answers"]["urgency"]["score"] = 2
        result = evaluate(CONTRACT, pilot, CONSUMER.decide)
        self.assertEqual([r["status"] for r in result["cases"][:2]], ["invalid_receipt", "invalid_receipt"])
        self.assertEqual(result["sample"]["invalid_or_failed"], 2)

    def test_provider_failure_and_adapter_exception_route_to_review(self):
        pilot = copy.deepcopy(PILOT)
        failure = pilot["cases"][0]["receipt"]["response"]
        failure["ok"] = False
        failure["error"] = "temporary_unavailable"
        failure.pop("answers")

        def broken_consumer(_state, _answers):
            raise RuntimeError("simulated consumer fault")

        result = evaluate(CONTRACT, pilot, broken_consumer)
        self.assertEqual(result["cases"][0]["status"], "provider_failure")
        self.assertEqual(result["cases"][1]["status"], "consumer_error")
        self.assertEqual(result["sample"]["invalid_or_failed"], 3)

    def test_held_out_sample_limits_do_not_hide_errors(self):
        pilot = copy.deepcopy(PILOT)
        for case in pilot["cases"]:
            case["split"] = "held_out"
        pilot["sample_limits"] = {"min_held_out_cases": 4, "max_automatic_errors": 0,
                                  "max_review_fraction": 0.5, "min_match_gain_over_baseline": 0}
        passed = evaluate(CONTRACT, pilot, CONSUMER.decide)
        self.assertTrue(passed["sample"]["checks_met"])
        pilot["cases"][0]["expected_disposition"] = "receipt_queue"
        failed = evaluate(CONTRACT, pilot, CONSUMER.decide)
        self.assertFalse(failed["sample"]["checks_met"])
        self.assertEqual(failed["sample"]["automatic_errors"], 1)

    def test_held_out_gate_requires_declared_minimum_and_baseline_gain(self):
        pilot = copy.deepcopy(PILOT)
        for case in pilot["cases"]:
            case["split"] = "held_out"
        pilot["sample_limits"] = {"min_held_out_cases": 5, "max_automatic_errors": 0,
                                  "max_review_fraction": 0.5, "min_match_gain_over_baseline": 0}
        self.assertFalse(evaluate(CONTRACT, pilot, CONSUMER.decide)["sample"]["checks_met"])
        pilot["sample_limits"]["min_held_out_cases"] = 4
        pilot["sample_limits"]["min_match_gain_over_baseline"] = 4
        self.assertFalse(evaluate(CONTRACT, pilot, CONSUMER.decide)["sample"]["checks_met"])

    def test_previewed_real_cases_cannot_claim_held_out(self):
        pilot = copy.deepcopy(PILOT)
        for case in pilot["cases"]:
            case["split"] = "development_screen"
        result = evaluate(CONTRACT, pilot, CONSUMER.decide)
        self.assertEqual(result["evidence_scope"], "development_screen_only")
        self.assertNotIn("checks_met", result["sample"])

    def test_preflight_bypass_is_not_treated_as_a_valid_model_result(self):
        pilot = copy.deepcopy(PILOT)
        pilot["cases"][-1]["receipt"] = copy.deepcopy(pilot["cases"][0]["receipt"])
        result = evaluate(CONTRACT, pilot, CONSUMER.decide)
        self.assertEqual(result["cases"][-1]["status"], "preflight_bypassed")
        self.assertEqual(result["sample"]["preflight_bypassed"], 1)

    def test_floating_model_alias_is_rejected(self):
        pilot = copy.deepcopy(PILOT)
        pilot["model"] = "jev-latest"
        with self.assertRaisesRegex(ValueError, "aliases can move"):
            evaluate(CONTRACT, pilot, CONSUMER.decide)

    def test_consumer_cannot_return_an_unlisted_disposition(self):
        result = evaluate(CONTRACT, PILOT, lambda _state, _answers: "send_refund")
        self.assertEqual(result["cases"][0]["status"], "consumer_error")
        self.assertEqual(result["cases"][0]["selected"], "human_review")
        self.assertIn("unknown disposition", result["cases"][0]["problem"])


if __name__ == "__main__":
    unittest.main()
