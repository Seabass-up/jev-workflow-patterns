---
layout: default
title: "Iteration 3 Sources and Boundaries"
description: "Refreshed official TypeSafe research, Jev source ranking, duplicate screen, and boundaries for the third public pattern catalog."
permalink: /iterations/03/sources/
kicker: "Sources · primary documentation and bounded design comparison"
---

[← Iteration 3 catalog]({{ '/iterations/03/' | relative_url }}) · [Source-selection receipt]({{ '/iterations/03/results/source-selection.json' | relative_url }}) · [Candidate screen]({{ '/iterations/03/results/candidate-duplicate-screen.json' | relative_url }}) · [Evaluation]({{ '/iterations/03/evaluation/' | relative_url }})

# Sources, source ranking, and duplicate boundary

The TypeSafe documentation index was refreshed on 2026-09-22 before the catalog was
designed. A bounded Jev rank call then ordered 12 already retrieved, public official-source
summaries. It used 1,624 billed input tokens, cost an estimated $0.000068208, and had
request digest <code>ee902db17e28048ff1f1cf17b26d0c529ff858f8be364dbd2cf8b97d0bfc05b5</code>.
It did not browse, establish authority, or prove novelty.

The highest ranked source mechanisms were RAG passage lanes, confidence handling,
composite scoring, entity alignment, semantic-find answerability, model limitations, and
fan-out. The catalog uses them as ingredients, not as TypeSafe-endorsed applications or
universal threshold recommendations.

## Primary sources used

- [System One](https://docs.typesafe.ai/concepts/system-one)
- [State](https://docs.typesafe.ai/concepts/state)
- [Primitives / typed questions](https://docs.typesafe.ai/primitives)
- [Confidence](https://docs.typesafe.ai/confidence)
- [Intent routing](https://docs.typesafe.ai/patterns/intent-routing)
- [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out)
- [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring)
- [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions)
- [Re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
- [Line-by-line semantic find](https://docs.typesafe.ai/cookbooks/semantic_find)
- [Structure recovery](https://docs.typesafe.ai/cookbooks/autoformat)
- [Skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion)
- [Knowledge graph entity alignment](https://docs.typesafe.ai/cookbooks/entity_alignment)
- [Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages)
- [Classification using confidence](https://docs.typesafe.ai/cookbooks/classification_using_confidence)
- [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

## Candidate comparison against earlier work

A second bounded Jev decision screen compared all 30 candidate descriptions with the 60
earlier catalog patterns. It reported no candidate as a renamed duplicate, but marked
component-level near overlaps around entity alignment, RAG lanes, answerability, staged
re-checking, and structure recovery. Those patterns were retained only because each page
states a different input relation and code-owned outcome:

- L13 is the per-pair alignment component; H27 is the controller that refuses model-only merge.
- L14 emits independent per-passage signals; H30 consumes a multi-passage ledger and assembles separate lanes.
- L16 asks whether a corpus has an answer; H26 decides whether code ranks, expands, or preserves conflict.
- L17 is an agent-skill re-check; H23 is a general candidate-catalog controller.
- L15 judges one line boundary; H25 sequences a document-wide two-pass recovery pipeline.

The complete typed duplicate screen is public as a [raw receipt]({{ '/iterations/03/results/candidate-duplicate-screen.json' | relative_url }}). It is advisory evidence for a bounded comparison—not a global novelty search.

## What these sources do not establish

- A source page does not establish that a task-authored pattern is globally new.
- A Jev rank does not make one source authoritative.
- A synthetic receipt does not prove target-domain accuracy or calibration.
- A typed probability does not approve an action or verify external state.
- No public artifact includes credentials, private records, a provider key, or a production integration.
