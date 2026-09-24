# Automotive performance profiles

Use this module for classifying the text a performance shop, tuner, or enthusiasts'
assistant handles: modification requests, statements of intended use, part fitment
text, tuning notes with code-flagged readings, rules excerpts about re-inspection,
install steps, dyno reports, and forum advice. A label is a reading of text. The
qualified installer, the tuner, and the tech inspector decide; model years, offsets,
logged readings, thresholds, and dyno figures are compared in code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/auto-performance/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| AP01, AP02, AP03 | Modification intake | Vehicle system changed; stated use; fitment claim against supplied fitment text |
| AP04, AP07, AP08 | Tuning, dyno, and advice | Symptom category from a note and code-written flags; measured result or claim in a dyno report; grounds a forum post offers |
| AP05, AP06 | Install and rules | Re-inspection under a supplied rules text; reversible or permanent install step |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/auto-performance/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/auto-performance/catalog.json).
The evaluation page reports the screening outcomes; a small synthetic check is not
qualification for a real shop.

Choose by what the label feeds:

- AP01, AP02, and AP03 feed intake. AP03 ignores model years and numeric ranges by
  design; code compares years, bolt patterns, offsets, and part numbers exactly and
  overrides a `supported` label when an exact check fails.
- AP04 feeds the tuning log. Code compares every reading with the tuner's targets and
  writes `reading_flags` in words before the question is asked; the tuner keeps the
  diagnosis and every calibration change.
- AP05 feeds a rules check. `threshold_dependent` hands a numeric threshold back to
  code; the inspector's or authority's determination is authoritative.
- AP06 feeds the job sheet's disclosure of permanent alterations; the installer
  decides how the work is done.
- AP07 and AP08 gate what figures and advice are shown. Code compares figures only
  when both are labelled measured, and verifies a cited source before ranking a post
  above anecdote.

## Prepare a bounded state

Supply the customer's, tuner's, or poster's words unchanged, the fitment text and
rules text as the vendor or organizer wrote them, and the flags code computed from
logged readings. Several contracts state a precedence order for text that describes
more than one system, use, symptom, item, or kind of grounds; keep those sentences
when adapting. Before inference, code validates `required_state_fields` and returns a
local `unknown` for absent or empty evidence, including an empty `reading_flags` list.

## Use the labels without taking over

No label decides that a modification is safe, legal, emissions-compliant, or fit for
the vehicle, admits a vehicle to an event or register, changes a calibration, approves
a part, or confirms that forum advice is correct. Send only authorized job text through
the approved provider path; keep customer identities, plates, vehicle identification
numbers, and account details out of the state unless the judgment needs them and the
transfer is authorized.

## Verify against the shop's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/auto-performance/evaluation/)
reports outcomes for the design cases and any separately authored challenge cases.
Before use, compare labels with the service writer's intake categories, parts returned
for fitment, the tuner's own log tags, the tech inspector's determinations, and the
installer's marking of permanent steps. Measure missed knock descriptions and missed
fitment exclusions first.
