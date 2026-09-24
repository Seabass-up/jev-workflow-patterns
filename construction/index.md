---
layout: default
title: "Construction: patterns for RFIs, submittals, logs, and changes"
description: "Eight question contracts for general-contractor project text: RFI intent, daily-log delay cause, submittal review action, change-order basis, safety observations against a supplied stop-work list, punch-list trade routing, schedule impact statements, and closeout document type."
permalink: /construction/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Construction

A general contractor's project engineers read the same documents on every job: RFIs from subcontractors, review stamps on submittals, the superintendent's daily log, change-order narratives, safety observation cards, punch lists, schedule notes, and the closeout binder. These eight contracts classify that text so the logs and trackers can route it. They are task-authored, advisory designs: a label is a reading of what a document states, never a safety, cost, schedule, or contractual determination, and the licensed, competent, or contractually responsible person decides.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/construction/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/construction/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 7/8 challenge cases** matched their prewritten labels: 31/32 overall. CN05 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## RFIs and submittals

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CN01 | [What an RFI asks the design team for]({{ '/construction/patterns/cn01/' | relative_url }}) | Keeps substitution proposals from hiding inside the RFI log and flags field conditions that may become change requests, while the design team still answers every RFI. |
| CN03 | [Reviewer's action on a submittal]({{ '/construction/patterns/cn03/' | relative_url }}) | Lets the submittal log carry a consistent status from free-text review comments so ordering and fabrication wait for the right condition, while the project engineer confirms every release. |

## Field records

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CN02 | [Cause a daily log gives for lost time]({{ '/construction/patterns/cn02/' | relative_url }}) | Turns free-text daily logs into countable delay causes without a person re-reading a month of entries, while the contract decides which delays are excusable. |
| CN05 · provisional | [Safety observation: stop-work condition, hazard to correct, or housekeeping]({{ '/construction/patterns/cn05/' | relative_url }}) | Gets every observation card into the right queue quickly, with listed stop-work conditions notified at once, while the competent person on site decides whether work actually stops. |
| CN06 | [Trade group a punch-list item is directed at]({{ '/construction/patterns/cn06/' | relative_url }}) | Routes hundreds of punch-list items to the right trade without the superintendent re-reading each one, while cost, fault, and closure stay with people and the tracker. |

## Changes, schedule, and closeout

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CN04 | [Stated basis for a change-order request]({{ '/construction/patterns/cn04/' | relative_url }}) | Sorts incoming change requests by their stated reason without a person re-reading each narrative, while entitlement, price, and who pays stay with the contract and the people who administer it. |
| CN07 | [Schedule note states a critical-path impact]({{ '/construction/patterns/cn07/' | relative_url }}) | Flags the narratives and notices that claim a completion-date impact for the scheduler's attention without anyone computing dates, while the schedule itself remains the authority. |
| CN08 | [Closeout document type from its title and opening text]({{ '/construction/patterns/cn08/' | relative_url }}) | Sorts a closeout package into the checklist's categories without a person opening every file, while validity, amounts, and legal effect stay with people and code. |

## Start with a small bundle

Start with CN01 (RFI intent) and CN03 (submittal action) for the document logs, CN04 (change-order basis) for the change log, and CN06 (punch-list trade routing) for closeout; each feeds a tracker that already exists and each has a person who confirms before anything is answered, released, ordered, or paid. Add CN05 (safety observation) only with the project's stop-work list in state and the standing notification in code.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

Code owns RFI, submittal, change-order, and punch-list numbers and dates, ball-in-court, the schedule and every date and float calculation, day counts per delay cause, lien-waiver amounts matched to pay applications, and the mapping from trade group to subcontractor. People own every safety decision (the competent person on site decides whether work stops, and that decision overrides CN05), every design answer, submittal release, change-order entitlement and price, time extension, and the sufficiency of any warranty or lien waiver. No contract cites or applies a building code or specification section, and no label says that a condition is safe, that a delay is excusable, or that a party must pay.

[Exact catalog]({{ '/construction/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/construction/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/construction.md)
