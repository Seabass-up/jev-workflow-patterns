---
layout: default
title: Dependency-DAG selective recomputation
description: Reuse only judgments whose declared inputs and upstream decisions are unchanged; wait for changed dependencies before rerunning downstream questions.
permalink: /patterns/dependency-dag-selective-recomputation/
kicker: Decision reuse · dependency graphs
---

For repeated evaluations, rerunning every Jev question after any state change can waste calls. This pattern describes judgments as nodes in a dependency directed acyclic graph (DAG). Code fingerprints each node's declared inputs and upstream output hashes, reuses only exact matches, and marks dependent nodes `wait` until changed upstream answers are available.

The novelty is the selective DAG invalidation and upstream binding—not ordinary caching. It is orchestration guidance, not a Jev API feature.

## When to use it

Use it when repeated states are similar, different typed judgments depend on different state fields, and some questions genuinely depend on prior answers. A change to one field can then invalidate just its consumers instead of the entire request.

Do not use it for one-off requests or when a well-defined stable projection and cache lifecycle are unavailable. Use your application's existing durable cache/checkpoint design; this planner does not persist records, call Jev, or replace transaction and tenancy controls.

## Node and state contract

Each stable node ID declares its input projection with RFC 6901 JSON Pointers, one exact typed question, and zero or more upstream node IDs. The plan-level context includes a resolved model version, a semantic decision-policy version, and a cache scope key.

```json
{
  "state": {
    "ticket": {
      "message": "I was charged twice for order O-104.",
      "order_id": "O-104"
    },
    "account": {"plan": "standard"}
  },
  "nodes": {
    "duplicate_charge": {
      "state_pointers": ["/ticket/message", "/ticket/order_id"],
      "depends_on": [],
      "question": {
        "type": "noul",
        "instructions": "Does the ticket report two charges for the same order?"
      }
    },
    "refund_path": {
      "state_pointers": ["/account/plan"],
      "depends_on": ["duplicate_charge"],
      "question": {
        "type": "choice",
        "instructions": "Given the supplied account plan and duplicate-charge judgment, what path should the workflow consider?",
        "criteria": {
          "standard_refund_review": "Review the duplicate-charge refund under the standard policy.",
          "not_applicable": "The upstream judgment does not establish a duplicate charge.",
          "needs_review": "The supplied facts do not support a reliable path."
        }
      }
    }
  },
  "cache_scope": "tenant:example",
  "model_version": "resolved-model-id",
  "decision_policy_version": "refund-routing-v1"
}
```

The node question should have enough context to be answerable from its selected projection plus the actual upstream decision objects that code places into the execution state. The plan must not substitute a hash for a dependency's semantic answer.

## Fingerprint and output contract

Canonical SHA-256 fingerprints bind:

- stable node ID and caller-declared cache scope;
- only the selected JSON Pointer projection;
- exact question content;
- resolved model ID (not a moving alias);
- semantic decision-policy version; and
- hashes of required upstream outputs.

Each node in the plan has one action:

| Action | Meaning |
| --- | --- |
| `reuse` | The prior record has the same fingerprint and a matching output digest, and all dependencies are reusable. The bound prior output is returned. |
| `run` | Inputs changed or no acceptable record exists, while upstream outputs are ready. The item contains the typed state to send to Jev. |
| `wait` | A dependency must be recomputed first. Do not send the waiting node to Jev or cache it. Record completed upstream outputs, then re-plan. |

The output digest catches accidental mismatches; it is not a signature and does not make an untrusted cache tamper-proof. The scope value participates in the hash but is **not** a security boundary. Keep tenant data in correctly separated storage as well.

## Code-controlled execution

1. Validate unique node IDs, pointers, questions, dependency edges, graph size, and acyclicity.
2. In topological order, select the declared JSON Pointer values and compute the current fingerprint.
3. Reuse only an exact fingerprint match with a valid output digest and ready dependencies.
4. Emit `run` with the selected input values and actual reusable upstream outputs, or `wait` when an upstream result is unavailable.
5. Execute only `run` entries, validate the resulting typed decision in application code, and store it using the caller's correctly scoped cache.
6. After a parent `run` completes, record its output and plan again. The child's fingerprint now binds the actual parent output hash.

The prototype caps a graph at 128 nodes. Missing pointers and cycles fail closed. Include source revision or ETag pointers whenever freshness matters. Version the decision policy when it changes the meaning of a question; display thresholds that only affect later presentation should usually be recomputed downstream instead.

## Safety and failure handling

- The planner is not a cache store. The caller owns persistence, isolation, expiration, concurrency, and data deletion.
- A scope string cannot protect data in a shared or incorrectly partitioned store.
- Resolve model aliases before fingerprinting; a floating alias cannot establish exact model identity.
- Include evidence freshness fields in the declared state projection, or stale judgments can be reused.
- A checksum detects mismatch but does not prevent an attacker or faulty store from replacing both a result and its digest.
- Test the planner's scope-sensitive fingerprints separately from caller integration tests that prove actual cross-tenant storage isolation; the planner alone cannot verify storage boundaries.
- Test unrelated field changes, relevant field changes, model/question/policy changes, upstream invalidation, wait-then-replan, missing pointers, cycles, oversized graphs, and corrupt cache entries.

## Skill

Use [`jev-dag-recomputation`](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-dag-recomputation/SKILL.md) to design, implement, or review this selective recomputation workflow.

## Related TypeSafe guidance

[State](https://docs.typesafe.ai/concepts/state) · [Primitives](https://docs.typesafe.ai/primitives) · [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out) · [How to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)
