# Real estate operations profiles

Use this module for classifying the text a brokerage or property management office
handles: draft listing claims, messages about a listed property, inspection-report
items, lease clauses, tenant messages, completed disclosure forms, offer messages, and
maintenance requests. A label is a reading of text about a property, a document, or a
request. Pricing, offer decisions, legal sufficiency, safety determinations, and
anything about a person stay with licensed people and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/real-estate/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| RE01, RE07 | Listings and offers | Listing claim against the property record; offer states, waives, or omits contingencies |
| RE02, RE05, RE08 | Inquiries and tenant requests | What an inquiry asks for; tenant message queue; emergency sign in a maintenance request |
| RE03, RE04, RE06 | Property documents | Severity an inspection item states as written; lease clause topic; disclosure addresses a named item |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/real-estate/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/real-estate/catalog.json).
The [evaluation page](https://seabass-up.github.io/jev-workflow-patterns/real-estate/evaluation/)
reports the screening outcomes; a small synthetic check is not qualification for a
real office.

Choose by what the label feeds:

- RE02, RE05, and RE08 feed routing queues. Code applies the response-time policy for
  `emergency_sign`, dispatches the on-call vendor, and keeps the technician's own
  determination on site as authoritative.
- RE01 feeds a listing hold. Code splits copy into single claims, supplies the property
  record with its revision, and compares counts and measurements exactly; the label
  never approves copy for publication.
- RE03, RE04, and RE06 feed document summaries and review checklists. The inspector's
  wording, the lease text, and the disclosure form stay unchanged; enforceability and
  legal sufficiency stay with counsel.
- RE07 fills a contingency field on an offer record. Contingency types and deadlines
  are extracted exactly in code, and acceptance stays with the seller and licensed
  agents.

## Prepare a bounded state

Supply the message, clause, report item, or disclosure text unchanged, the property
record or the named disclosure item as written, and nothing about the sender.
Fair-housing rules apply to the state as well as to the label: keep protected
characteristics, names, and contact details out of the state, and limit the required
fields to the text the judgment needs. Several contracts state a precedence order for
messages, clauses, or items that fit more than one label; keep those sentences when
adapting. Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent or empty evidence.

## Use the labels without taking over

No label sets a price, accepts an offer, grades a property, decides that a disclosure
or clause satisfies a law, or determines a response time. Routing and answers must not
vary by anything about a person. Send only authorized office text through the approved
provider path; keep tenant and buyer identities, unit addresses, account balances, and
deposit records out of the state unless the judgment needs them and the transfer is
authorized.

## Verify against the office's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/real-estate/evaluation/)
separates 24 design cases from separately authored challenge cases and reports the
outcomes. Before use, compare labels with the leasing office's queue assignments, the
maintenance coordinator's priorities and the technician's findings, the listing
coordinator's fact-check notes, the transaction coordinator's contingency entries, and
a compliance reviewer's disclosure checklist. Measure missed emergency signs and
listing claims wrongly called supported first.
