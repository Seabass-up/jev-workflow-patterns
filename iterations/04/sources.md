---
layout: default
title: "Iteration 4 · Sources"
description: "Fresh official TypeSafe documentation and bounded Jev source/duplicate screens."
permalink: /iterations/04/sources/
kicker: "Iteration 4 · source record"
---

[← Iteration 4 catalog]({{ '/iterations/04/' | relative_url }}) · [Question kernel]({{ '/iterations/04/question-kernel/' | relative_url }}) · [Evaluation]({{ '/iterations/04/evaluation/' | relative_url }})

# Fresh official sources and bounded comparison

The docs index was fetched before page exploration. Source material below is official TypeSafe documentation, fetched on 2026-09-22. Hashes bind the fetched text used for this task; they do not claim a source is immutable or that a later page revision says the same thing.

| Source | URL | Applied mechanism | SHA-256 at fetch |
| --- | --- | --- | --- |
| Documentation index | [Documentation index](https://docs.typesafe.ai/llms.txt) | 16013 characters fetched 2026-09-22; used to discover pages before source reads. | `not recorded in source receipt` |
| Advanced structure | [Advanced structure](https://docs.typesafe.ai/primitives/advanced.md) | Instructions, Choice options, Score levels, and Noul criteria accept structured JSON. | `73eeedee0c3ff68e5964c914ba006e4f59522fa8222e43bd960418febd13ea7f` |
| Use-case map | [Use-case map](https://docs.typesafe.ai/concepts/use-case-map.md) | Maps typed decisions to business, verification, guardrail, semantic lint, and feature-extraction workflows. | `9d193b6379d17a3ac2f236eda9f15136e32b360e78a66bef03ce59605edfac2d` |
| Self-consistency: nouls | [Self-consistency: nouls](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook.md) | Retains repeated Noul probabilities and routes threshold uncertainty to review. | `cee9cb98c52cfbf588e0dda5defd0ba0c0d78e1162df7f20ba7bed1ece9935ff` |
| Self-consistency: choices | [Self-consistency: choices](https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook.md) | Retains repeated Choice labels/probabilities and makes confidence-based abstention visible. | `e0444c2c4e9c9440595692eaa2806157d43080adc525f94fe5c204b2d7bafe36` |
| Structured-data extraction cascade | [Structured-data extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade.md) | Separates cheap extraction, per-field verification, and escalation. | `03675753d74f2a08c746afe04c4f4283b55e5c6931d58a6ca9c6268b954a1a2f` |
| Pre-parsed value extraction | [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook.md) | Code finds candidates; TypeSafe selects only a supplied candidate; code normalizes. | `c9ebb87b822ba958664b28b4e214e322dd62540c0964ea317d54da531a0fa6bd` |
| Citation check | [Citation check](https://docs.typesafe.ai/cookbooks/citation_check.md) | Use deterministic quote lookup before a Choice checks context relation to a claim. | `2497e2c62a4c5fb2d1aca1c4031fb7bd39948d27b13f18e1db07d8c5777cd529` |
| LLM guardrails | [LLM guardrails](https://docs.typesafe.ai/cookbooks/llm_guardrails.md) | Independent hazard questions and code-owned phase/policy routing; not a security proof. | `fb5935988e2c470ee0979b40e648d641b97604802093a1a6bf56d64dedd3e0d0` |
| Feature discovery | [Feature discovery](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery.md) | Question answers can form versioned numeric features; held-out evaluation remains required. | `00ee0cfff9cfd670ee87656fe38ce5f3588ac2f56cb0181b156c02a657a7f03b` |
| Jev 1.13 jaggedness | [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md) | Use literal criteria, keep math/precision in code, reduce indirection and irrelevant state. | `e69329bd32e91ac08f0bd2681ceb4aacc34923b9190e29c15c8f75d8e22950e2` |

## Jev-assisted selection and duplicate screen

The public source summaries were ranked by Jev before design. The raw request metadata and ordered candidates are in [source-selection.json]({{ '/iterations/04/results/source-selection.json' | relative_url }}). A second Jev screen compared 30 candidate designs against 90 earlier catalog patterns and three foundations. Two near-overlap candidates were rejected and replaced; remaining close comparisons are declared in [candidate-duplicate-screen.json]({{ '/iterations/04/results/candidate-duplicate-screen.json' | relative_url }}) and on the individual pages.

Jev's rank/screen is advisory. It does not establish global novelty, source authority, factual correctness, or eligibility for an operational use.
