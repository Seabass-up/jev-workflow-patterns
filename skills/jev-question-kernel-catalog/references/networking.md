# Networking operations profiles

Use this module for classifying the text a network operations desk handles:
tickets and user reports, change requests, maintenance notices, log lines, vendor
advisories, runbook steps, and monitoring alerts. A label is a reading of text.
Approval, execution, exact comparisons of addresses, hostnames, versions, and
thresholds, and every configuration change stay with people and code. The
profiles are defensive triage only; nothing describes attack, evasion, or
exploitation.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/networking/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| NW01, NW07 | Tickets and user reports | Symptom category for queueing; how widely a report says a problem is felt |
| NW02, NW03, NW06 | Changes, maintenance, and runbooks | Change type for approval routing; whether a notice states its affected scope; whether a runbook step states its reversal |
| NW04, NW05, NW08 | Logs, advisories, and alerts | Event kind of one log line; advisory product family against inventory text; alert under a supplied policy |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/networking/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/networking/catalog.json).
The evaluation page reports screening outcomes; this module claims none.

Choose by what the label feeds:

- NW01 and NW07 feed the service desk queue and priority. Code owns priority,
  the service-level clock, and major-incident declaration by ticket counts and
  monitoring correlation; the label never diagnoses a cause.
- NW02 feeds approval routing. Code checks blackout windows and exact device
  names; no configuration line is generated or approved by a label.
- NW03 feeds the decision to send a maintenance notice or return it to its
  author; the sender decides.
- NW04 classifies one log line. Counting state changes within a window and
  comparing against thresholds happen in code.
- NW05 says only whether a named product family appears in the inventory
  description. Version numbers, release trains, and serial numbers are compared
  exactly in code.
- NW06 reports whether a runbook step states its reversal, not whether the step
  is safe; the runbook owner decides.
- NW08 applies a supplied policy text to one alert. Paging, escalation,
  de-duplication, maintenance suppression, and every threshold comparison stay
  in code.

## Prepare a bounded state

Supply the requester's, author's, or device's words unchanged, one log line at a
time, the advisory's affected-products text separately from the inventory
description, and the alert policy as the team wrote it with any numeric
threshold already resolved by code. Several contracts state a precedence order
for text that reports more than one symptom, change type, or event kind; keep
those sentences when adapting. Before inference, code validates
`required_state_fields` and returns a local `unknown` for absent or empty
evidence.

## Use the labels without taking over

No label approves a change, executes a step, pages an engineer, declares an
incident, or determines that a device is affected by an advisory. Send only
authorized operational text through the approved provider path; keep
credentials, internal addresses and hostnames, customer identities, and account
details out of the state unless the judgment needs them and the transfer is
authorized.

## Verify against the operations desk's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/networking/evaluation/)
page reports outcomes for the design cases and any separately authored
challenge cases. Before use, compare labels with the queue the desk chose, the
change type the change manager recorded, the platform team's affected
determinations for past advisories, and the on-call engineer's acted or ignored
record for past alerts. Measure reporter_only labels that turned out to be
site-wide and requires_response alerts that were ignored first.
