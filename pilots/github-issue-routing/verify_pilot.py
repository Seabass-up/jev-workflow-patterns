"""Verify the frozen sample, deterministic baseline, and preserved failed replay."""

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "skills/jev-question-kernel-catalog/scripts"))

import baseline
import consumer
from qualify_workflow import evaluate


def main():
    plan = json.loads((HERE / "pilot-plan.json").read_text())
    contract = json.loads((HERE / "contract.json").read_text())
    def replay(sample_name, pilot_name, split):
        sample = json.loads((HERE / sample_name).read_text())
        pilot = json.loads((HERE / pilot_name).read_text())
        assert {key: pilot[key] for key in plan} == plan, "pilot changed frozen plan"
        assert len(sample["cases"]) == 24
        for source, case in zip(sample["cases"], pilot["cases"], strict=True):
            assert source["id"] == case["id"]
            assert source["state"] == case["state"]
            assert source["expected_disposition"] == case["expected_disposition"]
            assert source["baseline_disposition"] == case["baseline_disposition"]
            assert baseline.decide(source["state"]["title"]) == case["baseline_disposition"]
            assert case["split"] == split
        return sample, evaluate(contract, pilot, consumer.decide)

    screen_sample, screen = replay("sample-frozen.json", "pilot.json", "development_screen")
    held_sample, held = replay("sample-held-out.json", "pilot-held-out.json", "held_out")
    assert not {c["id"] for c in screen_sample["cases"]} & {c["id"] for c in held_sample["cases"]}
    assert screen["evidence_scope"] == "development_screen_only"
    assert held["evidence_scope"] == "held_out_as_declared"
    a, b = screen["sample"], held["sample"]
    assert (a["matched"], a["baseline_matched"], a["reviewed"],
            a["automatic_errors"], a["invalid_or_failed"]) == (15, 14, 4, 5, 0)
    assert "checks_met" not in a
    assert a["automatic_errors"] > plan["sample_limits"]["max_automatic_errors"]
    assert {row["id"] for row in screen["cases"] if row["automatic_error"]} == {
        "cli-gh-14208", "cli-gh-14153", "cli-gh-14118", "cli-gh-14055", "cli-gh-13862"
    }
    assert (b["matched"], b["baseline_matched"], b["reviewed"],
            b["automatic_errors"], b["invalid_or_failed"], b["checks_met"]) == (
                7, 4, 17, 0, 0, False), "held-out receipt or policy changed"
    print("development screen: 24 responses, 5 automatic label disagreements")
    print("held-out: 24 responses, 17 human reviews; predeclared gate FAILED")


if __name__ == "__main__":
    main()
