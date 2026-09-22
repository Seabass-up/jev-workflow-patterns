---
layout: default
title: "Iteration 2 · 30 Jev Question Patterns"
description: "Thirty versioned Jev question contracts for business, engineering, LLM, and harness workflows."
permalink: /iterations/02/
kicker: "Iteration 2 · Published 2026-09-22"
---

[← Main catalog]({{ '/' | relative_url }}) · [Evaluation]({{ '/iterations/02/evaluation/' | relative_url }}) · [Question kernel]({{ '/iterations/02/question-kernel/' | relative_url }}) · [Sources]({{ '/iterations/02/sources/' | relative_url }})

<div class="hero">
  <h2>Thirty new contracts, tested as questions rather than prompts.</h2>
  <p>Iteration 2 moves from basic routing toward policy applicability, ownership, version evidence, reproducibility, migration/rollback readiness, answer provenance, span selection, repeated-decision stability, deterministic date handling, and evidence-release controls.</p>
</div>

## What is here

- 7 business patterns: B08 through B14.
- 7 engineering patterns: E08 through E14.
- 6 LLM-workflow patterns: L07 through L12.
- 10 experimental harness designs: H11 through H20.
- 134 final synthetic fixtures and 147 final question checks.
- 168 preserved live synthetic Jev receipts, including the failed versions that led to contract refinement.

The final selected receipt for every current contract matched its synthetic fixture: 134 of 134 fixtures and 147 of 147 question checks. That is a regression check after prompt and fixture refinement, not an independent accuracy claim, calibration result, or production qualification.

## Pattern catalog

| ID | Domain | Pattern | Final synthetic receipt |
| --- | --- | --- | --- |
| [B08]({{ '/iterations/02/patterns/b08/' | relative_url }}) | business | Classify a policy-exception request | 4/4 |
| [B09]({{ '/iterations/02/patterns/b09/' | relative_url }}) | business | Identify the explicitly assigned business owner | 5/5 |
| [B10]({{ '/iterations/02/patterns/b10/' | relative_url }}) | business | Classify the remedy a customer asks for | 5/5 |
| [B11]({{ '/iterations/02/patterns/b11/' | relative_url }}) | business | Classify a field-service task by work mode | 5/5 |
| [B12]({{ '/iterations/02/patterns/b12/' | relative_url }}) | business | Classify approval evidence without granting approval | 4/4 |
| [B13]({{ '/iterations/02/patterns/b13/' | relative_url }}) | business | Assess whether a document revision applies to current work | 4/4 |
| [B14]({{ '/iterations/02/patterns/b14/' | relative_url }}) | business | Select the stated deadline expression, then resolve it in code | 5/5 |
| [E08]({{ '/iterations/02/patterns/e08/' | relative_url }}) | engineering | Classify reproducibility evidence for a reported failure | 4/4 |
| [E09]({{ '/iterations/02/patterns/e09/' | relative_url }}) | engineering | Classify retry safety from stated operation semantics | 4/4 |
| [E10]({{ '/iterations/02/patterns/e10/' | relative_url }}) | engineering | Classify a schema-rollout compatibility posture | 4/4 |
| [E11]({{ '/iterations/02/patterns/e11/' | relative_url }}) | engineering | Classify rollback readiness of a deployment plan | 4/4 |
| [E12]({{ '/iterations/02/patterns/e12/' | relative_url }}) | engineering | Check runbook precondition coverage | 4/4 |
| [E13]({{ '/iterations/02/patterns/e13/' | relative_url }}) | engineering | Classify telemetry coverage of an operational invariant | 4/4 |
| [E14]({{ '/iterations/02/patterns/e14/' | relative_url }}) | engineering | Classify the evidentiary status of an incident causal statement | 4/4 |
| [L07]({{ '/iterations/02/patterns/l07/' | relative_url }}) | llm | Select an answer-bearing source span from bounded candidates | 4/4 |
| [L08]({{ '/iterations/02/patterns/l08/' | relative_url }}) | llm | Classify input text role before prompt assembly | 5/5 |
| [L09]({{ '/iterations/02/patterns/l09/' | relative_url }}) | llm | Choose a child in an LLM-failure taxonomy | 5/5 |
| [L10]({{ '/iterations/02/patterns/l10/' | relative_url }}) | llm | Classify a draft assertion's provenance mode | 4/4 |
| [L11]({{ '/iterations/02/patterns/l11/' | relative_url }}) | llm | Score evidence coverage of an answer plan | 4/4 |
| [L12]({{ '/iterations/02/patterns/l12/' | relative_url }}) | llm | Classify whether a candidate instruction applies to the current task | 4/4 |
| [H11]({{ '/iterations/02/patterns/h11/' | relative_url }}) | harness | Confidence-backed taxonomy traversal with broad fallback | 4/4 |
| [H12]({{ '/iterations/02/patterns/h12/' | relative_url }}) | harness | Repeated-decision stability gate | 12/12 |
| [H13]({{ '/iterations/02/patterns/h13/' | relative_url }}) | harness | Date expression projection and deterministic calendar gate | 4/4 |
| [H14]({{ '/iterations/02/patterns/h14/' | relative_url }}) | harness | Bounded candidate extraction with offset provenance | 4/4 |
| [H15]({{ '/iterations/02/patterns/h15/' | relative_url }}) | harness | Role-separated prompt-assembly audit | 4/4 |
| [H16]({{ '/iterations/02/patterns/h16/' | relative_url }}) | harness | Pending-action invalidation on material state change | 4/4 |
| [H17]({{ '/iterations/02/patterns/h17/' | relative_url }}) | harness | Field-verification escalation cascade | 4/4 |
| [H18]({{ '/iterations/02/patterns/h18/' | relative_url }}) | harness | Answer evidence-obligation release ledger | 4/4 |
| [H19]({{ '/iterations/02/patterns/h19/' | relative_url }}) | harness | Policy hazard/severity routing matrix | 4/4 |
| [H20]({{ '/iterations/02/patterns/h20/' | relative_url }}) | harness | Human-adjudication confidence ledger | 4/4 |

## How to use this catalog

1. Start with the [question kernel]({{ '/iterations/02/question-kernel/' | relative_url }}) before copying a pattern.
2. Select the smallest pattern whose required state fields you can actually supply.
3. Keep the state factual and named; keep labels, expected answers, authority, and execution outside the Jev call.
4. Add a deterministic controller for identity, source revision, thresholds, actions, and escalation.
5. Run a fixture set that includes ordinary, missing, contradictory, and outside-taxonomy cases.
6. Preserve misses, bump the contract version, and rerun only the affected fixture set.

## Evaluation trail

The initial screen found 10 mismatches across 134 requests. A version-2 refinement found two more L09 taxonomy misses; version 3 resolved that taxonomy boundary and corrected H19 terminology to its named state field. The [evaluation]({{ '/iterations/02/evaluation/' | relative_url }}) preserves all 168 request receipts and explains why the final 100% fixture match is not a held-out result.

## Machine-readable artifacts

[Catalog JSON]({{ '/iterations/02/catalog.json' | relative_url }}) · [Final fixtures JSON]({{ '/iterations/02/fixtures.json' | relative_url }}) · [Screen manifest]({{ '/iterations/02/screens.json' | relative_url }}) · [Final acceptance selection]({{ '/iterations/02/results/final-acceptance.json' | relative_url }})

<div class="callout warning">
  <p><strong>Boundary:</strong> every sample uses synthetic data. The public catalog does not include credentials, private business records, production integrations, or authority to execute an operation. Typed answers are advisory inputs to caller-controlled code.</p>
</div>
