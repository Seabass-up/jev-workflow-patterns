---
layout: default
title: "Electrical: Sources"
description: "Public pages that motivated the question designs, with the digest of each page as read."
permalink: /electrical/sources/
kicker: "8 sources · inspiration, not a performance claim"
---

# Inspiration, not a performance claim

The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. For `browser_excerpt` records, the SHA-256 binds only the exact excerpt shown below; otherwise it binds the captured page text as read on the checked date. Neither digest establishes that a source is still current.

## ES-1: NFPA 70E, Standard for Electrical Safety in the Workplace (NFPA overview page)

[Read the source](https://www.nfpa.org/codes-and-standards/nfpa-70e-standard-development/70e) · checked 2026-09-23 · SHA-256 `f33c2550497ed868…` (covers the captured page text)

NFPA describes 70E as requirements for safe work practices that protect personnel by reducing exposure to major electrical hazards, originally developed at OSHA's request, helping avoid injuries and fatalities from shock, electrocution, arc flash, and arc blast, and assisting compliance with OSHA workplace electrical rules. Motivates EL02 as a text classification of reported hazard signs; the standard, not the label, governs practice.

Used by: [EL01]({{ '/electrical/patterns/el01/' | relative_url }}), [EL02]({{ '/electrical/patterns/el02/' | relative_url }})

## ES-2: NFPA 70, National Electrical Code (NFPA overview page)

[Read the source](https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70) · checked 2026-09-23 · SHA-256 `1bf44c4c05baf402…` (covers the captured page text)

NFPA describes NFPA 70, the National Electrical Code, as enforced in all 50 states and the benchmark for safe electrical design, installation, and inspection to protect people and property from electrical hazards, with edition, amendment, and errata records. Motivates EL01, EL03, EL04, EL07; no article is cited and no rule is applied by the model.

Used by: [EL01]({{ '/electrical/patterns/el01/' | relative_url }}), [EL03]({{ '/electrical/patterns/el03/' | relative_url }}), [EL04]({{ '/electrical/patterns/el04/' | relative_url }}), [EL07]({{ '/electrical/patterns/el07/' | relative_url }})

## ES-3: Wikipedia: Residual-current device

[Read the source](https://en.wikipedia.org/wiki/Residual-current_device) · checked 2026-09-23 · SHA-256 `abd4b6810c813529…` (covers the captured page text)

Describes ground-fault protective devices such as GFCIs as distinct from overcurrent devices. Motivates EL07 as a device-type classification; encyclopedic overview.

Used by: [EL02]({{ '/electrical/patterns/el02/' | relative_url }}), [EL07]({{ '/electrical/patterns/el07/' | relative_url }})

## ES-4: Washington State L&I: Electrical Permits, Fees & Inspections

[Read the source](https://lni.wa.gov/licensing-permits/electrical/electrical-permits-fees-and-inspections/) · checked 2026-09-23 · SHA-256 `3a8043f307add1a6…` (covers the captured page text)

A jurisdiction's public description of when electrical permits are required, fees, and inspections, including reinspection after corrections. Motivates EL03, EL04, EL05, EL06, EL08; the jurisdiction's rules stay in code.

Used by: [EL03]({{ '/electrical/patterns/el03/' | relative_url }}), [EL04]({{ '/electrical/patterns/el04/' | relative_url }}), [EL05]({{ '/electrical/patterns/el05/' | relative_url }}), [EL06]({{ '/electrical/patterns/el06/' | relative_url }}), [EL08]({{ '/electrical/patterns/el08/' | relative_url }})

## ES-5: Wikipedia: Arc-fault circuit interrupter

[Read the source](https://en.wikipedia.org/wiki/Arc-fault_circuit_interrupter) · checked 2026-09-23 · SHA-256 `ee06950813c7e186…` (covers the captured page text)

Describes arc-fault protection and dual-function devices combining it with ground-fault protection. Motivates EL07.

Used by: [EL07]({{ '/electrical/patterns/el07/' | relative_url }})

## ES-6: OSHA: Electrical - Overview

[Read the source](https://www.osha.gov/electrical) · checked 2026-09-23 · SHA-256 `7e717d18451c9466…` (covers the captured page text)

OSHA's electrical overview states that electricity is a serious workplace hazard, that its standards protect employees from shock, electrocution, fires, and explosions, and that the most frequent causes of electrical injuries include contact with power lines, lack of ground-fault protection, a missing or discontinuous path to ground, equipment not used as prescribed, and improper use of extension and flexible cords. Motivates EL02 (hazard signs) and EL07 (ground-fault protection devices); the on-site electrician's determination governs.

Used by: [EL02]({{ '/electrical/patterns/el02/' | relative_url }}), [EL07]({{ '/electrical/patterns/el07/' | relative_url }})

## ES-7: U.S. CPSC: GFCI Fact Sheet (Publication 099, September 2010)

[Read the source](https://www.cpsc.gov/s3fs-public/099_0.pdf) · checked 2026-09-27 · SHA-256 `61ddfd52e3a1a0c3…` (covers the recorded excerpt)

> Ground fault protection is integrated into GFCI receptacles and GFCI circuit breakers.

The CPSC fact sheet identifies GFCI receptacle and circuit-breaker types and their ground-fault protection function for shock protection. The PDF is dated 2010; this supports device-function terminology only, not current installation requirements or code compliance.

Used by: [EL07]({{ '/electrical/patterns/el07/' | relative_url }})

## ES-8: U.S. CPSC: Preventing Home Fires — Arc Fault Circuit Interrupters (Publication 5133, 2012 revision)

[Read the source](https://www.cpsc.gov/s3fs-public/5133%281%29.pdf) · checked 2026-09-27 · SHA-256 `3ca48c47e0a94972…` (covers the recorded excerpt)

> AFCIs are intended to address fire hazards; GFCIs address shock hazards. Combination devices include both AFCI and GFCI protection in one unit.

The CPSC fact sheet distinguishes AFCI fire-hazard function from GFCI shock-hazard function and notes a combination device may include both. The PDF is a 2012 revision; it supports device-function terminology only, not current installation requirements or code compliance.

Used by: [EL07]({{ '/electrical/patterns/el07/' | relative_url }})

Full digests are in [sources.json]({{ '/electrical/sources.json' | relative_url }}).

[Back to the collection]({{ '/electrical/' | relative_url }})
