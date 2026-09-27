---
layout: default
title: Bug-Hunting Pattern Evaluation
description: Transparent synthetic screening, preserved service failures and an unresolved disagreement.
permalink: /bug-hunting/evaluation/
---

# Bug-hunting screen — September 23, 2026

| Measure | Result |
| --- | --- |
| Profiles | 48, in eight families |
| Frozen scenarios | 144: one suspicious, one counterexample, one missing-evidence case per profile |
| Initial attempts | 144 |
| Initial successful responses | 142 |
| Initial matching labels | 141 of 142 responses; 141 of 144 planned cases |
| Initial service errors | Two HTTP 529 responses |
| Bounded recovery attempts | Two; both succeeded and matched |
| Selected successful responses | 144 |
| Selected matching labels | 143 of 144 |
| Unresolved semantic disagreement | BH41-2 |
| Successful request digests verified | 144 |

All successful screening responses used `jev-1.13.0`, with caching disabled. No question or expectation was revised after screening. All provider failures and the disagreement remain in the artifacts.

## Revision — September 26, 2026: a stated tie-break

A later review found that the shared instruction template selected `insufficient` first but never said which label wins when the evidence shows **both** a concrete violating path and a relevant guard. Version 2 of all 48 profiles adds one sentence: *If the evidence shows both a concrete violating path and a relevant guard, select risk_supported; the guard narrows the finding but does not cancel it.* The kernel's bug-hunting module states the same rule.

| Measure | Result |
| --- | --- |
| Revised profiles | 48 of 48, version 1 → 2 |
| Frozen scenarios | Unchanged; only their bound version moved to 2 |
| Refinement attempts | 144, no provider failures, no recovery calls |
| Refinement matching labels | 143 of 144 |
| Unresolved semantic disagreement | BH41-2 again: `insufficient`, confidence 0.46 |
| Version-1 artifacts | Preserved and still replayed against the preserved version-1 contract |

State and expected labels stayed frozen; the evaluator rejects any rewritten fixture. The revision was screened once, after its wording was fixed, with no further tuning. One refinement receipt (BH23-2, a matching `counterevidence`) carries probabilities that sum to 0.99 because the provider rounds them to two decimals; the evaluator now accepts the bridge's 0.02 tolerance instead of 1e-6, and still rejects larger gaps. The same case disagreeing under both wordings points at BH41's scenario or contract, not at the tie-break sentence.

## Scope revision — September 27, 2026: BH18 canonical equivalence

Review found that BH18 v2 said “visually equivalent identifiers,” while its contract and fixture concerned only identifiers declared **canonically equivalent**. Unicode distinguishes canonical equivalence from compatibility equivalence, and its separate confusable-detection standard treats visual look-alikes as a security-detection problem—not as an identifier-normalization rule. The catalog, page, and kernel reference now scope BH18 v3 to canonical-equivalence mismatch across storage and lookup. This wording-only revision does not recommend equating arbitrary confusables.

| Measure | Result |
| --- | --- |
| Current versions | BH01–BH17 and BH19–BH48 remain v2; BH18 is v3 |
| BH18 fixture states and expected labels | Unchanged from v2 |
| BH18 v2 preservation | Full prior contract, 3 fixtures, and 3 receipts retained |
| BH18 v3 fixture re-screen | 3 uncached calls; 3/3 labels matched; no provider failures |
| Fresh BH18 v3 contract screen | `bounded`, confidence 1.00; advisory only |

The previous term was changed because it overstated the intended equivalence relation, not to tune the contract toward a preferred fixture result. The evaluator now validates the v2 receipt against its preserved BH18 snapshot and the v3 receipt against the current contract, while selecting the latest valid version per profile. The full current selection remains 143/144 because BH41-2 is still unresolved; the overall Jev screen does not qualify bug discovery on real source code.

## What the screen actually tests

These are **author-written textual scenarios**, not executed buggy/fixed code pairs. They test whether the question distinguishes a described violating path, a described guard/compliant path, and missing evidence. They do not measure discovery recall over real code, ability to follow multi-file execution, bug severity, vulnerability exploitability, or repair correctness.

