---
layout: default
title: Email Pattern Evaluation
description: Original misses, versioned refinements, and replayable synthetic Jev evidence.
permalink: /email/evaluation/
---

# Email pattern evaluation — September 26, 2026

| Stage | Matches | Meaning |
| --- | --- | --- |
| Initial v1 | 34 / 36 | Two examples plus one empty-state probe per pattern |
| EM07/EM08 v2 reruns | 6 / 6 | All three fixtures for each changed contract |
| EM10 v2 first pass | 6 / 7 | Preserved miss: answer-like text without the underlying request was labeled substantive |
| EM10 v3 rerun | 7 / 7 | Replayed all EM10 cases with request-bound substantive-reply evidence |
| Selected current versions | 40 / 40 | Unchanged v1 receipts plus current revised versions and four added EM10 boundary cases |

The 56 stored fixture calls used `jev-1.13.0` through the existing approved bridge, with no cache hits. Receipts report 29,895 input and 3,185 output tokens. Their summed **bridge estimate** is $0.00125559; this is not an invoice or general cost benchmark. Supplemental semantic-review probes were separate from these fixture calls and are excluded from the counts and cost.

## What failed and changed

- **EM07-3:** Empty current text was classified `no_document_claim` (confidence 0.38), expected `unknown`.
- **EM08-3:** Empty request and draft were classified `omitted` (confidence 0.49), expected `unknown`.
- Both instructions already contained a general missing-evidence rule, but did not give it explicit precedence over the negative category. Version 2 states that absent/empty required text selects unknown first. This observed wording deficiency is established; the model's internal reason is unknown.
- **EM10 v1 overlap:** An out-of-office reply can also acknowledge receipt, while the contract had no precedence rule. The original examples did not contain both signals. EM10 v2 added explicit precedence and request context; its EM10-7 probe (answer-like body without `underlying_request`) still returned `substantive_reply` at 0.51 option probability and 0.38 confidence, against a frozen `unknown` expectation. Version 3 now requires a non-empty related request for `substantive_reply`; it also leaves receipt-only acknowledgments usable without that context. The v2 miss is preserved in [the first-pass snapshot]({{ '/email/results/em10-v2-first-pass.json' | relative_url }}).
- The evaluator previously required the current fixture IDs to exactly equal the original set, preventing a revised contract from adding regression cases. It now permits version-matched additions only for revised contracts while refusing removal or rewriting of any frozen case.
- Original fixture states and expected labels stayed frozen; added cases use new IDs and revised contract versions. Initial receipts, the full EM10 v2 first pass, and current v3 receipts remain separate. A production controller should also reject missing required evidence before spending an inference call.

## Replay locally

From the repository root, using Python 3 and no network:

```sh
python3 email/evaluate.py
python3 -m unittest discover -s email -p 'test_*.py' -v
```

The evaluator binds each raw request to its fixture state, exact question version, model, and SHA-256 digest; checks typed labels and probability values; preserves initial misses and the EM10 v2 miss; and selects only current-version receipts. Tests cover changed state/questions, digest tampering, stale versions, fixture additions/removals/rewrites, missing/duplicate receipts, invalid values, provider failure, and expectation separation.

The provider's `confidence` summarizes distribution shape; it is not defined as the selected option's probability. The checker validates each independently rather than requiring equality. A valid digest shows artifact binding, not authenticity of an external email or correctness of a judgment.

## Inspect the artifacts

- [Current catalog]({{ '/email/catalog.json' | relative_url }}) and [fixtures]({{ '/email/fixtures.json' | relative_url }})
- [Initial catalog]({{ '/email/results/initial-catalog.json' | relative_url }}) and [initial fixtures]({{ '/email/results/initial-fixtures.json' | relative_url }})
- [All initial receipts, including misses]({{ '/email/results/initial.json' | relative_url }})
- [Current revision receipts]({{ '/email/results/refinement.json' | relative_url }})
- [Preserved EM10 v2 first-pass receipts and miss]({{ '/email/results/em10-v2-first-pass.json' | relative_url }})
- [Machine-readable summary]({{ '/email/results/summary.json' | relative_url }})

## Limits and next qualification

The fixture author also designed the questions. Expectations are held outside provider state, but this is not independent annotation or a held-out test. Revised questions were tuned on these same cases. Four new EM10 boundary cases address specific overlaps and missing context; most other profiles still have only two substantive examples plus an empty-state probe, not coverage of every output label. No real mailbox, email parser, adversarial corpus, non-English set, attachment verifier, send path, or human-time baseline was tested.

Before operational use, freeze a representative, authorized and appropriately minimized corpus with independently reviewed labels. Include quote/forward boundaries, multiple recipients, changed requests, ambiguous dates, multiple request items, forged automatic replies, contradictory evidence, and absent attachments. Measure costly false positives and review workload; choose a risk-based threshold. Keep mailbox actions behind existing authorization and outcome checks.

[Email catalog]({{ '/email/' | relative_url }}) · [Official sources]({{ '/email/sources/' | relative_url }})
