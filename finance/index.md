---
layout: default
title: "Finance operations: patterns for documents, approvals, and explanations"
description: "Eight question contracts for finance operations text: document type, expense category fit, payment-terms kind, variance commentary, counterparty messages, budget cadence, approver replies, and bank memo consistency."
permalink: /finance/
kicker: "8 profiles · 32/32 labels matched · kernel 2.6.0"
---

# Finance operations

Accounts payable, accounting, and FP&A staff read the same kinds of text every day: an attachment that may be an invoice or a statement, a terms clause, a vendor's message, an approver's reply, a line of variance commentary, a bank memo. These eight contracts classify that text so intake, the request record, the close, and the reconciliation can route it. They are synthetic, task-authored designs and their labels are advisory. No label computes or compares an amount, resolves a date, grants an approval, or gives investment, tax, accounting, or legal advice.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/finance/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/finance/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 8/8 challenge cases** matched their prewritten labels: 32/32 overall. No pattern is provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Documents

| ID | Question pattern | Intended use |
| --- | --- | --- |
| FN01 | [Document type from its text: invoice, statement, credit note, or purchase order]({{ '/finance/patterns/fn01/' | relative_url }}) | Sorts mixed inbox attachments by what the text says the document is, without a template per vendor; matching, posting, and payment stay in code. |
| FN03 | [Kind of payment-terms expression on a document]({{ '/finance/patterns/fn03/' | relative_url }}) | Separates reading the terms clause from the date arithmetic and discount rules, which differ by vendor and stay in code. |
| FN08 | [Bank memo wording is consistent with the described transaction purpose]({{ '/finance/patterns/fn08/' | relative_url }}) | Surfaces reconciling items whose memo names a different counterparty or purpose, while amounts, dates, and exact references are matched in code. |

## Approvals and requests

| ID | Question pattern | Intended use |
| --- | --- | --- |
| FN02 | [Expense description falls within a supplied policy category]({{ '/finance/patterns/fn02/' | relative_url }}) | Flags miscoded expense lines before an approver sees them, while the category definition, its limits, and the allowability decision stay with policy and people. |
| FN06 | [Budget request states recurring or one-time spend]({{ '/finance/patterns/fn06/' | relative_url }}) | Sends recurring commitments down the right approval path without an analyst re-reading every request; totals, annualization, and thresholds stay in code. |
| FN07 | [Approver reply: explicit approval, conditional approval, deferral, or rejection]({{ '/finance/patterns/fn07/' | relative_url }}) | Stops a hedged or postponed reply from being treated as approval, while the approval itself is recorded only by the approval system and the approver. |

## Explanations and messages

| ID | Question pattern | Intended use |
| --- | --- | --- |
| FN04 | [Variance explanation names a cause or restates the number]({{ '/finance/patterns/fn04/' | relative_url }}) | Returns empty commentary to the line owner before the review meeting, while the variance itself is computed and checked in code. |
| FN05 | [Vendor or customer message: dispute, inquiry, remittance advice, or payment demand]({{ '/finance/patterns/fn05/' | relative_url }}) | Routes a shared finance inbox by what the sender is doing rather than by keyword, while invoice lookup, amount comparison, and case handling stay in code and with staff. |

## Start with a small bundle

For the payables inbox, FN01 (document type), FN05 (message intent), and FN03 (terms kind) with matching, lookup, and due-date resolution in code. For requests and approvals, FN02 (expense category fit), FN06 (budget cadence), and FN07 (approver reply) with limits, thresholds, and the approval record in code. For the close, FN04 (variance commentary) and FN08 (bank memo consistency) with the variance and the amount-and-date match computed in code.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a financial determination. Code extracts identifiers, amounts, and dates exactly, matches invoices to orders and receipts, resolves due dates and discounts, sums and annualizes budget amounts, applies policy limits and approval thresholds, and matches bank lines by amount, date, and reference. Approvals are recorded only by the approval system and the approver, allowability is decided by the approver under policy, and the reconciliation match is confirmed by the preparer and reviewer. Nothing here is investment, tax, accounting, or legal advice.

[Exact catalog]({{ '/finance/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/finance/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/finance.md)
