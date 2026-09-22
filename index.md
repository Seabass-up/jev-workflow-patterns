---
layout: default
title: Jev Workflow Patterns
description: Code-controlled Jev workflows and tested question patterns for business, engineering, LLMs and harnesses.
permalink: /
kicker: A practical pattern catalog
---

<div class="hero">
  <h2>Make the question precise. Keep the workflow under code control.</h2>
  <p>Jev evaluates the state you provide and returns typed judgments such as Choice, Score, or Noul. These patterns show how to shape that input, decide when to ask a follow-up, preserve evidence lineage, and avoid recomputing unchanged judgments.</p>
</div>

## New question catalog

[Iteration 1: 20 business, engineering and LLM patterns plus 10 experimental harness designs]({{ '/iterations/01/' | relative_url }}) includes individual pages, exact question JSON, follow-up policies, synthetic fixtures, preserved failures and offline controller tests.

Initial core screening matched 76/81 fixtures; a targeted refinement matched 15/15; harness screening matched 38/40. These are small design checks, not production accuracy or proof of global novelty. [Read the evaluation]({{ '/iterations/01/evaluation/' | relative_url }}).

## Three foundational patterns

<div class="card-grid">
  <section class="card">
    <span class="tag">Bounded extension</span>
    <h3><a href="{{ '/patterns/evidence-directed-allowlist-controller/' | relative_url }}">Evidence-directed allowlist controller</a></h3>
    <p>Ask a fixed target question first. If it remains unresolved, let Jev choose only from a caller-approved source catalog, then fetch and re-ask within explicit limits.</p>
    <p><a href="https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-evidence-directed-retrieval/SKILL.md">Open the Codex skill</a></p>
  </section>
  <section class="card">
    <span class="tag">New composition</span>
    <h3><a href="{{ '/patterns/lineage-aware-corroboration/' | relative_url }}">Lineage-aware corroboration</a></h3>
    <p>Judge one source at a time and count verified independent origins—not copies—as support, while preserving contradictions and review conditions.</p>
    <p><a href="https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-lineage-corroboration/SKILL.md">Open the Codex skill</a></p>
  </section>
  <section class="card">
    <span class="tag">New composition</span>
    <h3><a href="{{ '/patterns/dependency-dag-selective-recomputation/' | relative_url }}">Dependency-DAG selective recomputation</a></h3>
    <p>Fingerprint declared state projections and upstream outputs so unchanged judgments can be reused and only affected parts of a dependency graph are rerun.</p>
    <p><a href="https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-dag-recomputation/SKILL.md">Open the Codex skill</a></p>
  </section>
</div>

## Shared rules

- **State is evidence and context; questions are the judgments.** Use named JSON fields so each fact has a clear role.
- **Make each question answerable.** Name the subject, criteria, exclusions, and an explicit no-match or insufficient outcome where relevant.
- **Batch independent questions; sequence dependent ones in code.** A Jev question cannot see another question's answer from the same request.
- **Treat answers as advisory.** Code owns identity and revision checks, budgets, thresholds, cache scope, escalation, and actions.
- **Test outcomes, not just JSON shape.** Confidence is not a correctness guarantee or permission to act.

See the official [TypeSafe System One overview](https://docs.typesafe.ai/concepts/system-one), [state guide](https://docs.typesafe.ai/concepts/state), [question primitives](https://docs.typesafe.ai/primitives), and [confidence guide](https://docs.typesafe.ai/confidence).

<div class="callout warning">
  <p><strong>What this site includes:</strong> three foundational pattern guides and skills, plus separately versioned question catalogs with synthetic receipts and pure demonstration controllers. It does not ship a TypeSafe SDK, secrets, local workflow configuration, production integrations, or private business records.</p>
  <p>The original three-pattern prototype was exercised with 133 offline tests and five synthetic live Jev smoke calls on 2026-09-21; its local runtime and receipts remain outside this repository. Later iteration directories publish their own synthetic fixtures and results explicitly. Neither evidence track establishes production accuracy, calibration, or general reliability.</p>
</div>

## Public pages and skill files

Each pattern page includes a state/question example, the expected wrapper output, code-owned controls, limitations, and a link to its matching skill. The public [repository](https://github.com/Seabass-up/jev-workflow-patterns) contains the original skill source files under `skills/`.
