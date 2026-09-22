---
layout: default
title: Email Pattern Evaluation
description: Original misses, versioned refinements, and replayable synthetic Jev evidence.
permalink: /email/evaluation/
---

# Email pattern evaluation — September 22, 2026

| Stage | Matches | Meaning |
| --- | --- | --- |
| Initial v1 | 34 / 36 | Two examples plus one empty-state probe per pattern |
| EM07/EM08 v2 reruns | 6 / 6 | All three fixtures for each changed contract |
| Selected current versions | 36 / 36 | Unchanged v1 receipts plus revised v2 receipts |

The 42 live screening calls used `jev-1.13.0` through the existing approved bridge, with no cache hits. Receipts report 20,040 input and 2,340 output tokens. Their summed **bridge estimate** is $0.00084168; this is not an invoice or general cost benchmark. An additional two-question advisory design review was separate from these fixture calls and is excluded from the counts and cost.

## What failed and changed

- **EM07-3:** Empty current text was classified `no_document_claim` (confidence 0.38), expected `unknown`.
- **EM08-3:** Empty request and draft were classified `omitted` (confidence 0.49), expected `unknown`.
- Both instructions already contained a general missing-evidence rule, but did not give it explicit precedence over the negative category. Version 2 states that absent/empty required text selects unknown first. This observed wording deficiency is established; the model's internal reason is unknown.
- State and expected labels stayed frozen. The initial contracts and receipts are retained alongside v2. A production controller should also reject missing required evidence before spending an inference call.

## Replay locally

From the repository root, using Python 3 and no network:

```sh
python3 email/evaluate.py
python3 -m unittest discover -s email -p 'test_*.py' -v
```

The evaluator binds each raw request to its fixture state, exact question version, model, and SHA-256 digest; checks typed labels and probability values; preserves initial misses; and selects only current-version receipts. Thirteen tests cover changed state/questions, digest tampering, stale versions, missing/duplicate receipts, invalid values, provider failure, and expectation separation.

The provider's `confidence` summarizes distribution shape; it is not defined as the selected option's probability. The checker validates each independently rather than requiring equality. A valid digest shows artifact binding, not authenticity of an external email or correctness of a judgment.

## Inspect the artifacts

- [Current catalog]({{ '/email/catalog.json' | relative_url }}) and [fixtures]({{ '/email/fixtures.json' | relative_url }})
- [Initial catalog]({{ '/email/results/initial-catalog.json' | relative_url }}) and [initial fixtures]({{ '/email/results/initial-fixtures.json' | relative_url }})
- [All initial receipts, including misses]({{ '/email/results/initial.json' | relative_url }})
- [Six v2 receipts]({{ '/email/results/refinement.json' | relative_url }})
- [Machine-readable summary]({{ '/email/results/summary.json' | relative_url }})

## Limits and next qualification

The fixture author also designed the questions. Expectations are held outside provider state, but this is not independent annotation or a held-out test. Revised questions were tuned on these same cases. Only two substantive examples per pattern are covered, not every output label. No real mailbox, email parser, adversarial corpus, non-English set, attachment verifier, send path, or human-time baseline was tested.

Before operational use, freeze a representative, authorized and appropriately minimized corpus with independently reviewed labels. Include quote/forward boundaries, multiple recipients, changed requests, ambiguous dates, multiple request items, forged automatic replies, contradictory evidence, and absent attachments. Measure costly false positives and review workload; choose a risk-based threshold. Keep mailbox actions behind existing authorization and outcome checks.

[Email catalog]({{ '/email/' | relative_url }}) · [Official sources]({{ '/email/sources/' | relative_url }})
