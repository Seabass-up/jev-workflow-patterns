---
layout: default
title: "Marketing: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /marketing/evaluation/
kicker: "29/32 labels matched · 3 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 24 | 0 | 0 |
| Separately authored challenges | 8 | 5 | 3 | 0 |
| Total | 32 | 29 | 3 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [MK03-4]({{ '/marketing/patterns/mk03/' | relative_url }}) | challenge | `no_call_to_action` | `single_call_to_action` | 0.32 | Pattern remains provisional |
| [MK05-4]({{ '/marketing/patterns/mk05/' | relative_url }}) | challenge | `off_voice` | `on_voice` | 0.34 | Pattern remains provisional |
| [MK08-4]({{ '/marketing/patterns/mk08/' | relative_url }}) | challenge | `strategy` | `both` | 0.39 | Pattern remains provisional |

- MK03-4: Every imperative here (picture, ask yourself, keep reading) invites the reader to imagine something or to continue within the copy itself. The contract counts only requests to do something outside the copy, so none of these is a call to action despite the imperative mood.
- MK05-4: The copy clearly shows the guide's warm, plain-spoken, second-person traits, but it uses the banned word 'cheap' inside a negation, which the guide explicitly says still counts as use. The contract selects off_voice whenever a stated rule is broken, even when described traits are also present.
- MK08-4: Both requested edits are wording and imagery changes, but their only stated reason is that the piece addresses the wrong audience, and the contract counts a requested change whose stated reason is audience or positioning as a strategy comment. No separate execution point with a craft, clarity, correctness, or brand-rule reason is raised, so both does not apply.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/marketing/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/marketing/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/marketing/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/marketing/catalog.json' | relative_url }}) and [32 fixtures]({{ '/marketing/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/marketing/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/marketing/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 marketing/evaluate.py
python3 -m unittest discover -s marketing -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 22,310 input tokens and 1,867 output tokens. The local bridge estimates their total cost at $0.00093702. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/marketing/' | relative_url }})
