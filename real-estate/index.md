---
layout: default
title: "Real estate operations: patterns for listings, inquiries, and property documents"
description: "Eight question contracts for real estate operations text: listing claims, property inquiries, inspection-report items, lease clauses, tenant messages, disclosure statements, offer contingencies, and maintenance emergencies."
permalink: /real-estate/
kicker: "8 profiles · 30/32 labels matched · kernel 2.6.0"
---

# Real estate operations

A brokerage or property management office reads the same kinds of text every day: a draft listing, a message asking about a property, an inspector's report, a lease, a tenant's request, a completed disclosure form, an offer. These eight contracts classify that text so the listing desk, the leasing office, and the maintenance queue can route it. They are synthetic, task-authored designs and every label is advisory. Pricing, legal, and safety decisions stay with licensed people and code, and no label judges or infers anything about a person.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/real-estate/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/real-estate/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 6/8 challenge cases** matched their prewritten labels: 30/32 overall. RE02, RE04 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Listings and offers

| ID | Question pattern | Intended use |
| --- | --- | --- |
| RE01 | [Listing feature claim is supported by the property facts]({{ '/real-estate/patterns/re01/' | relative_url }}) | Catches a feature claim the record does not back before the listing is published, while the agent keeps the decision to edit the copy or the record. |
| RE07 | [Offer message states, waives, or omits contingencies]({{ '/real-estate/patterns/re07/' | relative_url }}) | Fills the contingency field on an offer record from free text so the listing agent sees every offer's conditions at a glance, without ranking or judging the offers. |

## Inquiries and tenant requests

| ID | Question pattern | Intended use |
| --- | --- | --- |
| RE02 · provisional | [What a property inquiry asks for]({{ '/real-estate/patterns/re02/' | relative_url }}) | Routes inquiries to the right desk by what the message actually asks instead of by keyword, while the listing system and a person supply every answer. |
| RE05 | [Queue a tenant message belongs in]({{ '/real-estate/patterns/re05/' | relative_url }}) | Sends each message to maintenance, leasing, or accounting on the first read, while the ledger and the lease text supply every answer. |
| RE08 | [Maintenance request describes an emergency sign]({{ '/real-estate/patterns/re08/' | relative_url }}) | Puts the first triage of after-hours and high-volume requests on a consistent footing, while the response-time policy and the technician on site keep the decision. |

## Property documents

| ID | Question pattern | Intended use |
| --- | --- | --- |
| RE03 | [Severity an inspection-report item states as written]({{ '/real-estate/patterns/re03/' | relative_url }}) | Turns a long report into a sortable list for the agent and the parties without changing the inspector's words or grading the property. |
| RE04 · provisional | [Topic a lease clause governs]({{ '/real-estate/patterns/re04/' | relative_url }}) | Lets the leasing office assemble a clause-by-clause summary from any lease format without deciding what a clause means legally. |
| RE06 | [Disclosure statement addresses the named item]({{ '/real-estate/patterns/re06/' | relative_url }}) | Finds blank and missing disclosure items before the form goes to the other party, while the truth of each statement and legal sufficiency stay with the parties and counsel. |

## Start with a small bundle

Start with RE08 (emergency sign), RE05 (tenant message), and RE02 (inquiry request): they route the highest-volume text and pair with a response-time policy that code enforces. Add RE01 (listing claim) once the property record can be supplied with its revision. RE03, RE04, RE06, and RE07 support document and offer review at lower volume.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text about a property, a document, or a request, never a judgment about a person. Fair-housing and anti-discrimination rules apply: no contract asks about, and no state should carry, a sender's or occupant's protected characteristics, and the office's routing and answers must not vary by them. Code compares numbers, dates, and measurements exactly, applies the response-time policy, records report, lease, and offer identifiers with their revisions, and leaves pricing, offer acceptance, the legal sufficiency of a disclosure or clause, and every safety determination to licensed people and the technician on site.

[Exact catalog]({{ '/real-estate/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/real-estate/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/real-estate.md)
