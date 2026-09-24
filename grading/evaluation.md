---
layout: default
title: "Grading: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /grading/evaluation/
kicker: "29/32 labels matched · 3 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 23 | 1 | 0 |
| Separately authored challenges | 8 | 6 | 2 | 0 |
| Total | 32 | 29 | 3 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [GR05-3]({{ '/grading/patterns/gr05/' | relative_url }}) | design | `unknown` | `working_shown` | 0.43 | Pattern remains provisional |
| [GR02-4]({{ '/grading/patterns/gr02/' | relative_url }}) | challenge | `evidence_found` | `evidence_partial` | 0.62 | Pattern remains provisional |
| [GR06-4]({{ '/grading/patterns/gr06/' | relative_url }}) | challenge | `verbatim` | `close_paraphrase` | 0.45 | Pattern remains provisional |

- GR05-3: The problem statement is empty, so the response cannot be read against the task it answers.
- GR02-4: The criterion names a count, so the contract says to judge only whether the described kind of evidence appears and to leave the count to code. One passage quotes the novel and then explains how the quotation supports the thesis, which does both components the criterion names, so a single instance is evidence_found rather than evidence_partial.
- GR06-4: The third sentence matches the source word for word, and the contract says quotation marks do not change the wording relation and that acceptability is not judged. Because the relation differs across the passage's sentences, the stated order verbatim, close_paraphrase, original selects verbatim even though the first two sentences are in the student's own words.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/grading/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/grading/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/grading/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/grading/catalog.json' | relative_url }}) and [32 fixtures]({{ '/grading/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/grading/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/grading/test_evaluate.py)
- [Source support review]({{ '/grading/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 grading/evaluate.py
python3 -m unittest discover -s grading -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 22,756 input tokens and 1,813 output tokens. The local bridge estimates their total cost at $0.000955752. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/grading/' | relative_url }})
