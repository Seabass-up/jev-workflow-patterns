# Whole-catalog review — local checkpoint

Goal: review every pattern, test it, repair confirmed defects, and commit locally.
No push, pull request, publication, or deployment is included.

## Coverage established

- 390 profiles in 30 catalogs, plus three foundational workflow guides.
- `baseline.json`: all 65 existing offline replay/test commands passed.
- `validator-repair.json`: all 65 commands passed after the iteration-01 validator repair and inventory tests.
- Each profile row binds its complete source contract with a SHA-256 and identifies its current version.
- Whole-contract advisory screening now covers all 390 profiles in 113 uncached Jev requests, with exact request/response binding checked by `scripts/verify_semantic_review.py`. It flagged 44 profiles for host review. No provider failures occurred.
- Wave 01 inspected eight flagged profiles: six flags were not confirmed by source inspection and 12 new live synthetic boundary cases; two require targeted/consumer review. Thirty-six other flagged profiles remain unreviewed. Unflagged profiles also need proportionate host verification because screening can miss defects.
- The 12 cases matched their frozen expectations. HA22's combined-target `unknown` answer has confidence 0.70, retained as uncertainty rather than promoted to confident automation. These are development screens, not independent held-out cases.
- `semantic-and-boundary-coverage.json` is the verified screen/behavior receipt summary; `host-triage-wave01.json` records source conclusions and measured usage. Semantic screening is not calibration evidence, production qualification, or approval of every question contract.

## Confirmed repair

Iteration 01 previously accepted a Choice response missing its probability distribution and passed it to the typed-signal proposal. The repaired validator checks full Choice/Score distribution coverage, finite values, bounded rounding tolerance, and maximum-Choice consistency. Regression tests cover malformed and missing distributions. All 136 historical iteration-01 request bindings still replay. See `jev-validator-candidate.json` for the low-confidence Jev triage output that preceded deterministic reproduction and `../../docs/lessons-learned.md` for the repair lesson.

## Resumption

### Iteration 03 source-triage checkpoint (wave 04)

All fourteen original iteration-three flags have been source-inspected. Five are
not confirmed as contract defects (E15/L14/L15/L16/H30); their frozen live boundary
cases match all eleven question expectations. Nine retain specific source-confirmed
ambiguity or missing-evidence/availability defects and need versioned repairs.
Thirteen original iteration-four flags are still not host-reviewed. This checkpoint
does not close the whole-pattern goal, the H05 policy issue, unflagged source review,
foundational-guide review or kernel/tooling review.

Iterations 02–04 shared a deterministic validator defect: 0.99/1.01 rounded
distributions were rejected while nonmaximum Choice labels were accepted.
The repaired validators use a per-value rounding bound and maximum-selection check;
cross-iteration tests also retain malformed-distribution rejection and tied maxima.
See `validator-rounding-reproduction.json`, `host-triage-wave04.json`, and the wave-04
frozen fixtures/receipts. These are local synthetic checks, not live qualification.

### Controller repair checkpoint

The iteration-01 L01 consumer finding is structurally repaired across all four
historical planners (120 profiles): callers must supply keyword `state=...`, and
missing/empty top-level required evidence returns review. Tests cover every declared
field, valid branch paths, and the mandatory-alert exception. This is not a change
to the semantic question contracts and does not establish nested schema validity,
semantic sufficiency, provenance or response-to-state binding. H05's competing-defect
recovery policy and the other source-review candidates remain open.

### Iteration 02 semantic review checkpoint

The subsequent wave 03 resolves B09/B13/L10/H15 at v2. All nine iteration-02
flags are now either source-refuted with targeted checks or repaired with versioned
regressions. The four new repairs match 25/25 cases; two low-confidence answers
remain review-required. Original screens and source contracts remain preserved.
The 27 not-yet-host-reviewed original flags elsewhere remain open.

Wave 02 source-inspected all nine iteration-02 flags. B11/L08/L09/H13 already
define mixed/ambiguous escapes; four fresh development cases confirm those paths.
H18 is repaired at v2 with explicit counterevidence precedence, seven new exact
receipt bindings (four unchanged regressions, three new boundaries), and consumer
tests preserving low-confidence review. B09/B13/L10/H15 retain specific co-occurrence
questions for targeted repair; no untested fix is claimed. Twenty-seven original
flags have not yet received host review. The full original 390-profile screen is
preserved; H18's old screen is explicitly marked not matching its current contract.

1. Exact receipts for the separate canonical checkout's earlier whole-contract screen were not located in the bounded lookup. Its uncommitted changes remain untouched. Reuse source-bound evidence only where actually available; do not rely on narrative counts.
2. Reuse only evidence bound to the exact current pattern hash/version. Independently test surviving candidates and realistic co-occurring labels, missing evidence, contradiction, and authority boundaries.
3. Version semantic changes; preserve original contracts and receipts; run targeted live synthetic regressions and held-out boundary cases.
4. Review the three foundational guides and kernel/tooling contracts, rerun the full suite, and commit scoped local changes.

Run another immutable snapshot with `python3 scripts/review_all_patterns.py --output reviews/2026-09-26/<new-name>.json`. Existing output files are not overwritten.
