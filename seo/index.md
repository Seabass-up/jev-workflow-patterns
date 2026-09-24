---
layout: default
title: "SEO: patterns for intent, on-page content, and links"
description: "Eight question contracts for SEO and content text: query intent, title tags, internal link anchors, meta descriptions, backlink context, FAQ entries, page changes, and topic fit."
permalink: /seo/
kicker: "8 profiles · 32/32 labels matched · kernel 2.6.0"
---

# SEO

SEO and content teams review the same kinds of text at scale: thousands of queries, every title and description on a site, the anchors of internal links, a backlink export, FAQ entries, and a change log. These eight contracts classify that text so a review can start from the flagged items instead of the whole list. They are task-authored, advisory designs. Counts, word lengths, rankings, and traffic are computed in code, and no label says whether a practice complies with any search engine's rules.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/seo/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/seo/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 8/8 challenge cases** matched their prewritten labels: 32/32 overall. No pattern is provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Query intent and topic fit

| ID | Question pattern | Intended use |
| --- | --- | --- |
| SE01 | [Search query intent from the query text]({{ '/seo/patterns/se01/' | relative_url }}) | Groups thousands of queries by intent from their wording alone, so a keyword list can be assigned to article, landing, or product pages without a person reading each query. |
| SE08 | [Page's primary topic matches the target query]({{ '/seo/patterns/se08/' | relative_url }}) | Checks a query-to-page map at scale so pages assigned to the wrong query are found before content work begins. |

## On-page content

| ID | Question pattern | Intended use |
| --- | --- | --- |
| SE02 | [Title tag describes the page's content]({{ '/seo/patterns/se02/' | relative_url }}) | Finds titles that are placeholders, site-wide boilerplate, or off-topic across a whole site without a person opening each page; the rewrite stays with the content team. |
| SE04 | [Meta description summarizes the page or withholds its point]({{ '/seo/patterns/se04/' | relative_url }}) | Reviews descriptions across a site for teasing or mismatched text in one pass, so editors rewrite only the ones flagged. |
| SE06 | [FAQ entry answers the question it poses]({{ '/seo/patterns/se06/' | relative_url }}) | Reviews every FAQ entry on a site for answers that dodge the question, so editors fix only the entries that need it. |
| SE07 | [Page change is a content update or a technical change]({{ '/seo/patterns/se07/' | relative_url }}) | Turns a site's change log into categories that code can line up against traffic and ranking dates, without a person reading each entry. |

## Links

| ID | Question pattern | Intended use |
| --- | --- | --- |
| SE03 | [Internal link anchor text describes its destination]({{ '/seo/patterns/se03/' | relative_url }}) | Surfaces generic and misleading anchors across a site's internal links so they can be fixed in bulk; which links to change stays with the team. |
| SE05 | [Backlink context is editorial, disclosed, user-submitted, or a listing]({{ '/seo/patterns/se05/' | relative_url }}) | Sorts a backlink export by context without a person opening every referring page; what to do with each group stays with the team. |

## Start with a small bundle

Start with SE01 (query intent) and SE08 (topic fit) to check a query-to-page map, then SE02 (title tag) and SE04 (meta description) for an on-page pass over the same pages; each feeds a review list, not an automatic rewrite. Add SE03 for internal anchors and SE05 for a backlink export once those crawls exist.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of supplied text. Code owns keyword lists, query volumes, title and description lengths, duplicate detection, link counts, rel-attribute parsing, diff generation, change dates, and rankings; people decide rewrites, link changes, and outreach. No label decides whether a page, link, or practice complies with a search engine's policies, whether a claim in a description is substantiated, or whether a change caused a ranking movement.

[Exact catalog]({{ '/seo/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/seo/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/seo.md)
