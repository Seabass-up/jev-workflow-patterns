---
layout: default
title: "Storytelling: Evaluation"
description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."
permalink: /storytelling/evaluation/
kicker: "27/32 labels matched · 3 provisional"
---

# What was tested

On September 23, 2026, `jev-1.13.0` evaluated 8 version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference.

| Split | Cases | Matching labels | Disagreements | Unresolved service errors |
| --- | ---: | ---: | ---: | ---: |
| Design examples | 24 | 20 | 4 | 0 |
| Separately authored challenges | 8 | 7 | 1 | 0 |
| Total | 32 | 27 | 5 | 0 |

All 32 initial calls returned a typed answer; no recovery call was needed.

## Preserve the disagreements

| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |
| --- | --- | --- | --- | ---: | --- |
| [ST04-1]({{ '/storytelling/patterns/st04/' | relative_url }}) | design | `stated` | `mixed` | 0.93 | Pattern remains provisional |
| [ST04-3]({{ '/storytelling/patterns/st04/' | relative_url }}) | design | `unknown` | `rendered` | 0.38 | Pattern remains provisional |
| [ST08-2]({{ '/storytelling/patterns/st08/' | relative_url }}) | design | `ungrounded_reference` | `grounded` | 0.54 | Pattern remains provisional |
| [ST08-3]({{ '/storytelling/patterns/st08/' | relative_url }}) | design | `unknown` | `grounded` | 0.77 | Pattern remains provisional |
| [ST05-4]({{ '/storytelling/patterns/st05/' | relative_url }}) | challenge | `ambiguous_speaker` | `speakers_clear` | 0.46 | Pattern remains provisional |

- ST04-1: Narration names the emotion and does not render it through action or sensation.
- ST04-3: The character name is empty.
- ST08-2: Captain Vesey, the letter, and the promise are neither in the reader's knowledge nor introduced by the passage.
- ST08-3: The reader-knowledge list is empty.
- ST05-4: Most lines are fixed by an action beat or by address (the third line addresses Ines and speaks of Marta in the third person, so it is Pell), but 'Stay out of it, Pell.' has no beat or tag, rules out only Pell, and there is no two-person alternation to lean on in a three-person exchange, so it could plausibly be Ines or Marta; one such line is enough for ambiguous_speaker.

These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.

## Receipts and reproducibility

- [Initial 32 receipts]({{ '/storytelling/results/screening.json' | relative_url }})
- [Recovery receipts]({{ '/storytelling/results/recovery.json' | relative_url }})
- [Exact summary]({{ '/storytelling/results/summary.json' | relative_url }})
- [Frozen question catalog]({{ '/storytelling/catalog.json' | relative_url }}) and [32 fixtures]({{ '/storytelling/fixtures.json' | relative_url }})
- [Offline evaluator](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/storytelling/evaluate.py) and [regression tests](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/storytelling/test_evaluate.py)
- [Source support review]({{ '/storytelling/results/source-review.json' | relative_url }})

Run from the repository root with Python 3:

```sh
python3 storytelling/evaluate.py
python3 -m unittest discover -s storytelling -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.

Successful fixture responses report 19,428 input tokens and 1,449 output tokens. The local bridge estimates their total cost at $0.000815976. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls.

## What remains untested

There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.

Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.

[Back to the collection]({{ '/storytelling/' | relative_url }})
