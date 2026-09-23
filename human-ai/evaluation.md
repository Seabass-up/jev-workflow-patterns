---
layout: default
title: "Human–AI Pattern Evaluation"
description: "Frozen design cases, separately authored challenges, preserved failures and evidence limits."
permalink: /human-ai/evaluation/
kicker: "92/96 labels matched · four provisional patterns"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 24 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs. Nine contract clarifications were made during pre-inference review and recorded in [research.json]({{ '/human-ai/research.json' | relative_url }}); no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 72 | 69 | 3 | 0 |
| Separately authored challenges | 24 | 23 | 1 | 0 |
| Total | 96 | 92 | 4 | 0 |

There were 96 initial calls: three `deadline_exceeded` errors and one HTTP 529. One later request per failed call succeeded, making 100 screening attempts with 96 successful responses. The causes of the provider/bridge failures are unknown. Recovery does not demonstrate an availability repair. All original failures remain in the initial receipt file; semantic disagreements were not eligible for recovery.

## Preserve the disagreements

| Fixture | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | ---: | --- |
| [HA06-1]({{ '/human-ai/patterns/ha06/' | relative_url }}) | `ambiguous` | `unique` | 0.53 | Pattern remains provisional |
| [HA10-2]({{ '/human-ai/patterns/ha10/' | relative_url }}) | `new_information` | `redundant_reentry` | 0.36 | Pattern remains provisional |
| [HA21-1]({{ '/human-ai/patterns/ha21/' | relative_url }}) | `activity_proxy` | `conflicting_incentive` | 0.97 | Pattern remains provisional |
| [HA17-4]({{ '/human-ai/patterns/ha17/' | relative_url }}) | `takes_over` | `preserves` | 0.48 | Pattern remains provisional |

- HA06-1: “Place the blue folder beside the red folder, then open it” was authored as ambiguous; Jev selected a unique referent. The catalog does not turn that choice into an object selection.
- HA10-2: a delivery-address question was treated as repeating a supplied pickup address. This can suppress a genuinely needed question.
- HA17-4: optional sample slogans were accepted as preserving authorship even though the user had expressly prohibited writing samples. Offering to help and already doing excluded work are not the same.
- HA21-1: counting folders despite retrieval failure was authored as an activity proxy; Jev treated it as a conflicting incentive with 0.97 confidence. The boundary may need better independent labeling and a future version. We do not silently decide the model or author must be right.

These are disagreements against authored expectations, not automatically four proven model defects. HA21 especially shows why confidence is not a correctness guarantee. Confidence summarizes the output distribution; it is not the chosen label's probability.

## Receipts and reproducibility

- [Initial 96 receipts]({{ '/human-ai/results/screening.json' | relative_url }})
- [Four bounded service recoveries]({{ '/human-ai/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/human-ai/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/human-ai/catalog.json' | relative_url }}) and [96 fixtures]({{ '/human-ai/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/human-ai/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/human-ai/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 human-ai/evaluate.py
python3 -m unittest discover -s human-ai -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, successful request hashes, model identity, answer/probability coverage, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does. It does not call Jev or regenerate missing results.

Successful fixture responses report 57,716 input tokens and 5,159 output tokens. The local bridge estimates their total cost at $0.002424072. That is an estimate, not an invoice, and excludes research calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, classroom study, usability test, live inbox, or production integration. Research-stage Jev source ranking and relevance judgments are separate from this fixture screen. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual human outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/human-ai/' | relative_url }})
