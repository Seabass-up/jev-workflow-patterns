"""Offline shadow replay of a typed Jev contract through trusted consumer code.

No provider call or business action occurs here. The adapter is Python code supplied
by the caller and is imported deliberately; run only an adapter you trust.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

from check_contract import missing_required_fields, require
from check_confidence import check_answer


def digest(request):
    payload = json.dumps(request, sort_keys=True, ensure_ascii=False,
                         allow_nan=False, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1


def validate_answer(question, answer, model):
    require(isinstance(answer, dict) and answer.get("type") == question["type"], "answer primitive mismatch")
    kind = question["type"]
    if kind == "noul":
        require(number(answer.get("noul")), "invalid Noul probability")
        return
    probabilities = answer.get("probabilities")
    require(isinstance(probabilities, dict) and all(number(v) for v in probabilities.values()),
            "invalid answer probabilities")
    require(number(answer.get("confidence")), "invalid answer confidence")
    require(math.isclose(sum(probabilities.values()), 1, abs_tol=0.03), "probabilities do not sum to one")
    if kind == "choice":
        labels = set(question["criteria"])
        require(set(probabilities) == labels and answer.get("choice") in labels, "Choice option mismatch")
        require(probabilities[answer["choice"]] >= max(probabilities.values()), "Choice is not a maximum")
        # The bundled approximation was measured on jev-1.13.0 receipts only.
        if model == "jev-1.13.0":
            require(check_answer(answer) is None, "Choice confidence inconsistent with probabilities")
    else:
        levels = question["criteria"]
        keys = {str(i) for i in range(len(levels))}
        require(set(probabilities) == keys, "Score level mismatch")
        score = answer.get("score")
        require(type(score) in (int, float) and math.isfinite(score) and 0 <= score <= len(levels) - 1,
                "invalid Score")
        expectation = sum(i * probabilities[str(i)] for i in range(len(levels)))
        require(math.isclose(score, expectation, abs_tol=0.05), "Score inconsistent with levels")
        legend = answer.get("legend")
        require(isinstance(legend, dict) and set(map(str, legend)) == keys, "Score legend mismatch")
        require(all(legend[str(i)] == levels[i] for i in range(len(levels))), "Score legend changed")


def validate_receipt(contract, pilot, case, receipt):
    require(isinstance(receipt, dict), "receipt missing")
    request = {"state": case["state"], "questions": contract["request"]["questions"], "model": pilot["model"]}
    response = receipt.get("response")
    require(isinstance(response, dict), "receipt response missing")
    require(receipt.get("request_sha256") == digest(request), "receipt digest not bound to case and contract")
    require(response.get("request_sha256") == digest(request), "request digest mismatch")
    require(type(response.get("ok")) is bool, "response status missing")
    if response["ok"] is False:
        require(not response.get("answers") and response.get("error"), "invalid provider failure")
        return None
    require(response.get("model") == pilot["model"], "response model mismatch")
    require(response.get("advisory_only") is True, "non-advisory response")
    for key in ("elapsed_ms", "estimated_cost_usd"):
        value = response.get(key)
        require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                "invalid provider-reported " + key)
    answers = response.get("answers")
    questions = request["questions"]
    require(isinstance(answers, dict) and set(answers) == set(questions), "answer coverage mismatch")
    for qid, question in questions.items():
        validate_answer(question, answers[qid], pilot["model"])
    return answers


def load_adapter(path):
    spec = importlib.util.spec_from_file_location("jev_qualification_consumer", path)
    require(spec is not None and spec.loader is not None, "cannot load consumer adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(callable(getattr(module, "decide", None)), "consumer adapter needs decide(state, answers)")
    return module.decide


def evaluate(contract, pilot, consumer):
    require(type(pilot.get("version")) is int and type(contract.get("version")) is int
            and pilot.get("contract_id") == contract.get("contract_id")
            and pilot["version"] == contract["version"],
            "pilot contract/version mismatch")
    require(isinstance(pilot.get("model"), str) and re.fullmatch(r"jev-\d+\.\d+\.\d+", pilot["model"]),
            "versioned Jev model required; aliases can move")
    review = pilot.get("review_disposition")
    require(isinstance(review, str) and review, "review disposition required")
    allowed = pilot.get("allowed_dispositions")
    require(isinstance(allowed, list) and allowed and all(isinstance(v, str) and v for v in allowed)
            and len(allowed) == len(set(allowed)) and review in allowed,
            "allowed_dispositions must be unique and include review")
    cases = pilot.get("cases")
    require(isinstance(cases, list) and cases, "pilot needs cases")
    require(all(isinstance(c, dict) for c in cases), "pilot cases must be objects")
    require(len({c.get("id") for c in cases}) == len(cases), "duplicate case ID")
    rows = []
    for case in cases:
        require(case.get("split") in ("synthetic_demo", "held_out"), "unknown case split")
        require(isinstance(case.get("state"), dict), "named state required")
        for key in ("id", "expected_disposition", "baseline_disposition"):
            require(isinstance(case.get(key), str) and case[key], "missing case " + key)
        require(case["expected_disposition"] in allowed and case["baseline_disposition"] in allowed,
                "case uses unknown disposition")
        missing = missing_required_fields(contract, case["state"])
        status, selected = "evaluated", review
        problem = None
        elapsed_ms = None
        estimated_cost_usd = None
        if missing:
            status = "preflight_missing"
            problem = "required state missing or empty: " + ", ".join(missing)
            if case.get("receipt") is not None:
                status = "preflight_bypassed"
        else:
            try:
                answers = validate_receipt(contract, pilot, case, case.get("receipt"))
                if answers is None:
                    status = "provider_failure"
                    problem = str(case["receipt"]["response"]["error"])
                else:
                    response = case["receipt"]["response"]
                    elapsed_ms = response["elapsed_ms"]
                    estimated_cost_usd = response["estimated_cost_usd"]
            except (ValueError, TypeError, KeyError, IndexError) as error:
                status = "invalid_receipt"
                problem = str(error)
                selected = review
            if status == "evaluated":
                try:
                    selected = consumer(case["state"], answers)
                    require(isinstance(selected, str) and selected, "consumer must return a disposition string")
                    require(selected in allowed, "consumer returned an unknown disposition")
                except Exception as error:
                    status = "consumer_error"
                    problem = type(error).__name__ + ": " + str(error)
                    selected = review
        rows.append({"id": case["id"], "split": case["split"], "status": status,
                     "selected": selected, "expected": case["expected_disposition"],
                     "baseline": case["baseline_disposition"], "match": selected == case["expected_disposition"],
                     "baseline_match": case["baseline_disposition"] == case["expected_disposition"],
                     "automatic_error": selected != review and selected != case["expected_disposition"],
                     "elapsed_ms": elapsed_ms, "estimated_cost_usd": estimated_cost_usd,
                     "problem": problem})
    held = [r for r in rows if r["split"] == "held_out"]
    measured = held or rows
    sample = {"cases": len(measured), "matched": sum(r["match"] for r in measured),
              "baseline_matched": sum(r["baseline_match"] for r in measured),
              "reviewed": sum(r["selected"] == review for r in measured),
              "automatic_errors": sum(r["automatic_error"] for r in measured),
              "preflight_bypassed": sum(r["status"] == "preflight_bypassed" for r in measured),
              "invalid_or_failed": sum(r["status"] in ("provider_failure", "invalid_receipt", "consumer_error")
                                       for r in measured),
              "reported_elapsed_ms_total": round(sum(r["elapsed_ms"] or 0 for r in measured), 3),
              "bridge_estimated_cost_usd_total": round(sum(r["estimated_cost_usd"] or 0 for r in measured), 10)}
    sample["review_fraction"] = round(sample["reviewed"] / sample["cases"], 4)
    dispositions = sorted({r["expected"] for r in measured} | {r["selected"] for r in measured})
    sample["by_disposition"] = {
        label: {"true_positive": sum(r["selected"] == label and r["expected"] == label for r in measured),
                "false_positive": sum(r["selected"] == label and r["expected"] != label for r in measured),
                "false_negative": sum(r["selected"] != label and r["expected"] == label for r in measured)}
        for label in dispositions
    }
    limits = pilot.get("sample_limits", {})
    require(isinstance(limits, dict), "sample_limits must be an object")
    if held:
        require(type(limits.get("min_held_out_cases")) is int and limits["min_held_out_cases"] > 0,
                "held-out sample needs a positive min_held_out_cases")
        require(type(limits.get("max_automatic_errors")) is int and limits["max_automatic_errors"] >= 0,
                "held-out sample needs max_automatic_errors")
        require(number(limits.get("max_review_fraction")), "held-out sample needs max_review_fraction")
        require(type(limits.get("min_match_gain_over_baseline")) is int,
                "held-out sample needs min_match_gain_over_baseline")
        sample["checks_met"] = (sample["cases"] >= limits["min_held_out_cases"]
                                and sample["matched"] - sample["baseline_matched"] >= limits["min_match_gain_over_baseline"]
                                and sample["automatic_errors"] <= limits["max_automatic_errors"]
                                and sample["reviewed"] / sample["cases"] <= limits["max_review_fraction"]
                                and sample["preflight_bypassed"] == 0 and sample["invalid_or_failed"] == 0)
    return {"contract_id": contract["contract_id"], "contract_version": contract["version"],
            "model": pilot["model"], "evidence_scope": "held_out_as_declared" if held else "synthetic_demo_only",
            "sample": sample, "cases": rows,
            "limits": "The split and independent labels are caller declarations, not verified here. This checks planned consumer dispositions; it does not execute actions, prove outcome delivery, or establish production accuracy."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("pilot", type=Path)
    parser.add_argument("adapter", type=Path, help="Trusted local Python file exporting decide(state, answers)")
    parser.add_argument("--require-sample-checks", action="store_true")
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text())
        pilot = json.loads(args.pilot.read_text())
        result = evaluate(contract, pilot, load_adapter(args.adapter))
        print(json.dumps(result, indent=2))
        if args.require_sample_checks and result["sample"].get("checks_met") is not True:
            return 1
        return 0
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(json.dumps({"evaluation": "failed", "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
