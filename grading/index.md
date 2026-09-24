---
layout: default
title: "Grading support: patterns for submissions, rubrics, and feedback"
description: "Eight question contracts for grading text: prompt coverage, evidence for one rubric criterion, actionable feedback, citation presence, shown working, wording relation to a source, rubric level boundaries, and whether a labelled conclusion concludes."
permalink: /grading/
kicker: "8 profiles · 29/32 labels matched · kernel 2.6.0"
---

# Grading support

Teachers and grading assistants read the same kinds of text for every class: a set of submissions against one prompt, a rubric whose levels may or may not be distinguishable, comments going back to students, and passages that may echo a source. These eight contracts classify that text so a teacher's reading time goes where it is needed. They are synthetic, task-authored designs and their labels are advisory. Every judgment concerns the work or the rubric wording, never the student; grades, points, late policies, and any academic-integrity decision stay with the teacher and code.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/grading/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/grading/evaluation/' | relative_url }})

## What the screen established

**23/24 design cases and 6/8 challenge cases** matched their prewritten labels: 29/32 overall. GR02, GR05, GR06 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Submission content

| ID | Question pattern | Intended use |
| --- | --- | --- |
| GR01 | [Submission addresses the assigned prompt]({{ '/grading/patterns/gr01/' | relative_url }}) | Flags off-topic and partial responses before the rubric is applied, so the teacher reads those first; what they earn stays with the teacher. |
| GR05 · provisional | [Response shows its working or only a final answer]({{ '/grading/patterns/gr05/' | relative_url }}) | Separates responses the teacher can follow from bare answers before marks are assigned; correctness is checked by the teacher or code. |
| GR08 | [Section labelled conclusion actually concludes]({{ '/grading/patterns/gr08/' | relative_url }}) | Points the teacher to conclusions that restate or wander before the essay is graded; the grade and the feedback wording stay with the teacher. |

## Sources and citation

| ID | Question pattern | Intended use |
| --- | --- | --- |
| GR04 | [Quoted claim is accompanied by a citation]({{ '/grading/patterns/gr04/' | relative_url }}) | Points the teacher to quoted material without a citation before the essay is graded; whether the citation format is correct and whether the source exists are checked in code and by the teacher. |
| GR06 · provisional | [Student passage relative to a supplied source passage]({{ '/grading/patterns/gr06/' | relative_url }}) | Gives the teacher a reading of wording and structure for a passage code has paired with a source; any academic-integrity decision stays with the teacher. |

## Rubric and feedback text

| ID | Question pattern | Intended use |
| --- | --- | --- |
| GR02 · provisional | [Work shows evidence for one rubric criterion]({{ '/grading/patterns/gr02/' | relative_url }}) | Gives the teacher a per-criterion pointer to where evidence is or is not, one criterion per question, so the rubric is applied to the work rather than to an impression. |
| GR03 | [Feedback comment names a concrete next step]({{ '/grading/patterns/gr03/' | relative_url }}) | Lets a teacher or feedback assistant see which comments a student can act on before the comments are returned; nothing about the student is judged. |
| GR07 | [Two rubric levels overlap without a stated boundary]({{ '/grading/patterns/gr07/' | relative_url }}) | Finds rubric levels a grader cannot tell apart before the rubric is used, so the teacher can revise the wording; the rubric itself stays the teacher's. |

## Start with a small bundle

Start with GR01 (prompt coverage) and GR02 (evidence per criterion) to organise a first read of a submission set, add GR03 (feedback next step) before comments are returned, and run GR07 (level boundaries) once on the rubric before it is used. Add GR04, GR05, GR06, and GR08 for the assignment types they fit.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a mark. Code checks word counts, section headings, answer keys, citation formats, and exact string overlap; the teacher assigns levels, points, and grades, applies late and resubmission policies, and makes any academic-integrity decision. No contract judges a student's ability, effort, circumstances, or honesty, and GR06 describes a wording relation only. Student work and feedback are personal data: send only the passages the judgment needs, through an authorized path, with identifying details removed.

[Exact catalog]({{ '/grading/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/grading/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/grading.md)
