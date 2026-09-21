---
name: jev-dag-recomputation
description: Use when repeated Jev decisions have explicit dependencies and changing application state should invalidate only affected decisions instead of rerunning every question.
---

# Jev Dependency-DAG Recomputation

Use this pattern to plan selective reuse for repeated evaluations with real dependencies. It is a code-owned invalidation planner, not a Jev feature or a persistent cache implementation.

## Define stable decision nodes

- Give each node a stable ID, one exact typed question, a list of declared JSON Pointers for its input projection, and explicit upstream node IDs.
- Use questions with enough meaning and criteria to produce stable typed judgments. Include no-match or insufficient outcomes when the task can genuinely be unresolved.
- Batch independent questions over the same state where useful. Add a dependency only when code cannot form the later state/options until an upstream answer exists.
- Keep presentation/composition thresholds downstream unless they change the semantic question.

## Plan and execute in code

- Fingerprint canonical node ID, only its declared state projection, exact question, resolved model version, semantic decision-policy version, cache scope, and hashes of required upstream outputs.
- Never use a floating model alias as the version fingerprint.
- Reuse only when the prior record's complete fingerprint matches, its output digest matches its value, and dependencies are ready.
- Execute only `run` entries. A `wait` entry is not executable and must not be cached; after recording completed upstream decisions, plan again so the dependent fingerprint binds the real upstream output.
- Validate Jev results before accepting them into the caller-owned cache. Retain the question, model/policy versions, state projection, and provenance needed for later audit.
- Include source revision/ETag fields in state pointers where evidence freshness matters.

The reference planner returns `reuse`, `run`, or `wait`; rejects missing pointers and cycles; and caps a graph at 128 nodes. It does not call Jev, persist a cache, provide transactions, or protect tenant boundaries. A cache-scope string affects the fingerprint but is not a security control—separate data in storage as well. SHA-256 output digests detect accidental mismatch but are not signatures or tamper-proofing.

Test both invalidation and reuse: unchanged inputs, unrelated field changes, changed declared inputs, question/model/policy changes, changed upstream output, wait-then-replan, missing pointers, cycles, and corrupted records. Separately test cross-tenant storage isolation in the caller's integration layer; the planner only fingerprints the scope string and does not prove storage separation.

For a complete node JSON example, fingerprint contract, and plan outputs, read the [pattern guide](../../patterns/dependency-dag-selective-recomputation.md) in this repository or the [published page](https://seabass-up.github.io/jev-workflow-patterns/patterns/dependency-dag-selective-recomputation/). See TypeSafe's official [state](https://docs.typesafe.ai/concepts/state), [primitives](https://docs.typesafe.ai/primitives), and [speculative fan-out](https://docs.typesafe.ai/patterns/fan-out) docs.
