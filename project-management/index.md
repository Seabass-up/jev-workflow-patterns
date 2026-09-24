---
layout: default
title: "Project management: patterns for status, change, and decisions"
description: "Eight question contracts for project management text: status updates, risk register entries, change requests, blockers, meeting note items, action items, stakeholder replies, and retrospective items."
permalink: /project-management/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Project management

Project managers and their assistants read the same kinds of text every week: a status update, a risk register entry, a change request, a blocker, meeting notes, an action item, a stakeholder's reply, a retrospective card. These eight contracts classify what that text states so a digest, a decision log, or an escalation path can route it. They are task-authored designs and their labels are advisory. Schedule dates, budgets, approvals, and who is contacted stay with code and with people.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/project-management/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/project-management/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 7/8 challenge cases** matched their prewritten labels: 31/32 overall. PM02 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Status, risk, and blockers

| ID | Question pattern | Intended use |
| --- | --- | --- |
| PM01 | [Status update reports on track, at risk, or slipped]({{ '/project-management/patterns/pm01/' | relative_url }}) | Lets a portfolio view or weekly digest sort updates by what the author actually reports, while the dates and the official health rating stay with the schedule and the project manager. |
| PM02 · provisional | [Risk entry states an owner, a trigger, and a mitigation]({{ '/project-management/patterns/pm02/' | relative_url }}) | Flags incomplete register entries at intake so the risk review spends its time on the risks rather than on chasing missing columns. |
| PM04 | [Blocker waits on an internal or an external party]({{ '/project-management/patterns/pm04/' | relative_url }}) | Routes blockers to the right escalation path: a team lead for internal waits, the account or vendor contact for external ones, and the task owner for blockers that need no one else. |

## Change, decisions, and actions

| ID | Question pattern | Intended use |
| --- | --- | --- |
| PM03 | [Change request alters scope or clarifies it]({{ '/project-management/patterns/pm03/' | relative_url }}) | Keeps the change board's queue to real scope changes and lets clarifications be answered from the scope statement, without the model deciding approval. |
| PM05 | [Meeting note item records a decision, a discussion, or a deferral]({{ '/project-management/patterns/pm05/' | relative_url }}) | Builds a decision log from notes without a person re-reading every meeting, while the log keeps the note's own words. |
| PM06 | [Action item names an owner and a due expression]({{ '/project-management/patterns/pm06/' | relative_url }}) | Catches ownerless or undated actions before they leave the meeting; resolving 'by Friday' to a calendar date stays in code. |

## Stakeholders and retrospectives

| ID | Question pattern | Intended use |
| --- | --- | --- |
| PM07 | [Stakeholder reply approves, declines, acknowledges, or asks]({{ '/project-management/patterns/pm07/' | relative_url }}) | Keeps approvals from being logged on the strength of a 'thanks, received', and surfaces the questions that hold a request up. |
| PM08 | [Retrospective item points at process, tooling, staffing, or requirements]({{ '/project-management/patterns/pm08/' | relative_url }}) | Groups retrospective items by the kind of change they call for so each group reaches the person who can act on it. |

## Start with a small bundle

Start with PM01 (status update), PM05 (decision versus discussion), and PM06 (owner and due expression), because they feed the weekly digest and the decision log directly and each depends on a single text field. Add PM03 (scope change versus clarification) once the change board's routing rule is written in code.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a project determination. Code owns every date comparison and duration, the resolution of a due expression to a calendar date, the official health rating, budgets and cost effects, the party list and escalation path, and the check that a replying stakeholder holds the authority a request needs. No label approves a change, rates a risk, or grants approval; the change board, the risk owner, and the stakeholder decide. Retrospective and staffing labels describe what an item says about availability and skills, never a judgment of a person.

[Exact catalog]({{ '/project-management/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/project-management/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/project-management.md)
