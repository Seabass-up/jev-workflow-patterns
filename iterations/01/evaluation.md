---
layout: default
title: "Iteration 1 evaluation"
description: "What the Jev pattern tests establish, what failed, and what remains unproven."
permalink: /iterations/01/evaluation/
---

[Catalog]({{ '/iterations/01/' | relative_url }})

## Outcome

Thirty question patterns were authored and screened using the existing Jev bridge, model `jev-1.13.0`, on 2026-09-22. All provider calls succeeded; semantic failures remain in the record. This is a **design screen**, not a validation of field accuracy, calibration, business value or autonomous operation.

| Screen | Live requests | Fixtures matching declared expectations | Labeled question matches | Provisional threshold-decided labeled answers | Matches among threshold-decided answers |
| --- | ---: | ---: | ---: | ---: | ---: |
| Initial 20 core patterns | 81 | 76/81 | 99/104 | 93/104 | 93/93 |
| Targeted refinement | 15 | 15/15 | 31/31 | 31/31 | 31/31 |
| Ten harness components | 40 | 38/40 | 41/44 | 41/44 | 39/41 |

The threshold metric uses Choice/Score confidence ≥ 0.8 or Noul ≤ 0.2 / ≥ 0.8. It is descriptive only; it counts labeled judgments, **not** authorized actions. Two E01 scores were deliberately unlabeled because their evidence gate said missing/conflict. Ignoring an unused branch is intentional, not an omitted failure. Full raw outputs are retained.

There were **136 screening requests**, plus one source-ranking request. Eight refinement requests reused initial cases; seven were newly authored after inspecting failures. There is no independent held-out test set, blind external labeling, repeated-run stability study, long-running harness evaluation or real business data trial. The author designed both contracts and labels. Do not pool these screens into a single “accuracy” claim.

## Failures retained

- **B01-3:** A courtesy message with no work request returned `clarify` (confidence 0.57) instead of `no_match`. The original criteria explicitly overlapped: “no specific request” could be clarification or no-match. Version 2 reserves clarification for an actual requested action with unresolved meaning and explicitly sends courtesy/no-action messages to no-match.
- **B02-1, B02-2, B02-4:** Stated resident access arrangements returned 0.55, 0.28 and 0.32 instead of the declared yes range. The wording referred to a “named person” and did not explicitly isolate access from location. Version 2 accepts a stated resident/manager role and judges access independently of missing or conflicting location. This fixes the written contract ambiguity; we cannot prove the model's internal cause.
- **L05-3:** “The editor” was labeled as a clear target by the fixture author, but Jev returned 0.56. That target is genuinely underspecified. The original label/result remains unchanged. A separate diagnostic case naming the Pine Editor project matched all three expected judgments; no L05 prompt change was made.
- **H01-4:** “Do it” made both invented interpretations look plausible (0.83 and 0.86), despite no supplied referent. This is a high-probability grounding failure. A caller-owned target-binding guard blocks the fixture in the pure controller test, but does not repair or qualify the model component. **Do not adopt H01 as a target or permission inference mechanism.**
- **H09-3:** An unsolicited navigation redesign was expected as `optional_extension` but returned `unrelated` (confidence 0.41). The label boundary is debatable; both categories must stay outside current execution. The low-confidence controller holds it for review. No prompt tuning or relabeling hides this result.

## Refinement design

Only B01 and B02 contracts changed. Their eight original fixtures were replayed, then six fresh diagnostic cases tested courtesy/ambiguous/negated intent and role-based/hopeful/location-independent access. One additional L05 case tested a concrete target. All 15 matched the frozen expectations. This is targeted regression evidence, not proof of generalization.

## Code-level verification

`evaluate.py` reconstructs each exact request from its screen's preserved question contract and state, canonicalizes the JSON and recomputes the bridge's SHA-256 request digest. **136/136 receipts bind correctly.** It recomputes expected matches instead of trusting stored pass flags.

**31 offline tests passed** using Python's standard library. Tests cover output types, finite probabilities, missing/unknown answers, provider failures, unused-branch gating, counterevidence retention, dispatch clarification order, exact tool-and-argument equivalence, target-binding failure, mandatory alert preservation, bounded repair attempts and non-executing review proposals.

The first offline test run exposed an incorrect test assumption that every speculative Score needed an expected label. It was repaired to allow only E01's explicitly unused impact branch when evidence is missing/conflicting. The application gate and recorded results were unchanged.

The reference controllers are **pure demonstration functions**. They do not read real records, dispatch crews, execute tools, compact memory, send notifications, merge data, or revise delivered recommendations. Their trusted `control` metadata must come from host/code verification, never from a model or untrusted document.

## Usage and timing

| Screen | Billed input tokens reported by bridge | Estimated Jev cost (USD) | Median bridge elapsed | Maximum bridge elapsed |
| --- | ---: | ---: | ---: | ---: |
| Core initial | 38,472 | 0.001615824 | 546.195 ms | 710.823 ms |
| Refinement | 7,723 | 0.000324366 | 539.582 ms | 850.896 ms |
| Harness | 20,262 | 0.000851004 | 637.298 ms | 771.999 ms |

Screening total: **66,457 input tokens; estimated $0.002791194**. Including the separate source-ranking call: **69,256 input tokens; estimated $0.002908752**. These are bridge estimates, not an independently reconciled provider invoice. They exclude Codex work, browsing, implementation, publication and human review; they are not a measured total-workflow saving.

Independent questions for one fixture were batched in that fixture's request. Fixture requests were dispatched through three workers, with bridge serialization where applicable. Elapsed values are bridge-observed request times, including its local waiting; not pure model latency or an end-to-end production SLA. Cache was disabled and no automatic retries were made.

## Next adoption gate

Choose one narrow pilot; create an authorized domain sample with independent labels, critical counterexamples, abstentions and a simple non-Jev baseline. Measure wrong decisions, coverage, follow-up turns, review time and actual end-to-end outcomes. Predeclare thresholds according to consequences. Keep exact arithmetic, identity, authority, freshness and actions in code. Promote only when the pilot demonstrates useful results; four research cycles will not by themselves qualify any pattern for production.
