---
layout: default
title: Email Pattern Sources
description: Official TypeSafe documentation underlying the email question designs.
permalink: /email/sources/
---

# Sources and design provenance

The [complete TypeSafe documentation index](https://docs.typesafe.ai/llms.txt) was fetched first. The following official pages were checked September 22, 2026:

| Source | What it supports |
| --- | --- |
| [State](https://docs.typesafe.ai/concepts/state) | Named evidence fields, text input, and separate questions |
| [Choice](https://docs.typesafe.ai/primitives/choice) | Explicit answer categories and full question instructions |
| [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions) | Independent judgments over shared state |
| [Confidence](https://docs.typesafe.ai/confidence) | Distribution-summary confidence and use-case-dependent thresholds |

The 12 email profiles are authored adaptations using these primitives and the existing kernel. They are not copied TypeSafe email cookbooks or a comprehensive prior-art survey. Similar mechanisms intentionally recur across domains; each page explains its specific email distinction and consuming boundary.

Synthetic email text was written for this evaluation; no private inbox records or credentials are in the published artifacts. Local tests establish artifact integrity and selected regression behavior, not performance in an operational mailbox.

[Email catalog]({{ '/email/' | relative_url }}) · [Evaluation]({{ '/email/evaluation/' | relative_url }})
