---
layout: default
title: "Iteration 4 · Evaluation"
description: "Frozen synthetic receipt protocol and bounded results for the final Jev pattern catalog."
permalink: /iterations/04/evaluation/
kicker: "Iteration 4 · test evidence"
---

[← Iteration 4 catalog]({{ '/iterations/04/' | relative_url }}) · [Question kernel]({{ '/iterations/04/question-kernel/' | relative_url }}) · [Sources]({{ '/iterations/04/sources/' | relative_url }})

# Evaluation: freeze first, then preserve every result

Before any provider call, this iteration froze 60 synthetic fixture states (two per contract) and their expected labels outside every submitted state. The initial live screen made 60 Jev calls and matched **58/60** fixtures and **58/60** question checks. Both misses remain in [the initial raw screen]({{ '/iterations/04/results/initial-screen.json' | relative_url }}); neither was overwritten.

| Miss | Confirmed contract issue | Versioned repair | Targeted rerun |
| --- | --- | --- | --- |
| H37 quote missing | Contextual contradiction could outrank code's exact-quote-missing result. | V2 makes `quote_missing` a literal priority branch before contextual relation is evaluated. | H37 support + missing, 2/2 matched. |
| H38 feature challenger | The V1 question asked Jev to interpret a numerical RMSE comparison. | V2 asks only whether revisions/split/metric are validly bound; code owns the numeric comparison. | H38 valid binding + leakage, 2/2 matched. |

The 4 targeted V2 calls matched **4/4**. The selected current contracts match **60/60 fixtures** and **60/60 question checks**. Every raw response is bound to its returned model/state/question request digest; the offline evaluator rejects malformed probabilities, unknown choices, labels leaked into state, missing question checks, or a final selection that does not use the current fixture and question contract.

## Measured synthetic-screen cost

The 64 raw synthetic receipts used 32,178 billed input tokens and 3,736 output tokens, with estimated cost **$0.001351476** and summed provider elapsed time **27,184.934 ms**. These are this screen's receipt measurements—not an account-wide cost, latency, or accuracy claim.

- [Initial raw screen]({{ '/iterations/04/results/initial-screen.json' | relative_url }})
- [Targeted refinement screen]({{ '/iterations/04/results/refinement-screen.json' | relative_url }})
- [Final current-contract acceptance]({{ '/iterations/04/results/final-acceptance.json' | relative_url }})
- [Machine-readable summary]({{ '/iterations/04/results/summary.json' | relative_url }})

## What the screen can and cannot show

It can show agreement with these clear synthetic labels, typed receipt integrity, whether explicit boundary cases need refinement, and whether controllers fail closed on malformed/provider-failure inputs. It cannot show production accuracy, calibration, reliability under real distribution shift, security, legal compliance, human acceptance, or permission to act.

## Reproduce the offline checks

```sh
python3 iterations/04/evaluate.py
python3 -m unittest discover -s iterations/04 -p 'test_*.py' -v
```

The normal offline evaluator makes no provider call. Raw provider receipts contain only synthetic records.
## 2026-09-26 local controller evidence preflight

The advisory `plan` API now requires `state=...` as a keyword argument. Omission,
missing top-level required fields, nulls, whitespace-only strings and empty arrays
or objects return `review / missing_required_state` before model answers are used.
This repairs the previous API's inability to inspect required evidence. Iteration 1's
mandatory policy-alert override remains independent of model/evidence availability.

This is a structural presence check only: nonempty records may still be false,
stale, contradictory or incomplete internally. It does not authenticate a response,
validate nested schemas, or grant authority. Providers should also be called only
after preflight. Branch tests use explicitly supplied synthetic evidence, not proof
of real-world source grounding. Cross-iteration negative tests exercise all 120
profiles in `scripts/test_iteration_state_preflight.py`; historical question
contracts, fixtures and provider receipts are unchanged. Local repair, not deployment.
