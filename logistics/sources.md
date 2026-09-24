---
layout: default
title: "Logistics: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /logistics/sources/
kicker: "5 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## LGS-1: Wikipedia: Proof of delivery

[Read the source](https://en.wikipedia.org/wiki/Proof_of_delivery) · checked 2026-09-23 · SHA-256 `21d9102b971e69e5…`

Describes proof of delivery as a document confirming receipt of goods, including a signed acknowledgment of receipt held by the carrier and electronic proof-of-delivery records exchanged between companies, and notes disputes that arise when a recipient denies receiving a delivery message. Motivates LG02 as a reading of the carrier's note and the delivery-message contracts LG01, LG04, LG06, and LG08. This is motivation for the designs, not evidence of Jev performance.

Used by: [LG01]({{ '/logistics/patterns/lg01/' | relative_url }}), [LG02]({{ '/logistics/patterns/lg02/' | relative_url }}), [LG04]({{ '/logistics/patterns/lg04/' | relative_url }}), [LG06]({{ '/logistics/patterns/lg06/' | relative_url }}), [LG08]({{ '/logistics/patterns/lg08/' | relative_url }})

## LGS-2: Wikipedia: Commercial invoice

[Read the source](https://en.wikipedia.org/wiki/Commercial_invoice) · checked 2026-09-23 · SHA-256 `eb53cd77c0cc7c0f…`

Describes the commercial invoice as a customs document that identifies the parties, the goods, the country of manufacture, and tariff codes, and distinguishes it from an invoice for payment and from a packing list. Motivates LG03: the model classifies the document's type from its text, and code validates its fields. Motivation only, not evidence of Jev performance.

Used by: [LG03]({{ '/logistics/patterns/lg03/' | relative_url }})

## LGS-3: Wikipedia: Certificate of origin

[Read the source](https://en.wikipedia.org/wiki/Certificate_of_origin) · checked 2026-09-23 · SHA-256 `65ecd2549a5e9ff0…`

Defines a certificate or declaration of origin as a document attesting that listed goods originate in a particular country, prepared by the exporter or manufacturer and often certified by a chamber of commerce or authority. Motivates the certificate_of_origin label in LG03 and its rule that an origin line inside another document is not a certificate. Motivation only, not evidence of Jev performance.

Used by: [LG03]({{ '/logistics/patterns/lg03/' | relative_url }})

## LGS-4: Wikipedia: Freight claim

[Read the source](https://en.wikipedia.org/wiki/Freight_claim) · checked 2026-09-23 · SHA-256 `764174d5cae6e470…`

Describes a freight or cargo claim as a demand against a carrier for loss of or damage to a shipment, the carrier's standard of care and duty of reasonable dispatch, and that the recoverable amount is governed by contract and insurance rules. Motivates LG01, LG04, LG05, LG06, and LG08 as classifications of text made before any liability or amount is decided. Motivation only, not evidence of Jev performance.

Used by: [LG01]({{ '/logistics/patterns/lg01/' | relative_url }}), [LG04]({{ '/logistics/patterns/lg04/' | relative_url }}), [LG05]({{ '/logistics/patterns/lg05/' | relative_url }}), [LG06]({{ '/logistics/patterns/lg06/' | relative_url }}), [LG08]({{ '/logistics/patterns/lg08/' | relative_url }})

## LGS-5: Wikipedia: Stockout (backorder)

[Read the source](https://en.wikipedia.org/wiki/Backorder) · checked 2026-09-23 · SHA-256 `6c9b1ba009385be7…`

Defines a backorder as an order placed for an out-of-stock item that is awaiting fulfillment, and discusses shoppers substituting another item when the ordered one is unavailable. Motivates LG07's distinction between a delayed shipment, a proposed substitute, and a cancellation. Motivation only, not evidence of Jev performance.

Used by: [LG07]({{ '/logistics/patterns/lg07/' | relative_url }})

Full digests are in [sources.json]({{ '/logistics/sources.json' | relative_url }}).

[Back to the collection]({{ '/logistics/' | relative_url }})
