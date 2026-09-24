---
layout: default
title: "Call controls: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /controls/evaluation/
kicker: "38/40 labels matched · 2 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 10 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

Before any fixture was written, CT08's own question was run over every non-unknown option pair of this collection and the storytelling and electrical collections. Four electrical contracts and one storytelling contract received precedence sentences or narrower descriptions as a result. The three passes are preserved in [overlap-review.json]({{ '/controls/results/overlap-review.json' | relative_url }}); two logically complementary pairs (CT07 and CT08's own) were labelled unknown and were left as written.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 30 | 28 | 2 | 0 |
| Separately authored challenges | 10 | 10 | 0 | 0 |
| Total | 40 | 38 | 2 | 0 |

All 40 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [CT03-3]({{ '/controls/patterns/ct03/' | relative_url }}) | design | `unknown` | `drops_an_action` | 0.72 | Pattern remains provisional |
| [CT07-2]({{ '/controls/patterns/ct07/' | relative_url }}) | design | `not_a_complement` | `exact_complement` | 0.56 | Pattern remains provisional |

- CT03-3: The command list is empty.
- CT07-2: A message asking for a refund and a receipt makes both true; a message asking for nothing makes both false.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 40 receipts]({{ '/controls/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/controls/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/controls/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/controls/catalog.json' | relative_url }}) and [40 fixtures]({{ '/controls/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/controls/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/controls/test_evaluate.py)
- [Pre-inference overlap review]({{ '/controls/results/overlap-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 controls/evaluate.py
python3 -m unittest discover -s controls -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 23,253 input tokens and 1,927 output tokens. The local bridge estimates their total cost at $0.000976626. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/controls/' | relative_url }})
