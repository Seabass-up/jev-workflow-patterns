---
layout: default
title: "Contract review support: patterns for clauses, obligations, and redlines"
description: "Eight question contracts for contract review support: clause type, obligated party, reciprocal or one-sided drafting, term expressions, redline comments, defined-term use, notice elements, and carve-outs."
permalink: /legal-contracts/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Contract review support

Contract operations staff and paralegal assistants prepare an agreement for a lawyer by filing clauses under headings, building an obligations register, flagging one-sided drafts, filling the term and notice columns, and triaging redline comments. These eight contracts classify the clause and comment text that work runs on. They are synthetic, task-authored designs and every label is advisory: it organizes the review, and the lawyer reads everything. No label says whether a clause is enforceable, how much risk it carries, or what a party should do.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/legal-contracts/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/legal-contracts/evaluation/' | relative_url }})

## What the screen established

**23/24 design cases and 8/8 challenge cases** matched their prewritten labels: 31/32 overall. LC02 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Clause reading

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LC01 | [Clause type from the clause text]({{ '/legal-contracts/patterns/lc01/' | relative_url }}) | Files clauses pulled from an unfamiliar agreement under checklist headings without a person reading each one first; the lawyer still reads every clause. |
| LC02 · provisional | [Which named party a clause obligates]({{ '/legal-contracts/patterns/lc02/' | relative_url }}) | Builds an obligations register by party without a person re-reading every clause; the lawyer confirms the register. |
| LC03 | [Clause is reciprocal, asymmetric, or one-sided as written]({{ '/legal-contracts/patterns/lc03/' | relative_url }}) | Flags one-sided drafts of clauses that are often exchanged reciprocally, such as confidentiality or indemnity, before the lawyer reads the draft. |

## Term, notice, and exception mechanics

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LC04 | [What a term expression describes]({{ '/legal-contracts/patterns/lc04/' | relative_url }}) | Fills the term column of the contract register from the expression itself, without the model computing an end date or a notice deadline. |
| LC07 | [Notice method and recipient are stated]({{ '/legal-contracts/patterns/lc07/' | relative_url }}) | Lists the notice provisions that lack a delivery method or a recipient before the lawyer reads the draft; addresses and deadlines stay in code. |
| LC08 | [Clause states an exception to its own rule]({{ '/legal-contracts/patterns/lc08/' | relative_url }}) | Lists every carve-out and every cross-referenced exception for the lawyer to check, without a person scanning each clause for exception language. |

## Redlines and defined terms

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LC05 | [Redline comment is substantive, editorial, or a question]({{ '/legal-contracts/patterns/lc05/' | relative_url }}) | Separates the comments a lawyer must decide from the ones a paralegal can resolve, without a person triaging the whole comment list first. |
| LC06 | [Defined term is used in the sense its definition gives]({{ '/legal-contracts/patterns/lc06/' | relative_url }}) | Catches drift between a definition and its uses before the lawyer reads the draft; code owns the exact matching of the term. |

## Start with a small bundle

Start with LC01 (clause type) to file clauses, LC02 (obligated party) to build the obligations register, LC05 (redline comment) to order the lawyer's comment queue, and LC07 (notice elements) to fill the notices table. Add LC04 once code extracts term expressions, and LC03, LC06, and LC08 for the flag lists the lawyer works from.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of clause or comment text, not legal advice. Code owns exact matching of party names and defined terms, clause numbering, cross-reference resolution, every date, period, and deadline, and the acceptance or rejection of any change; people own every legal conclusion. Nothing in this collection decides enforceability, risk, fairness, or what a party should do, and the reviewing lawyer's reading overrides any label.

[Exact catalog]({{ '/legal-contracts/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/legal-contracts/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/legal-contracts.md)
