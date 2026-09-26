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

The evaluator checks exact state/question/version binding, label membership, numerical response structure, successful request digests, original coverage, the restricted recovery set, and that the version-2 revision changed no frozen fixture. Version-1 receipts are validated against the preserved version-1 contract, version-2 receipts against the current one. It compares its result with the saved summary. Seventeen tests cover tampered state/questions/digests, stale versions, preserved version-1 binding, malformed answers, expectation separation, retained disagreement, and failure handling.

A small pure `classify_for_review` helper demonstrates conservative status mapping: low-confidence leads remain candidates, counterevidence never becomes bug-free, and stale bindings remain unresolved. It is not a production review engine, permission checker, or source authenticator. These tests exercise the evaluator/controller—not the 48 proposed reproduction recipes.

## Usage and cost boundary

Successful screening/recovery receipts report 82,466 input and 7,007 output tokens, with summed bridge-estimated cost **$0.003463572**. The 144 refinement receipts report 86,786 input and 7,007 output tokens, summed bridge estimate **$0.003645012**; across both screens, 288 verified request digests and **$0.007108584**. Failed-call billing is unknown. Separate design consultations are excluded. These are returned estimates for this screen, not an invoice, whole-workflow cost, latency benchmark, or measured savings.

## Artifacts and next qualification

- [Exact contracts, version 2]({{ '/bug-hunting/catalog.json' | relative_url }})
- [Frozen state and labels]({{ '/bug-hunting/fixtures.json' | relative_url }})
- [Preserved version-1 contracts]({{ '/bug-hunting/results/initial-catalog.json' | relative_url }}) and [version-1 fixtures]({{ '/bug-hunting/results/initial-fixtures.json' | relative_url }})
- [All 144 original attempts]({{ '/bug-hunting/results/screening.json' | relative_url }})
- [Two recovery attempts]({{ '/bug-hunting/results/recovery.json' | relative_url }})
- [144 version-2 refinement receipts]({{ '/bug-hunting/results/refinement.json' | relative_url }}) and [every refinement attempt]({{ '/bug-hunting/results/refinement-attempts.json' | relative_url }})
- [Replay summary]({{ '/bug-hunting/results/summary.json' | relative_url }})

Before relying on a profile, build isolated executable faulty/fixed pairs and independently labeled real-source packets. Preserve source revision, callers, tests, existing guards and omissions. Run the named deterministic check. Measure false positives, missed known defects, unresolved rate, and added review effort. Do not expose private repository content beyond authorization.

[Catalog]({{ '/bug-hunting/' | relative_url }}) · [Official documentation]({{ '/bug-hunting/sources/' | relative_url }})
