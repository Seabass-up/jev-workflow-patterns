---
layout: default
title: "Human resources: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /human-resources/evaluation/
kicker: "29/32 labels matched · 2 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 23 | 1 | 0 |
| Separately authored challenges | 8 | 6 | 2 | 0 |
| Total | 32 | 29 | 3 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [HR06-3]({{ '/human-resources/patterns/hr06/' | relative_url }}) | design | `unknown` | `all_elements_stated` | 0.43 | Pattern remains provisional |
| [HR06-4]({{ '/human-resources/patterns/hr06/' | relative_url }}) | challenge | `inconsistent_elements` | `missing_elements` | 0.35 | Pattern remains provisional |
| [HR07-4]({{ '/human-resources/patterns/hr07/' | relative_url }}) | challenge | `generalization_only` | `generalization_with_example` | 0.92 | Pattern remains provisional |

- HR06-3: The checklist of required elements is empty, so there is nothing to check the letter against.
- HR06-4: The start date is only referenced as agreed on a call, which the contract says does not count as stated, so an element is missing; base salary is also given two different values ($58,000 and $56,000), and the contract's tie-break says that when elements are both missing and inconsistent, inconsistent_elements is selected.
- HR07-4: 'Needs improvement' is a pattern claim; the April release cycle names a period but the comment does not describe what the employee did in it, so it is not an instance under the contract's definition, leaving a pattern claim with no instance.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/human-resources/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/human-resources/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/human-resources/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/human-resources/catalog.json' | relative_url }}) and [32 fixtures]({{ '/human-resources/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/human-resources/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/human-resources/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 human-resources/evaluate.py
python3 -m unittest discover -s human-resources -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 22,750 input tokens and 1,793 output tokens. The local bridge estimates their total cost at $0.0009555. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/human-resources/' | relative_url }})
