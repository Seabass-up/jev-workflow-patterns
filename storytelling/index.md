---
layout: default
title: "Storytelling: patterns for authors and editing assistants"
description: "Eight question contracts about manuscript text: scene change, viewpoint, canon consistency, rendered emotion, speaker clarity, payoffs, voice, and reader grounding."
permalink: /storytelling/
kicker: "8 profiles · 27/32 labels matched · kernel 2.5.0"
---

# Storytelling

An author revising a long manuscript, or an assistant helping one, keeps asking small, checkable questions: did this scene change anything, can the reader tell who is speaking, does this line sound like her, did I ever pay off that key. These eight contracts turn those questions into bounded text judgments over the author's own material. They are task-authored adaptations of ordinary craft guidance, not rules, and the author decides every revision.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/storytelling/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/storytelling/evaluation/' | relative_url }})

## What the screen established

**20/24 design cases and 7/8 challenge cases** matched their prewritten labels: 27/32 overall. ST04, ST05, ST08 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Structure

| ID | Question pattern | Intended use |
| --- | --- | --- |
| ST01 | [Scene changes the situation]({{ '/storytelling/patterns/st01/' | relative_url }}) | Helps an author or editing assistant find scenes that could be cut or merged because nothing changes in them. |
| ST06 | [Later passage pays off the setup]({{ '/storytelling/patterns/st06/' | relative_url }}) | Helps track planted details so they are paid off or removed before publication. |

## Consistency

| ID | Question pattern | Intended use |
| --- | --- | --- |
| ST02 | [Passage reveals what the viewpoint character cannot know]({{ '/storytelling/patterns/st02/' | relative_url }}) | Catches viewpoint slips that break the reader's trust in a limited point of view. |
| ST03 | [Passage contradicts the story bible]({{ '/storytelling/patterns/st03/' | relative_url }}) | Keeps names, dates, places, and rules of the world consistent across a long or serialized work. |
| ST08 · provisional | [Passage relies on something the reader has not been told]({{ '/storytelling/patterns/st08/' | relative_url }}) | Catches references to characters, places, or events that were cut or moved earlier in revision. |

## Craft

| ID | Question pattern | Intended use |
| --- | --- | --- |
| ST04 · provisional | [Emotion is stated or rendered]({{ '/storytelling/patterns/st04/' | relative_url }}) | Gives an author a way to find told emotion beats they may want to render, without a rule that telling is always wrong. |
| ST05 · provisional | [Reader can tell who is speaking]({{ '/storytelling/patterns/st05/' | relative_url }}) | Finds exchanges where dropped tags or similar voices leave the reader guessing. |
| ST07 | [Line matches the character's voice profile]({{ '/storytelling/patterns/st07/' | relative_url }}) | Keeps a character sounding like themselves across drafts and co-written chapters. |

## Start with a small bundle

For a revision pass, try ST01 (scene change), ST06 (payoffs), and ST08 (reader grounding) with a story bible maintained in code. For line editing, ST04 (stated or rendered emotion), ST05 (speaker clarity), and ST07 (voice). For a serialized or co-written work, ST02 and ST03 guard viewpoint and canon.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

The judgments examine supplied passages against supplied context, not the author or their ability. A label is information for revision; stated emotion, ambiguous speakers, and unpaid setups are sometimes deliberate. Code owns the story bible, knowledge ledgers, scene boundaries, and revisions; nothing here edits text.

[Exact catalog]({{ '/storytelling/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/storytelling/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/storytelling.md)
