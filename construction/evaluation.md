---
layout: default
title: "Construction: Evaluation"
description: "Original and versioned synthetic screens, preserved disagreements, and evidence limits."
permalink: /construction/evaluation/
kicker: "34/35 current labels matched · CN05 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` screened eight version-1 Choice contracts on synthetic text. The archived first run had 24/24 design and 7/8 challenge labels match (31/32). The v1 CN05 disagreement remains unchanged in the history.

On September 26, a targeted contract review found a scope mismatch: CN05's purpose used the project's stop-work list, while its instructions added a broad active-exposure trigger outside that list. Jev favored a list-bound v2 rule (top probability 0.91; confidence 0.89). The diagnosis itself was less decisive (scope mismatch 0.58; confidence 0.44), so the repair was checked against CN05's stated purpose and named field rather than treated as an authority on safety policy. The request and response are preserved in [contract-review-v2.json]({{ '/construction/results/contract-review-v2.json' | relative_url }}).

The uncached v2 screen used seven reviewer-authored development cases: three design and four challenge cases. Expectations remained outside provider inputs. No recovery call was needed.

| Selection | Split | Cases | Matching labels | Disagreements | Provider errors |
| --- | --- | ---: | ---: | ---: | ---: |
| Archived v1 | Design | 24 | 24 | 0 | 0 |
| Archived v1 | Challenge | 8 | 7 | 1 | 0 |
| CN05 v2 refinement | Design | 3 | 2 | 1 | 0 |
| CN05 v2 refinement | Challenge | 4 | 4 | 0 | 0 |
| Current-version selection | Design | 24 | 23 | 1 | 0 |
| Current-version selection | Challenge | 11 | 11 | 0 | 0 |
| Current-version selection | Total | 35 | 34 | 1 | 0 |

CN05 remains provisional. The current screen has one unresolved label disagreement; none of these synthetic results qualifies a real safety workflow.

## Preserve the disagreements

| Fixture | Version | Expected | Jev chose | Reported confidence | Interpretation |
| --- | ---: | --- | --- | ---: | --- |
| CN05-4 | 1 | `stop_work_condition` | `hazard_to_correct` | 1.0 | Original v1 disagreement retained; the broad active-exposure rule and list-only purpose did not align. |
| CN05-7 | 2 | `unknown` | `positive_no_deficiency` | 0.95 | Empty stop-work list was explicitly expected to be unknown. This is a question-level miss; code-owned preflight is specified to stop the call and return local `unknown`. |

The v2 rule now makes the supplied list the boundary for `stop_work_condition`. Unlisted hazards—including active exposure—are `hazard_to_correct` and must go to human review under project procedures. That label does not say a condition is safe, set urgency, or decide whether work stops. The v2 CN05-8 challenge matched this clarified boundary. The original CN05-4 expectation was not edited: its v1 record and response remain in the archived snapshot.

Jev's confidence describes the returned distribution, follows the option count, and is not the chosen label's probability or a correctness guarantee. A matching synthetic case is not a safety decision.

## Receipts and reproducibility

- [Archived initial catalog]({{ '/construction/results/initial-catalog.json' | relative_url }}), [archived initial fixtures]({{ '/construction/results/initial-fixtures.json' | relative_url }}), and [archived initial summary]({{ '/construction/results/initial-summary.json' | relative_url }})
- [Original 32 receipts]({{ '/construction/results/screening.json' | relative_url }}) and [original recovery receipts]({{ '/construction/results/recovery.json' | relative_url }})
- [Seven CN05 v2 receipts]({{ '/construction/results/refinement.json' | relative_url }}) and [v2 recovery receipts]({{ '/construction/results/refinement-recovery.json' | relative_url }})
- [Exact current summary]({{ '/construction/results/summary.json' | relative_url }})
- [Current question catalog]({{ '/construction/catalog.json' | relative_url }}) and [39 fixture records, including four preserved v1 cases]({{ '/construction/fixtures.json' | relative_url }})
- [Source support review]({{ '/construction/results/source-review.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/construction/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/construction/test_evaluate.py)

Run from the repository root with Python 3:

```sh
python3 construction/evaluate.py
python3 -m unittest discover -s construction -p 'test_*.py' -v
```

The evaluator replays both versions, verifies all 39 screening request digests, and checks exact state/question/version binding, model identity, answer and probability coverage, confidence consistency, immutable v1 cases, challenge/design splits, and recovery eligibility. Known semantic disagreements remain visible rather than failing replay.

The 39 screening calls report 33,606 input and 2,833 output tokens; the bridge estimates $0.001411452 total for those screens. The separate contract-review call used 1,372 input and 120 output tokens and estimates $0.000057624. These are estimates, not invoices, and do not establish model savings.

## What remains untested

These are synthetic reviewer-authored development screens, not a random or held-out sample. There is no real project safety-manager agreement study, workflow integration replay, calibration assessment, subgroup analysis, or measurement of downstream outcome. The code-owned preflight and notification/queue behavior are described as boundaries; this collection does not implement or verify a live consumer.

Before any real use, independently label representative authorized observations with the project safety manager, verify the actual project list and human routing against the consuming code, measure missed listed conditions first, and confirm that unlisted hazards reach human review. Keep work-stoppage and response-urgency decisions with the competent person and project policy.

[Back to the collection]({{ '/construction/' | relative_url }})
