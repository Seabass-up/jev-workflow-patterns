---
layout: default
title: "Iteration 3 · Jev Question Patterns"
description: "Thirty synthetic-screened Jev question contracts for commercial, engineering, LLM, and harness decisions."
permalink: /iterations/03/
kicker: "Iteration 3 · 30 versioned typed-decision patterns"
---

[← Pattern home]({{ '/' | relative_url }}) · [Question kernel]({{ '/iterations/03/question-kernel/' | relative_url }}) · [Evaluation]({{ '/iterations/03/evaluation/' | relative_url }}) · [Sources]({{ '/iterations/03/sources/' | relative_url }})

# Iteration 3: make the state, answer space, and follow-up explicit

This iteration adds 30 task-authored Jev contracts: seven business, seven
engineering, six LLM, and ten harness patterns. Each page exposes the exact typed
question JSON, named state fields, caller-owned controls, a simpler baseline, a direct
comparison with earlier work, and limitations.

The central rule is simple: Jev gets a narrow semantic judgment over a compact state;
code owns identity, revision, arithmetic, candidate coverage, thresholds, permissions,
side effects, and verification.

<div class="card-grid">
  <section class="card">
    <span class="tag">Frozen before live calls</span>
    <h3>61 synthetic fixtures</h3>
    <p>Expected labels are stored outside every state submitted to Jev. The public fixture file contains no private business data or credentials.</p>
  </section>
  <section class="card">
    <span class="tag">Preserved evidence</span>
    <h3>67 live receipts</h3>
    <p>The initial 58/61 fixture result and all three misses remain public. Two altered contracts and one clarified fixture were rerun; the final selected contracts match 61/61 fixtures.</p>
  </section>
  <section class="card">
    <span class="tag">Reusable guide</span>
    <h3>Catalog skill</h3>
    <p>The shared <a href="https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/SKILL.md">Jev Question Kernel Catalog skill</a> helps choose a fitting pattern without turning a typed result into an action.</p>
  </section>
</div>

## Business

| ID | Pattern | Core judgment |
| --- | --- | --- |
| [B15]({{ '/iterations/03/patterns/b15/' | relative_url }}) | Align remittance to commercial account | Same, related/review, different, or insufficient candidate relationship. |
| [B16]({{ '/iterations/03/patterns/b16/' | relative_url }}) | Commercial pricing basis | Fixed, unit-rate, time-and-materials, allowance, or unstated. |
| [B17]({{ '/iterations/03/patterns/b17/' | relative_url }}) | Delivery acknowledgement | Receipt, dispatch, documented exception, or unclear evidence. |
| [B18]({{ '/iterations/03/patterns/b18/' | relative_url }}) | Project-plan predecessor | Unblocked, waiting, unrelated, or insufficient dependency relation. |
| [B19]({{ '/iterations/03/patterns/b19/' | relative_url }}) | Billing-support bundle | Supported, missing, contradictory, or insufficient package. |
| [B20]({{ '/iterations/03/patterns/b20/' | relative_url }}) | Contract renewal mechanism | Automatic, conditioned, option, expiry, or unclear wording. |
| [B21]({{ '/iterations/03/patterns/b21/' | relative_url }}) | Recurring service trigger | One-time, calendar, condition, event, or unclear rule. |

## Engineering

| ID | Pattern | Core judgment |
| --- | --- | --- |
| [E15]({{ '/iterations/03/patterns/e15/' | relative_url }}) | Test-failure origin evidence | Product, harness, environment, or mixed/insufficient indication. |
| [E16]({{ '/iterations/03/patterns/e16/' | relative_url }}) | Configuration precedence | Override, base, explicit conflict, or insufficient rule. |
| [E17]({{ '/iterations/03/patterns/e17/' | relative_url }}) | Migration disposition | Transform, quarantine, duplicate skip, reject, or insufficient. |
| [E18]({{ '/iterations/03/patterns/e18/' | relative_url }}) | Replay/idempotence evidence | Single effect, duplicate risk, pre-effect failure, or insufficient. |
| [E19]({{ '/iterations/03/patterns/e19/' | relative_url }}) | Cache freshness relation | Fresh, stale, unverifiable source change, or no cache. |
| [E20]({{ '/iterations/03/patterns/e20/' | relative_url }}) | Cancellation boundary | Before-effects, compensation, unsupported, or insufficient. |
| [E21]({{ '/iterations/03/patterns/e21/' | relative_url }}) | Error-boundary owner | Caller, middleware, domain service, no owner, or insufficient. |

