---
layout: default
title: "Web data collection: patterns for permissions, page structure, and record quality"
description: "Eight question contracts for teams that collect public web data: policy excerpts against a described use, target record-type detection, field meaning, operator notices, personal-data exclusion, page-change triage, duplicate records, and page kind."
permalink: /web-scraping/
kicker: "8 profiles · 31/32 labels matched · kernel 2.6.0"
---

# Web data collection

A team that collects public web data reads a site's terms and robots rules before it starts, watches for notices from the operator, and keeps its extractors working as pages change. These eight contracts classify that text: what a policy excerpt says about a described use, whether a page holds the target record type, whether an extracted value means what its field means, what an operator's notice asks, whether a record holds personal data the team's policy excludes, whether a page change is structural, whether two records describe one entity, and whether a page is an item, a listing, or navigation. They are task-authored, advisory designs. Request behavior, rate policy, legal review, and every exact check stay with code and people.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/web-scraping/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/web-scraping/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 7/8 challenge cases** matched their prewritten labels: 31/32 overall. WS04 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Permissions and notices

| ID | Question pattern | Intended use |
| --- | --- | --- |
| WS01 | [Policy excerpt permits, forbids, or conditions the described collection]({{ '/web-scraping/patterns/ws01/' | relative_url }}) | Gives the compliance reading of a policy excerpt a consistent first pass; the legal conclusion and the exact robots path match stay with people and code. |
| WS04 · provisional | [Site notice asks collectors to stop or make contact]({{ '/web-scraping/patterns/ws04/' | relative_url }}) | Makes sure an operator's request to stop or get in touch is seen and honored the first time instead of being logged as a fetch failure. |
| WS05 | [Record contains personal data the supplied policy excludes]({{ '/web-scraping/patterns/ws05/' | relative_url }}) | Applies the team's own written exclusion rules to each record consistently before storage, without the model deciding what any law requires. |

## Page structure

| ID | Question pattern | Intended use |
| --- | --- | --- |
| WS02 | [Page excerpt contains the target record type]({{ '/web-scraping/patterns/ws02/' | relative_url }}) | Keeps extractors from parsing pages that hold no target records and flags crawls that drifted into another record type, without a person opening each page. |
| WS06 | [Page change is structural or content-only for the extractor]({{ '/web-scraping/patterns/ws06/' | relative_url }}) | Routes extractor maintenance to a template fix, a data refresh, or nothing, instead of treating every diff as a breakage. |
| WS08 | [Page is an item page, a listing page, or navigation]({{ '/web-scraping/patterns/ws08/' | relative_url }}) | Keeps item extractors off listing and navigation pages and finds the item pages a crawl can treat as a record's source; canonical URL selection stays in code. |

## Record quality

| ID | Question pattern | Intended use |
| --- | --- | --- |
| WS03 | [Extracted value carries the meaning of its field]({{ '/web-scraping/patterns/ws03/' | relative_url }}) | Catches a price field holding a crossed-out old price or a date field holding the posting date instead of the event date, before the record enters the dataset. |
| WS07 | [Two extracted records describe the same entity]({{ '/web-scraping/patterns/ws07/' | relative_url }}) | Resolves the cross-source duplicates that formatting differences hide, while exact identifier matches and the merge itself stay in code. |

## Start with a small bundle

Before a crawl starts, WS01 (policy excerpt) with the exact robots match in code and legal review of anything conditioned or forbidden. While it runs, WS04 (operator notice) with the halt in code, and WS08 (page kind) to route each page to the right extractor. For the data that comes back, WS05 (personal-data exclusion) with the policy revision recorded and WS03 (field meaning) with exact format checks.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a permission, a legal conclusion, or a merge. Code performs exact robots path and user-agent matching, enforces request rate, halts collection on any stop or contact notice, drops the fields the exclusion policy names, compares identifiers exactly, chooses canonical URLs, and never retries, changes client identity, or takes another route to content after a notice. People own legal review of terms, contact with site operators, and the exclusion policy itself. Nothing in this collection helps evade blocking, rate limits, or access controls.

[Exact catalog]({{ '/web-scraping/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/web-scraping/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/web-scraping.md)
