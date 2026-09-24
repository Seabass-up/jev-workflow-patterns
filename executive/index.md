---
layout: default
title: "Executive decisions: patterns for memos, proposals, and escalations"
description: "Eight question contracts for executive memo and proposal text: the decision requested, reversibility as written, evidence type, alternatives, kind of ask, downside acknowledgement, success metrics, and escalation policy fit."
permalink: /executive/
kicker: "8 profiles · 30/32 labels matched · kernel 2.6.0"
---

# Executive decisions

A CEO's office reads a stream of memos, proposals, and escalation requests, and much of the triage is about the text rather than the merits: does the memo say what it wants decided, does the proposal name an alternative, is there a number anyone could check. These eight contracts classify that framing, evidence, and completeness so a chief of staff can return incomplete documents and order the docket. They are synthetic, task-authored designs and their labels are advisory. The decision itself, its merits, and who may approve it stay with the executives and with code.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/executive/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/executive/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 6/8 challenge cases** matched their prewritten labels: 30/32 overall. CE02, CE06 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Decision framing

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CE01 | [Memo states the decision being asked for]({{ '/executive/patterns/ce01/' | relative_url }}) | Lets a chief of staff return memos that ask for a decision without saying which one, before they take a slot on the agenda. |
| CE02 · provisional | [Proposal describes a reversible or one-way commitment]({{ '/executive/patterns/ce02/' | relative_url }}) | Flags proposals that ask for a binding commitment without saying so, and pilots that state their own exit, so scrutiny can match what is written. |
| CE05 | [The memo asks for a decision, information, or alignment]({{ '/executive/patterns/ce05/' | relative_url }}) | Routes memos to the right handling: decisions to the docket, information requests to whoever holds the answer, alignment checks to a quick reply. |

## Evidence and completeness

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CE03 | [Evidence offered is data, anecdote, or none]({{ '/executive/patterns/ce03/' | relative_url }}) | Shows at a glance whether a recommendation rests on figures, on a few stories, or on assertion, without anyone re-reading the whole document. |
| CE04 | [Alternatives considered are compared, named, or absent]({{ '/executive/patterns/ce04/' | relative_url }}) | Catches single-option proposals before the meeting so the executive team is asked to choose, not only to approve. |
| CE06 · provisional | [Risk section names a downside or only upside]({{ '/executive/patterns/ce06/' | relative_url }}) | Separates proposals that have thought about failure from those that say risks are manageable, without judging whether the named risk is the right one. |
| CE07 | [Success metric is measurable or vague]({{ '/executive/patterns/ce07/' | relative_url }}) | Makes sure every funded proposal carries a statement that could later be checked, without the model computing or validating any figure. |

## Escalations

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CE08 | [Escalation matches the supplied escalation policy]({{ '/executive/patterns/ce08/' | relative_url }}) | Keeps escalations the policy does not cover off the executive agenda and sends numeric-threshold cases to code, without the model applying the threshold. |

## Start with a small bundle

Start with CE01 (decision stated) and CE05 (kind of ask) to sort incoming memos, CE04 (alternatives) and CE06 (downside) as the completeness check returned to authors, and CE08 (escalation policy fit) with the policy text supplied by code and numeric limits compared after the label.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of memo or proposal text, never a recommendation on the decision, a judgment of the author, or a finding that a proposal is sound. Code supplies the current escalation policy revision, compares amounts, dates, and counts against limits, enforces delegated authority and approval permissions, and records who decided. No profile evaluates a person's performance, and documents about personnel, legal exposure, or unreleased financials are sent only through an authorized path.

[Exact catalog]({{ '/executive/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/executive/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/executive.md)
