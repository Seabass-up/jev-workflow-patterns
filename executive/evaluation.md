---
layout: default
title: "Executive: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /executive/evaluation/
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
| [CE02-4]({{ '/executive/patterns/ce02/' | relative_url }}) | challenge | `reversibility_not_addressed` | `one_way_as_written` | 0.39 | Pattern remains provisional |
| [CE06-4]({{ '/executive/patterns/ce06/' | relative_url }}) | challenge | `generic_risk_only` | `downside_stated` | 0.51 | Pattern remains provisional |

- CE02-4: The only irreversibility language describes the consequence of not acting, not the commitment being asked for; the text never states a way to exit the agreement nor that the agreement is permanent or binding, so it says nothing about undoing the commitment itself.
- CE06-4: The specific harms named are consequences of not adopting the plan, not ways the recommended course could fail, cost more, take longer, or cause harm; the plan's own risks are mentioned only as generic manageable execution risk, so no specific downside of the recommended course is stated.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/executive/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/executive/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/executive/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/executive/catalog.json' | relative_url }}) and [32 fixtures]({{ '/executive/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/executive/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/executive/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 executive/evaluate.py
python3 -m unittest discover -s executive -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 21,862 input tokens and 1,862 output tokens. The local bridge estimates their total cost at $0.000918204. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/executive/' | relative_url }})
