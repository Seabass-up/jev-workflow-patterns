---
layout: default
title: "Iteration 2 Evaluation"
description: "Versioned synthetic Jev evaluation receipts, preserved misses, and final contract acceptance."
permalink: /iterations/02/evaluation/
kicker: "Evaluation · Synthetic design checks"
---

[← Iteration 2 catalog]({{ '/iterations/02/' | relative_url }}) · [Question kernel]({{ '/iterations/02/question-kernel/' | relative_url }}) · [Raw summary JSON]({{ '/iterations/02/results/summary.json' | relative_url }})

# Evaluation: preserve the miss, repair the contract, rerun the affected case

This is a small synthetic design evaluation. It tests whether a fixed, typed question contract produces its intended answer on deliberately constructed cases. It does not measure production accuracy, real-world calibration, safety, security, legal compliance, or global novelty.

## Result timeline

| Stage | Requests | Fixture matches | Question checks | What it means |
| --- | ---: | ---: | ---: | --- |
| Initial core v1 | 86 | 80 | 85 / 91 | Six question-contract or fixture ambiguities were found. |
| Initial harness v1 | 48 | 44 | 52 / 56 | Four harness ambiguities were found. |
| Core refinement v2 | 17 | 15 | 15 / 17 | Two L09 taxonomy overlaps remained visible. |
| Harness refinement v2 | 8 | 8 | 12 / 12 | H11 and H19 revisions matched their revised cases. |
| L09 refinement v3 | 5 | 5 | 5 / 5 | The final taxonomy distinction matched all five cases. |
| H19 terminology v3 | 4 | 4 | 8 / 8 | Criteria were aligned to the named proposed_action state field and retested. |
| Final selected contracts | 134 | 134 | 147 / 147 | Latest receipt per final contract and fixture. |

The 168 recorded calls used 84,112 billed input tokens with an estimated provider cost of $0.003532704. Those values are preserved in the raw receipts and are historical observations, not a future price quote.

## Initial misses and what changed

| Pattern | Finding | Repair |
| --- | --- | --- |
| B08 | Generic policy language was treated as a prohibition. | Version 2 says generic ordinary-procedure wording is insufficient unless it expressly defines a prohibition or review route. |
| E13 | Unspecified normal metrics were treated as a proxy for an invariant. | Version 2 requires a named measurement and relation before classifying a proxy. |
| L09 | Failure taxonomy mixed unmet requirements, malformed representation, and a voluntary design request. | Version 2 first clarified no-match and precedence; version 3 separates semantic/capability omissions from malformed wire representations. |
| L11 | A vague answer plan and an evidence-complete plan had overly sharp score expectations. | Version 2 made output/source/limitation obligations explicit and made the synthetic no-plan case actually contain no plan. |
| H11 | A visual-change request was forced into a software-support child. | Version 2 makes a non-failure change request a no-match and retains the broader taxonomy node. |
| H19 | Severity was expected even though the case stated no consequence; later copy still referred to a message field that no longer existed. | Version 2 separates proposed action from stated effect; version 3 aligns criteria to proposed_action and retests it. The score may only rate an effect that the state explicitly provides. |

This is exactly why the catalog reports pre-refinement misses. Updating a question after inspecting a test set can make a regression check perfect; it cannot establish generalization. A production candidate would need held-out, independently adjudicated, representative data and predeclared acceptance criteria.

## Repeated-decision check

H12 repeated each of four low-stakes synthetic cases three times with cache disabled. Each group produced the same choice label across its three calls. That is a 4-group observation, not proof that repeated agent decisions are generally stable. The controller still routes disagreement, low confidence, high consequence, or an unverified rule to review.

## Receipt integrity

The offline verifier checks all of the following without a provider call:

- Every receipt has a typed answer shape that matches its recorded question contract.
- Each saved request digest binds the exact model, synthetic state, and question object.
- Expected labels do not appear anywhere in the state submitted to Jev.
- Saved observations and match flags recompute from the raw typed answer.
- Final acceptance uses the latest receipt for each pattern contract: v1 for unchanged patterns, v2 for B08/E13/L11/H11, and v3 for L09/H19.
- The pure controller demonstrations return a proposal or review route only; no demonstration executes an operation.

Run locally from this directory:

~~~text
python3 evaluate.py
python3 -m unittest -v test_evaluate.py
~~~

[Open all result receipts]({{ '/iterations/02/results/' | relative_url }}) · [Open the standalone evaluator]({{ '/iterations/02/evaluate.py' | relative_url }})
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
## H18 counterevidence precedence revision — 2026-09-26, local only

H18 v1 allowed a missing counterevidence obligation to satisfy both `partial` and
`counterevidence_unaddressed`. V2 first uses `insufficient` for an unmatchable plan
or ledger, then prioritizes omitted or misrepresented direct counterevidence over
ordinary missing obligations. Original H18 v1 and its four fixtures are preserved
in `results/h18-pre-review-contract.json`; all initial provider receipts remain.

One uncached rerun of the four unchanged cases plus three frozen new synthetic
development cases matched 7/7 labels. The unmatchable-subject and addressed-counterevidence
cases returned confidence 0.32 and 0.59 respectively; consumer tests verify both
route to review under the provisional 0.8 gate. This is not independent held-out
accuracy or production qualification. `h18-review-v2` adds seven exact request bindings,
for 175 total; the final historical fixture selection remains 134/134 and 147/147
question matches. The evaluator rejects changed original states/expectations and
revision receipts not bound to the current H18 contract. No push or deployment.
