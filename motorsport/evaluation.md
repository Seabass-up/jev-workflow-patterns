---
layout: default
title: "Motorsport: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /motorsport/evaluation/
kicker: "31/32 labels matched · 1 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 24 | 0 | 0 |
| Separately authored challenges | 8 | 7 | 1 | 0 |
| Total | 32 | 31 | 1 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [MR04-4]({{ '/motorsport/patterns/mr04/' | relative_url }}) | challenge | `observation` | `conformance_claim` | 0.4 | Pattern remains provisional |

- MR04-4: The statement reports the measured value and quotes the limit side by side but never asserts that the plank is within or outside it, passes or fails, and proposes no action; the comparison of the two numbers is code's job, so the statement remains an observation.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/motorsport/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/motorsport/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/motorsport/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/motorsport/catalog.json' | relative_url }}) and [32 fixtures]({{ '/motorsport/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/motorsport/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/motorsport/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 motorsport/evaluate.py
python3 -m unittest discover -s motorsport -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 21,545 input tokens and 1,923 output tokens. The local bridge estimates their total cost at $0.00090489. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/motorsport/' | relative_url }})
