---
layout: default
title: "Sources and novelty boundary"
description: "Primary references used for the question contracts and the ten proposed harness compositions."
permalink: /iterations/01/sources/
---

[Catalog]({{ '/iterations/01/' | relative_url }})

Reviewed 2026-09-22. The TypeSafe [documentation index](https://docs.typesafe.ai/llms.txt) was fetched first; 18 cookbook descriptions were ranked with Jev to focus further reading. Selected primary pages were then read directly. A model rank helped choose reading order; it did not establish truth, source completeness or novelty.

## Jev's documented building blocks

- [Primitives](https://docs.typesafe.ai/primitives): closed-set judgments, meaningful question wording and independent questions.
- [State](https://docs.typesafe.ai/concepts/state): text and structured context for one request.
- [Choice](https://docs.typesafe.ai/primitives/choice), [Noul](https://docs.typesafe.ai/primitives/noul), [Score](https://docs.typesafe.ai/primitives/score): distinct output semantics.
- [Confidence](https://docs.typesafe.ai/confidence): uncertainty behavior; no universal deployment threshold.
- [HTTP API](https://docs.typesafe.ai/api): current request contract.
- [Intent routing](https://docs.typesafe.ai/patterns/intent-routing) and [composite scoring](https://docs.typesafe.ai/patterns/composite-scoring): code-controlled composition.
- [Entity alignment](https://docs.typesafe.ai/cookbooks/entity_alignment): candidate identity comparison.
- [RAG passage classification](https://docs.typesafe.ai/cookbooks/classifying_rag_passages): bounded evidence relevance.
- [Citation checking](https://docs.typesafe.ai/cookbooks/citation_check): claims judged against supplied context.
- [Extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade): narrow validation and escalation around extraction.
- [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13): limitations supporting deterministic handling of exact operations.

The business and engineering applications are authored examples using these components, not representations that TypeSafe already publishes those exact workflows.

## Related harness work

| Design | Closest inspected reference | Distinction claimed here—not global novelty |
| --- | --- | --- |
| H01 | [Structured Uncertainty guided Clarification for LLM Agents](https://arxiv.org/abs/2511.08798) | Explicit interpretation plausibility plus exact next-read equivalence; clarification itself is established prior art. Grounding failed one synthetic case. |
| H02 | [OpenHands stuck detector source](https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/conversation/stuck_detector.py) | Question-specific semantic progress rather than only equivalent repeated events. The inspected implementation compares event content while ignoring varying IDs. |
| H03 | [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | A per-branch status audit attached to a required branch ledger; preserving unresolved work during compaction is not new. |
| H04 | [Rethinking Rubric Generation](https://arxiv.org/abs/2602.05125) | Route factual, subject and preference disagreements to different recoveries. This paper is adjacent work on criteria separation, not evidence it implements this exact router. |
| H05 | [AgentDebug](https://arxiv.org/abs/2509.25370), [HarnessFix](https://arxiv.org/abs/2606.06324) | A smaller typed defect selector and bounded question-contract repair. Failure taxonomy and trace-grounded targeted repairs have clear prior art. |
| H06 | [AgentEvals](https://github.com/langchain-ai/agentevals/blob/main/README.md), [TypeSafe extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade) | Add example-versus-real-task role classification to exact argument/provenance checks; neither existing containment nor schema validation establishes this meaning. |
| H07 | [Microsoft Research notification decision analysis](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/priorities.pdf) | A bounded semantic materiality classifier within an existing notification policy. Balancing interruption and delayed-action costs is long-established work. |
| H08 | [Devil's Advocate](https://arxiv.org/abs/2405.16334) | Compare explicitly supplied diagnostic predictions before safe-cost selection. The reference is adjacent anticipatory reflection, not proof of a novel diagnostic-selection algorithm. |
| H09 | [HarnessFix](https://arxiv.org/abs/2606.06324) | A task-scope/backlog gate at proposed-step time; established harness governance is not claimed as an invention. |
| H10 | [Citation checking](https://docs.typesafe.ai/cookbooks/citation_check), [our previous DAG pattern]({{ '/patterns/dependency-dag-selective-recomputation/' | relative_url }}) | Connect changed premises to a delivered-recommendation history and correction review, rather than only recomputing a cached answer. |

The three earlier published patterns remain unchanged: evidence-directed retrieval, lineage-aware corroboration and dependency-DAG selective recomputation. These ten designs add lifecycle-specific compositions, but share components with those patterns and the 20 core questions. They are not ten independent scientific discoveries.

## Scope of the search

This was a bounded documentation-and-primary-source screen, not an exhaustive literature review, patent search or proof that no equivalent implementation exists. Papers' abstracts and relevant implementation sections were inspected; their benchmarks were not reproduced. No source's reported performance is inherited by this catalog. A plausible composition can still fail and remains valuable only if a later baseline comparison demonstrates an improvement.

Each harness page names a simpler baseline and an explicit falsifier. Actual baseline-versus-workflow experiments remain future work; the present live tests exercise the semantic components, and offline tests exercise pure controller behavior.
