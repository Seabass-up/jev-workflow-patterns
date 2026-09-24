---
layout: default
title: "Project management: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /project-management/evaluation/
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
| [PM02-4]({{ '/project-management/patterns/pm02/' | relative_url }}) | challenge | `trigger_missing` | `fully_stated` | 1.0 | Pattern remains provisional |

- PM02-4: The owner is a named person in a specific role and the mitigation describes concrete actions, but the trigger column merely restates the risk itself, and the contract says a restatement of the risk is neither a trigger nor a mitigation. With the owner present and the trigger absent, trigger_missing applies regardless of the low likelihood note, which the contract says not to judge.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/project-management/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/project-management/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/project-management/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/project-management/catalog.json' | relative_url }}) and [32 fixtures]({{ '/project-management/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/project-management/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/project-management/test_evaluate.py)
- [Source support review]({{ '/project-management/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 project-management/evaluate.py
python3 -m unittest discover -s project-management -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 22,600 input tokens and 1,812 output tokens. The local bridge estimates their total cost at $0.0009492. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/project-management/' | relative_url }})
