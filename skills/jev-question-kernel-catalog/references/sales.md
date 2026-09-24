# Sales operations profiles

Use this module for classifying the text a sales team or CRM assistant handles:
prospect messages, stated objections, proposal sections, follow-up statements,
discount requests against the seller's policy text, pipeline notes, and competitor
mentions. A label is a reading of text. Amounts, dates, pipeline stages, pricing,
concessions, and approvals stay with code and people.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/sales/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| SA01, SA02, SA03, SA08 | Prospect messages | What the message asks for; kind of objection; which buying signal is stated; what a competitor mention does |
| SA04, SA06 | Proposals and pricing | How a proposal section responds to a requirement; whether a discount request is one the policy text describes |
| SA05, SA07 | Pipeline notes | How a follow-up names its time; whether a note records an agreed next step |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/sales/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/sales/catalog.json).
The evaluation page reports the outcomes of the synthetic screening cases; that is a
small check of the contracts as written, not qualification for a real sales team.

Choose by what the label feeds:

- SA01 feeds the reply queue. An `objection_raised` label passes the same message to
  SA02; a `decline` never closes the opportunity without a person, and a
  `pricing_request` never sends a price.
- SA03 fills qualification fields from the prospect's own words. Code stores the
  amount, date, and named roles exactly and compares them with thresholds; the label
  only says which kind of signal the text states.
- SA04 builds a compliance matrix from what each proposal section claims. Whether a
  requirement is actually met, and any contractual commitment, stay with the proposal
  owner.
- SA06 sends requests the policy text already describes to the standard path and
  everything else to the approver named in the policy. Percentages, seat counts, and
  terms are compared in code; the model never grants a discount.
- SA07 finds notes with no agreed next step; code then passes the next-step sentence
  to SA05 for how its time is named and resolves any named time to a date. Neither
  label moves a stage or decides whether a statement is a commitment; B05 does that.
- SA08 takes one competitor name code matched and says what the mention does. Every
  claim about a competitor comes from reviewed material, never from the model.

## Prepare a bounded state

Supply the prospect's or rep's words unchanged, the requirement paired with its
proposal section by identifier, the discount policy text as written, and the
competitor name code matched. Several contracts state a precedence order for text
that does more than one thing, such as a message that both objects and asks for
pricing, or a note that states both a closed outcome and a follow-up task; keep those
sentences when adapting. Before inference, code validates `required_state_fields`
and returns a local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label sets a price, grants a concession, approves a discount, resolves a date,
changes a pipeline stage, closes an opportunity, or makes a compliance claim in a
proposal. No label judges a prospect or a rep; each reads the supplied text only.
Send only authorized opportunity text through the approved provider path; keep
contact details, contract values, and account identifiers out of the state unless the
judgment needs them and the transfer is authorized. Substantiation of any claim about
a competitor and the legal compliance of proposal and pricing statements stay with
people.

## Verify against the team's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/sales/evaluation/)
separates 24 design cases from separately authored challenge cases and reports the
outcomes. Before use, compare labels with how the team actually handled inbound
messages, the qualification fields reps filled, the compliance matrix a proposal
manager completed, the approval path each discount request followed, and a sales
manager's review of pipeline notes. Measure missed declines, missed objections, and
missed buying signals first.
