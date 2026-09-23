"""Offline Choice-confidence consistency checks; no network, inference, or accuracy claim.

For a Choice with n options, published TypeSafe confidence closely follows
(n * max_probability - 1) / (n - 1). The formula comes from the confidence
page's approximation and was fitted to 447 stored jev-1.13.0 answers (n = 2-6,
maximum difference 0.020 at two-decimal rounding). Treat it as an observed
contract to recheck after model or API changes, not as the provider's definition.
Score confidence is ordinal-aware and has no published formula; it is only counted.
"""
import json
import math
from pathlib import Path
import sys

DEFAULT_TOLERANCE = 0.03


def finite_probability(value):
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1


def choice_confidence(probabilities):
    """Expected confidence from a Choice probability mapping or sequence."""
    values = list(probabilities.values()) if isinstance(probabilities, dict) else list(probabilities)
    if len(values) < 2 or not all(finite_probability(v) for v in values):
        raise ValueError("need at least two finite probabilities in [0, 1]")
    n = len(values)
    return min(1.0, max(0.0, (n * max(values) - 1) / (n - 1)))


def required_top_probability(confidence_threshold, option_count):
    """Top probability a Choice needs to reach a confidence threshold with n options."""
    if not finite_probability(confidence_threshold) or type(option_count) is not int or option_count < 2:
        raise ValueError("need a threshold in [0, 1] and at least two options")
    return (confidence_threshold * (option_count - 1) + 1) / option_count


def check_answer(answer, tolerance=DEFAULT_TOLERANCE):
    """Return None when consistent, otherwise a problem description."""
    probabilities = answer.get("probabilities")
    confidence = answer.get("confidence")
    if not isinstance(probabilities, dict) or not finite_probability(confidence):
        return "missing or invalid probabilities/confidence"
    try:
        expected = choice_confidence(probabilities)
    except ValueError as exc:
        return str(exc)
    if abs(expected - confidence) > tolerance:
        return "confidence %.4f differs from expected %.4f" % (confidence, expected)
    return None


ANSWER_FIELDS = {"choice": {"choice", "probabilities", "confidence"},
                 "score": {"score", "probabilities", "confidence", "legend"}}


def answers(value, path="$"):
    """Yield (json_path, answer) for every typed Choice or Score answer object.

    Question definitions (type, instructions, criteria) are not answers. Any object
    carrying an answer field is yielded, so an incomplete answer is reported rather
    than silently skipped.
    """
    if isinstance(value, dict):
        if ANSWER_FIELDS.get(value.get("type"), set()) & set(value):
            yield path, value
        for key, child in value.items():
            yield from answers(child, path + "." + str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from answers(child, path + "[" + str(index) + "]")


def json_files(paths):
    for path in paths:
        path = Path(path)
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*.json") if p.is_file())
        else:
            yield path


def check(paths, tolerance=DEFAULT_TOLERANCE):
    report = {"files_scanned": 0, "choice_answers_checked": 0, "score_answers_not_checked": 0,
              "max_abs_difference": 0.0, "by_option_count": {}, "failures": [],
              "tolerance": tolerance,
              "scope": "Consistency of stored Choice confidence with its probabilities; not correctness."}
    for file in json_files(paths):
        report["files_scanned"] += 1
        for path, answer in answers(json.loads(file.read_text())):
            if answer["type"] == "score":
                report["score_answers_not_checked"] += 1
                continue
            report["choice_answers_checked"] += 1
            problem = check_answer(answer, tolerance)
            if problem:
                report["failures"].append({"file": str(file), "path": path, "problem": problem})
                continue
            n = len(answer["probabilities"])
            difference = abs(choice_confidence(answer["probabilities"]) - answer["confidence"])
            report["max_abs_difference"] = round(max(report["max_abs_difference"], difference), 4)
            report["by_option_count"][str(n)] = report["by_option_count"].get(str(n), 0) + 1
    report["by_option_count"] = dict(sorted(report["by_option_count"].items(), key=lambda kv: int(kv[0])))
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: check_confidence.py RECEIPT_JSON_OR_DIRECTORY...")
    result = check(sys.argv[1:])
    print(json.dumps(result, indent=2))
    if result["failures"]:
        raise SystemExit("Choice confidence inconsistent with probabilities")
