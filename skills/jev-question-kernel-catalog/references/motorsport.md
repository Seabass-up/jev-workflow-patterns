# Motorsport measurement profiles

Use this module for classifying the text a race engineering or quality team writes
around tight-tolerance measurements: metrology reports, anomaly notes, tolerance
specifications, finding statements, setup change logs, telemetry summaries,
scrutineering notes, and hypotheses. A label is a reading of text. Every numeric
comparison, tolerance check, unit conversion, and pass or fail decision happens in
code, and the scrutineers, quality lead, and race engineer decide.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/motorsport/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| MR01, MR02, MR04 | Measurement reports | Report states instrument, reference, and conditions; cause an anomaly note assigns; finding is a conformance claim, observation, or recommendation |
| MR03, MR07 | Specifications and scrutineering | Property a tolerance text constrains; subject of a scrutineering note |
| MR05, MR06, MR08 | Setup, telemetry, and hypotheses | One or several parameters changed; telemetry comparison names its baseline; hypothesis names a measurable quantity |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/motorsport/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/motorsport/catalog.json).
The [evaluation page](https://seabass-up.github.io/jev-workflow-patterns/motorsport/evaluation/)
reports the screening outcomes; that is a small synthetic check, not qualification
for a real team.

Choose by what the label feeds:

- MR01 and MR04 guard the conformance record. A value enters only with a
  `complete_procedure` label or a reviewer sign-off, and every `conformance_claim`
  is re-checked in code against the stored value, tolerance, and unit.
- MR02 routes an anomaly to calibration, setup, or parts follow-up according to what
  the author concluded; the investigator's closed cause is authoritative.
- MR03 and MR07 select which record a specification or scrutineering note belongs
  to. Code parses the number and unit and performs the comparison; the scrutineers
  decide compliance.
- MR05, MR06, and MR08 feed the debrief. Code diffs setup sheets, computes telemetry
  deltas from the named baseline, and evaluates a prediction from logged data; the
  race engineer decides what a run showed.

## Prepare a bounded state

Supply the technician's, engineer's, or scrutineer's words unchanged, the measured
quantity as the request names it, and nothing the model should compute: no tolerance
bands to compare, no unit conversions, no expected results. Several contracts state a
precedence order for text that does more than one thing, such as a finding that both
observes and claims, a note that raises two subjects, or a note that attributes two
causes; keep those sentences when adapting. Before inference, code validates
`required_state_fields` and returns a local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label decides that a part conforms, a car is legal, a cause is real, a change was
wise, or a prediction came true. Send only authorized team text through the approved
provider path; keep driver identities, chassis and part serial numbers, supplier
contracts, and regulation text under licence out of the state unless the judgment
needs them and the transfer is authorized. Safety-equipment notes are handled under
the series' rules regardless of any label.

## Verify against the team's own records

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/motorsport/evaluation/)
separates the 24 design cases from separately authored challenge cases and reports
their outcomes. Before use, compare labels with the quality lead's report reviews,
the causes recorded when anomalies were closed, setup-sheet diffs, baselines found
in the data store, and the crew assignments of scrutineering notes. Measure missed
conformance claims and runs wrongly treated as single-variable first.
