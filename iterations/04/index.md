---
layout: default
title: "Iteration 4 · Jev Question Patterns"
description: "Thirty final-cycle synthetic-screened Jev question contracts for business, engineering, LLM, and harness decisions."
permalink: /iterations/04/
kicker: "Iteration 4 · final 30 typed-decision patterns"
---

[← Pattern home]({{ '/' | relative_url }}) · [Question kernel]({{ '/iterations/04/question-kernel/' | relative_url }}) · [Evaluation]({{ '/iterations/04/evaluation/' | relative_url }}) · [Sources]({{ '/iterations/04/sources/' | relative_url }})

# Iteration 4: choose the JSON decision shape before asking Jev

This final four-cycle catalog adds 30 task-authored Jev contracts: seven business, seven engineering, six LLM, and ten harness patterns. Each page names its state fields, exact typed question JSON, deterministic boundary, simpler baseline, comparison to earlier work, and limitations.

The kernel remains: provide a small named state, ask a narrow literal question with a closed answer space, preserve a no-evidence/unknown route, and let code own candidate coverage, arithmetic, IDs, thresholds, permissions, side effects, and verification.

<div class="card-grid">
  <section class="card"><span class="tag">Frozen first</span><h3>60 synthetic fixtures</h3><p>Two independently authored fixtures per contract are stored outside all provider state.</p></section>
  <section class="card"><span class="tag">Prior-art screen</span><h3>90 earlier contracts</h3><p>All candidates were compared with the three earlier catalogs and three foundations; near overlaps carry explicit written deltas.</p></section>
  <section class="card"><span class="tag">Bounded outcome</span><h3>Advisory JSON</h3><p>Every contract routes uncertainty to a code- or human-owned next step. No question authorizes an operation.</p></section>
</div>

## Business

| ID | Pattern | Purpose |
| --- | --- | --- |
| [B22]({{ '/iterations/04/patterns/b22/' | relative_url }}) | Classify buyer decision-role evidence | Turn a contact's stated role in a purchase into a bounded follow-up branch without assigning authority. |
| [B23]({{ '/iterations/04/patterns/b23/' | relative_url }}) | Score stated purchase-intent strength | Expose the strength of language about buying without inventing deal value or forecasting revenue. |
| [B24]({{ '/iterations/04/patterns/b24/' | relative_url }}) | Classify competitive-displacement evidence | Separate named competitive context from vague comparison language before a sales workflow prepares research. |
| [B25]({{ '/iterations/04/patterns/b25/' | relative_url }}) | Classify communication opt-out scope | Interpret the stated scope of a communications preference while code retains identity, policy, and suppression control. |
| [B26]({{ '/iterations/04/patterns/b26/' | relative_url }}) | Score customer churn-signal severity | Surface escalating departure language separately from a particular dispute, support request, or remedy. |
| [B27]({{ '/iterations/04/patterns/b27/' | relative_url }}) | Classify advertising-claim substantiation posture | Make a campaign claim's supplied support posture reviewable without treating a model result as legal clearance. |
| [B28]({{ '/iterations/04/patterns/b28/' | relative_url }}) | Classify disclosure-audience authority evidence | Keep a requester's stated relationship distinct from actual authentication and disclosure permission. |
## Engineering

| ID | Pattern | Purpose |
| --- | --- | --- |
| [E22]({{ '/iterations/04/patterns/e22/' | relative_url }}) | Classify extractor field source-support diagnosis | Detect whether an extractor's proposed field is tied to the intended source evidence before downstream use. |
| [E23]({{ '/iterations/04/patterns/e23/' | relative_url }}) | Verify cross-field label/value associations | Catch a structured output whose values appear in source text but are paired to the wrong labels. |
| [E24]({{ '/iterations/04/patterns/e24/' | relative_url }}) | Classify test-double behavioral fidelity gap | Surface whether a mock removes a behavior material to the test's claimed conclusion. |
| [E25]({{ '/iterations/04/patterns/e25/' | relative_url }}) | Classify trace-event relationship type | Separate causality evidence from same-request and merely temporal log correlation. |
| [E26]({{ '/iterations/04/patterns/e26/' | relative_url }}) | Classify semantic lint enforcement tier | Choose a safe enforcement shape for a rule instead of pretending every guideline is deterministically lintable. |
| [E27]({{ '/iterations/04/patterns/e27/' | relative_url }}) | Classify generated repair semantic impact | Distinguish formatting or constrained canonicalization from a repair that changes meaning before any write is considered. |
| [E28]({{ '/iterations/04/patterns/e28/' | relative_url }}) | Classify dependency-upgrade intent | Read release-note language about a current integration without substituting it for compatibility tests. |
## LLM components

