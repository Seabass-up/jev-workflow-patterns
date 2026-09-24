# Electrical contracting profiles

Use this module for classifying the text an electrical contractor's office handles:
customer fault reports, described conditions, work descriptions, inspection
correction items, inspector notes, permitting-office messages, product descriptions,
and photo descriptions. A label is a reading of text. Licensed judgment on site, the
jurisdiction's rules, exact ratings, and safety procedures stay with people and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/electrical/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| EL01, EL02 | Service calls | Reported symptom for dispatch; hazard signs that call for de-energizing |
| EL03, EL04, EL05, EL06, EL08 | Permits and inspections | Work type for a permit rule; correction-item routing; inspection outcome; office request; photo coverage |
| EL07 | Materials | Protective device type from a product description |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/electrical/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/electrical/catalog.json).
All 32 screening cases matched their authored labels; that is a small synthetic
check, not qualification for a real office.

Choose by what the label feeds:

- EL01 and EL02 feed dispatch. Code enforces the standing escalation for
  `burning_smell_or_heat` and `immediate_hazard`; the electrician's own determination
  on site overrides the label.
- EL03 feeds a permit rule that code applies per jurisdiction and revision. The model
  never decides whether a permit is required.
- EL05 updates a working job record; the jurisdiction's recorded result is
  authoritative and disagreement goes to the office.
- EL07 identifies the protection type only. Ampere, voltage, and listing marks are
  compared exactly in code before a purchase proceeds.

## Prepare a bounded state

Supply the customer's or inspector's words unchanged, the project roles as written,
the inspection type, and the policy lists code owns. Several contracts state a
precedence order for reports that mention more than one symptom, work type, or party;
those sentences were added after a pre-inference overlap check, so keep them when
adapting. Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent or empty evidence.

## Use the labels without taking over

No label diagnoses a fault, sizes a circuit, applies a code article, assigns cost,
or accepts an inspection. Send only authorized job text through the approved provider
path; keep customer identities, addresses, permit numbers, and account details out
of the state unless the judgment needs them and the transfer is authorized.

## Verify against the office's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/electrical/evaluation/)
separates 24 design cases from 8 separately authored challenge cases. Before use,
compare labels with dispatcher categorizations, permits actually pulled, the
jurisdiction's recorded inspection results, and technician findings after the visit.
Measure missed hazard signs first.
