---
layout: default
title: Research edition in the Jev kernel
description: Ten source-bound advisory contracts, preserved research status, and practical consumer safeguards.
permalink: /kernel/research-edition/
kicker: Kernel v2.8.0 · pinned research supplement
---

# Ten research contracts, with their evidence limits

This page describes the preserved September 27 snapshot. The later
[2.9.0 research working import]({{ '/kernel/research-working/' | relative_url }})
separately adds 19 audit-pending contracts, including JP-001@4 and JP-017@1,
plus one composition. It does not alter this older bundle.

The kernel now has a separate research module drawn from **Research Jev Patterns**
at `48a8b4569a9ce5b17ce1119d63179e84a2990ae6` (September 27, 2026). It preserves
the ten admitted v0.2.0 contracts byte-for-byte. JP-011 is version 2; the other nine
are version 1. They are attributed task adapters, not ten new reasoning primitives,
and are counted separately from the existing 390-profile catalog.

[Read the complete skill module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/research-edition.md)
· [Inspect the source-bound manifest](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/manifest.json)
· [Return to the kernel]({{ '/kernel/' | relative_url }})

## Choose the task and its consumer

| Contract | Useful question | What the answer can do |
| --- | --- | --- |
| [JP-002](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-002.v1.json) | What stage is explicitly documented for this work item? | Annotate planned, performed, tested or explicitly accepted; review missing/conflicting evidence |
| [JP-003](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-003.v1.json) | Would this observation distinguish the two stated predictions? | Help select an informative diagnostic observation, without authorizing a test |
| [JP-004](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-004.v1.json) | Does this non-detection support the scoped absence claim? | Distinguish suitable complete coverage from inadequate, contrary or unknown evidence |
| [JP-005](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-005.v1.json) | Which supplied span has the requested role? | Let code copy a validated exact span; never generate a missing value |
| [JP-007](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-007.v1.json) | Are these records the same entity, related-but-distinct, or different? | Annotate a relation for curator review, never merge records automatically |
| [JP-008](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-008.v1.json) | Is this block a heading, list item or body text? | Build a text-preserving, escaped local formatting preview |
| [JP-010](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-010.v1.json) | Does this change break a stated consumer dependency? | Annotate impact for that consumer, not approve a deployment |
| [JP-011 v2](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-011.v2.json) | Is benefit evidence available, and what functional effect is described? | Combine availability and benefit with code-owned effort arithmetic and host vetoes |
| [JP-012](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-012.v1.json) | Does this feedback name a concrete next step for the submitted work? | Annotate feedback structure, not correctness, kindness or student ability |
| [JP-013](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/research-edition/contracts/JP-013.v1.json) | What exposure-assignment mechanism does this methods excerpt report? | Annotate reported assignment with exact source binding, not causality or study quality |

Read the full contract and consumer guidance before use. The small bundle includes
contracts, provenance and an offline import checker—not executable research
consumers, the full inference archive, or production authorization. A new application
needs its own tested consumer and representative evaluation. Each source threshold
is provisional; a top probability of 0.85 is not demonstrated 85% factual accuracy.

## What the research established

The admitted subset matched 120/120 development and 60/60 fresh challenge labels.
The same author created the fresh synthetic cases before inference. Separate
blinded model reviews are recorded, but did not independently author those cases.
No specialist or production qualification follows from these results.

The existing JP-002 public-record pilot combined six historical NASA/DOE/USGS cases
with six synthetic controls. One frozen call matched 12/12 labels and produced nine
read-only previews, three reviews, five public previews and zero wrong previews.
The public cases did not test explicit recipient acceptance or unresolved conflict;
those boundaries were synthetic. Its code baseline abstained on all multi-item
public records, so a target-aware baseline is still needed before claiming practical
advantage. The pilot added no new pattern to the master list.

The kernel carries forward the pilot's replay lessons: check the response against
the exact canonical request, recompute baseline and gate counts, bind every preview
to its target and dated source, and preserve original inference artifacts when a
separate verifier repairs replay checks.

## What remains held or incomplete

**JP-001, JP-006, JP-009 and JP-014** retain their v0.2.0 held/excluded dispositions.
**JP-017** is a separate working addition with research results but a pending wider
audit; its contract is not selectable in this import. Later held leads are also not
promoted. The requested checkpoint described a paused, incomplete research goal.
This integration does not resume research or change its current goal state.

The checkpoint's coverage index has 155 academic routes across eight groups: 22
have mixed transfer screens, 133 do not, and zero have individual domain validation.
All remain `UNSCREENED` for specialist/domain validation. Fifty occupations and
211 rated task statements are discovery coverage, not validated jobs. The final
project audit and older release-manifest drift remain unresolved research work.

## Check a copied skill locally

From the complete `jev-question-kernel-catalog` folder:

```sh
python3 scripts/check_research_import.py
python3 scripts/check_research_import.py --show JP-011
python3 -m unittest discover -s scripts -p 'test_research_import.py'
```

The checker validates exact import hashes, allowed versions, excluded entries and
packaging. It makes no provider calls and executes no consumer. With the original
research repository available, `--source-root PATH` checks the exact pinned Git
objects even if that repository has newer commits. It does not rebuild the source
catalog or claim to reproduce every historical result.
