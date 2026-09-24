---
layout: default
title: "Real estate: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /real-estate/evaluation/
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
| [RE02-4]({{ '/real-estate/patterns/re02/' | relative_url }}) | challenge | `availability_question` | `pricing_question` | 0.76 | Pattern remains provisional |
| [RE04-4]({{ '/real-estate/patterns/re04/' | relative_url }}) | challenge | `maintenance` | `use` | 0.68 | Pattern remains provisional |

- RE02-4: The tour is declined rather than requested, so showing_request does not apply. The message then asks about availability, price, and a feature, and the contract's precedence puts availability_question ahead of pricing_question and property_details_question regardless of sentence order.
- RE04-4: The clause covers use (restricting alterations and lock changes) and maintenance (assigning responsibility to maintain and repair). Both precedence orders the contract states list maintenance before use, so maintenance applies even though the clause opens as an alterations restriction.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/real-estate/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/real-estate/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/real-estate/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/real-estate/catalog.json' | relative_url }}) and [32 fixtures]({{ '/real-estate/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/real-estate/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/real-estate/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 real-estate/evaluate.py
python3 -m unittest discover -s real-estate -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 22,030 input tokens and 1,761 output tokens. The local bridge estimates their total cost at $0.00092526. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/real-estate/' | relative_url }})
