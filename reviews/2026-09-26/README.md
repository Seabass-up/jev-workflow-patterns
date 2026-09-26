# Whole-catalog review — local checkpoint

Goal: review every pattern, test it, repair confirmed defects, and commit locally.
No push, pull request, publication, or deployment is included.

## Coverage established

- 390 profiles in 30 catalogs, plus three foundational workflow guides.
- `baseline.json`: all 65 existing offline replay/test commands passed.
- `validator-repair.json`: all 65 commands passed after the iteration-01 validator repair and inventory tests.
- Each profile row binds its complete source contract with a SHA-256 and identifies its current version.
- Semantic and live boundary review remain pending. Existing recorded-response replay is not a new model test, calibration evidence, production qualification, or approval of every question contract.

## Confirmed repair

Iteration 01 previously accepted a Choice response missing its probability distribution and passed it to the typed-signal proposal. The repaired validator checks full Choice/Score distribution coverage, finite values, bounded rounding tolerance, and maximum-Choice consistency. Regression tests cover malformed and missing distributions. All 136 historical iteration-01 request bindings still replay. See `jev-validator-candidate.json` for the low-confidence Jev triage output that preceded deterministic reproduction and `../../docs/lessons-learned.md` for the repair lesson.

## Resumption

1. Review prior whole-contract screening evidence from the separate canonical checkout read-only; preserve its ongoing uncommitted work.
2. Reuse only evidence bound to the exact current pattern hash/version. Independently test surviving candidates and realistic co-occurring labels, missing evidence, contradiction, and authority boundaries.
3. Version semantic changes; preserve original contracts and receipts; run targeted live synthetic regressions and held-out boundary cases.
4. Review the three foundational guides and kernel/tooling contracts, rerun the full suite, and commit scoped local changes.

Run another immutable snapshot with `python3 scripts/review_all_patterns.py --output reviews/2026-09-26/<new-name>.json`. Existing output files are not overwritten.
