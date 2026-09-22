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

## Jev Question Kernel v2

[Start with the kernel]({{ '/kernel/' | relative_url }}) to design a typed question,
check its evidence, and test changes. One portable skill now contains authoring,
evidence/provenance, and evaluation/drift modules, practical JSON examples, and a
local structural checker. Domain profiles connect it to all 120 research-catalog
patterns plus 12 email profiles. Skill version 2.2.0 adds a Choice-confidence
consistency check and option-count threshold guidance.

## Discovery: TypeSafe introduction review

[Read the introduction review]({{ '/discovery/introduction-review/' | relative_url }})
for claims checked against 473 preserved Jev receipts and nine pattern candidates
with an advisory duplicate screen. Choice confidence closely follows the option
count, so the 0.8 floor used by 53 earlier patterns requires top probabilities from
0.833 to 0.90. These are candidates, not a screened catalog. New patterns found
while using Jev go through the [discovery intake]({{ '/discovery/' | relative_url }}).

## New: 12 email patterns

[Browse the email catalog]({{ '/email/' | relative_url }}) for reply ownership,
current versus quoted requests, thread changes, commitments, date meaning,
scheduling, attachment claims, draft coverage, waiting responsibility, automatic
replies, invoice disputes, and closure/reopening evidence.

The current versions match 36/36 synthetic examples after two empty-input
refinements; all 42 live screening receipts and original misses are preserved.
[Read the email evaluation]({{ '/email/evaluation/' | relative_url }}).
These are advisory question profiles, not an inbox integration or an accuracy guarantee.

## Current question catalog

[Iteration 4: 30 final-cycle question contracts]({{ '/iterations/04/' | relative_url }}) adds buyer-role, purchase-intent, competitive-context, communication-preference, churn, claim-substantiation, and disclosure-evidence decisions; field-support, label/value association, test-double, trace, lint-tier, repair-impact, and upgrade-intent checks; answer-work, fidelity, retrieval-posture, answer-directness, primitive-fit, and feature-validity questions; plus repeatability, extraction, candidate-binding, canary, ingress/egress, citation, feature, fixture, and drift harness controllers.

It preserves **64 live synthetic Jev receipts**: an initial 58/60 result, both misses, four v2 targeted reruns, and a selected 60/60 current-fixture set with 60/60 current question checks. The H37 refinement makes code-confirmed missing quotes take priority; the H38 refinement moves numeric RMSE comparison from Jev into deterministic code. This is a bounded revision-aware regression check—not a production accuracy, calibration, security, legal-compliance, or novelty claim. [Read the Iteration 4 evaluation]({{ '/iterations/04/evaluation/' | relative_url }}) · [Browse the exact JSON contracts]({{ '/iterations/04/catalog.json' | relative_url }}) · [Use the shared catalog skill](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/SKILL.md).

## Earlier question catalog

[Iteration 3: 30 new question contracts and an installable catalog skill]({{ '/iterations/03/' | relative_url }}) adds commercial-account alignment, pricing, delivery, predecessor, billing-support, renewal, service-trigger, diagnostic-origin, configuration, migration, replay, cache, cancellation, error-owner, entity alignment, RAG lanes, answerability, skill re-check, decision-depth, snapshot, candidate-coverage, composite-score, structure, retrieval, merge-hold, fan-out, precision, and ledger patterns.

It preserves 67 live synthetic Jev receipts: the initial 58/61 fixture result, all three misses, six targeted reruns, and a final selected 61/61 current-fixture set with 84/84 current question checks. This is a small revision-aware regression check—not a production accuracy, calibration, security, or novelty claim. [Read the Iteration 3 evaluation]({{ '/iterations/03/evaluation/' | relative_url }}) · [Use the shared catalog skill](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/SKILL.md).

[Iteration 2: 30 versioned business, engineering, LLM, and harness patterns]({{ '/iterations/02/' | relative_url }}) adds policy-exception, owner, remedy, revision, deadline-expression, reproducibility, retry, migration, rollback, telemetry, provenance, source-span, taxonomy, stability, deterministic-date, offset, plan-invalidation, field-verification, evidence-release, policy-routing, and calibration-ledger patterns.

It preserves 168 synthetic Jev receipts: the initial misses, two version-2 L09 misses, and the later refined contracts. The latest receipt for every final fixture matched 134/134 fixtures and 147/147 question checks. This is a small regression check on an iterated synthetic set—not a production accuracy, calibration, or novelty claim. [Read the Iteration 2 evaluation]({{ '/iterations/02/evaluation/' | relative_url }}).

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

Each pattern page includes a named state contract, exact question JSON, code-owned controls, limitations, and a link to a compatible dedicated or shared skill. The public [repository](https://github.com/Seabass-up/jev-workflow-patterns) contains the source skill files under `skills/`.
