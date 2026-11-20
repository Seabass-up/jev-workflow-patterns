---
layout: default
title: "Executive: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /executive/evaluation/
kicker: "35/35 labels matched · no provisional patterns"
---

# What was tested

The original screen on September 23, 2026 used `jev-1.13.0` for 8 version-1 Choice contracts and 32 synthetic cases. On September 27, 3 contracts were revised after challenge-boundary findings and retested with version-matched fixtures. Original v1 receipts and expectations remain preserved separately. Reviewer-authored additions are targeted development regressions, not held-out evidence.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 24 | 0 | 0 |
| Challenge and regression cases | 11 | 11 | 0 | 0 |
| Total | 35 | 35 | 0 | 0 |

All 32 original v1 calls and 15 versioned v2 calls returned typed answers; no recovery call was needed. The v1 requests remain preserved separately.

## Preserve the disagreements

Every case matched its authored label. A full match on 35 synthetic cases is a small design check, not evidence of accuracy in use.

## Preserved version-1 disagreements

| Fixture | Expected | V1 Jev answer | Confidence |
| --- | --- | --- | ---: |
| [CE02-4]({{ '/executive/patterns/ce02/' | relative_url }}) | `reversibility_not_addressed` | `one_way_as_written` | 0.39 |
| [CE06-4]({{ '/executive/patterns/ce06/' | relative_url }}) | `generic_risk_only` | `downside_stated` | 0.51 |

These original requests, questions, expected labels, and responses are preserved in the v1 snapshot and screening receipts. The contract versions changed to make the intended boundaries explicit; the old disagreements were not relabeled or overwritten. Matching v2 regression cases do not prove general accuracy.

## Current answers below the recorded review threshold

The stored confidence is a summary of the output distribution, not the selected label's probability. The following answer is below its profile's recorded workflow review threshold:

| Fixture | Label | Confidence | Threshold | Handling |
| --- | --- | ---: | ---: | --- |
| `CE01-4` | `no_decision_requested` | 0.67 | 0.8 | Human review required by the recorded policy |
| `CE07-2` | `qualitative_outcome` | 0.59 | 0.8 | Human review required by the recorded policy |
| `CE02-5` | `reversibility_not_addressed` | 0.56 | 0.8 | Human review required by the recorded policy |

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/executive/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/executive/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/executive/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/executive/catalog.json' | relative_url }}) and [35 fixtures]({{ '/executive/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/executive/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/executive/test_evaluate.py)
- [Version-1 catalog snapshot]({{ '/executive/results/initial-catalog.json' | relative_url }}), [version-1 fixtures]({{ '/executive/results/initial-fixtures.json' | relative_url }}), and [version-1 summary]({{ '/executive/results/initial-summary.json' | relative_url }})
- [Versioned refinement receipts (15)]({{ '/executive/results/refinement.json' | relative_url }})
- [Source support review]({{ '/executive/results/source-review.json' | relative_url }})
- [Wave 20 pattern audit]({{ '/executive/results/wave20-audit.json' | relative_url }})
- [Supplemental source support review (September 27)]({{ '/executive/results/source-review-wave20.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 executive/evaluate.py
python3 -m unittest discover -s executive -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 24,957 input tokens and 2,046 output tokens. The local bridge estimates their total cost at $0.001048194. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/executive/' | relative_url }})
