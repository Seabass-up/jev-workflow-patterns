---
layout: default
title: "Iteration 2 Sources and Research Boundaries"
description: "Official TypeSafe documentation and bounded prior-art references used for the second Jev pattern catalog."
permalink: /iterations/02/sources/
kicker: "Sources · Discover first, then design and test"
---

[← Iteration 2 catalog]({{ '/iterations/02/' | relative_url }}) · [Source-selection receipt]({{ '/iterations/02/results/source-selection.json' | relative_url }}) · [Evaluation]({{ '/iterations/02/evaluation/' | relative_url }})

# Sources and research boundaries

The official TypeSafe documentation index was refreshed before this iteration. A single advisory Jev rank call then prioritized 18 already retrieved documentation summaries for closer reading. That call cost an estimated $0.000091392, used 2,176 billed input tokens, and did not fetch material, establish authority, or prove novelty. Its complete typed output is preserved in the [source-selection receipt]({{ '/iterations/02/results/source-selection.json' | relative_url }}).

## Primary implementation sources

- [System One overview](https://docs.typesafe.ai/concepts/system-one)
- [State](https://docs.typesafe.ai/concepts/state)
- [Primitives / questions](https://docs.typesafe.ai/primitives)
- [Confidence routing](https://docs.typesafe.ai/patterns/confidence-routing)
- [Advanced structured questions](https://docs.typesafe.ai/primitives/advanced)
- [Function calling cookbook](https://docs.typesafe.ai/cookbooks/function_calling)
- [Date extraction cookbook](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook)
- [Pre-parsed value extraction cookbook](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook)
- [Hierarchical classification cookbook](https://docs.typesafe.ai/cookbooks/hierarchical_classification)
- [LLM guardrails cookbook](https://docs.typesafe.ai/cookbooks/llm_guardrails)
- [SDE cascade cookbook](https://docs.typesafe.ai/cookbooks/sde_cascade)
- [Choice consistency cookbook](https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook)
- [Noul consistency cookbook](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook)

These sources describe TypeSafe components and examples. The patterns here are task-authored compositions of those components. They do not claim TypeSafe endorses them, and none of the documentation replaces an application-specific validation, authority, or action policy.

## Bounded prior-art comparison

H12 cites the following research only as a bounded comparison point for repeated-decision agreement. No reported metrics, methods, or claims are imported into this catalog.

- [TrACE: Don’t Overthink It: Inter-Rollout Action Agreement as a Free Adaptive-Compute Signal for LLM Agents](https://arxiv.org/abs/2604.08369)
- [When Agents Disagree With Themselves](https://arxiv.org/abs/2602.11619)
- [SAND](https://arxiv.org/abs/2507.07441)
- [How Consistent Are LLM Agents?](https://arxiv.org/abs/2605.28840)

## What source use does not establish

- A source page does not prove a new pattern is globally novel.
- A Jev ranking of sources does not make one source authoritative.
- A synthetic receipt does not validate real-world accuracy or calibration.
- A typed probability does not approve an action.
- A public page does not contain the API key, a local Keychain bridge, private records, or a production connection.

For reproducibility, use the published [catalog JSON]({{ '/iterations/02/catalog.json' | relative_url }}), [fixture JSON]({{ '/iterations/02/fixtures.json' | relative_url }}), and [offline verifier]({{ '/iterations/02/evaluate.py' | relative_url }}).
