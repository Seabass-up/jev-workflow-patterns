---
layout: default
title: "Networking operations: patterns for tickets, changes, and alerts"
description: "Eight question contracts for network operations text: ticket symptoms, change request types, maintenance notice scope, log line events, advisory product families, runbook step reversibility, reported problem scope, and alerts under a supplied policy."
permalink: /networking/
kicker: "8 profiles · 30/32 labels matched · kernel 2.6.0"
---

# Networking operations

A network operations desk and its assistants read the same kinds of text all day: a requester's description of a symptom, a change request, a maintenance notice, a log line, a vendor advisory, a runbook step, a monitoring alert. These eight contracts classify that text so the queue, the approval path, the log pipeline, and the alert handler can route it. They are task-authored, advisory designs. Approval, execution, exact comparisons of addresses, hostnames, versions, and thresholds, and every configuration change stay with people and code; no label diagnoses a cause or decides that a device is affected.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/networking/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/networking/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 6/8 challenge cases** matched their prewritten labels: 30/32 overall. NW01, NW02 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Tickets and user reports

| ID | Question pattern | Intended use |
| --- | --- | --- |
| NW01 · provisional | [Symptom category for a network ticket]({{ '/networking/patterns/nw01/' | relative_url }}) | Queues tickets by what the requester actually reports experiencing instead of by keyword, while the desk keeps priority and assignment. |
| NW07 | [How widely a user report says a problem is felt]({{ '/networking/patterns/nw07/' | relative_url }}) | Separates a single-device complaint from a possible site outage on the report's own words, so code can prioritize and ask the scope question when it is missing. |

## Changes, maintenance, and runbooks

| ID | Question pattern | Intended use |
| --- | --- | --- |
| NW02 · provisional | [Type of change a request describes]({{ '/networking/patterns/nw02/' | relative_url }}) | Separates reading what a request says will change from the approval rule, which differs by change type and must stay in code. |
| NW03 | [Maintenance notice states who will be affected]({{ '/networking/patterns/nw03/' | relative_url }}) | Returns notices that only name the equipment being worked on to their author before recipients have to ask whether they are affected. |
| NW06 | [Runbook step states its own reversal]({{ '/networking/patterns/nw06/' | relative_url }}) | Flags state-changing steps with no stated reversal during runbook review, before a change window, without deciding whether the step is safe. |

## Logs, advisories, and alerts

| ID | Question pattern | Intended use |
| --- | --- | --- |
| NW04 | [Event kind reported by one log line]({{ '/networking/patterns/nw04/' | relative_url }}) | Turns free-text log lines from mixed vendors into a small set of event kinds without a parser per message format; counting and thresholds stay in code. |
| NW05 | [Advisory product family appears in the inventory description]({{ '/networking/patterns/nw05/' | relative_url }}) | Sorts incoming advisories by whether a named family is deployed before a person reads each one; version and serial comparisons stay in code. |
| NW08 | [Alert requires a response under the supplied policy]({{ '/networking/patterns/nw08/' | relative_url }}) | Applies the team's own written alert policy consistently across alert wording from different monitors, while paging and thresholds stay in code. |

## Start with a small bundle

For the service desk, NW01 (symptom) and NW07 (reported scope) with priority and major-incident rules in code. For the change desk, NW02 (change type), NW03 (notice scope), and NW06 (runbook step reversal). For the signal pipeline, NW08 (alert under policy) with paging and thresholds in code, then NW04 (log line event) and NW05 (advisory family) once inventory and log parsing are in place.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not an operational determination. Code compares IP addresses, hostnames, version numbers, and serial numbers exactly, resolves every numeric threshold before a question is asked, enforces blackout windows and approvals, pages and escalates, and executes nothing on a label's say-so. People approve changes, decide whether a runbook step may run, and declare incidents. The profiles are defensive triage only: nothing describes attack, evasion, or exploitation, and log lines are classified by what they report, not attributed to anyone.

[Exact catalog]({{ '/networking/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/networking/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/networking.md)
