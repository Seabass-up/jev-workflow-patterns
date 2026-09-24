---
layout: default
title: "Logistics: patterns for shipments, exceptions, and supplier messages"
description: "Eight question contracts for logistics text: carrier exceptions, proof-of-delivery notes, customs document types, receiving discrepancies, claim narratives, order notes, supplier messages, and stated causes of missed delivery commitments."
permalink: /logistics/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Logistics

A logistics coordinator and the warehouse system read the same text all day: a carrier's exception scan, a driver's delivery note, an inbound customs document, a receiver's dock note, a claim narrative, a customer's order note, a supplier's message about an open order. These eight contracts classify that text so it can be routed and coded without a person reading every line. They are synthetic, task-authored designs and their labels are advisory. Quantities, dates, amounts, and liability are compared or decided in code and by people; no label settles a claim or a chargeback.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/logistics/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/logistics/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 7/8 challenge cases** matched their prewritten labels: 31/32 overall. LG04 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Carrier updates and delivery

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LG01 | [Exception type in a carrier tracking update]({{ '/logistics/patterns/lg01/' | relative_url }}) | Sorts carrier updates into the queue that can act on them (reschedule, trace, claim, or address fix) without a coordinator reading every scan line; the carrier's identifiers and dates stay untouched. |
| LG02 | [Proof-of-delivery note records a handoff or an unattended drop]({{ '/logistics/patterns/lg02/' | relative_url }}) | Lets a coordinator answer a where-is-my-package question and see whether a person accepted the item before opening a dispute; the note's own words are preserved. |
| LG08 | [Cause category named in a service-failure note]({{ '/logistics/patterns/lg08/' | relative_url }}) | Groups missed commitments by stated cause so recurring problems surface, while whether a commitment was actually missed and any credit or penalty are computed in code. |

## Documents, receiving, and claims

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LG03 | [Customs document type from its text]({{ '/logistics/patterns/lg03/' | relative_url }}) | Files inbound customs paperwork under the right document type before a broker or coordinator checks its contents; values, codes, and completeness are checked in code. |
| LG04 · provisional | [Discrepancy type in a receiving note]({{ '/logistics/patterns/lg04/' | relative_url }}) | Turns free-text dock notes into a discrepancy code the inventory system can carry, while received counts and paperwork quantities are compared in code. |
| LG05 | [Cause of damage as a claim narrative states it]({{ '/logistics/patterns/lg05/' | relative_url }}) | Routes a claim to the carrier, the packing team, or the supplier for review based on what the claimant wrote, before anyone decides liability; amounts and deadlines stay in code. |
| LG06 | [Order note contains a handling or delivery instruction]({{ '/logistics/patterns/lg06/' | relative_url }}) | Surfaces notes that change how an order is packed or delivered before it leaves the warehouse, without a person reading every note; which instructions can be honored stays in code. |

## Supplier messages

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LG07 | [Supplier message announces a backorder, a substitution, or a cancellation]({{ '/logistics/patterns/lg07/' | relative_url }}) | Routes supplier messages to replanning, buyer approval, or reordering without a buyer triaging each one; dates, quantities, and prices are compared in code. |

## Start with a small bundle

For the exception desk, start with LG01 (carrier exception type), LG02 (proof-of-delivery handoff), and LG08 (stated cause of a missed commitment), with date comparison and any credit computed in code. For inbound and claims, LG04 (receiving discrepancy) and LG05 (stated cause of damage); add LG03 (customs document type) when the site imports. LG07 (supplier message) belongs with purchasing.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a finding about the shipment. Code matches identifiers, compares quantities, timestamps, promised dates, and claim amounts, applies carrier terms and service agreements, and posts inventory adjustments. People decide claim liability, chargebacks, settlements, and customs classification, and a customs broker owns any declaration. A proof-of-delivery label never establishes that the addressee received the goods; the carrier's record and the dispute process do. No label decides whether a service credit or penalty applies.

[Exact catalog]({{ '/logistics/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/logistics/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/logistics.md)
