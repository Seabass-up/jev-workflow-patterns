---
layout: default
title: "Call controls: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /controls/sources/
kicker: "6 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## CS-1: TypeSafe: Confidence

[Read the source](https://docs.typesafe.ai/confidence.md) · checked 2026-09-22 · SHA-256 `97dafe98b7797990…`

Confidence is derived from the probability distribution; the page's three-option approximation generalizes to the option-count relationship measured in this repository. Motivates CT01.

Used by: [CT01]({{ '/controls/patterns/ct01/' | relative_url }})

## CS-2: TypeSafe: How to build with TypeSafe

[Read the source](https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md) · checked 2026-09-22 · SHA-256 `d9f4d34c1349bf5a…`

Decomposes a tool-call trace and a phishing message into atomic questions and suggests reasoning-model ensembles for labels. Several of its trace checks are exact comparisons this collection moves into code. Motivates CT02, CT06, CT09, CT10.

Used by: [CT02]({{ '/controls/patterns/ct02/' | relative_url }}), [CT06]({{ '/controls/patterns/ct06/' | relative_url }}), [CT09]({{ '/controls/patterns/ct09/' | relative_url }}), [CT10]({{ '/controls/patterns/ct10/' | relative_url }})

## CS-3: TypeSafe: Jev 1.13 jaggedness

[Read the source](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md) · checked 2026-09-22 · SHA-256 `e69329bd32e91ac0…`

Literal reading, math in code, state-side context rot, and non-guaranteed structural invariants such as a question and its negation. Motivates CT01, CT02, CT03, CT05, CT07, CT08, CT09.

Used by: [CT01]({{ '/controls/patterns/ct01/' | relative_url }}), [CT02]({{ '/controls/patterns/ct02/' | relative_url }}), [CT03]({{ '/controls/patterns/ct03/' | relative_url }}), [CT05]({{ '/controls/patterns/ct05/' | relative_url }}), [CT07]({{ '/controls/patterns/ct07/' | relative_url }}), [CT08]({{ '/controls/patterns/ct08/' | relative_url }}), [CT09]({{ '/controls/patterns/ct09/' | relative_url }})

## CS-4: TypeSafe: Smart home assistant demo

[Read the source](https://docs.typesafe.ai/demos/smart-home.md) · checked 2026-09-22 · SHA-256 `155c0af9a4ae31d2…`

A Noul detects a compound request, a language model splits it, and each command is re-evaluated. Motivates CT03 and CT04.

Used by: [CT03]({{ '/controls/patterns/ct03/' | relative_url }}), [CT04]({{ '/controls/patterns/ct04/' | relative_url }})

## CS-5: TypeSafe: Models

[Read the source](https://docs.typesafe.ai/models.md) · checked 2026-09-22 · SHA-256 `9d20bb3c90a01475…`

English is the primary training language; other languages need testing and attention to confidence. Motivates CT05.

Used by: [CT05]({{ '/controls/patterns/ct05/' | relative_url }})

## CS-6: TypeSafe: Agent skill

[Read the source](https://docs.typesafe.ai/agent-skill.md) · checked 2026-09-22 · SHA-256 `5ed8f74a13376052…`

Recommends collaborative question editing and keeping questions and thresholds reviewable; the human-AI evaluation in this repository found nine overlapping contracts by hand. Motivates CT08.

Used by: [CT08]({{ '/controls/patterns/ct08/' | relative_url }})

Full digests are in [sources.json]({{ '/controls/sources.json' | relative_url }}).

[Back to the collection]({{ '/controls/' | relative_url }})
