# Project management profiles

Use this module for classifying the text a project manager or their assistant
handles: status updates, risk register entries, change requests, blocker reports,
meeting note items, action items, stakeholder replies, and retrospective items. A
label is a reading of what the text states. Schedule dates, durations, budgets,
approvals, the party list, and who is contacted stay with code and with people.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/project-management/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| PM01, PM02, PM04 | Status, risk, and blockers | Slip, risk, or on track as stated; owner, trigger, and mitigation present; blocker waits on an internal or external party |
| PM03, PM05, PM06 | Change, decisions, and actions | Scope change, clarification, defect, or schedule-only change; decision, discussion, or deferral; owner and due expression present |
| PM07, PM08 | Stakeholders and retrospectives | Reply approves, declines, acknowledges, or asks; retrospective item points at process, tooling, staffing, or requirements |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/project-management/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/project-management/catalog.json).
The evaluation page reports screening outcomes; a small synthetic check is not
qualification for a real project office.

Choose by what the label feeds:

- PM01 feeds a portfolio digest. It reads what the author states about a date; code
  owns the schedule, every date comparison, and the official health rating.
- PM02 and PM06 are completeness checks on a single entry. Code resolves a due
  expression to a calendar date and matches an owner to the roster; the label only
  says whether the entry states them.
- PM03 feeds the change board's queue. The label separates a scope change from a
  clarification, a defect report, or a timing-only change; approval and cost effect
  are decided by the board and computed in code.
- PM04 feeds an escalation path chosen in code from the party list. A party the list
  does not name yields `unknown`, not a guess.
- PM05 writes to a decision log in the note's exact words. PM07 updates a request's
  status; code checks that the replying stakeholder holds the needed authority.
- PM08 groups retrospective items for a facilitator. Staffing labels describe what
  an item says about availability and skills, never a judgment of a person.

## Prepare a bounded state

Supply the author's words unchanged: the status update, the register entry, the
change request with the approved scope statement, the blocker report with the
party list as code maintains it, one note item at a time, one action item at a
time, the request sent with the reply, and one retrospective item. Several
contracts state a precedence order for text that mentions more than one
condition, kind, party, or area; keep those sentences when adapting. Before
inference, code validates `required_state_fields` and returns a local `unknown`
for absent or empty evidence.

## Use the labels without taking over

No label moves a date, computes a duration or cost, approves a change, rates a
risk, grants approval, contacts a stakeholder, or attributes blame. Send only
authorized project text through the approved provider path; keep customer
identities, contract values, credentials, and personal details out of the state
unless the judgment needs them and the transfer is authorized.

## Verify against the project's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/project-management/evaluation/)
page reports outcomes for the design cases and any separately authored challenge
cases. Before use, compare labels with the project manager's health ratings, the
change board's dispositions, the hand-kept decision log and action tracker, and how
blockers were actually escalated. Measure missed slips and approvals logged from a
mere acknowledgment first.
