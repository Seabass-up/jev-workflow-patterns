---
layout: default
title: "Cybersecurity operations: patterns for triage, requests, and advisories"
description: "Eight question contracts for security operations text: the ask a reported email makes, an alert narrative against its stated context, an advisory's named products against an asset description, a report against a severity definition, an access-request justification, a policy-exception request's compensating control, an authentication log outcome, and a vendor questionnaire answer."
permalink: /cybersecurity/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Cybersecurity operations

A security operations analyst reads the same kinds of text all day: an email a user reported, an alert with someone's explanation attached, a vendor advisory against the asset inventory, an incident report against the severity scale, an access request, an exception request, a log line, a vendor's questionnaire answer. These eight contracts classify that text so the queue, the ticket, and the reviewer get a consistent first reading. They are synthetic, task-authored designs and every label is advisory. Nothing here describes attack techniques or tooling; indicator matching, version comparison, thresholds, containment, and every access decision stay with code and people.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/cybersecurity/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/cybersecurity/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 7/8 challenge cases** matched their prewritten labels: 31/32 overall. CY02 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Triage

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CY01 | [What a user-reported email asks the recipient to do]({{ '/cybersecurity/patterns/cy01/' | relative_url }}) | Sorts the report queue by the ask the message actually makes instead of by the reporter's guess, while sender checks, quarantine, and finance notification stay with code and the analyst. |
| CY02 · provisional | [Alert narrative accounted for by the stated context]({{ '/cybersecurity/patterns/cy02/' | relative_url }}) | Keeps an analyst from closing an alert on an explanation that covers only part of what was observed, while the truth of the explanation is verified by people. |
| CY04 | [Incident report states the conditions a severity definition requires]({{ '/cybersecurity/patterns/cy04/' | relative_url }}) | Applies the organization's own severity wording to a report consistently, while the incident lead assigns the severity and code compares any numeric thresholds. |
| CY07 | [Authentication outcome described by a log event]({{ '/cybersecurity/patterns/cy07/' | relative_url }}) | Normalizes the wording of many systems' authentication messages into one outcome label, while counting, thresholds, and account actions stay in code. |

## Requests and reviews

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CY05 | [Access request justification is bound to a stated task]({{ '/cybersecurity/patterns/cy05/' | relative_url }}) | Sends requests with a task-bound justification to a quick approval path and the rest back to the requester, while the approver keeps the decision and code keeps the permission model. |
| CY06 | [Policy-exception request names a compensating control]({{ '/cybersecurity/patterns/cy06/' | relative_url }}) | Separates requests that come with a compensating control from those that ask to drop a requirement outright, before the risk owner reviews them. |
| CY08 | [Vendor questionnaire answer is responsive to the question asked]({{ '/cybersecurity/patterns/cy08/' | relative_url }}) | Points reviewer time at the answers that need follow-up instead of reading every answer in full, while the adequacy of each described practice stays with the reviewer. |

## Advisories

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CY03 | [Advisory names the product an asset description runs]({{ '/cybersecurity/patterns/cy03/' | relative_url }}) | Filters the advisory feed by what each asset is described as running before exact version and build comparison in code, instead of a person reading every advisory against the inventory. |

## Start with a small bundle

For the report queue, CY01 (what a reported email asks) with sender, link, and attachment checks in code, and CY07 (authentication outcome) with counting and thresholds in code. For alert and incident handling, CY02 (stated context against the narrative) and CY04 (severity definition against the report) with the analyst's disposition recorded as authoritative. For the review desk, CY05 (access justification) and CY06 (compensating control) with the approver and risk owner deciding.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a security determination. Code matches sender domains, link hosts, hashes, addresses, and product identifiers exactly, compares versions and numeric thresholds, counts events, and applies the permission model. People verify explanations, assign severity, decide access and exceptions, judge vendor answers, and carry out every containment, blocking, and notification step. No contract describes exploitation, evasion, or attack tooling, and no label declares a message malicious or safe.

[Exact catalog]({{ '/cybersecurity/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/cybersecurity/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/cybersecurity.md)
