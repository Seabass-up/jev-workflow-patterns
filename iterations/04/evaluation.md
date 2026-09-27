---
layout: default
title: "Iteration 4 · Evaluation"
description: "Frozen synthetic receipt protocol and bounded results for the final Jev pattern catalog."
permalink: /iterations/04/evaluation/
kicker: "Iteration 4 · test evidence"
---

[← Iteration 4 catalog]({{ '/iterations/04/' | relative_url }}) · [Question kernel]({{ '/iterations/04/question-kernel/' | relative_url }}) · [Sources]({{ '/iterations/04/sources/' | relative_url }})

# Evaluation: freeze first, then preserve every result

The original screen froze 60 synthetic fixture states (two per contract), with expected labels kept outside every submitted state. The initial screen made 60 Jev calls and matched **58/60** fixtures and question checks. Both misses remain in the [initial raw screen]({{ '/iterations/04/results/initial-screen.json' | relative_url }}).

| Miss | Confirmed contract issue | Versioned repair | Targeted rerun |
| --- | --- | --- | --- |
| H37 quote missing | Contextual contradiction could outrank code's exact-quote-missing result. | V2 makes `quote_missing` a literal priority branch before contextual relation is evaluated. | H37 support + missing, 2/2 matched. |
| H38 feature challenger | The V1 question asked Jev to interpret a numerical RMSE comparison. | V2 asks only whether revisions/split/metric are validly bound; code owns the numeric comparison. | H38 valid binding + leakage, 2/2 matched. |

The four targeted H37/H38 v2 calls matched **4/4**. A later whole-contract overlap review flagged 13 Iteration 4 patterns: ten Choice contracts were source-confirmed and versioned to v2; B23, B26 and H33 have no Choice question, so label-overlap screening did not apply.

The ten revised Choice contracts now cover every current label with 46 synthetic fixtures (20 existing cases plus 26 development boundaries). The retained first v2 screen matched **41/45**; its four misses remain unchanged in the [first-pass record]({{ '/iterations/04/results/overlap-v2-first-pass.json' | relative_url }}). After contract and fixture refinement, the current v2 screen matched **46/46**. The selected current contracts match **86/86 fixtures and question checks** across the original 60 cases, four H37/H38 refinements, and 26 new boundaries.

The original v1 option-pair audit covers 64 pairs. The current v2 audit covers all 77 category pairs and Jev selected only `disjoint` or `precedence_resolved`; these are advisory screens, not proof of semantic disjointness. The first L20 review's unresolved `verbatim_source`/`typed_value` pair is retained along with its resolution: any request combining distinct fidelity modes now selects `mixed_output_obligations` first. One `L24-underspecified` result remains low-confidence; it is a review case, not a forced workflow decision.

Every selected raw response is bound to its model/state/question request digest. The offline evaluator rejects malformed probabilities, unknown choices, labels leaked into provider state, missing checks, fixture-version mismatches, stale final selections, and corrupted overlap-audit requests.

## Measured synthetic-screen cost

The retained fixture-screen receipts cover 155 requests and record 91,317 billed input tokens, 9,956 output tokens, estimated cost **$0.003835314**, and 43,880.2 ms summed provider time. The retained whole-contract/pairwise audit receipts cover 17 requests and record 62,323 billed input tokens, 9,061 output tokens, estimated cost **$0.002617566**, and 5,393.581 ms summed provider time. These totals describe only the receipts retained in this iteration's artifacts; they are not account-wide measures.

- [Initial raw screen]({{ '/iterations/04/results/initial-screen.json' | relative_url }})
- [Targeted refinement screen]({{ '/iterations/04/results/refinement-screen.json' | relative_url }})
- [Preserved first v2 overlap screen]({{ '/iterations/04/results/overlap-v2-first-pass.json' | relative_url }})
- [Current v2 overlap screen]({{ '/iterations/04/results/overlap-v2-screen.json' | relative_url }})
- [Whole-contract and label-pair audit]({{ '/iterations/04/results/overlap-audit.json' | relative_url }})
- [Final current-contract acceptance]({{ '/iterations/04/results/final-acceptance.json' | relative_url }})
- [Machine-readable summary]({{ '/iterations/04/results/summary.json' | relative_url }})

## What the screen can and cannot show

It can show agreement with these clear synthetic labels, typed receipt integrity, whether explicit boundary cases need refinement, and whether controllers fail closed on malformed/provider-failure inputs. It cannot show production accuracy, calibration, reliability under real distribution shift, security, legal compliance, human acceptance, or permission to act.

## Reproduce the offline checks

```sh
python3 iterations/04/evaluate.py
python3 -m unittest discover -s iterations/04 -p 'test_*.py' -v
```

The normal offline evaluator makes no provider call. Raw provider receipts contain only synthetic records. These results do not establish production accuracy, calibration, security, legal compliance, operational permission, or deployment readiness.
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
