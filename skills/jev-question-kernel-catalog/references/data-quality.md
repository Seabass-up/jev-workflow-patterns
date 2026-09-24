# Data quality profiles

Use this module for classifying the text that surrounds a dataset: a dictionary
entry beside sampled values, a pair of records, a free-text value against a taxonomy
entry, a note about a missing value, a schema change note, a field definition, an
analyst's note on a flagged outlier, and an annotator's escalation note. A label is
a reading of text. Type checks, counts, thresholds, identifier matching, agreement
statistics, and every decision to change data, a definition, or a guideline stay
with code and people.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/data-quality/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| DQ01, DQ05, DQ06 | Definitions and schemas | Definition against a code-drawn sample; effect a schema change note describes; whether a definition admits two readings |
| DQ02, DQ03, DQ04, DQ07 | Records and values | Same entity or a related one; free-text value against a proposed taxonomy entry; reason a note gives for a missing value; what an outlier note states |
| DQ08 | Annotation | What an annotator's escalation note faults |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/data-quality/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/data-quality/catalog.json).
The evaluation page reports screening outcomes; this module claims none, and a
synthetic screen is not qualification for a real dataset.

Choose by what the label feeds:

- DQ01 and DQ06 feed a dictionary review queue. Code draws the samples and runs
  type, format, and range checks; the data owner approves any rewording.
- DQ02 feeds entity-resolution review behind exact identifier checks. Code decides
  when authoritative identifiers agree or disagree, and a curator approves every
  merge; `related_but_distinct` keeps a branch, variant, or member from being merged
  into its parent.
- DQ03 verifies a coding that code proposed from exact and synonym matches.
  `fits_no_listed_entry` goes to the taxonomy owner; the model never adds an entry.
- DQ04 and DQ07 pick a handling rule for one value. Code detects the null or the
  outlier and applies the rule; no label fills, removes, or alters a value.
- DQ05 gates a change note against the schema diff code computes; disagreement
  between the note and the diff goes to a person.
- DQ08 routes an annotation escalation to the guideline, the item, or a discussion;
  the annotation lead approves any guideline change.

## Prepare a bounded state

Supply the definition, note, or record text unchanged, the entity type or taxonomy
level code selected, and only the sibling entries at one level. Several contracts
state a precedence order for notes that give more than one reason or describe more
than one kind of change; keep those sentences when adapting. Before inference, code
validates `required_state_fields` and returns a local `unknown` for absent or empty
evidence.

## Use the labels without taking over

No label marks data correct, merges records, assigns a taxonomy code, fills or drops
a value, approves a schema change, rewrites a definition, or labels an annotation
item. Send only authorized dataset text through the approved provider path; keep
personal identifiers, account numbers, and record keys out of the state unless the
judgment needs them and the transfer is authorized, and never ask a question about
the people a record describes.

## Verify against the steward's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/data-quality/evaluation/)
page reports outcomes for the design cases and any separately authored challenge
cases. Before use, compare labels with steward audits of the dictionary, curator
decisions on candidate pairs, coder decisions on free-text values, consumer breakages
after past schema changes, and the annotation lead's triage of escalations. Measure
`same_entity` labels on pairs a curator kept separate and `additive_only` labels on
changes that later broke a consumer first.
