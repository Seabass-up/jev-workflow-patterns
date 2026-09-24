---
layout: default
title: "Cybersecurity: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /cybersecurity/sources/
kicker: "5 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## CY-S1: NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management (CSRC publication page)

[Read the source](https://csrc.nist.gov/pubs/sp/800/61/r3/final) · checked 2026-09-23 · SHA-256 `4453b4006396c0ba…`

Describes incident response as detection and analysis of events, prioritization by impact, and coordination with other risk-management activities. Motivates CY02 (an alert narrative against its stated context), CY04 (a report against a severity definition), and CY07 (log events as detection input) as text classifications within that workflow. This is motivation for the pattern designs, not evidence of Jev performance.

Used by: [CY01]({{ '/cybersecurity/patterns/cy01/' | relative_url }}), [CY02]({{ '/cybersecurity/patterns/cy02/' | relative_url }}), [CY04]({{ '/cybersecurity/patterns/cy04/' | relative_url }}), [CY07]({{ '/cybersecurity/patterns/cy07/' | relative_url }})

## CY-S2: Wikipedia: Phishing

[Read the source](https://en.wikipedia.org/wiki/Phishing) · checked 2026-09-23 · SHA-256 `1c5e4a365cdd16f4…`

Encyclopedic overview of messages that pose as trusted senders to obtain sign-in details, deliver harmful attachments, or redirect payments, and of the user-reporting channels organizations run. Motivates CY01 as a classification of the ask a reported message makes; it is motivation for the design, not evidence of Jev performance, and no technique is reproduced in the contract.

Used by: [CY01]({{ '/cybersecurity/patterns/cy01/' | relative_url }})

## CY-S3: NIST SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations (CSRC publication page)

[Read the source](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) · checked 2026-09-23 · SHA-256 `be41d479ef7f5d01…`

Catalog of security and privacy controls that includes least-privilege access, the use of compensating controls where a control cannot be implemented as written, and supply chain risk management including supplier assessments. Motivates CY05 (task-bound access justification), CY06 (compensating control named in an exception request), and CY08 (vendor questionnaire answers). Motivation only, not evidence of Jev performance; no control is applied by the model.

Used by: [CY05]({{ '/cybersecurity/patterns/cy05/' | relative_url }}), [CY06]({{ '/cybersecurity/patterns/cy06/' | relative_url }}), [CY08]({{ '/cybersecurity/patterns/cy08/' | relative_url }})

## CY-S4: Wikipedia: Common Vulnerabilities and Exposures

[Read the source](https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures) · checked 2026-09-23 · SHA-256 `baf4da6ef33334dd…`

Describes the public identifier system for vulnerabilities and the advisories that name affected products and versions. Motivates CY03 as a classification of whether an advisory's affected-product text names a described asset's product or an included component, with version comparison left to code. Motivation, not evidence of Jev performance.

Used by: [CY03]({{ '/cybersecurity/patterns/cy03/' | relative_url }})

## CY-S5: NIST SP 800-92, Guide to Computer Security Log Management (CSRC publication page)

[Read the source](https://csrc.nist.gov/pubs/sp/800/92/final) · checked 2026-09-23 · SHA-256 `86ad62728c6432ec…`

Describes log management, including authentication events recorded by many systems in differing formats and the analysis that depends on normalizing them. Motivates CY07 as a normalization of one event's stated authentication outcome, with parsing, counting, and thresholds in code. Motivation, not evidence of Jev performance.

Used by: [CY07]({{ '/cybersecurity/patterns/cy07/' | relative_url }})

Full digests are in [sources.json]({{ '/cybersecurity/sources.json' | relative_url }}).

[Back to the collection]({{ '/cybersecurity/' | relative_url }})
