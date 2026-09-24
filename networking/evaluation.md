---
layout: default
title: "Networking: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /networking/evaluation/
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
| [NW01-4]({{ '/networking/patterns/nw01/' | relative_url }}) | challenge | `wireless_association` | `latency_or_packet_loss` | 0.79 | Pattern remains provisional |
| [NW02-4]({{ '/networking/patterns/nw02/' | relative_url }}) | challenge | `firewall_policy_change` | `dns_record_change` | 0.84 | Pattern remains provisional |

- NW01-4: The text reports two symptoms, latency_or_packet_loss and wireless_association, and the contract's precedence order places wireless_association ahead of latency_or_packet_loss. The remark that the password was accepted negates a credential rejection rather than describing one, so authentication_or_access does not apply.
- NW02-4: The request describes two change types, a DNS record update and a firewall permit rule, while physical and routing changes are explicitly negated rather than requested. Among the types actually described, the precedence order places firewall_policy_change before dns_record_change.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/networking/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/networking/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/networking/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/networking/catalog.json' | relative_url }}) and [32 fixtures]({{ '/networking/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/networking/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/networking/test_evaluate.py)
- [Source support review]({{ '/networking/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 networking/evaluate.py
python3 -m unittest discover -s networking -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 20,759 input tokens and 1,892 output tokens. The local bridge estimates their total cost at $0.000871878. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/networking/' | relative_url }})
