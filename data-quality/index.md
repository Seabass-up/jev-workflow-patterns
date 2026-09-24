---
layout: default
title: "Data quality: patterns for definitions, records, and annotations"
description: "Eight question contracts for the text around a dataset: a column definition against sampled values, entity identity across two records, a free-text value against a taxonomy entry, the reason for a missing value, a schema change note, a dictionary definition's readings, an outlier note, and an annotation escalation."
permalink: /data-quality/
kicker: "8 profiles · 29/32 labels matched · kernel 2.6.0"
---

# Data quality

Data engineers, analysts, and annotation leads spend much of their day reading text about data rather than the data itself: a dictionary entry beside a sample of values, two records that might be one customer, a note explaining a blank, a schema change announcement, an analyst's comment on a flagged outlier, an annotator's reason for escalating an item. These eight contracts classify that text so dictionary review, entity-resolution review, coding, missing-value handling, and annotation triage can route it. They are synthetic, task-authored designs and advisory. Every count, statistic, threshold, type check, and identifier match is computed in code, and no label decides that data is correct.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/data-quality/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/data-quality/evaluation/' | relative_url }})

## What the screen established

**21/24 design cases and 8/8 challenge cases** matched their prewritten labels: 29/32 overall. DQ03, DQ06 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Definitions and schemas

| ID | Question pattern | Intended use |
| --- | --- | --- |
| DQ01 | [Column definition matches the described sample values]({{ '/data-quality/patterns/dq01/' | relative_url }}) | Finds columns whose documentation and content have drifted apart before an analyst trusts the definition, while type, format, and range checks stay in code. |
| DQ05 | [Schema change note is additive, narrowing, or a meaning change]({{ '/data-quality/patterns/dq05/' | relative_url }}) | Catches the change that keeps a column's name and type but alters what it means, which a schema diff cannot see, while the diff and the consumer list stay in code. |
| DQ06 · provisional | [Dictionary definition admits one reading or two]({{ '/data-quality/patterns/dq06/' | relative_url }}) | Surfaces definitions that will produce values recorded on two different bases before the data is collected, while the rewording stays with the data owner. |

## Records and values

| ID | Question pattern | Intended use |
| --- | --- | --- |
| DQ02 | [Two records describe the same entity]({{ '/data-quality/patterns/dq02/' | relative_url }}) | Gives entity-resolution review a reading of the record text that separates a duplicate from a branch, variant, or member, while identifier matching and the merge decision stay with code and a curator. |
| DQ03 · provisional | [Free-text value fits the proposed taxonomy entry]({{ '/data-quality/patterns/dq03/' | relative_url }}) | Lets code auto-apply codings that fit the written definition and route the rest to a coder or the taxonomy owner, instead of a person re-reading every value. |
| DQ04 | [Reason a note gives for a missing value]({{ '/data-quality/patterns/dq04/' | relative_url }}) | Separates legitimate absence from collection gaps and processing losses so code can apply the right handling rule instead of treating every null the same way. |
| DQ07 | [Outlier note states a cause or only the value]({{ '/data-quality/patterns/dq07/' | relative_url }}) | Lets code decide whether an exclusion or correction is documented well enough to stand, without the model judging the value or the cause itself. |

## Annotation

| ID | Question pattern | Intended use |
| --- | --- | --- |
| DQ08 | [What an annotation escalation note faults]({{ '/data-quality/patterns/dq08/' | relative_url }}) | Routes escalations to a guideline revision, a definition rewording, item adjudication, or a discussion without the annotation lead re-reading every note. |

## Start with a small bundle

For a dictionary audit, start with DQ06 (definition readings) and DQ01 (definition against a code-drawn sample), then DQ05 (schema change notes) gated on the diff code computes. For record stewardship, DQ02 (same entity) behind exact identifier checks and a curator's merge approval, with DQ04 (missing-value reasons) for the completeness audit. For annotation leads, DQ08 (escalation triage) alongside CT06 for rationale consistency.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of definitions, notes, and record text, not a determination that data is correct, complete, or duplicated. Code owns type and format checks, null and outlier detection, identifier equality, string similarity, agreement statistics, schema diffs, and every threshold. A curator approves any merge, a data owner approves any definition or schema change, and the annotation lead approves any guideline change. Personal data in records is supplied only when the judgment needs it and the transfer is authorized, and no question asks the model anything about the people a record describes.

[Exact catalog]({{ '/data-quality/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/data-quality/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/data-quality.md)
