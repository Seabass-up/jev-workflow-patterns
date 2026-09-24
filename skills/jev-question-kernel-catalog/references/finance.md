# Finance operations profiles

Use this module for classifying the text that accounts payable, accounting, and FP&A
staff handle: inbound commercial documents, payment-terms clauses, expense
descriptions, vendor and customer messages, budget requests, approver replies,
variance commentary, and bank memos. A label is a reading of text. Amounts, dates,
matching, approval records, policy limits, and every accounting, tax, and legal
determination stay with code and people.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/finance/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| FN01, FN03, FN08 | Documents | Document type from its text; kind of payment-terms expression; bank memo wording against the described purpose |
| FN02, FN06, FN07 | Approvals and requests | Expense description against one supplied category; recurring or one-time budget cadence; what an approver's reply does |
| FN04, FN05 | Explanations and messages | Variance commentary names a driver or restates the number; vendor or customer message intent |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/finance/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/finance/catalog.json).
The evaluation page reports screening outcomes; a small synthetic check is not
qualification for a real finance team.

Choose by what the label feeds:

- FN01, FN03, and FN05 feed inbox routing and invoice intake. Code extracts
  identifiers, amounts, and dates exactly, matches invoices to orders and receipts,
  copies the verbatim terms expression, and resolves due dates and discounts.
- FN02, FN06, and FN07 feed the request record. Code supplies the category definition
  and its revision, checks amounts against limits and thresholds, sums and annualizes
  budget figures, and records an approval only through the approval system with the
  approver's message as evidence. The label never creates an approval.
- FN04 returns commentary to a line owner before review; code computes the variance
  and checks any quoted amounts against the ledger.
- FN08 flags a reconciling item; code matches amounts, dates, and exact references,
  and the preparer and reviewer confirm the match.

## Prepare a bounded state

Supply the document text, the message, or the approver's words unchanged, the one
category definition or expected purpose code owns, and the variance line as code
states it. Several contracts state a precedence order for text that does more than
one thing, such as a message that both disputes and demands payment, or a terms clause
that states both a discount and a net period; keep those sentences when adapting.
Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent or empty evidence. Keep bank account numbers, card numbers,
tax identifiers, and personal details out of the state unless the judgment needs
them and the transfer is authorized.

## Use the labels without taking over

No label computes or compares an amount, resolves a date, decides that an expense
is allowable, grants or records an approval, confirms a reconciliation match, or
gives investment, tax, accounting, or legal advice. Send only authorized finance text
through the approved provider path; keep counterparties' banking details and
employees' personal information out of the state.

## Verify against the team's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/finance/evaluation/)
reports outcomes for the design cases and any separately authored challenge cases.
Before use, compare labels with how accounts payable filed and routed a month of
documents and messages, the category coding auditors applied, the approvals recorded
in the approval system, the FP&A reviewer's accept-or-return decisions, and the
matches the reconciliation preparer confirmed. Measure missed remittance advice and
replies wrongly labelled as explicit approval first.
