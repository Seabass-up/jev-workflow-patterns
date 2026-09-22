---
layout: default
title: "Iteration 2 Raw Receipts"
description: "Machine-readable synthetic Jev receipts and summary files for Iteration 2."
permalink: /iterations/02/results/
kicker: "Results · JSON evidence"
---

[← Iteration 2 catalog]({{ '/iterations/02/' | relative_url }}) · [Evaluation]({{ '/iterations/02/evaluation/' | relative_url }})

# Raw evaluation receipts

These JSON files preserve synthetic inputs, typed Jev outputs, expected labels outside the submitted state, request digests, and match calculations. They are evidence for the small design checks only; they do not establish production performance.

- [Initial core v1: 86 requests]({{ '/iterations/02/results/core-initial.json' | relative_url }})
- [Initial harness v1: 48 requests]({{ '/iterations/02/results/harness-screen.json' | relative_url }})
- [Core refinement v2: 17 requests]({{ '/iterations/02/results/core-refinement.json' | relative_url }})
- [Harness refinement v2: 8 requests]({{ '/iterations/02/results/harness-refinement.json' | relative_url }})
- [L09 refinement v3: 5 requests]({{ '/iterations/02/results/core-refinement-v3.json' | relative_url }})
- [H19 refinement v3: 4 requests]({{ '/iterations/02/results/harness-refinement-v3.json' | relative_url }})
- [Final acceptance selection: 134 fixtures]({{ '/iterations/02/results/final-acceptance.json' | relative_url }})
- [Summary]({{ '/iterations/02/results/summary.json' | relative_url }})
- [Source-selection receipt]({{ '/iterations/02/results/source-selection.json' | relative_url }})

Run the [offline verifier]({{ '/iterations/02/evaluate.py' | relative_url }}) to independently re-check the digest bindings and selection map.
