# Contract review support profiles

Use this module for classifying the text a contract operations desk or paralegal
assistant organizes before a lawyer reviews an agreement: individual clauses, party
names as the agreement defines them, code-extracted term expressions, redline
comments with the passage they attach to, and a defined term with one of its uses.
A label is a reading of text that organizes the review. Enforceability, risk, what
a party should do, and every other legal conclusion stay with the reviewing lawyer;
exact matching, dates, and cross-references stay in code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/legal-contracts/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| LC01, LC02, LC03 | Clause reading | Clause type for filing; which named party a clause binds; reciprocal, asymmetric, or one-sided drafting |
| LC04, LC07, LC08 | Term, notice, and exception mechanics | What a term expression describes; notice method and recipient stated; carve-out stated, referenced, or absent |
| LC05, LC06 | Redlines and defined terms | Redline comment substantive, editorial, or a question; defined term used in the sense its definition gives |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/legal-contracts/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/legal-contracts/catalog.json).
The evaluation page reports the outcomes of the design and challenge cases; a
synthetic check is not qualification for a real review desk.

Choose by what the label feeds:

- LC01 feeds the checklist headings a clause is filed under. A clause that is none
  of the five types comes back `unknown` and a person files it.
- LC02 feeds the obligations register. Code supplies `party_a` and `party_b` exactly
  as the agreement defines them and routes clauses naming a third party to a person.
- LC03, LC06, and LC08 feed flag lists the lawyer works from: one-sided drafts,
  uses that drift from a definition, and carve-outs to check. Code decides which
  clause types the practice expects to be reciprocal before a `one_sided` label is
  flagged.
- LC04 feeds the term column of the contract register. Code extracts the expression
  with its offsets and resolves every date, period, and deadline; the label only says
  what kind of mechanism the expression describes.
- LC05 orders the lawyer's comment queue. A `substantive_change` label queues the
  comment for the lawyer; an `editorial_change` label is applied only after a person
  accepts it.
- LC07 feeds the notices table. Code records addresses and periods exactly and
  computes any notice deadline.

## Prepare a bounded state

Supply each clause, comment, or passage unchanged and one at a time, the party names
or defined labels exactly as the agreement uses them, the definition text next to a
single use, and the extracted term expression together with its clause as context.
Several contracts state a precedence order for text that fits more than one label
(clause types, term mechanisms, comments that are both editorial and substantive,
carve-outs both stated and referenced); keep those sentences when adapting. Before
inference, code validates `required_state_fields` and returns a local `unknown` for
absent or empty evidence, and it confirms by exact match that a defined term
actually appears in the passage supplied to LC06.

## Use the labels without taking over

No label decides whether a clause is enforceable, fair, or acceptable, how much
risk it carries, whether an obligation has been performed, whether a notice was
validly given, or whether a redline change should be accepted. The reviewing
lawyer's reading overrides any label. Send only authorized agreement text through
the approved provider path; keep client identities, signatories, account details,
and privileged annotations out of the state unless the judgment needs them and the
transfer is authorized.

## Verify against the lawyer's own markup

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/legal-contracts/evaluation/)
separates design cases from separately authored challenge cases and reports their
outcomes. Before use, compare labels with the headings, obligations register, notices
table, and carve-out list a paralegal completed on already-reviewed agreements, and
with the lawyer's disposition of each redline comment. Measure first the one-sided
clauses, drifting definitions, and substantive comments that a label missed.
