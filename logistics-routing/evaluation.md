---
layout: default
title: "Logistics routing: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /logistics-routing/evaluation/
kicker: "30/32 labels matched · 2 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 24 | 0 | 0 |
| Separately authored challenges | 8 | 6 | 2 | 0 |
| Total | 32 | 30 | 2 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [LR03-4]({{ '/logistics-routing/patterns/lr03/' | relative_url }}) | challenge | `contact_instruction` | `vehicle_restriction` | 0.98 | Pattern remains provisional |
| [LR04-4]({{ '/logistics-routing/patterns/lr04/' | relative_url }}) | challenge | `road_closure_or_detour` | `vehicle_problem` | 0.68 | Pattern remains provisional |

- LR03-4: The liftgate is mentioned only to say it is not required, so the text states no limit on which vehicle or equipment can serve the stop. It gives both a contact instruction and a handling instruction, and the contract's order selects contact_instruction before handling_instruction.
- LR04-4: The warning light is mentioned but the driver explicitly does not attribute the deviation to it, and the contract says to use only the cause the driver states rather than one inferred from the report. The only stated cause is the closed road and posted detour, so the vehicle_problem tier of the precedence order is never reached.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/logistics-routing/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/logistics-routing/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/logistics-routing/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/logistics-routing/catalog.json' | relative_url }}) and [32 fixtures]({{ '/logistics-routing/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/logistics-routing/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/logistics-routing/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 logistics-routing/evaluate.py
python3 -m unittest discover -s logistics-routing -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 21,324 input tokens and 1,907 output tokens. The local bridge estimates their total cost at $0.000895608. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/logistics-routing/' | relative_url }})
