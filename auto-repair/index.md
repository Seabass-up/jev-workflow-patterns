---
layout: default
title: "Auto repair: patterns for intake, authorization, and service writing"
description: "Eight question contracts for auto repair shop text: customer symptom descriptions, stop-driving signs in a report, repair-order line types, customer replies to an estimate, part descriptions, warranty narratives, technician inspection notes, and estimate explanations."
permalink: /auto-repair/
kicker: "8 profiles · 32/32 labels matched · kernel 2.6.0"
---

# Auto repair

A service advisor reads the same kinds of text all day: a customer's description of what the car is doing, a reply to an estimate, a technician's inspection note, a part listing from a supplier, a warranty narrative. These eight contracts classify that text so intake, the repair order, and the parts and warranty desks can route it. They are synthetic, task-authored designs and their labels are advisory. The technician's determination, the customer's authorization record, prices, dates, mileage, and coverage decisions stay with people and code; no label diagnoses a fault or decides whether a vehicle is safe to drive.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/auto-repair/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/auto-repair/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 8/8 challenge cases** matched their prewritten labels: 32/32 overall. No pattern is provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Intake

| ID | Question pattern | Intended use |
| --- | --- | --- |
| AR01 | [Symptom category from a customer's description]({{ '/auto-repair/patterns/ar01/' | relative_url }}) | Sorts incoming concerns by what the customer actually reports instead of by keyword, while the advisor keeps the write-up and the technician keeps the diagnosis. |
| AR02 | [Customer report contains a stop-driving sign]({{ '/auto-repair/patterns/ar02/' | relative_url }}) | Puts the first intake question on a consistent footing so the advisor can respond in the right order, while the technician retains every safety determination. |

## Authorization and presentation

| ID | Question pattern | Intended use |
| --- | --- | --- |
| AR04 | [Customer reply approves, declines, or questions an estimate]({{ '/auto-repair/patterns/ar04/' | relative_url }}) | Separates the reading of a customer's reply from the authorization record, which code keeps with the time, method, and exact scope. |
| AR07 | [Inspection note is a safety item, a recommendation, or informational]({{ '/auto-repair/patterns/ar07/' | relative_url }}) | Keeps the customer-facing inspection summary ordered by what the technician actually wrote, without the model making its own safety call. |
| AR08 | [Estimate explanation itemizes parts and labor]({{ '/auto-repair/patterns/ar08/' | relative_url }}) | Flags estimates that do not show the customer what is parts and what is labor before they go out, while code checks the arithmetic and the jurisdiction's estimate rule. |

## Service writing

| ID | Question pattern | Intended use |
| --- | --- | --- |
| AR03 | [Repair-order line is diagnosis, repair, or maintenance]({{ '/auto-repair/patterns/ar03/' | relative_url }}) | Keeps line types consistent across writers without a person re-reading every line; labor time, price, and billing codes stay in code. |
| AR05 | [Part origin and condition from a part description]({{ '/auto-repair/patterns/ar05/' | relative_url }}) | Catches a quote or invoice line whose part type differs from what the customer was told before the part is installed; part numbers and prices stay in code. |
| AR06 | [Warranty narrative describes a defect, wear, or external damage]({{ '/auto-repair/patterns/ar06/' | relative_url }}) | Applies the policy's own words to the technician's account consistently, while the warranty administrator keeps the coverage decision and code keeps dates and mileage. |

## Start with a small bundle

For the front counter, AR01 (symptom category) and AR02 (stop-driving signs) with the standing advisor script in code, then AR04 (customer reply) with the authorization record kept by code. For the write-up desk, AR03 (line type) and AR08 (parts and labor itemized) with the arithmetic and the jurisdiction's estimate rule in code. Add AR05 (part origin) at the parts counter and AR06 (warranty cause) and AR07 (inspection note) once the technician's own categories are recorded as authoritative.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a diagnosis, a safety determination, or a coverage decision. The technician decides whether a vehicle is safe to drive and what is wrong with it; the warranty administrator decides coverage; the customer's authorization is recorded by code with its time, channel, and exact scope under the jurisdiction's rules. Code sums every amount, compares measurements with limits, matches part numbers, applies date and mileage limits, and enforces the disclosure rule for used and rebuilt parts regardless of any model output. No label is shown to a customer as advice.

[Exact catalog]({{ '/auto-repair/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/auto-repair/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/auto-repair.md)
