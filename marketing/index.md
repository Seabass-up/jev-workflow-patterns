---
layout: default
title: "Marketing: patterns for copy, claims, and briefs"
description: "Eight question contracts for marketing text: claim support, promotional versus transactional content, calls to action, audience fit, brand voice, competitor mentions, brief completeness, and review-comment routing."
permalink: /marketing/
kicker: "8 profiles · 29/32 labels matched · kernel 2.6.0"
---

# Marketing

A marketing team and the content assistants that support it read the same kinds of text all day: a claim and the evidence offered for it, an outbound message, a draft against a persona or a brand guide, a competitor's name in copy, a brief, a reviewer's comment. These eight contracts classify that text so review queues, sending rules, and intake forms can route it. They are task-authored, advisory designs; no label approves copy, substantiates a claim, or decides what any law or regulator requires.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/marketing/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/marketing/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 5/8 challenge cases** matched their prewritten labels: 29/32 overall. MK03, MK05, MK08 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Claims and comparisons

| ID | Question pattern | Intended use |
| --- | --- | --- |
| MK01 | [Claim in copy is supported by the supplied evidence]({{ '/marketing/patterns/mk01/' | relative_url }}) | Catches copy that outruns its own evidence before a person reviews substantiation, while the substantiation and legal calls stay with people. |
| MK06 | [Competitor mention is a comparative claim or a neutral reference]({{ '/marketing/patterns/mk06/' | relative_url }}) | Surfaces comparative claims for substantiation and review before publication, without deciding whether any comparison is fair, accurate, or lawful. |

## Copy and messages

| ID | Question pattern | Intended use |
| --- | --- | --- |
| MK02 | [Promotional or transactional content under the team's definition]({{ '/marketing/patterns/mk02/' | relative_url }}) | Sorts outbound messages by content type so code can apply the organization's sending, consent, and unsubscribe rules; the primary-purpose determination and its legal consequences stay with people. |
| MK03 · provisional | [Copy asks the reader for one action, several, or none]({{ '/marketing/patterns/mk03/' | relative_url }}) | Flags copy that competes with itself or never asks for anything before it reaches a reviewer, without deciding what the call to action should be. |
| MK04 | [Copy addresses the stated audience persona]({{ '/marketing/patterns/mk04/' | relative_url }}) | Catches copy written for the wrong reader before creative review, while the persona itself and the targeting decision stay with the team. |
| MK05 · provisional | [Copy matches the supplied brand-voice guide]({{ '/marketing/patterns/mk05/' | relative_url }}) | Applies the brand guide consistently across many drafts and channels; the guide's content and every judgment of taste stay with the brand team. |

## Briefs and reviews

| ID | Question pattern | Intended use |
| --- | --- | --- |
| MK07 | [Campaign brief states goal, audience, and metric]({{ '/marketing/patterns/mk07/' | relative_url }}) | Sends incomplete briefs back before creative time is spent, without judging whether the goal is right or the metric is achievable. |
| MK08 · provisional | [Review comment on creative is about strategy or execution]({{ '/marketing/patterns/mk08/' | relative_url }}) | Routes strategy comments to the campaign owner and execution comments to the creative team without a person triaging every thread, while every decision about the work stays with those people. |

## Start with a small bundle

For claim review, MK01 (claim support) and MK06 (competitor mention) feeding the substantiation queue. For draft review, MK03 (calls to action), MK04 (audience fit), and MK05 (brand voice) with exact banned-word checks in code. Add MK02 (promotional or transactional content) when the sending team keeps its own written definition, and MK07 (brief completeness) at intake.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a substantiation, compliance, or publication decision. Code extracts claims with offsets, compares figures and banned words exactly, supplies the current revision of the brand guide, persona, and classification rule, and routes labels to the people who decide. Substantiation, legal and regulatory compliance, and the primary-purpose determination for any message stay with people; the model never judges whether a claim or comparison is lawful.

[Exact catalog]({{ '/marketing/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/marketing/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/marketing.md)
