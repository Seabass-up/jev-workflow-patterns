---
layout: default
title: "Human resources: patterns for documents, requests, and process routing"
description: "Eight question contracts for human-resources text: job-description requirements, policy-question routing, interview notes, concern intake, exit-interview themes, offer-letter completeness, review comments, and employee requests."
permalink: /human-resources/
kicker: "8 profiles · 36/37 labels matched · kernel 2.6.0"
---

# Human resources

An HR operations or people-team assistant reads the same kinds of text every day: a requirement line in a posting, a question in the shared inbox, an interviewer's note, a reported concern, an exit comment, an offer letter, a review comment, a request for time off or a monitor. These eight contracts classify that text so the right document check, queue, or workflow opens. They are task-authored, advisory designs: a label reads what a document says or where a request belongs, never a person's protected characteristics, health, honesty, or worth, and every employment decision stays with people.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, bounded follow-up guidance, synthetic fixtures, and a proposed verification method. Revised profiles preserve their original evidence separately and add explicitly attributed versioned cases.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/human-resources/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/human-resources/evaluation/' | relative_url }})

## What the screen established

**23/24 design cases and 13/13 challenge cases** matched their prewritten labels: 36/37 overall. HR06 remains provisional. All 37 successful current-selection request digests replay.

Current selection: 36/37 cases matched. The original version-1 screen's disagreements remain preserved; only the 3 versioned contract refinements were rerun. These adaptive regression cases are not held out. 3 current answer(s) fall below the recorded confidence review threshold and require human review.

The original v1 challenge disagreements are retained with their original requests and expected labels. Versioned reruns do not overwrite those receipts, and reviewer-authored regression cases are not independent human labels or a representative test set.

## Documents

| ID | Question pattern | Intended use |
| --- | --- | --- |
| HR01 | [Job-description requirement is essential or preferred]({{ '/human-resources/patterns/hr01/' | relative_url }}) | Lets a posting review list must-have requirements separately from nice-to-haves before a person checks that each essential one is job-related; the label reads wording, not the job. |
| HR06 · provisional | [Offer letter states every required element]({{ '/human-resources/patterns/hr06/' | relative_url }}) | Catches a merged template that dropped or doubled an element before the letter is sent; the values themselves and the approval stay with people and code. |

## Requests and routing

| ID | Question pattern | Intended use |
| --- | --- | --- |
| HR02 | [Which team a policy question belongs to]({{ '/human-resources/patterns/hr02/' | relative_url }}) | Routes questions from a shared inbox by what is asked rather than by keyword, while the owning team answers and code applies the routing table. |
| HR04 | [Route a reported concern by the organization's intake policy]({{ '/human-resources/patterns/hr04/' | relative_url }}) | Gets a concern to the process that handles it without a person re-reading every intake message, while the supplied policy text defines the routes and people handle the concern. |
| HR08 | [What an employee request asks for]({{ '/human-resources/patterns/hr08/' | relative_url }}) | Opens the right workflow from a free-text request without a person reading every message; eligibility, approval, and fulfillment stay with code and the approver. |

## Notes and feedback

| ID | Question pattern | Intended use |
| --- | --- | --- |
| HR03 | [Interview note records evidence or an opinion]({{ '/human-resources/patterns/hr03/' | relative_url }}) | Sends opinion-only notes back to the interviewer for a described example before the debrief, so the hiring discussion rests on what was observed; no label rates the candidate. |
| HR05 | [Theme of an exit-interview comment]({{ '/human-resources/patterns/hr05/' | relative_url }}) | Turns free-text exit comments into themes a people team can count across departures, while the comment itself stays the record and no label characterizes the person. |
| HR07 | [Review comment cites a specific example]({{ '/human-resources/patterns/hr07/' | relative_url }}) | Prompts a manager to add an example before a review is finalized, so the written record shows what happened; no label rates the employee or the fairness of the comment. |

## Start with a small bundle

For the shared inbox, HR02 (policy question) and HR08 (request type) with the routing table and eligibility checks in code, and HR04 (concern intake) with the organization's own policy text supplied as state. For document quality, HR06 (offer-letter completeness) and HR07 (review comment cites an example), which return text to its author rather than deciding anything.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text or a routing step, not an assessment of a person. Code owns the routing tables, eligibility and balance checks, the offer checklist and its exact values, who may send or approve, and the standing rule that any concern describing imminent physical danger is escalated regardless of label. People make hiring, pay, promotion, discipline, and separation decisions, investigate concerns, and decide whether a requirement is job-related or lawful. No label classifies or infers race, sex, age, disability, religion, national origin, health, honesty, or worth, and exit and interview text is aggregated or shared only under the organization's own consent and privacy rules.

[Exact catalog]({{ '/human-resources/catalog.json' | relative_url }}) · [37 frozen fixtures]({{ '/human-resources/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/human-resources.md)
