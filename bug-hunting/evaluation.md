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

The evaluator checks exact state/question/version binding, label membership, numerical response structure, successful request digests, original coverage, and the restricted recovery set. It compares its result with the saved summary. Sixteen tests cover tampered state/questions/digests, stale versions, malformed answers, expectation separation, retained disagreement, and failure handling.

A small pure `classify_for_review` helper demonstrates conservative status mapping: low-confidence leads remain candidates, counterevidence never becomes bug-free, and stale bindings remain unresolved. It is not a production review engine, permission checker, or source authenticator. These tests exercise the evaluator/controller—not the 48 proposed reproduction recipes.

## Usage and cost boundary

Successful screening/recovery receipts report 82,466 input and 7,007 output tokens, with summed bridge-estimated cost **$0.003463572**. Failed-call billing is unknown. A separate one-call/two-question design consultation is excluded. These are returned estimates for this screen, not an invoice, whole-workflow cost, latency benchmark, or measured savings.

## Artifacts and next qualification

- [Exact contracts]({{ '/bug-hunting/catalog.json' | relative_url }})
- [Frozen state and labels]({{ '/bug-hunting/fixtures.json' | relative_url }})
- [All 144 original attempts]({{ '/bug-hunting/results/screening.json' | relative_url }})
- [Two recovery attempts]({{ '/bug-hunting/results/recovery.json' | relative_url }})
- [Replay summary]({{ '/bug-hunting/results/summary.json' | relative_url }})

Before relying on a profile, build isolated executable faulty/fixed pairs and independently labeled real-source packets. Preserve source revision, callers, tests, existing guards and omissions. Run the named deterministic check. Measure false positives, missed known defects, unresolved rate, and added review effort. Do not expose private repository content beyond authorization.

[Catalog]({{ '/bug-hunting/' | relative_url }}) · [Official documentation]({{ '/bug-hunting/sources/' | relative_url }})
