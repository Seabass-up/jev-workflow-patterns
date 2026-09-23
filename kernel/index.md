---
layout: default
title: Jev Question Kernel v2
description: One reusable skill for authoring Jev questions, checking evidence, and evaluating changes.
permalink: /kernel/
kicker: Kernel v2 · one skill, three modules
---

# Ask a question your software can use

Start with the decision your application needs. Supply relevant evidence, define a
typed answer space, and specify what happens when the evidence cannot establish an
answer. The Jev Question Kernel brings authoring, evidence checks, and evaluation
into the existing `jev-question-kernel-catalog` skill.

[Open the skill](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/SKILL.md)
· [Get the complete skill folder](https://github.com/Seabass-up/jev-workflow-patterns/tree/main/skills/jev-question-kernel-catalog)

## Use the module that fits the work

| Module | What it helps you produce | Guide |
| --- | --- | --- |
| Contract authoring | A precise question, typed options, uncertainty policy, and bounded follow-up | [Authoring](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/authoring.md) |
| Evidence and provenance | Source and revision checks, exact quotation lookup, and semantic support judgments | [Evidence](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/evidence.md) |
| Evaluation and drift | Frozen cases, retained failures, repeat audits, and a decision about reevaluation | [Evaluation](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/evaluation.md) |

A new reusable question normally needs authoring and a proportionate evaluation.
Source-sensitive tasks add the evidence module. Existing use does not require
repeating a benchmark on every call.

## A concrete example

Instead of asking “analyze this payment message,” ask “does the sender explicitly
request money back?” Give a Choice consumer three defined outcomes:
`refund_requested`, `no_refund_request`, and `insufficient`.
“Do not refund me; I need a receipt” tests negation. An empty message tests missing
evidence. A contradictory message tests the review path.

The output prepares a support category. Eligibility, permissions, and the actual
refund remain separate application decisions.

[Contract example](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/contract-example.json)
· [Frozen example fixtures](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/fixtures-example.json)

These files are local authoring envelopes, not provider request schemas. Only state
and questions go into the configured Jev call. Expected answers remain local.

## Drill down with a reason

Batch independent questions over the same state. Make another request when code
needs the first answer to retrieve evidence, construct new state, or select candidates.
Declare a budget and stop when evidence is unavailable or the budget is exhausted.

A repeatability audit is a deliberate exception: repeat the same question under a
declared sample/cost budget, identify cached answers, and preserve all outcomes.
Agreement measures stability; it does not establish truth.

## Check a copied skill package

Copy the complete skill folder through your compatible skill installation workflow.
The modules, assets, and helper use paths within that folder. Installation is separate
from browsing this site; no global harness settings change automatically.

Run from the copied skill folder with Python 3:

```sh
python3 scripts/check_contract.py assets/contract-example.json assets/fixtures-example.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The helper validates selected local structure and fixture expectations without a
network call. It does not establish source authenticity, candidate completeness,
question quality, or performance on new data.

## Choose from all four catalogs

[48 bug-hunting profiles]({{ '/bug-hunting/' | relative_url }}) extend the kernel
in skill version 2.2.0. They cover concurrency, persistence, API contracts,
UI behavior, resources, trust boundaries, tests/releases, and LLM/agent workflows.
The [bug-hunting module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/bug-hunting.md)
keeps candidate judgments separate from independently verified findings.

[Twelve email profiles]({{ '/email/' | relative_url }}) now extend the kernel in
the email module introduced in skill version 2.1.0. They cover email ownership, quotes, changes, commitments,
scheduling, attachments, draft coverage, waiting, automatic responses, invoice
questions, and closure. The [email module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/email.md)
keeps mailbox evidence and action controls explicit.

[Iteration 1]({{ '/iterations/01/' | relative_url }}) ·
[Iteration 2]({{ '/iterations/02/' | relative_url }}) ·
[Iteration 3]({{ '/iterations/03/' | relative_url }}) ·
[Iteration 4]({{ '/iterations/04/' | relative_url }})

The 120 examples are optional domain profiles. Match the actual input relationship,
consumer, and limitations before adapting one. Historical contracts and synthetic
receipts retain their versions; Kernel v2 does not retroactively requalify them.

The design follows TypeSafe's [state](https://docs.typesafe.ai/concepts/state),
[question](https://docs.typesafe.ai/primitives), and
[confidence](https://docs.typesafe.ai/confidence) documentation, refreshed September 22, 2026.
Code owns exact values, calculations, policy, permissions, actions, and verification.
