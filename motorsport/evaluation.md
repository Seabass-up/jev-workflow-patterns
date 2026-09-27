---
layout: default
title: "Motorsport: Evaluation"
description: "Versioned synthetic design checks, preserved disagreements, and evidence limits."
permalink: /motorsport/evaluation/
kicker: "34/34 current labels matched · MR04 v2 · no current provisional patterns"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated eight version-1 Choice contracts on synthetic text. Each had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. The frozen version-1 screen matched 31/32 cases; MR04-4 remains an archived disagreement.

During source review, the host comparison of MR04's question with MR04-4 confirmed a wording gap: version 1 did not explicitly distinguish a statement that lists a measured value and an applicable limit from one that says how the two relate. Version 2 states that without an explicit relation the text remains an observation; code still owns the numeric comparison. The original four fixture states and labels were preserved, and two reviewer-authored development challenges were added. Expectations were kept outside provider inputs.

| Evaluation set | Design | Challenge | Total | Matching labels |
| --- | ---: | ---: | ---: | ---: |
| Initial version-1 whole catalog | 24/24 | 7/8 | 32 | 31 |
| MR04 version-2 refinement | 3/3 | 3/3 | 6 | 6 |
| Current selected catalog | 24/24 | 10/10 | 34 | 34 |

All six version-2 requests were uncached and returned typed answers; no provider failure or recovery call occurred. The current selection reuses 28 unchanged version-1 receipts and the six MR04 version-2 receipts. All 32 initial requests remain replayable against the preserved version-1 catalog and fixtures. MR04-4's original miss is not overwritten or relabeled: the unchanged case was evaluated separately against version 2 and matched `observation` at confidence 0.97.

## Preserve the version-1 disagreement

| Fixture | Version | Expected | Jev chose | Reported confidence | Disposition |
| --- | ---: | --- | --- | ---: | --- |
| [MR04-4]({{ '/motorsport/patterns/mr04/' | relative_url }}) | 1 | `observation` | `conformance_claim` | 0.4 | Preserved in initial history |
| [MR04-4]({{ '/motorsport/patterns/mr04/' | relative_url }}) | 2 | `observation` | `observation` | 0.97 | Matches the revised contract |

The version-1 output showed that the original wording left this boundary open; it does not establish an internal model cause. The source-grounded repair was to make the intended textual distinction explicit, not to change the fixture expectation. Confidence summarizes the output distribution; it is not a correctness guarantee.

## Receipts and reproducibility

- [Initial version-1 catalog]({{ '/motorsport/results/initial-catalog.json' | relative_url }}) and [frozen version-1 fixtures]({{ '/motorsport/results/initial-fixtures.json' | relative_url }})
- [Initial version-1 receipts]({{ '/motorsport/results/screening.json' | relative_url }}) and [version-2 MR04 receipts]({{ '/motorsport/results/refinement.json' | relative_url }})
- [Initial recovery receipts]({{ '/motorsport/results/recovery.json' | relative_url }}) and [version-2 recovery receipts]({{ '/motorsport/results/refinement-recovery.json' | relative_url }})
- [Initial summary]({{ '/motorsport/results/initial-summary.json' | relative_url }}) and [current exact summary]({{ '/motorsport/results/summary.json' | relative_url }})
- [Current question catalog]({{ '/motorsport/catalog.json' | relative_url }}) and [34 current fixtures]({{ '/motorsport/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/motorsport/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/motorsport/test_evaluate.py)
- [Source support review]({{ '/motorsport/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 motorsport/evaluate.py
python3 -m unittest discover -s motorsport -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, confidence consistency, fixture splits, source references, additive revision history, and recovery eligibility. It replays the initial version-1 evidence, the MR04 v2 refinement, and the current selected catalog separately; frozen states and labels cannot be rewritten or removed.

Across the 38 historical and refinement requests, successful receipts report 25,768 input tokens and 2,254 output tokens. The local bridge estimates their total cost at $0.001082256. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

These are small synthetic development screens, not representative or held-out data. There is no repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed work, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence, exact numeric checks, and action controls outside the model.

[Back to the collection]({{ '/motorsport/' | relative_url }})