| ID | Pattern | Purpose |
| --- | --- | --- |
| [L19]({{ '/iterations/04/patterns/l19/' | relative_url }}) | Classify answer work type before model routing | Pick a response workflow based on the requested work shape rather than treating all questions as free-form generation. |
| [L20]({{ '/iterations/04/patterns/l20/' | relative_url }}) | Classify output fidelity contract | Make the caller's required faithfulness mode explicit before it asks a model to produce JSON or text. |
| [L21]({{ '/iterations/04/patterns/l21/' | relative_url }}) | Classify retrieved-content instruction posture | Flag behavior-directing text inside retrieved material without converting that classification into an injection-safety guarantee. |
| [L22]({{ '/iterations/04/patterns/l22/' | relative_url }}) | Classify question-answer directness | Assess whether a candidate answer actually addresses the user's question, separately from whether evidence supports it. |
| [L23]({{ '/iterations/04/patterns/l23/' | relative_url }}) | Classify primitive or composition fit | Choose an output type that matches the desired JSON consumer before writing a brittle prompt-and-parse contract. |
| [L24]({{ '/iterations/04/patterns/l24/' | relative_url }}) | Classify semantic feature-question validity | Reject feature questions that leak the target, duplicate existing signals, or cannot be observed from permitted text. |
## Harness compositions

| ID | Pattern | Purpose |
| --- | --- | --- |
| [H31]({{ '/iterations/04/patterns/h31/' | relative_url }}) | Noul threshold-crossing repeat audit | Keep repeated probability samples visible when a policy threshold could change a disposition. |
| [H32]({{ '/iterations/04/patterns/h32/' | relative_url }}) | Choice plurality, agreement, and abstention audit | Expose the operational tradeoff between repeat agreement and confidence-based abstention for a Choice workflow. |
| [H33]({{ '/iterations/04/patterns/h33/' | relative_url }}) | Verified structured-extraction cascade | Compose a cheap extractor with per-field semantic verification and an explicit escalation rung. |
| [H34]({{ '/iterations/04/patterns/h34/' | relative_url }}) | Verbatim candidate-value normalization conveyor | Bind a code-found candidate span to a Jev selection and deterministic normalization without allowing model-generated values. |
| [H35]({{ '/iterations/04/patterns/h35/' | relative_url }}) | Semantic lint canary and human-disagreement controller | Admit a semantic lint change only after a fixed labeled canary exposes new disagreements for review. |
| [H36]({{ '/iterations/04/patterns/h36/' | relative_url }}) | Ingress/egress message-risk ledger | Keep independently screened input and output risks separate so code can apply phase-specific policy. |
| [H37]({{ '/iterations/04/patterns/h37/' | relative_url }}) | Quote-existence preflight and contextual support gate | Separate deterministic quote lookup from semantic contextual support before an answer cites a source. |
| [H38]({{ '/iterations/04/patterns/h38/' | relative_url }}) | Feature-matrix provenance and holdout challenger | Make semantic-feature revisions and held-out evidence bindings inspectable while deterministic code owns metric comparison. |
| [H39]({{ '/iterations/04/patterns/h39/' | relative_url }}) | Literal-boundary contract fixture controller | Exercise a new question's negations, exclusions, no-evidence cases, and conflicts before it is used as an application contract. |
| [H40]({{ '/iterations/04/patterns/h40/' | relative_url }}) | Semantic-feature drift and retraining hold | Stop a semantic-feature pipeline from silently reusing an old evaluation after question, population, or held-out behavior changes. |

## Machine-readable artifacts

[Catalog JSON]({{ '/iterations/04/catalog.json' | relative_url }}) · [Frozen fixtures]({{ '/iterations/04/fixtures.json' | relative_url }}) · [Screen manifest]({{ '/iterations/04/screens.json' | relative_url }}) · [Source selection]({{ '/iterations/04/results/source-selection.json' | relative_url }}) · [Duplicate screen]({{ '/iterations/04/results/candidate-duplicate-screen.json' | relative_url }})

<div class="callout warning"><p><strong>Boundary:</strong> synthetic screens only. They are not production-accuracy, calibration, security, legal-compliance, global-novelty, or operational-integration claims. A typed answer never grants authority or verifies external state.</p></div>