## LLM components

| ID | Pattern | Core judgment |
| --- | --- | --- |
| [L13]({{ '/iterations/03/patterns/l13/' | relative_url }}) | Entity mention alignment | Ordered different/review/same relation with companion field signals. |
| [L14]({{ '/iterations/03/patterns/l14/' | relative_url }}) | RAG passage lanes | Independent relevance, evidence, premise-conflict, and instruction-like signals. |
| [L15]({{ '/iterations/03/patterns/l15/' | relative_url }}) | Hard-wrapped continuation | Whether two adjacent lines form one sentence. |
| [L16]({{ '/iterations/03/patterns/l16/' | relative_url }}) | Corpus answerability | Whether a bounded corpus has a direct, partial, missing, or ambiguous answer. |
| [L17]({{ '/iterations/03/patterns/l17/' | relative_url }}) | Detailed skill re-check | Which detailed shortlist entry fits, or none. |
| [L18]({{ '/iterations/03/patterns/l18/' | relative_url }}) | System One decision depth | Direct, bounded comparison, multistep, or insufficient work shape. |

## Harness compositions

| ID | Pattern | Code-owned controller outcome |
| --- | --- | --- |
| [H21]({{ '/iterations/03/patterns/h21/' | relative_url }}) | Source-snapshot pin | Consume only a response whose exact fingerprint code verifies. |
| [H22]({{ '/iterations/03/patterns/h22/' | relative_url }}) | Candidate coverage | Expand or review incomplete/ambiguous candidate universes. |
| [H23]({{ '/iterations/03/patterns/h23/' | relative_url }}) | Broad then detailed re-check | Keep broad rank and allow detailed no-match. |
| [H24]({{ '/iterations/03/patterns/h24/' | relative_url }}) | Atomic scores plus veto | Compute weights in code; a named veto is non-compensable. |
| [H25]({{ '/iterations/03/patterns/h25/' | relative_url }}) | Structure recovery | Stitch first, classify blocks second, preserve characters. |
| [H26]({{ '/iterations/03/patterns/h26/' | relative_url }}) | Answerability then selection | Stop/expand before a rank becomes a forced answer. |
| [H27]({{ '/iterations/03/patterns/h27/' | relative_url }}) | Entity merge hold | Require deterministic identity proof or curator review. |
| [H28]({{ '/iterations/03/patterns/h28/' | relative_url }}) | Bounded fan-out | Batch only independent questions on one immutable snapshot. |
| [H29]({{ '/iterations/03/patterns/h29/' | relative_url }}) | Numeric boundary | Move exact arithmetic and dates to deterministic code. |
| [H30]({{ '/iterations/03/patterns/h30/' | relative_url }}) | RAG lane ledger | Keep evidence, counterevidence, and excluded instruction-like content traceable. |

## Machine-readable artifacts

[Catalog JSON]({{ '/iterations/03/catalog.json' | relative_url }}) · [Frozen fixtures]({{ '/iterations/03/fixtures.json' | relative_url }}) · [Screen manifest]({{ '/iterations/03/screens.json' | relative_url }}) · [Initial raw screen]({{ '/iterations/03/results/initial-screen.json' | relative_url }}) · [Refinement raw screen]({{ '/iterations/03/results/refinement-screen.json' | relative_url }}) · [Final acceptance selection]({{ '/iterations/03/results/final-acceptance.json' | relative_url }})

<div class="callout warning">
  <p><strong>Boundary:</strong> these are synthetic design checks, not claims of production accuracy, calibration, security, legal compliance, or global novelty. A typed answer never grants authority, performs an operation, or verifies external state.</p>
</div>
