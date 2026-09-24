---
layout: default
title: "Sales operations: patterns for prospect messages, objections, and pipeline notes"
description: "Eight question contracts for sales text: what a prospect asks for, objection kind, stated buying signals, proposal responses to requirements, follow-up timing, discount requests against policy text, pipeline next steps, and competitor mentions."
permalink: /sales/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Sales operations

Sales teams and CRM assistants read prospect messages, objections, proposal drafts, discount requests, and pipeline notes all day. These eight contracts classify that text so the right person, material, or reminder is used. They are task-authored, advisory designs: a label is a reading of what the text says. Amounts, dates, pipeline stages, pricing, and approvals stay in code and with people.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/sales/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/sales/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 7/8 challenge cases** matched their prewritten labels: 31/32 overall. SA08 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Prospect messages

| ID | Question pattern | Intended use |
| --- | --- | --- |
| SA01 | [What a prospect message asks for]({{ '/sales/patterns/sa01/' | relative_url }}) | Routes inbound prospect messages by what they ask for instead of by keyword, while the account owner keeps the reply. |
| SA02 | [Which kind of objection the prospect raises]({{ '/sales/patterns/sa02/' | relative_url }}) | Separates price, timing, authority, and need objections consistently so responses match the concern rather than the rep's guess. |
| SA03 | [Which buying signal the prospect states]({{ '/sales/patterns/sa03/' | relative_url }}) | Fills qualification fields from what the prospect actually wrote and flags messages that state nothing, while code keeps amounts and dates. |
| SA08 · provisional | [What a competitor mention does in the message]({{ '/sales/patterns/sa08/' | relative_url }}) | Routes comparison questions to the right material and incumbent situations to the right play without a rep re-reading every mention. |

## Proposals and pricing

| ID | Question pattern | Intended use |
| --- | --- | --- |
| SA04 | [Proposal section responds to a stated requirement]({{ '/sales/patterns/sa04/' | relative_url }}) | Builds the compliance matrix from the proposal's own words and catches requirements the draft never answers before it is sent. |
| SA06 | [Discount request is one the policy text describes]({{ '/sales/patterns/sa06/' | relative_url }}) | Sends requests the policy already covers to the standard path and everything else to a person, while code checks every percentage and threshold. |

## Pipeline notes

| ID | Question pattern | Intended use |
| --- | --- | --- |
| SA05 | [How a follow-up commitment names its time]({{ '/sales/patterns/sa05/' | relative_url }}) | Lets code schedule reminders from specific commitments and flag vague ones for the rep, without the model resolving any date. |
| SA07 | [CRM note records an agreed next step]({{ '/sales/patterns/sa07/' | relative_url }}) | Finds opportunities with no agreed next step from the notes themselves, without moving a stage or judging the rep. |

## Start with a small bundle

Start with SA01 (what the message asks for), SA03 (which buying signal it states), SA07 (whether the note records an agreed next step), and SA05 (how a follow-up names its time). Together they route the inbound message, fill qualification from the prospect's words, and find opportunities with no timed next step, while code keeps every amount, date, and stage.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a sales decision. Code matches competitor names, compares discount percentages and thresholds against policy, resolves follow-up times to dates, sets pipeline stages, and sends nothing on its own. Pricing, concessions, approvals, and compliance claims in proposals stay with the account owner, the approver named in policy, and the proposal owner. No label judges a prospect or a rep, only the supplied text. Substantiation of any claim about a competitor and the legal compliance of proposal and pricing statements stay with people.

[Exact catalog]({{ '/sales/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/sales/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/sales.md)
