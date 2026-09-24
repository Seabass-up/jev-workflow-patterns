# Grading support profiles

Use this module for classifying the text a teacher or grading assistant handles:
submissions read against a prompt, a rubric's criteria and level descriptions,
feedback comments, quoted material, worked responses, and passages paired with a
source. A label is a reading of the work or the rubric wording, never of the student.
Grades, points, late policies, and any academic-integrity decision stay with the
teacher and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/grading/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| GR01, GR05, GR08 | Submission content | Prompt coverage; working shown or final answer only; a labelled conclusion concludes |
| GR04, GR06 | Sources and citation | Citation attached to quoted material; wording relation to a source passage |
| GR02, GR03, GR07 | Rubric and feedback text | Evidence for one criterion; a comment names a next step; adjacent levels state a boundary |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/grading/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/grading/catalog.json).
The evaluation page reports screening outcomes; a screening is a small synthetic
check, not qualification for a classroom.

Choose by what the label feeds:

- GR01 and GR02 feed the teacher's reading order. Code splits the rubric into one
  criterion per call and checks counts, lengths, and headings exactly; the level and
  points for each criterion stay with the teacher.
- GR03 feeds a review of comments before they are returned. Code never rewrites or
  sends a comment; `evaluation_only` and `generic_advice` are listed, not fixed.
- GR04 and GR06 feed a per-passage list shown with the source alongside. Code runs
  exact and near-exact matching first and checks citation format against the
  reference list; the teacher makes any decision about acceptability or integrity.
- GR05 feeds a method-mark queue. The stated answer is compared with the key in code;
  the label says nothing about correctness.
- GR07 runs once on the rubric before it is used, pairing adjacent levels of each
  criterion; numeric thresholds between levels are compared in code.
- GR08 feeds a list of conclusions for the teacher to read first.

## Prepare a bounded state

Supply the prompt as assigned, one rubric criterion per call with any numeric
threshold stripped and checked in code, the student's words unchanged, the feedback
comment as written, and the source passage code paired with the student's passage.
Several contracts state a precedence for mixed cases: partial coverage beside
unrelated material, an evaluation beside a concrete step, verbatim sentences beside
original ones, and restating beside new material; keep those sentences when adapting.
Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent or empty evidence. Remove student names, identifiers, and any
detail the judgment does not need.

## Use the labels without taking over

No label assigns a level, points, or a grade, applies a late or resubmission policy,
decides that a passage is plagiarised, or says anything about a student's ability,
effort, or circumstances. GR06 describes a wording relation only; GR04 reports
whether a citation is attached, not whether it is correct or the source exists.
Student work and feedback are personal data: send only the passages the judgment
needs through the approved provider path, with identifying details removed, and keep
grades and records out of the state.

## Verify against the teacher's own marking

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/grading/evaluation/)
page reports outcomes for the design cases and for separately authored challenge
cases. Before use, compare labels with the teacher's per-criterion marks, on-topic
notes, method-mark decisions, citation checklist, and comments on conclusions across
a graded set. Measure first the cases where a label would have moved a submission out
of the teacher's reading queue.
