---
layout: default
title: "Data quality: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /data-quality/evaluation/
kicker: "29/32 labels matched · 2 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 21 | 3 | 0 |
| Separately authored challenges | 8 | 8 | 0 | 0 |
| Total | 32 | 29 | 3 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [DQ03-3]({{ '/data-quality/patterns/dq03/' | relative_url }}) | design | `unknown` | `fits_sibling_entry` | 0.32 | Pattern remains provisional |
| [DQ06-2]({{ '/data-quality/patterns/dq06/' | relative_url }}) | design | `admits_two_readings` | `single_reading` | 0.42 | Pattern remains provisional |
| [DQ06-3]({{ '/data-quality/patterns/dq06/' | relative_url }}) | design | `unknown` | `circular_or_empty` | 0.92 | Pattern remains provisional |

- DQ03-3: No proposed entry is supplied, so there is no definition to check the value against.
- DQ06-2: The definition fixes the unit and currency but not whether the price is before or after line discounts or tax, so two people could record different amounts.
- DQ06-3: No definition text is supplied, so there is no wording to judge.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/data-quality/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/data-quality/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/data-quality/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/data-quality/catalog.json' | relative_url }}) and [32 fixtures]({{ '/data-quality/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/data-quality/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/data-quality/test_evaluate.py)
- [Source support review]({{ '/data-quality/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 data-quality/evaluate.py
python3 -m unittest discover -s data-quality -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 24,547 input tokens and 1,959 output tokens. The local bridge estimates their total cost at $0.001030974. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/data-quality/' | relative_url }})
