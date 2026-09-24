# Construction profiles

Use this module for classifying the text a general contractor's project engineers
handle: RFIs, submittal review responses, daily logs, change-order narratives,
safety observation cards, punch-list items, schedule notes, and closeout documents.
A label is a reading of what a document states. Safety decisions, design answers,
submittal releases, change-order entitlement and price, time extensions, and the
sufficiency of a warranty or lien waiver stay with people and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/construction/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| CN01, CN03 | RFIs and submittals | What an RFI asks the design team for; the reviewer's stated action on a submittal |
| CN02, CN05, CN06 | Field records | Cause a daily log states for lost time; safety observation against the project's stop-work list; trade group for a punch-list item |
| CN04, CN07, CN08 | Changes, schedule, and closeout | Stated basis of a change-order request; stated critical-path impact; closeout document type |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/construction/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/construction/catalog.json).
The evaluation page reports the outcomes of the design and challenge cases; a
small synthetic check is not qualification for a real project.

Choose by what the label feeds:

- CN01 and CN03 feed the RFI and submittal logs. Code opens a formal substitution
  request when CN01 reads `substitution_request`, and ordering or fabrication waits
  until CN03 reads `approved` or `approved_as_noted` and the project engineer confirms.
- CN02 feeds a per-cause day count. The contract, not the label, decides whether a
  delay is excusable or compensable.
- CN04 feeds the change log with the basis the requester stated; entitlement, price,
  and who pays are decided by the people who administer the contract.
- CN05 feeds the observation queue. The project's own stop-work list is supplied in
  state, any `stop_work_condition` label triggers the standing notification in code,
  and the competent person on site decides whether work stops. The electrical
  collection's EL02 applies fixed electrical hazard signs from an electrician's side;
  CN05 covers any trade and takes its conditions from the project's safety plan.
- CN06 feeds the punch-list tracker with a trade group; code maps the group to the
  subcontractor. EL04 assigns an electrical correction item to a party from the
  electrician's side; CN06 works from the general contractor's side across trades.
- CN07 flags notes that state a milestone or completion impact for the scheduler.
  The schedule itself computes every date and float value.
- CN08 sorts closeout documents for the checklist; lien-waiver amounts and dates are
  matched to pay applications in code and sufficiency is a person's decision.

## Prepare a bounded state

Supply the RFI, review response, log entry, narrative, observation, punch item, or
document text unchanged, plus the lists code owns: the project's stop-work
conditions as written in the safety plan for CN05 and the four trade-group scope
descriptions for CN06. Several contracts state a precedence order for text that
gives more than one cause, basis, or type; keep those sentences when adapting.
Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent or empty evidence, including an empty stop-work list or an
empty scope mapping.

## Use the labels without taking over

No label answers an RFI, releases a submittal, decides that a delay is excusable,
approves a change order or its price, says that a condition is safe or that work
must stop, assigns cost or fault for a punch item, computes a date, or judges a
lien waiver's legal effect. No contract cites or applies a building code or a
specification section. Send only authorized project text through the approved
provider path; keep owner identities, contract amounts, addresses, and account
details out of the state unless the judgment needs them and the transfer is
authorized.

## Verify against the project's own logs

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/construction/evaluation/)
separates the 24 design cases from separately authored challenge cases and reports
their outcomes. Before use, compare labels with the categories the project engineer
assigned on a closed project's RFI, submittal, and change logs, the superintendent's
delay coding and punch-list assignments, the safety manager's classification of
observation cards, and the scheduler's recorded impacts. Measure missed stop-work
conditions first, then material released or claims relied on where the label read
the document differently from the log.
