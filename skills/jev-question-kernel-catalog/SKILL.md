---
name: jev-question-kernel-catalog
description: Select, adapt, or evaluate a bounded Jev question pattern from the public catalog when typed JSON judgments need clear state, criteria, follow-ups, and code-owned safeguards.
---

# Jev Question Kernel Catalog

Use this skill when a task needs one bounded semantic judgment with a typed Jev result—not an open-ended recommendation, a calculation, a permission decision, or an autonomous action.

The public pattern catalog is a set of synthetic-screened examples, not a production
runtime or an accuracy guarantee. Start with the question kernel at
../../iterations/03/question-kernel.md, then open the individual public pattern page
whose input relation and controller outcome actually match the task.

## Choose the smallest fitting pattern

- **Business B15–B21:** commercial identity, pricing language, delivery evidence, project dependencies, billing support, renewal, and recurring-service rules.
- **Engineering E15–E21:** diagnostic evidence, configuration precedence, migration disposition, replay evidence, cache freshness, cancellation, and error ownership.
- **LLM L13–L18:** entity alignment, RAG lanes, text continuation, corpus answerability, detailed skill re-checks, and decision-depth routing.
- **Harness H21–H30:** snapshot binding, candidate coverage, two-stage re-checking, score/veto composition, structure recovery, retrieval routing, merge holds, bounded fan-out, numeric boundaries, and RAG ledgers.

Do not pick a pattern merely because the nouns sound similar. Compare its:

1. named state relation;
2. typed output meaning;
3. caller-owned follow-up; and
4. stated limitation.

If none fit, write a new narrow contract rather than relabeling an existing one.

## Implement the question, not a chat prompt

- Supply named JSON fields containing only the evidence needed for the judgment.
- Put every answer label's complete meaning in instructions and criteria. Include an explicit insufficient, no-match, ambiguous, or review path whenever the state can fail to establish a result.
- Choose Choice for a bounded branch, Score for an ordered concrete dimension, or Noul for one narrow proposition. Batch only independent questions against the same immutable state.
- Keep expected labels outside the state in a synthetic fixture. Keep source IDs, revisions, candidate membership, calculations, permissions, writes, and external actions in code.
- If a later question needs an earlier answer, make a second request after code retrieves or constructs the new state.

## Use the result safely

Treat every result as advisory. A Choice confidence measures distribution concentration, not truth or authorization; a middle Noul probability is uncertainty, not a silent decision.

Before consuming a result, code should bind it to the current state/revision and check
the declared candidate set. Use deterministic code for dates, arithmetic, IDs,
thresholds, routing policy, and all side effects. Escalate missing, contradictory,
low-confidence, out-of-scope, or consequential cases through the task's authorized path.

## Test and record

Freeze synthetic ordinary, missing, conflict, and boundary cases before a live call. Save
the exact state, question contract, model, response, request digest, and match result.
If a case misses, retain it; alter the question or fixture only with a documented
semantic reason, version an altered contract, and rerun the affected cases. A passing
synthetic regression set is not production accuracy, calibration, security, or global
novelty.