The same author designed the questions and labels. Each label has only one case per profile. There is no held-out corpus, independent labeling, mutation-detection benchmark, adversarial suite, or human-time baseline. Similar cases can cue the intended answer. The three-case match status is not an operational qualification.

## Preserved failures and disagreement

- **BH09-2** and **BH39-1** returned `provider_http_529`, with no judgments. Each received one explicitly bounded recovery call using the unchanged state and question. Recovery succeeded; it does not erase the original availability failures.
- **BH41-2** expected `counterevidence`: the scenario says the installed executable resolves the intended package revision and passes an affected-path smoke. Jev selected `insufficient` at confidence 0.35. Its internal cause is unknown. BH41 remains provisional; the next check is actual path/import/build and runtime evidence, not repeated rewording until a preferred label appears.
- No transport error is represented as a negative bug finding. Confidence is validated independently of the probability of the selected option.

## Replay and demonstration controller

From the repository root:

```sh
python3 bug-hunting/evaluate.py
python3 -m unittest discover -s bug-hunting -p 'test_*.py' -v
```

The evaluator checks exact state/question/version binding, label membership, numerical response structure, successful request digests, original coverage, bounded recovery, and unchanged fixture state/expectations across revisions. Version-1 receipts bind to the v1 snapshots; v2 receipts bind to current v2 contracts or the preserved BH18 v2 snapshot; BH18 v3 receipts bind to the current v3 question. It selects current results by each profile's version and compares the result with the saved summary. Tests cover tampering, stale-version rejection, preserved v1/v2 binding, mixed current versions, malformed answers, expectation separation, retained disagreement, failure handling, and exact question/fixture parity across all 48 pages.

A small pure `classify_for_review` helper demonstrates conservative status mapping: low-confidence leads remain candidates, counterevidence never becomes bug-free, and stale bindings remain unresolved. It is not a production review engine, permission checker, or source authenticator. These tests exercise the evaluator/controller—not the 48 proposed reproduction recipes.

## Usage and cost boundary

Successful fixture responses across the v1 initial screen, v2 refinement, and selective BH18 v3 refinement report 171,075 input and 14,160 output tokens, with summed bridge-estimated cost **$0.007185150** over 291 verified digests. The first 288 digests and $0.007108584 are the preserved v1/v2 screens; BH18 v3 adds three successful responses. Failed-call billing is unknown. Separate design consultations are excluded. These are returned estimates for this screen, not an invoice, whole-workflow cost, latency benchmark, or measured savings.

## Artifacts and next qualification

- [Current exact contracts (47 v2, BH18 v3)]({{ '/bug-hunting/catalog.json' | relative_url }})
- [Frozen states and labels]({{ '/bug-hunting/fixtures.json' | relative_url }})
- [Preserved version-1 contracts]({{ '/bug-hunting/results/initial-catalog.json' | relative_url }}) and [version-1 fixtures]({{ '/bug-hunting/results/initial-fixtures.json' | relative_url }})
- [Preserved BH18 v2 contract and fixtures]({{ '/bug-hunting/results/bh18-version-2.json' | relative_url }})
- [All 144 original attempts]({{ '/bug-hunting/results/screening.json' | relative_url }})
- [Two recovery attempts]({{ '/bug-hunting/results/recovery.json' | relative_url }})
- [144 version-2 refinement receipts]({{ '/bug-hunting/results/refinement.json' | relative_url }}) and [every version-2 attempt]({{ '/bug-hunting/results/refinement-attempts.json' | relative_url }})
- [Three current BH18 v3 receipts]({{ '/bug-hunting/results/refinement-v3.json' | relative_url }}) and [version-3 attempts and recoveries]({{ '/bug-hunting/results/refinement-v3-attempts.json' | relative_url }})
- [Replay summary]({{ '/bug-hunting/results/summary.json' | relative_url }})

Before relying on a profile, build isolated executable faulty/fixed pairs and independently labeled real-source packets. Preserve source revision, callers, tests, existing guards and omissions. Run the named deterministic check. Measure false positives, missed known defects, unresolved rate, and added review effort. Do not expose private repository content beyond authorization.

[Catalog]({{ '/bug-hunting/' | relative_url }}) · [Official documentation]({{ '/bug-hunting/sources/' | relative_url }})
