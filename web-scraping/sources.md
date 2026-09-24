---
layout: default
title: "Web data: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /web-scraping/sources/
kicker: "5 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## WS-S1: RFC 9309: Robots Exclusion Protocol (RFC Editor)

[Read the source](https://www.rfc-editor.org/rfc/rfc9309.html) · checked 2026-09-23 · SHA-256 `bbaa280636d3e38f…`

Specifies how a site publishes robots rules and how crawlers are expected to read allow and disallow groups, and describes how a crawler should treat unavailable or error responses. Motivates WS01 as a reading of what a policy excerpt says and WS04 as recognizing a notice; exact path and user-agent matching stay in code. Motivation only, not evidence of Jev performance.

Used by: [WS01]({{ '/web-scraping/patterns/ws01/' | relative_url }}), [WS04]({{ '/web-scraping/patterns/ws04/' | relative_url }})

## WS-S2: Wikipedia: Web scraping

[Read the source](https://en.wikipedia.org/wiki/Web_scraping) · checked 2026-09-23 · SHA-256 `b6be8bd045f58fe0…`

Overview of extracting data from web pages, the page-structure changes that break extractors, and the legal and terms-of-use questions around collection. Motivates WS02, WS03, WS06, and WS08 as page-structure and record-quality readings and the legal boundary in WS01; motivation only, not evidence of Jev performance.

Used by: [WS01]({{ '/web-scraping/patterns/ws01/' | relative_url }}), [WS02]({{ '/web-scraping/patterns/ws02/' | relative_url }}), [WS03]({{ '/web-scraping/patterns/ws03/' | relative_url }}), [WS04]({{ '/web-scraping/patterns/ws04/' | relative_url }}), [WS05]({{ '/web-scraping/patterns/ws05/' | relative_url }}), [WS06]({{ '/web-scraping/patterns/ws06/' | relative_url }}), [WS07]({{ '/web-scraping/patterns/ws07/' | relative_url }}), [WS08]({{ '/web-scraping/patterns/ws08/' | relative_url }})

## WS-S3: Wikipedia: Record linkage

[Read the source](https://en.wikipedia.org/wiki/Record_linkage) · checked 2026-09-23 · SHA-256 `6a196fac634a8b37…`

Describes matching records that refer to the same entity across sources without a shared identifier, and the false-match and missed-match errors involved. Motivates WS07; motivation only, not evidence of Jev performance.

Used by: [WS07]({{ '/web-scraping/patterns/ws07/' | relative_url }})

## WS-S4: Wikipedia: Canonical link element

[Read the source](https://en.wikipedia.org/wiki/Canonical_link_element) · checked 2026-09-23 · SHA-256 `0cd40b9f765e1b6c…`

Describes how a site designates the preferred URL among duplicate or near-duplicate pages. Motivates WS08 as a page-kind reading while canonical URL selection stays in code; motivation only, not evidence of Jev performance.

Used by: [WS08]({{ '/web-scraping/patterns/ws08/' | relative_url }})

## WS-S5: Wikipedia: Personal data

[Read the source](https://en.wikipedia.org/wiki/Personal_data) · checked 2026-09-23 · SHA-256 `00a4ae6c3339d6ee…`

Describes what information about an identifiable individual counts as personal data under various frameworks. Motivates WS05 as applying a team's own written exclusion policy to a record; no law is applied by the model. Motivation only, not evidence of Jev performance.

Used by: [WS05]({{ '/web-scraping/patterns/ws05/' | relative_url }})

Full digests are in [sources.json]({{ '/web-scraping/sources.json' | relative_url }}).

[Back to the collection]({{ '/web-scraping/' | relative_url }})
