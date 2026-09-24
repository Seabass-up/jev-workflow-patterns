---
layout: default
title: "Motorsport: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /motorsport/sources/
kicker: "5 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## MR-S1: Wikipedia: Metrology

[Read the source](https://en.wikipedia.org/wiki/Metrology) · checked 2026-09-23 · SHA-256 `7fb437e6fe9e0edc…`

Describes metrology as defining units, realising them in practice, and tracing practical measurements to reference standards, with calibration and harmonised test procedures and report formats giving confidence in results. Motivates MR01 as a check that a report states its instrument, reference, and conditions, and MR02 as a reading of whether a note blames the instrument. Motivation only, not evidence of Jev performance.

Used by: [MR01]({{ '/motorsport/patterns/mr01/' | relative_url }}), [MR02]({{ '/motorsport/patterns/mr02/' | relative_url }})

## MR-S2: NIST: Measurement Uncertainty (Statistical Engineering Division topic page)

[Read the source](https://www.nist.gov/itl/sed/topic-areas/measurement-uncertainty) · checked 2026-09-23 · SHA-256 `729fb9d8a1c8a35d…`

States that a measurand has a numerical magnitude and a reference that gives that magnitude meaning, and that uncertainty characterises the dispersion of values attributable to it. Motivates MR01 (a reference must be stated), MR02 and MR04 (a value is not a result until compared in code), MR03 (the property must be identified before its limit is applied), and MR08 (a prediction needs a named quantity). Motivation only, not evidence of Jev performance.

Used by: [MR01]({{ '/motorsport/patterns/mr01/' | relative_url }}), [MR02]({{ '/motorsport/patterns/mr02/' | relative_url }}), [MR03]({{ '/motorsport/patterns/mr03/' | relative_url }}), [MR04]({{ '/motorsport/patterns/mr04/' | relative_url }}), [MR08]({{ '/motorsport/patterns/mr08/' | relative_url }})

## MR-S3: Wikipedia: Engineering tolerance

[Read the source](https://en.wikipedia.org/wiki/Engineering_tolerance) · checked 2026-09-23 · SHA-256 `8d45a77d81c9c266…`

Defines a tolerance as the permissible limit of variation, notes that tolerances can be applied to any dimension or physical property, and that a part outside tolerance is unusable by design intent while a stated tolerance does not by itself imply compliance. Motivates MR03 (which property is constrained), MR04 (a conformance claim is distinct from an observation), and MR07 (dimensional and mass notes). Motivation only, not evidence of Jev performance.

Used by: [MR03]({{ '/motorsport/patterns/mr03/' | relative_url }}), [MR04]({{ '/motorsport/patterns/mr04/' | relative_url }}), [MR07]({{ '/motorsport/patterns/mr07/' | relative_url }})

## MR-S4: Wikipedia: Racing setup

[Read the source](https://en.wikipedia.org/wiki/Racing_setup) · checked 2026-09-23 · SHA-256 `c12744b5a1560563…`

Lists the adjustable parameters of a racing car, such as dampers, anti-roll bars, gear ratios, tyre pressures, wing angles, toe, camber, brake bias, and ride height, and the handling trends adjustments usually produce. Motivates MR05 (a change log names one or several of these parameters), MR06 (a change is judged against a reference run), and MR07 (scrutineering notes concern the same adjustable geometry). Motivation only, not evidence of Jev performance.

Used by: [MR05]({{ '/motorsport/patterns/mr05/' | relative_url }}), [MR06]({{ '/motorsport/patterns/mr06/' | relative_url }}), [MR07]({{ '/motorsport/patterns/mr07/' | relative_url }})

## MR-S5: Wikipedia: Telemetry (motor racing section)

[Read the source](https://en.wikipedia.org/wiki/Telemetry) · checked 2026-09-23 · SHA-256 `36bc7b6bd4ed9795…`

Describes race engineers interpreting data collected during a test or race to tune the car, including accelerations, temperatures, wheel speeds, and suspension displacement, and systems that compute an expected lap time the driver is measured against. Motivates MR05 and MR06 (a run is compared with a named reference from logged channels) and MR08 (a hypothesis should name a logged quantity). Motivation only, not evidence of Jev performance.

Used by: [MR05]({{ '/motorsport/patterns/mr05/' | relative_url }}), [MR06]({{ '/motorsport/patterns/mr06/' | relative_url }}), [MR08]({{ '/motorsport/patterns/mr08/' | relative_url }})

Full digests are in [sources.json]({{ '/motorsport/sources.json' | relative_url }}).

[Back to the collection]({{ '/motorsport/' | relative_url }})
