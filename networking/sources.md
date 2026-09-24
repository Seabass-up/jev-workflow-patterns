---
layout: default
title: "Networking: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /networking/sources/
kicker: "5 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.

## NW-S1: RFC 5424: The Syslog Protocol (RFC Editor)

[Read the source](https://www.rfc-editor.org/rfc/rfc5424) · checked 2026-09-23 · SHA-256 `85b2e74f30dd645e…`

Defines the syslog protocol used to convey event notification messages from network devices and services, with a structured message format carrying severity and facility fields. Motivates NW04 as a classification of what one log line reports; parsing of the structured fields stays in code. This is motivation for the pattern, not evidence of Jev performance.

Used by: [NW04]({{ '/networking/patterns/nw04/' | relative_url }})

## NW-S2: Wikipedia: Change management (ITSM)

[Read the source](https://en.wikipedia.org/wiki/Change_management_(ITSM)) · checked 2026-09-23 · SHA-256 `4758540f6773295e…`

Describes change management as the discipline that applies standardized methods and procedures to all changes to IT infrastructure so as to minimize related incidents, balancing the need for change against its potential impact. Motivates NW02 (change type for approval routing), NW05 (advisory-driven changes), and NW06 (runbook step reversibility); approval and execution stay with people and code. This is motivation for the patterns, not evidence of Jev performance.

Used by: [NW02]({{ '/networking/patterns/nw02/' | relative_url }}), [NW05]({{ '/networking/patterns/nw05/' | relative_url }}), [NW06]({{ '/networking/patterns/nw06/' | relative_url }})

## NW-S3: Wikipedia: Maintenance window

[Read the source](https://en.wikipedia.org/wiki/Maintenance_window) · checked 2026-09-23 · SHA-256 `76b11fd31ad48781…`

Describes a maintenance window as a period announced in advance during which preventive maintenance that could disrupt service may be performed, so that clients can prepare for possible disruption. Motivates NW03 as a check that a notice states who or what will be affected; window times and customer mappings stay in code. This is motivation for the pattern, not evidence of Jev performance.

Used by: [NW03]({{ '/networking/patterns/nw03/' | relative_url }})

## NW-S4: Wikipedia: Network monitoring

[Read the source](https://en.wikipedia.org/wiki/Network_monitoring) · checked 2026-09-23 · SHA-256 `46191d4c906a6753…`

Describes systems that monitor a network for slow or failing components and notify administrators of outages, and notes that status-request failures usually produce an action from the monitoring system. Motivates NW08 (alert classification under a supplied policy) and NW04 (log line events); paging, escalation, and thresholds stay in code. This is motivation for the patterns, not evidence of Jev performance.

Used by: [NW04]({{ '/networking/patterns/nw04/' | relative_url }}), [NW08]({{ '/networking/patterns/nw08/' | relative_url }})

## NW-S5: Wikipedia: Incident management (fetched via the Incident management (ITSM) redirect)

[Read the source](https://en.wikipedia.org/wiki/Incident_management_(ITSM)) · checked 2026-09-23 · SHA-256 `f1aa615e919da5d6…`

Describes incident management as measures to remedy sudden disruptions and prevent recurrence, including the IT service management practice of restoring service after an incident. Motivates NW01 (symptom category for a ticket) and NW07 (how widely a report says a problem is felt); priority and major-incident declaration stay in code. This is motivation for the patterns, not evidence of Jev performance.

Used by: [NW01]({{ '/networking/patterns/nw01/' | relative_url }}), [NW07]({{ '/networking/patterns/nw07/' | relative_url }})

Full digests are in [sources.json]({{ '/networking/sources.json' | relative_url }}).

[Back to the collection]({{ '/networking/' | relative_url }})
