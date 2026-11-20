---
layout: default
title: "Human resources: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /human-resources/evaluation/
kicker: "36/37 labels matched · 1 provisional"
---

# What was tested

The original screen on September 23, 2026 used `jev-1.13.0` for 8 version-1 Choice contracts and 32 synthetic cases. On September 27, 3 contracts were revised after challenge-boundary findings and retested with version-matched fixtures. Original v1 receipts and expectations remain preserved separately. Reviewer-authored additions are targeted development regressions, not held-out evidence.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 23 | 1 | 0 |
| Challenge and regression cases | 13 | 13 | 0 | 0 |
| Total | 37 | 36 | 1 | 0 |

All 32 original v1 calls and 17 versioned v2 calls returned typed answers; no recovery call was needed. The v1 requests remain preserved separately.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [HR06-3]({{ '/human-resources/patterns/hr06/' | relative_url }}) | design | `unknown` | `all_elements_stated` | 0.62 | Pattern remains provisional |

- HR06-3: The checklist of required elements is empty, so there is nothing to check the letter against.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Preserved version-1 disagreements

| Fixture | Expected | V1 Jev answer | Confidence |
| --- | --- | --- | ---: |
| [HR06-3]({{ '/human-resources/patterns/hr06/' | relative_url }}) | `unknown` | `all_elements_stated` | 0.43 |
| [HR06-4]({{ '/human-resources/patterns/hr06/' | relative_url }}) | `inconsistent_elements` | `missing_elements` | 0.35 |
| [HR07-4]({{ '/human-resources/patterns/hr07/' | relative_url }}) | `generalization_only` | `generalization_with_example` | 0.92 |

These original requests, questions, expected labels, and responses are preserved in the v1 snapshot and screening receipts. The contract versions changed to make the intended boundaries explicit; the old disagreements were not relabeled or overwritten. Matching v2 regression cases do not prove general accuracy.

## Current answers below the recorded review threshold

The stored confidence is a summary of the output distribution, not the selected label's probability. The following answer is below its profile's recorded workflow review threshold:

| Fixture | Label | Confidence | Threshold | Handling |
| --- | --- | ---: | ---: | --- |
| `HR01-4` | `essential` | 0.63 | 0.8 | Human review required by the recorded policy |
| `HR03-2` | `opinion_only` | 0.51 | 0.8 | Human review required by the recorded policy |
| `HR06-3` | `all_elements_stated` | 0.62 | 0.8 | Human review required by the recorded policy |

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/human-resources/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/human-resources/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/human-resources/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/human-resources/catalog.json' | relative_url }}) and [37 fixtures]({{ '/human-resources/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/human-resources/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/human-resources/test_evaluate.py)
- [Version-1 catalog snapshot]({{ '/human-resources/results/initial-catalog.json' | relative_url }}), [version-1 fixtures]({{ '/human-resources/results/initial-fixtures.json' | relative_url }}), and [version-1 summary]({{ '/human-resources/results/initial-summary.json' | relative_url }})
- [Versioned refinement receipts (17)]({{ '/human-resources/results/refinement.json' | relative_url }})
- [Source support review]({{ '/human-resources/results/source-review.json' | relative_url }})
- [Wave 23 pattern review audit]({{ '/human-resources/results/wave23-audit.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 human-resources/evaluate.py
python3 -m unittest discover -s human-resources -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 26,801 input tokens and 2,084 output tokens. The local bridge estimates their total cost at $0.001125642. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

The synthetic screen is small and targeted; there is no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/human-resources/' | relative_url }})
