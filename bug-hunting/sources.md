---
layout: default
title: Bug-Hunting Sources and Provenance
description: Official TypeSafe guidance and the boundary between authored patterns and demonstrated bugs.
permalink: /bug-hunting/sources/
---

# Sources and provenance

The [TypeSafe documentation index](https://docs.typesafe.ai/llms.txt) was fetched first on September 23, 2026. Relevant current official guidance:

| Source | Design consequence |
| --- | --- |
| [Choice](https://docs.typesafe.ai/primitives/choice) | Use explicit competing evidence states and complete instructions; question IDs are only handles |
| [Jev with coding agents](https://docs.typesafe.ai/introduction/coding-agents) | Jev supplies typed judgments, not generated fixes or an autonomous coding agent |
| [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | Keep exact arithmetic/time/identity in code, provide relevant context, and do not treat adversarial text classification as a security boundary |
| [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/) | Distinguishes canonical from compatibility equivalence; BH18 applies only to the equivalence relation explicitly declared by the application contract |
| [Unicode Technical Standard #39: Unicode Security Mechanisms](https://unicode.org/reports/tr39/) | Treats visual confusability as a separate security-detection problem; do not equate confusables or normalize them as identifier equality |

The TypeSafe HTML pages and documentation index were reread on September 27, 2026. The current pages still describe the Choice request/response shape, Jev as a typed-decision tool rather than a coding-agent LLM, and Jev 1.13's literal-reading and adversarial-content limitations. The Unicode UAX #15 and UTS #39 pages were also checked on September 27, 2026 for BH18's terminology boundary. Browser rereads did not produce refreshed raw-page digests; this is a freshness note, not independent Jev performance evidence. The Jev 1.13 limitations page itself says it was last reviewed September 17, 2026.

These are authored bug-hunting adaptations, not official TypeSafe bug-detector benchmarks or a complete prior-art survey. Individual pages define their contract rather than claiming universal language, framework, or operating-system semantics. Confirm actual runtime/library specifications when applying a profile.

The catalog intentionally reuses a common three-state evidence contract. The distinctions are the adverse hypothesis, required context, counterexample, and verification method—not 48 unrelated algorithms. Existing engineering and harness catalogs contain related building blocks.

Only synthetic text was sent for these screens. No third-party target was scanned, private repository was uploaded, or live defect was repaired. A source review becomes a finding only after appropriate independent verification.

[Catalog]({{ '/bug-hunting/' | relative_url }}) · [Evaluation]({{ '/bug-hunting/evaluation/' | relative_url }})
