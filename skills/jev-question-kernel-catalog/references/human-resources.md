# Human resources profiles

Use this module for classifying the text an HR operations or people team handles:
requirement lines in job postings, policy questions from a shared inbox, interviewer
notes, reported concerns, exit-interview comments, offer letters, performance-review
comments, and employee requests. A label is a reading of document text or a routing
step. It never classifies a person's protected characteristics, health, honesty, or
worth, and every employment decision, eligibility check, and investigation stays with
people and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/human-resources/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| HR01, HR06 | Documents | Requirement line marked essential or preferred; offer letter states every checklist element |
| HR02, HR04, HR08 | Requests and routing | Policy question to the owning team; reported concern to the intake route the policy text defines; request type for a workflow |
| HR03, HR05, HR07 | Notes and feedback | Interview note describes evidence or only an opinion; exit-comment theme; review comment cites a specific example |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/human-resources/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/human-resources/catalog.json).
The evaluation page reports the outcomes of the screening cases; this module asserts
no result, and a small synthetic screen is not qualification for a real people team.

Choose by what the label feeds:

- HR02 and HR08 feed a shared-inbox router. Code owns the table from label to queue
  or workflow, the eligibility and balance checks, and the answer; the label only
  says where a question or request belongs.
- HR04 feeds concern intake. The organization's own policy text is supplied as
  `policy_routes` and defines the four routes; code applies the standing rule that
  any concern describing imminent physical danger is escalated regardless of label,
  and people investigate.
- HR01 and HR06 feed a document check that returns text to its author. A person
  decides whether an essential requirement is job-related, and code compares offer
  values with the approved offer record exactly.
- HR03 and HR07 feed a quality prompt, not a rating: an opinion-only interview note or
  a generalization-only review comment goes back to its writer for a described
  example. Hiring and performance decisions stay with people.
- HR05 feeds an aggregate of exit themes. Code stores the comment verbatim, counts
  themes only above the minimum group size policy sets, and keeps individual comments
  out of a manager's view unless the departing employee agreed.

## Prepare a bounded state

Supply the requirement line and its heading, the question, note, comment, or request
as written, the offer letter with its checklist, and the intake policy text as the
organization publishes it. Several contracts state a precedence for text that fits
more than one label (a question spanning two areas, a concern fitting two routes, a
request asking for two things, a comment naming two reasons); keep those sentences when
adapting. Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent or empty evidence. Keep names, employee identifiers, health
details, and anything the judgment does not need out of the state; a routing label
needs the request, not the employee record.

## Use the labels without taking over

No label rates a candidate or employee, grants leave or equipment, approves an offer,
decides that a requirement is lawful, or determines whether a concern is true or
serious. No label classifies or infers race, sex, age, disability, religion, national
origin, health, honesty, or worth. Send only authorized text through the approved
provider path, and share exit and interview text only under the organization's own
consent and privacy rules.

## Verify against the people team's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/human-resources/evaluation/)
separates 24 design cases from 8 separately authored challenge cases and reports what
happened. Before use, compare labels with the queue that answered each question, the
route an intake coordinator chose, the workflow a coordinator opened, recruiters'
tagging of requirement lines, and an HR business partner's reading of notes and
comments. Measure concerns the label sent away from safety or employee relations first,
then offer letters whose omissions the label missed.
