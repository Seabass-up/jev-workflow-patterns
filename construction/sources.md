---
layout: default
title: "Construction: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /construction/sources/
kicker: "6 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## CN-S1: Wikipedia: Request for information

[Read the source](https://en.wikipedia.org/wiki/Request_for_information) · checked 2026-09-23 · SHA-256 `5e0e72050e515bfe…`

Has a section on the construction industry stating that an RFI is used when the project's construction documentation lacks information, and that a contractor or supplier may use one to raise the omission or misapplication of a product and seek clarification of the owner's intended use or acceptance of the specified product. Motivates CN01 as a reading of what an RFI asks for; this is motivation for the contract design, not evidence of Jev performance.

Used by: [CN01]({{ '/construction/patterns/cn01/' | relative_url }})

## CN-S2: Wikipedia: Submittals (construction)

[Read the source](https://en.wikipedia.org/wiki/Submittals_(construction)) · checked 2026-09-23 · SHA-256 `617b3336d2be7b0f…`

Describes the submittal process in which the contractor sends shop drawings and product data to the architect for review, the review resulting in approval, partial approval, notes, or rejection, with the architect sometimes rejecting the entire submittal or requesting resubmittal of some items, and notes the lead time between review and fabrication. Motivates CN03 as a reading of the reviewer's stated action and CN01's separation of substitution proposals from clarifications; motivation only, not evidence of Jev performance.

Used by: [CN01]({{ '/construction/patterns/cn01/' | relative_url }}), [CN03]({{ '/construction/patterns/cn03/' | relative_url }})

## CN-S3: Wikipedia: Change order

[Read the source](https://en.wikipedia.org/wiki/Change_order) · checked 2026-09-23 · SHA-256 `f0b35bcec5a767e9…`

Defines a change order as work added to or deleted from the original scope of a contract, which may alter the contract amount or completion date, and notes that change orders are common on most projects. Motivates CN04 as a reading of the basis a change-order request states; the page does not classify bases, and the contract and its administrators decide entitlement. Motivation only, not evidence of Jev performance.

Used by: [CN04]({{ '/construction/patterns/cn04/' | relative_url }})

## CN-S4: Wikipedia: Critical path method

[Read the source](https://en.wikipedia.org/wiki/Critical_path_method) · checked 2026-09-23 · SHA-256 `851a4e86d1894569…`

Explains that critical activities have no float and cannot be delayed without lengthening the project, that non-critical activities carry float, that the technique is widely used to plan and control construction projects, and that as-built critical path analysis is used to assess the causes of a delay. Motivates CN07 as a reading of whether a note states a milestone or completion impact versus float absorption, and CN02's separation of stated delay causes; all float and date computation stays in the scheduling software. Motivation only, not evidence of Jev performance.

Used by: [CN02]({{ '/construction/patterns/cn02/' | relative_url }}), [CN07]({{ '/construction/patterns/cn07/' | relative_url }})

## CN-S5: Wikipedia: Construction management

[Read the source](https://en.wikipedia.org/wiki/Construction_management) · checked 2026-09-23 · SHA-256 `4754c0cc3a87073d…`

Describes construction management as integrating cost, schedule, quality, safety, and scope, lists quality and safety management, contract administration, and documentation and claims management among its responsibilities, states that project documentation includes diaries, logs, and daily field reports kept as records for dispute resolution, and names the warranty period and closeout as the final phase. Motivates CN02 (daily logs), CN05 (safety observations), CN06 (punch lists as a quality and closeout record), and CN08 (closeout documents); motivation only, not evidence of Jev performance.

Used by: [CN02]({{ '/construction/patterns/cn02/' | relative_url }}), [CN04]({{ '/construction/patterns/cn04/' | relative_url }}), [CN05]({{ '/construction/patterns/cn05/' | relative_url }}), [CN06]({{ '/construction/patterns/cn06/' | relative_url }}), [CN08]({{ '/construction/patterns/cn08/' | relative_url }})

## CN-S6: OSHA: Construction Industry

[Read the source](https://www.osha.gov/construction) · checked 2026-09-23 · SHA-256 `7d3f5e6b2490fdb6…`

OSHA's construction page describes construction as a high-hazard industry with serious hazards such as falls from rooftops, unguarded machinery, being struck by heavy equipment, electrocution, silica, and asbestos, and offers regulatory and guidance resources to identify, reduce, and eliminate hazards. Motivates CN05 as a reading of safety observations against a supplied stop-work list; the standards themselves stay with the safety officer.

Used by: [CN05]({{ '/construction/patterns/cn05/' | relative_url }})

Full digests are in [sources.json]({{ '/construction/sources.json' | relative_url }}).

[Back to the collection]({{ '/construction/' | relative_url }})
