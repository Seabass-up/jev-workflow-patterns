---
layout: default
title: "Motorsport measurement: patterns for tight-tolerance findings, setup logs, and hypotheses"
description: "Eight question contracts for motorsport measurement text: procedure completeness, anomaly attribution, constrained property, finding type, setup change count, telemetry baseline, scrutineering subject, and hypothesis testability."
permalink: /motorsport/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Motorsport measurement

Race engineering and quality teams read metrology reports, anomaly notes, setup change logs, telemetry summaries, and scrutineering notes where a fraction of a millimetre or a few grams matters. These eight contracts classify what that text states: whether a procedure is complete, what cause a note assigns, which property a limit constrains, whether a finding claims conformance, how many variables a run changed, whether a comparison names its baseline, what a scrutineering note concerns, and whether a hypothesis is measurable. They are task-authored, advisory designs. The model never reads a number as a result: every comparison, conversion, and pass or fail decision happens in code, and the scrutineers, quality lead, and race engineer decide.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/motorsport/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/motorsport/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 7/8 challenge cases** matched their prewritten labels: 31/32 overall. MR04 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Measurement reports

| ID | Question pattern | Intended use |
| --- | --- | --- |
| MR01 | [Measurement report states a complete procedure]({{ '/motorsport/patterns/mr01/' | relative_url }}) | Catches reports that cannot be reproduced or audited before their value enters the setup or conformance record; the value itself is never judged by the model. |
| MR02 | [Anomaly note attributes a deviation to instrument, setup, part, or nothing]({{ '/motorsport/patterns/mr02/' | relative_url }}) | Routes anomalies to calibration, setup, or parts follow-up according to what the author concluded, without the model deciding what the true cause is. |
| MR04 · provisional | [Finding statement is a conformance claim, an observation, or a recommendation]({{ '/motorsport/patterns/mr04/' | relative_url }}) | Separates statements that assert pass or fail from statements that merely report or propose, so no claimed conformance enters a record without an exact check. |

## Specifications and scrutineering

| ID | Question pattern | Intended use |
| --- | --- | --- |
| MR03 | [Which property a tolerance specification constrains]({{ '/motorsport/patterns/mr03/' | relative_url }}) | Lets a regulation extract or drawing note be filed against the right property without the model reading any number or computing any limit. |
| MR07 | [What a scrutineering note concerns]({{ '/motorsport/patterns/mr07/' | relative_url }}) | Routes each note to the right crew and measurement record; whether the car complies stays with the scrutineers and the exact checks in code. |

## Setup, telemetry, and hypotheses

| ID | Question pattern | Intended use |
| --- | --- | --- |
| MR05 | [Setup change log records one variable changed or several]({{ '/motorsport/patterns/mr05/' | relative_url }}) | Flags runs whose result cannot be attributed to one change before the engineer draws a conclusion from them; the attribution itself stays with the engineer. |
| MR06 | [Telemetry summary names its comparison baseline]({{ '/motorsport/patterns/mr06/' | relative_url }}) | Keeps words like faster, cooler, or more stable out of the debrief record unless the reference run, lap, car, or model is named; the numbers themselves are compared in code. |
| MR08 | [Hypothesis states a measurable prediction]({{ '/motorsport/patterns/mr08/' | relative_url }}) | Improves the chance that a test run can confirm or refute what it was meant to test; whether the prediction came true is decided from logged data in code. |

## Start with a small bundle

Start with MR01 (procedure completeness) and MR04 (finding type) in front of the conformance record, so no value enters without a stated procedure and no claimed pass bypasses the exact check in code. Add MR05 (setup change count) and MR06 (telemetry baseline) in the debrief flow, so the engineer sees which runs can be attributed to one change against a named reference. MR07 routes scrutineering notes once the first four are trusted.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a measurement result or a compliance decision. Code stores values and units exactly as written, converts units, compares against the tolerance record, computes every telemetry delta, and diffs setup sheets; the model never decides that a part conforms, a car is legal, or a cause is real. The scrutineers' decisions, the quality lead's sign-off, and the race engineer's conclusions are authoritative, and safety-equipment notes are handled under the series' rules regardless of any label.

[Exact catalog]({{ '/motorsport/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/motorsport/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/motorsport.md)
