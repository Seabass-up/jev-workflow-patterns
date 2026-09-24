---
layout: default
title: "Auto repair: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /auto-repair/evaluation/
kicker: "32/32 labels matched · no provisional patterns"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 24 | 0 | 0 |
| Separately authored challenges | 8 | 8 | 0 | 0 |
| Total | 32 | 32 | 0 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

Every case matched its authored label. A full match on 32 synthetic cases is a small design check, not evidence of accuracy in use.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/auto-repair/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/auto-repair/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/auto-repair/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/auto-repair/catalog.json' | relative_url }}) and [32 fixtures]({{ '/auto-repair/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/auto-repair/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/auto-repair/test_evaluate.py)
- [Source support review]({{ '/auto-repair/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 auto-repair/evaluate.py
python3 -m unittest discover -s auto-repair -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 22,949 input tokens and 1,765 output tokens. The local bridge estimates their total cost at $0.000963858. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/auto-repair/' | relative_url }})
