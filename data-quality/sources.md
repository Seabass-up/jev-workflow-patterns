---
layout: default
title: "Data quality: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /data-quality/sources/
kicker: "5 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## DQ-S1: Wikipedia: Data quality

[Read the source](https://en.wikipedia.org/wiki/Data_quality) · checked 2026-09-23 · SHA-256 `6d3ab578eb7614bc…`

Describes data quality through dimensions such as accuracy, completeness, consistency, and validity, and describes profiling and cleansing against agreed definitions and reference data. Motivates DQ01, DQ05, DQ06, and DQ07 as readings of documentation and notes rather than checks of the data itself. This is motivation for the judgments, not evidence of Jev performance.

Used by: [DQ01]({{ '/data-quality/patterns/dq01/' | relative_url }}), [DQ02]({{ '/data-quality/patterns/dq02/' | relative_url }}), [DQ03]({{ '/data-quality/patterns/dq03/' | relative_url }}), [DQ05]({{ '/data-quality/patterns/dq05/' | relative_url }}), [DQ06]({{ '/data-quality/patterns/dq06/' | relative_url }}), [DQ07]({{ '/data-quality/patterns/dq07/' | relative_url }}), [DQ08]({{ '/data-quality/patterns/dq08/' | relative_url }})

## DQ-S2: Wikipedia: Record linkage

[Read the source](https://en.wikipedia.org/wiki/Record_linkage) · checked 2026-09-23 · SHA-256 `6a196fac634a8b37…`

Describes finding records that refer to the same entity across sources that may lack a shared identifier, using deterministic rules, probabilistic thresholds, blocking, and pairs set aside for manual validation. Motivates DQ02 as the text reading inside a code-owned linkage pipeline. This is motivation, not evidence of Jev performance.

Used by: [DQ02]({{ '/data-quality/patterns/dq02/' | relative_url }})

## DQ-S3: Wikipedia: Missing data

[Read the source](https://en.wikipedia.org/wiki/Missing_data) · checked 2026-09-23 · SHA-256 `8654f6bdc0e05a51…`

Distinguishes reasons values are missing, such as nonresponse, attrition, improper collection, and data-entry mistakes, and states that understanding why data are missing matters for handling the remaining data correctly. Motivates DQ04 as a classification of the reason a note states; handling rules stay in code. This is motivation, not evidence of Jev performance.

Used by: [DQ04]({{ '/data-quality/patterns/dq04/' | relative_url }})

## DQ-S4: Frictionless Data: Table Schema specification (v1)

[Read the source](https://specs.frictionlessdata.io/table-schema/) · checked 2026-09-23 · SHA-256 `c9f81d5d1f86b7b6…`

Specifies field descriptors for tabular data with a name, type, format, description, and constraints, plus a list of values to treat as missing. Motivates DQ01, DQ03, DQ05, and DQ06 as readings of field descriptions, category definitions, and constraint changes; type and constraint validation stays in code. This is motivation, not evidence of Jev performance.

Used by: [DQ01]({{ '/data-quality/patterns/dq01/' | relative_url }}), [DQ03]({{ '/data-quality/patterns/dq03/' | relative_url }}), [DQ04]({{ '/data-quality/patterns/dq04/' | relative_url }}), [DQ05]({{ '/data-quality/patterns/dq05/' | relative_url }}), [DQ06]({{ '/data-quality/patterns/dq06/' | relative_url }})

## DQ-S5: Wikipedia: Inter-rater reliability

[Read the source](https://en.wikipedia.org/wiki/Inter-rater_reliability) · checked 2026-09-23 · SHA-256 `7e2761f2927f481a…`

Describes agreement among independent raters who code the same items, the statistics used to measure it, and the need for clearly stated guidelines and periodic retraining when rating targets are ambiguous. Motivates DQ08 as a triage of what an escalation note faults; agreement statistics are computed in code. This is motivation, not evidence of Jev performance.

Used by: [DQ08]({{ '/data-quality/patterns/dq08/' | relative_url }})

Full digests are in [sources.json]({{ '/data-quality/sources.json' | relative_url }}).

[Back to the collection]({{ '/data-quality/' | relative_url }})
