---
layout: default
title: "Automotive performance: patterns for modifications, tuning notes, and fitment"
description: "Eight question contracts for automotive performance text: the vehicle system a modification changes, stated use, fitment claims, tuning-note symptoms, re-inspection under rules text, install reversibility, dyno report claims, and the grounds a forum post offers."
permalink: /auto-performance/
kicker: "8 profiles · 34/34 current labels matched · AP03 v2"
---

# Automotive performance

Performance shops, tuners, and enthusiasts' assistants read modification requests, fitment text, tuning logs, install instructions, dyno reports, and forum threads. These eight contracts classify that text so intake, the tuning log, the job sheet, and an advice ranker can act on a consistent reading. They are synthetic, task-authored designs and advisory. The qualified installer, the tuner, and the tech inspector decide, and every numeric comparison happens in code.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, at least three design examples, and challenge cases. Versioned refinements preserve earlier states and labels and may add boundary cases; a development-added case is not described as an independent held-out challenge.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/auto-performance/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/auto-performance/evaluation/' | relative_url }})

## What the screen established

The original version-1 screen matched **24/24 design cases and 8/8 independently authored challenges** (32/32). AP03 v2 preserves and re-screens its four original states and labels, then adds two development-authored fitment-boundary challenges; all six v2 cases match. The current selected set matches **24/24 design and 10/10 challenge cases** (34/34). AP03-6's `unknown` answer has confidence 0.37, below its 0.8 review floor, so it is not an automatic pass-through. No pattern has a recorded label disagreement. The original cases were not rewritten or relabeled.

The original challenge authors saw each contract but not its design examples or model results. AP03-5 and AP03-6 were added by the contract reviewer during revision and are development evidence, not independent challenges. Neither set is independent human labeling, a representative test set, or a measure of benefit in use.

## Modification intake

| ID | Question pattern | Intended use |
| --- | --- | --- |
| AP01 | [Vehicle system changed by a modification request]({{ '/auto-performance/patterns/ap01/' | relative_url }}) | Sorts modification requests by the system they touch instead of by keyword, while the shop keeps the scoping and quoting decision. |
| AP02 | [Stated use of the vehicle: track, street, show, or mixed]({{ '/auto-performance/patterns/ap02/' | relative_url }}) | Makes the stated use explicit before parts are chosen, so a street-only car is not quoted a competition setup and a track car is not quoted show parts. |
| AP03 | [Fitment claim supported by the supplied fitment text]({{ '/auto-performance/patterns/ap03/' | relative_url }}) | Catches a part ordered for a vehicle its fitment text excludes or conditions before it ships, while exact year, dimension, and part-number checks stay in code. |

## Tuning, dyno, and advice

| ID | Question pattern | Intended use |
| --- | --- | --- |
| AP04 | [Symptom category described by a tuning note and its flagged readings]({{ '/auto-performance/patterns/ap04/' | relative_url }}) | Tags pulls by the symptom described, using comparisons code has already made, so the tuner can review knock and lean events first; the tuner keeps the diagnosis and every change to the calibration. |
| AP07 | [Dyno report states a measured result with conditions, or a claim]({{ '/auto-performance/patterns/ap07/' | relative_url }}) | Separates measured results from advertised or estimated figures before numbers are compared, so a customer is not shown a gain computed from an estimate. |
| AP08 | [Forum advice cites a source or measurement, or is anecdote]({{ '/auto-performance/patterns/ap08/' | relative_url }}) | Keeps an assistant from repeating unsourced forum advice as fact, and tells the reader what kind of grounds a post offers before they act on it. |

## Install and rules

| ID | Question pattern | Intended use |
| --- | --- | --- |
| AP05 | [Described change calls for re-inspection under the supplied rules text]({{ '/auto-performance/patterns/ap05/' | relative_url }}) | Answers the recurring question of whether a change needs to go back through tech or be declared, from the rules text the organizer or authority supplied, without the model deciding eligibility. |
| AP06 | [Install step is reversible or permanent]({{ '/auto-performance/patterns/ap06/' | relative_url }}) | Lets a shop disclose permanent alterations before work starts and estimate return-to-stock effort from the instructions, while the installer decides how the work is done. |

## Start with a small bundle

For intake, AP01 (system changed), AP02 (stated use), and AP03 (fitment claim) with exact year, offset, and part-number checks in code. For the tuning bay, AP04 (symptom category from a note and code-written flags) and AP07 (measured result or claim). Add AP05 (re-inspection under rules text) and AP06 (reversible or permanent) when the job sheet needs a rules check and disclosure of permanent alterations.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, never a safety, emissions-compliance, legality, or fitness determination. Code compares model years, offsets, dimensions, logged readings, thresholds, and dyno figures exactly; supplies rules text with its revision; records the inspector's, authority's, and tuner's own determinations as authoritative; and never changes a calibration, admits a vehicle, or approves a part from a label. The qualified installer decides whether and how any work is done.

[Exact catalog]({{ '/auto-performance/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/auto-performance/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/auto-performance.md)
