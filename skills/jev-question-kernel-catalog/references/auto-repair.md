# Auto repair profiles

Use this module for classifying the text an auto repair shop handles: a customer's
description of a symptom, a reported condition, repair-order lines, replies to an
estimate, part descriptions, warranty narratives, technician inspection notes, and
estimate explanations. A label is a reading of text. The technician's determination,
the customer's authorization record, prices, dates, mileage, and coverage decisions
stay with people and code.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/auto-repair/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| AR01, AR02 | Intake | Symptom category from the customer's description; stop-driving signs versus inspection versus routine |
| AR04, AR07, AR08 | Authorization and presentation | What a customer reply does with an estimate; how a technician's inspection note characterizes an item; whether an estimate itemizes parts and labor |
| AR03, AR05, AR06 | Service writing | Repair-order line type; part origin and condition; warranty narrative cause against a supplied policy text |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/auto-repair/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/auto-repair/catalog.json).
The evaluation page reports the screening outcomes; a small synthetic check is not
qualification for a real shop.

Choose by what the label feeds:

- AR01 and AR02 feed the front counter. Code runs the standing advisor script for
  `stop_driving_sign`; the technician's own determination once the vehicle is seen
  overrides the label, and no label is shown to the customer as advice.
- AR04 feeds the authorization record, which code keeps with the time, channel,
  amount, and exact scope under the jurisdiction's rule. No work starts on the label
  alone; the advisor confirms scope for `approves_in_part`.
- AR03 and AR08 feed the write-up desk. Labor operation codes, flat-rate time, and
  every amount stay in code; code sums parts, labor, supplies, and tax and blocks an
  estimate whose stated total does not match.
- AR05 identifies a part's stated origin and condition only. Part numbers are matched
  exactly in code, and the disclosure rule for used and rebuilt parts is applied there.
- AR06 and AR07 route a narrative or a note by the technician's own words. The warranty
  administrator decides coverage; date and mileage limits are compared in code; the
  category the technician selected on the inspection form is authoritative.

## Prepare a bounded state

Supply the customer's, writer's, or technician's words unchanged, the estimate
summary the customer was actually sent, and the policy text in force as written.
Several contracts state a precedence order for text that mentions more than one
symptom, work type, or characterization, and AR06 says to select `unknown` when a
narrative describes more than one cause without saying which caused the failure;
keep those sentences when adapting. Before inference, code validates
`required_state_fields` and returns a local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label diagnoses a fault, decides that a vehicle is or is not safe to drive,
authorizes work, prices a line, compares a measurement with a limit, or decides
warranty coverage. Send only authorized shop text through the approved provider
path; keep customer names, contact details, vehicle identification numbers, plate
numbers, and payment details out of the state unless the judgment needs them and
the transfer is authorized.

## Verify against the shop's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/auto-repair/evaluation/)
separates the design cases from separately authored challenge cases and reports the
outcomes. Before use, compare labels with the concern types and line types on closed
repair orders, the authorization records advisors entered, the categories technicians
selected on the inspection form, the parts desk's part-type records, and the warranty
administrator's cause codes. Measure missed stop-driving signs and safety items first.
