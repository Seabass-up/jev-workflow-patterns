---
layout: default
title: "Auto performance: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /auto-performance/evaluation/
kicker: "34/34 current labels matched · AP03 v2 · no provisional patterns"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated eight version-1 Choice contracts on synthetic text. Each had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs; the original contracts and labels remain preserved.

During source review, AP03's v1 `supported` wording required the fitment text to name drivetrain, but its positive fixture did not. AP03 v2 clarifies broad category statements versus explicit fitment conditions. The four original AP03 states and expected labels were preserved and re-screened at v2; two development-authored boundary challenges were added for an explicit unresolved drivetrain condition and vague nonempty fitment text. These added cases are not claimed as held-out or independently authored.

| Evaluation set | Design | Challenge | Total | Matching labels |
| --- | ---: | ---: | ---: | ---: |
| Initial version-1 whole catalog | 24/24 | 8/8 | 32 | 32 |
| AP03 version-2 refinement | 3/3 | 3/3 | 6 | 6 |
| Current selected catalog | 24/24 | 10/10 | 34 | 34 |

All 38 unique screening requests returned typed answers; no recovery call was needed. The current selection reuses the 28 unrevised v1 profile receipts and the six AP03 v2 receipts. All AP03 v1 results remain separately replayable against their frozen v1 contract. AP03-6 matched `unknown` at confidence 0.37, below the recorded 0.8 review floor; the declared follow-up remains necessary.

## Preserve the disagreements

Every current case matched its authored label. The original 32-case screen and six-case AP03 refinement are synthetic design checks, not evidence of accuracy in use; the low-confidence AP03-6 answer is not promoted for automatic use.

## Receipts and reproducibility

- [Initial version-1 catalog and fixtures]({{ '/auto-performance/results/initial-catalog.json' | relative_url }}) and [frozen version-1 fixture states]({{ '/auto-performance/results/initial-fixtures.json' | relative_url }})
- [Initial version-1 receipts]({{ '/auto-performance/results/screening.json' | relative_url }}) and [AP03 version-2 receipts]({{ '/auto-performance/results/refinement.json' | relative_url }})
- [Initial recovery receipts]({{ '/auto-performance/results/recovery.json' | relative_url }}) and [AP03 version-2 recovery receipts]({{ '/auto-performance/results/refinement-recovery.json' | relative_url }})
- [Exact summary]({{ '/auto-performance/results/summary.json' | relative_url }})
- [Current question catalog]({{ '/auto-performance/catalog.json' | relative_url }}) and [34 current fixtures]({{ '/auto-performance/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/auto-performance/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/auto-performance/test_evaluate.py)
- [Source support review]({{ '/auto-performance/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 auto-performance/evaluate.py
python3 -m unittest discover -s auto-performance -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, confidence consistency, fixture splits, source references, additive revision history, and recovery eligibility. It replays the v1 evidence against the preserved v1 catalog and the current selection against AP03 v2. Fixture states and expectations cannot be rewritten or removed during a revision.

Across the 38 unique screening calls, successful receipts report 30,922 input tokens and 2,240 output tokens. The local bridge estimates their total cost at $0.001298724. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/auto-performance/' | relative_url }})
