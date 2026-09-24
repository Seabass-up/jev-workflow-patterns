---
layout: default
title: "Electrical contracting: patterns for service, permits, and materials"
description: "Eight question contracts for electrical contracting text: dispatch symptoms, hazard signs, work type, correction routing, inspection outcomes, office requests, device types, and photo evidence."
permalink: /electrical/
kicker: "8 profiles · 32/32 labels matched · kernel 2.5.0"
---

# Electrical contracting

An electrical contractor's office reads the same kinds of text every day: a customer's description of a fault, an inspector's notes, a message from the permitting office, a product listing for a submittal. These eight contracts classify that text so dispatch, the job record, and purchasing can route it. They are synthetic, task-authored designs. Licensed judgment on site, the jurisdiction's permit rules, and safety procedures stay with people and code; no label diagnoses a fault or decides that a permit is or is not required.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/electrical/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/electrical/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 8/8 challenge cases** matched their prewritten labels: 32/32 overall. No pattern is provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Service calls

| ID | Question pattern | Intended use |
| --- | --- | --- |
| EL01 | [Symptom category for electrical dispatch]({{ '/electrical/patterns/el01/' | relative_url }}) | Sorts service requests by what the customer actually reports instead of by keyword, while dispatch keeps the scheduling decision. |
| EL02 | [Reported condition calls for de-energizing before work]({{ '/electrical/patterns/el02/' | relative_url }}) | Puts the first safety decision on a consistent footing while the licensed electrician on site retains authority. |

## Permits and inspections

| ID | Question pattern | Intended use |
| --- | --- | --- |
| EL03 | [Described work type for a permit determination]({{ '/electrical/patterns/el03/' | relative_url }}) | Separates the semantic reading of a request from the permit rule, which differs by jurisdiction and must stay in code. |
| EL04 | [Who must act on an inspection correction item]({{ '/electrical/patterns/el04/' | relative_url }}) | Routes correction items to the electrical contractor, another trade, the owner, or the utility without a person re-reading every notice. |
| EL05 | [Inspection outcome from the inspector's notes]({{ '/electrical/patterns/el05/' | relative_url }}) | Turns free-text inspection notes into a status code the job record can carry, without overriding the official result. |
| EL06 | [What the permitting office is asking for]({{ '/electrical/patterns/el06/' | relative_url }}) | Lets the office answer the right request quickly instead of reading every jurisdiction message from scratch. |
| EL08 | [Photo description covers the requested evidence]({{ '/electrical/patterns/el08/' | relative_url }}) | Reduces rejected virtual-inspection submissions when the described photo does not show the requested item. |

## Materials

| ID | Question pattern | Intended use |
| --- | --- | --- |
| EL07 | [Protective device type from a product description]({{ '/electrical/patterns/el07/' | relative_url }}) | Catches a submittal or purchase that describes the wrong protection type before it is installed; ratings and listings stay in code. |

## Start with a small bundle

For dispatch, EL01 (symptom) and EL02 (hazard signs) with the standing escalation rule in code. For the permit desk, EL03 (work type), EL05 (inspection outcome), EL06 (office request), and EL04 (correction routing). For purchasing, EL07 (device type) with exact rating checks in code.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not an electrical determination. Code applies the jurisdiction's permit rule and fee, records the official inspection result as authoritative, compares ratings and listings exactly, and enforces de-energizing and lockout procedures regardless of any model output. The on-site electrician's hazard determination overrides EL02.

[Exact catalog]({{ '/electrical/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/electrical/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/electrical.md)
