# Marketing profiles

Use this module for classifying the text a marketing team and its content assistants
handle: a claim and the evidence offered for it, outbound messages, draft copy against
a persona or a brand-voice guide, competitor mentions, campaign briefs, and reviewer
comments on creative. A label is a reading of text. Substantiation, legal and
regulatory compliance, and the decision to publish stay with people and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/marketing/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| MK01, MK06 | Claims and comparisons | Claim matches, overstates, or is contradicted by its supplied evidence; competitor mention is a comparative claim or a neutral reference |
| MK02, MK03, MK04, MK05 | Copy and messages | Promotional or transactional content under the team's definition; one call to action, several, or none; copy addresses the stated persona; copy matches the brand-voice guide |
| MK07, MK08 | Briefs and reviews | Brief states goal, audience, and metric; review comment is about strategy or execution |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/marketing/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/marketing/catalog.json).
The evaluation page reports the outcomes of the synthetic screening cases; those cases
are a small authored check, not qualification for a real team.

Choose by what the label feeds:

- MK01 and MK06 feed the substantiation queue. Code extracts one claim at a time with
  offsets, compares figures and competitor names exactly, and sends every label except
  `supported_as_worded`, and every `comparative_claim`, to the reviewer who decides.
- MK02 feeds sending rules only when the team supplies its own written definition of
  promotional and transactional content. `both_present` goes to a person; the model
  never decides the primary purpose of a message or what any law requires.
- MK03, MK04, and MK05 feed draft review. Code checks banned words and punctuation
  exactly before inference; `guide_silent` is a gap to raise with the brand team, not
  approval.
- MK07 feeds intake. A label other than `complete` returns the brief with the named
  gap; the marketing lead decides whether work proceeds anyway.
- MK08 routes review threads: `strategy` and `both` to the campaign owner, `execution`
  to the creative team. Nothing is resolved, closed, or ranked by the label.

## Prepare a bounded state

Supply the claim and its registered evidence, the message or copy as written for one
placement, the current revision of the persona, brand guide, or classification rule
the team owns, one competitor name at a time, and the brief or comment unchanged.
Several contracts state a precedence order for text that fits more than one label,
such as a claim that is both partly contradicted and partly supported, or copy that
both names a competitor and compares against it; keep those sentences when adapting.
Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent or empty evidence.

## Use the labels without taking over

No label substantiates a claim, decides that a comparison or a message is lawful,
approves copy for publication, changes a persona or a brand guide, or resolves a
review comment. Send only authorized campaign text through the approved provider
path; keep customer lists, contact details, unpublished pricing, and contract terms
out of the state unless the judgment needs them and the transfer is authorized.

## Verify against the team's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/marketing/evaluation/)
separates the 24 design cases from separately authored challenge cases and reports the
outcomes. Before use, compare labels with the substantiation reviewer's decisions, the
compliance team's message classifications, the brand team's voice reviews, intake
decisions on submitted briefs, and how campaign owners triaged review threads. Measure
missed comparative claims and claims the label called supported that a reviewer
rejected first.
