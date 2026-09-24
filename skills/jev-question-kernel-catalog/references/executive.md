# Executive decision profiles

Use this module for classifying the text a CEO, an executive team, or a chief of
staff reads before a decision: memos, proposals, business cases, and escalation
requests. A label is a reading of how the text frames its ask, what evidence it
offers, and what it leaves out. The decision itself, its merits, spending limits,
and who may approve what stay with people and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/executive/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| CE01, CE02, CE05 | Decision framing | Decision stated or background only; reversible or one-way as written; decision, information, or alignment asked |
| CE03, CE04, CE06, CE07 | Evidence and completeness | Data, anecdote, or no evidence; alternatives compared, named, or absent; downside named or upside only; measurable or vague success criterion |
| CE08 | Escalations | Request matches a condition in the supplied escalation policy text |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/executive/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/executive/catalog.json).
The [evaluation page](https://seabass-up.github.io/jev-workflow-patterns/executive/evaluation/)
reports the screening outcomes; this module does not restate them, and a synthetic
screen is not qualification for a real executive office.

Choose by what the label feeds:

- CE01 and CE05 feed the docket. A memo whose decision is unspecified or that asks
  for nothing goes back to the author or to a reading queue; the chief of staff
  sets the agenda, not the label.
- CE02 feeds how much scrutiny a proposal gets. The label reads what the proposal
  says about undoing the action; whether the action is in fact reversible is the
  executive's judgment.
- CE03, CE04, CE06, and CE07 feed a completeness note returned to the author before
  the meeting. None of them says the evidence is correct, the rejected alternative
  was worse, the risk is real, or the metric is the right one.
- CE08 feeds routing. Code supplies the policy text from the current revision, and
  any condition that turns on an amount, date, or count is compared in code after
  the label.

## Prepare a bounded state

Supply the memo or proposal text as the author wrote it, and for CE08 the escalation
policy text at its current revision. Do not summarize a memo before asking; a summary
can add a decision statement or a metric the author never wrote. Several contracts
state a precedence order for text that does more than one thing, such as naming a
decision after long background or citing both data and an anecdote; keep those
sentences when adapting. Before inference, code validates `required_state_fields`
and returns a local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label recommends approving or rejecting a proposal, judges the author, computes a
cost or a return, compares an amount with a limit, or decides that an escalation was
justified. Send only authorized internal documents through the approved provider
path; keep board materials, personnel matters, and unreleased financial figures out
of the state unless the judgment needs them and the transfer is authorized.

## Verify against the executive office's own record

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/executive/evaluation/)
separates the 24 design cases from separately authored challenge cases and reports
what each screen found. Before use, compare labels with how the chief of staff
actually triaged a quarter of memos, which proposals were returned for missing
alternatives, risks, or metrics, and which escalations the executive team accepted
as within policy. Measure memos labeled `decision_stated` that the executive team
could not act on first.
