---
layout: default
title: "SEO: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /seo/sources/
kicker: "5 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## SE-S1: Wikipedia: Web query (web search query)

[Read the source](https://en.wikipedia.org/wiki/Web_search_query) · checked 2026-09-23 · SHA-256 `72c6fc464a604d09…`

Describes the common three-way classification of search queries as informational, navigational, or transactional by what the searcher is trying to do. Motivates SE01 as a text classification of a query's wording; encyclopedic overview and motivation only, not evidence of Jev performance.

Used by: [SE01]({{ '/seo/patterns/se01/' | relative_url }})

## SE-S2: Google Search Central: Influencing Title Links in Google Search

[Read the source](https://developers.google.com/search/docs/appearance/title-link) · checked 2026-09-23 · SHA-256 `2dbf315ff73b33b3…`

Recommends title elements that are descriptive of the page's content and warns against boilerplate, placeholder, and keyword-list titles. Motivates SE02 as a comparison of a title with a page summary and SE08 as a topic-fit check; the guidance is motivation for the patterns, not evidence of Jev performance, and no policy determination is made by the model.

Used by: [SE02]({{ '/seo/patterns/se02/' | relative_url }}), [SE08]({{ '/seo/patterns/se08/' | relative_url }})

## SE-S3: Google Search Central: How to Write Meta Descriptions

[Read the source](https://developers.google.com/search/docs/appearance/snippet) · checked 2026-09-23 · SHA-256 `e01782f47bbab3be…`

Explains that a meta description should accurately summarize the page and be specific to it rather than generic or a list of keywords. Motivates SE04 as a comparison of a description with a page summary, with separate labels for teasing, boilerplate, and mismatch; motivation only, not evidence of Jev performance.

Used by: [SE04]({{ '/seo/patterns/se04/' | relative_url }})

## SE-S4: Google Search Central: SEO Link Best Practices for Google

[Read the source](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) · checked 2026-09-23 · SHA-256 `9aae3dfed29ae9aa…`

Recommends descriptive anchor text over generic phrases and describes qualifying outbound links with rel values such as sponsored, ugc, and nofollow. Motivates SE03 as an anchor-versus-destination reading and SE05 as a classification of the context around a link; code parses rel attributes exactly and the model never judges compliance. Motivation only, not evidence of Jev performance.

Used by: [SE03]({{ '/seo/patterns/se03/' | relative_url }}), [SE05]({{ '/seo/patterns/se05/' | relative_url }})

## SE-S5: Google Search Central: Creating Helpful, Reliable, People-First Content

[Read the source](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) · checked 2026-09-23 · SHA-256 `a9526f252d7b5b25…`

A self-assessment list asking whether a headline or title summarizes the content without exaggeration, whether a site has a primary purpose or focus, whether content substantially changed rather than only its date, and whether the content answers the questions it raises. Motivates SE02, SE04, SE06, SE07, and SE08 as readings of page text; the questions are motivation for the patterns, not evidence of Jev performance.

Used by: [SE02]({{ '/seo/patterns/se02/' | relative_url }}), [SE04]({{ '/seo/patterns/se04/' | relative_url }}), [SE06]({{ '/seo/patterns/se06/' | relative_url }}), [SE07]({{ '/seo/patterns/se07/' | relative_url }}), [SE08]({{ '/seo/patterns/se08/' | relative_url }})

Full digests are in [sources.json]({{ '/seo/sources.json' | relative_url }}).

[Back to the collection]({{ '/seo/' | relative_url }})
