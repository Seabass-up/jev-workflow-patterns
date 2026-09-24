---
layout: default
title: "Logistics routing: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /logistics-routing/sources/
kicker: "6 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## LR-S1: Wikipedia: Vehicle routing problem

[Read the source](https://en.wikipedia.org/wiki/Vehicle_routing_problem) · checked 2026-09-23 · SHA-256 `cc91ed5ee0b8d51c…`

Describes routing as a computed optimization with variants for time windows at delivery locations, vehicle capacity, and pickup and delivery. Motivates LR01, LR02, LR03, LR04, LR05, and LR07 as readings of which constraint or preference a text states, with the solver computing distance, time, capacity, and sequence. Motivation only, not evidence of Jev performance.

Used by: [LR01]({{ '/logistics-routing/patterns/lr01/' | relative_url }}), [LR02]({{ '/logistics-routing/patterns/lr02/' | relative_url }}), [LR03]({{ '/logistics-routing/patterns/lr03/' | relative_url }}), [LR04]({{ '/logistics-routing/patterns/lr04/' | relative_url }}), [LR05]({{ '/logistics-routing/patterns/lr05/' | relative_url }}), [LR07]({{ '/logistics-routing/patterns/lr07/' | relative_url }})

## LR-S2: Wikipedia: Dangerous goods

[Read the source](https://en.wikipedia.org/wiki/Dangerous_goods) · checked 2026-09-23 · SHA-256 `0c3f3b05dd45c3b2…`

Overview of dangerous goods classification, identification numbers, labeling, and transport documents. Motivates LR06 as a reading of whether order text declares a hazard; the regulatory class of record stays with the product master and the carrier's rules. Motivation only, not evidence of Jev performance.

Used by: [LR06]({{ '/logistics-routing/patterns/lr06/' | relative_url }})

## LR-S3: Wikipedia: Cold chain

[Read the source](https://en.wikipedia.org/wiki/Cold_chain) · checked 2026-09-23 · SHA-256 `ef1e01cca56e9eb6…`

Describes temperature-controlled supply chains that use refrigeration to keep perishable goods such as produce and pharmaceuticals within a range in transport. Motivates LR06 as a reading of whether order text declares a temperature requirement; the temperature band applied to the vehicle stays in code. Motivation only, not evidence of Jev performance.

Used by: [LR06]({{ '/logistics-routing/patterns/lr06/' | relative_url }})

## LR-S4: USPS Publication 28: Postal Addressing Standards (Postal Explorer contents page)

[Read the source](https://pe.usps.com/text/pub28/welcome.htm) · checked 2026-09-23 · SHA-256 `24343d96a567ecac…`

Official contents of an addressing standard covering the standardized delivery address line, secondary unit designators, and dual addresses. Motivates LR08 as a reading of how many places an address text names before code validates or standardizes it. Motivation only, not evidence of Jev performance.

Used by: [LR08]({{ '/logistics-routing/patterns/lr08/' | relative_url }})

## LR-S5: Wikipedia: Dispatcher

[Read the source](https://en.wikipedia.org/wiki/Dispatcher) · checked 2026-09-23 · SHA-256 `e66372ad5d8fc48c…`

Describes dispatchers in trucking, courier, and other operations who relay information, direct personnel, and make real-time adjustments as conditions and delays change. Motivates LR01, LR03, LR04, and LR05 as readings of the notes, driver reports, and customer messages a dispatcher handles; the adjustment itself stays with the dispatcher and code. Motivation only, not evidence of Jev performance.

Used by: [LR01]({{ '/logistics-routing/patterns/lr01/' | relative_url }}), [LR03]({{ '/logistics-routing/patterns/lr03/' | relative_url }}), [LR04]({{ '/logistics-routing/patterns/lr04/' | relative_url }}), [LR05]({{ '/logistics-routing/patterns/lr05/' | relative_url }})

## LR-S6: FMCSA: Summary of Hours of Service Regulations

[Read the source](https://www.fmcsa.dot.gov/regulations/hours-service/summary-hours-service-regulations) · checked 2026-09-23 · SHA-256 `1fae6af272b66756…`

FMCSA summarizes driving-time limits, the 14-hour window, required breaks, weekly limits, sleeper-berth splits, the adverse-driving-conditions extension, and the short-haul exception for property-carrying drivers. Motivates LR02 and LR04 as readings of time-window and deviation text; every hours-of-service calculation and compliance decision stays in code and with the carrier.

Used by: [LR02]({{ '/logistics-routing/patterns/lr02/' | relative_url }}), [LR04]({{ '/logistics-routing/patterns/lr04/' | relative_url }})

Full digests are in [sources.json]({{ '/logistics-routing/sources.json' | relative_url }}).

[Back to the collection]({{ '/logistics-routing/' | relative_url }})
