# Whole-catalog review — local checkpoint

Goal: review every pattern, test it, repair confirmed defects, and commit locally.
No push, pull request, publication, or deployment is included.

## Coverage established

- 390 profiles in 30 catalogs, plus three foundational workflow guides.
- `baseline.json`: all 65 existing offline replay/test commands passed.
- `validator-repair.json`: all 65 commands passed after the iteration-01 validator repair and inventory tests.
- Each profile row binds its complete source contract with a SHA-256 and identifies its current version.
- Whole-contract advisory screening now covers all 390 profiles in 113 uncached Jev requests, with exact request/response binding checked by `scripts/verify_semantic_review.py`. It flagged 44 profiles for host review. No provider failures occurred.
- Source dispositions cover all 44 profiles originally flagged by the advisory screen across waves 01–09, including versioned repairs, source-refuted flags, and checks that did not apply to non-Choice contracts. The two wave-01 follow-ups (H05's co-occurring-defect contract and L01's required-state consumer boundary) are resolved locally. The initial `semantic-coverage.json` remains a frozen screen inventory: 346 profiles were unflagged in that baseline, not a current remaining-work count. Separate source-review waves below have since covered email, call controls, and auto performance. Three foundations, remaining profiles, and kernel/tooling still need proportionate review because screening can miss defects.
- The 12 cases matched their frozen expectations. HA22's combined-target `unknown` answer has confidence 0.70, retained as uncertainty rather than promoted to confident automation. These are development screens, not independent held-out cases.
- `semantic-and-boundary-coverage.json` is the verified screen/behavior receipt summary; `host-triage-wave01.json` records source conclusions and measured usage. Semantic screening is not calibration evidence, production qualification, or approval of every question contract.

## Confirmed repair

Iteration 01 previously accepted a Choice response missing its probability distribution and passed it to the typed-signal proposal. The repaired validator checks full Choice/Score distribution coverage, finite values, bounded rounding tolerance, and maximum-Choice consistency. Regression tests cover malformed and missing distributions. All 136 historical iteration-01 request bindings still replay. See `jev-validator-candidate.json` for the low-confidence Jev triage output that preceded deterministic reproduction and `../../docs/lessons-learned.md` for the repair lesson.

## Resumption

### Email profile review and EM10 v3 repair (wave 10)

All 12 email contracts, required-state declarations, consumer boundaries, fixtures,
receipts and pattern pages were source-inspected, with the email evaluator replaying
the prior screens. Supplemental Jev overlap signals were checked against the full
criteria: EM01 defines owner-with-others versus other-only, EM02 routes contradictory
current/quoted intent to `unknown`, EM05 routes conflicting roles for one date phrase
to `unknown`, EM06 makes explicit alternatives counterproposals, EM08 prioritizes
deferral, EM09 uses `unknown` when the next step is unclear, and EM11 routes multiple
equally primary intents to `unknown`. EM10 v1 was the confirmed gap: an out-of-office
notice could also read as a receipt acknowledgment without a tie-break.

EM10 v2 added precedence and request context but still labeled an answer-like message
without its underlying request as `substantive_reply` (0.51 option probability,
0.38 confidence) against a frozen `unknown` expectation. That first pass is preserved
in `email/results/em10-v2-first-pass.json`. EM10 v3 requires a non-empty
`underlying_request` before assigning `substantive_reply`, makes the co-occurrence
order explicit, and retains receipt-only acknowledgments without request context.
Seven uncached v3 synthetic cases match 7/7, including the prior miss and four added
boundaries. The evaluator now permits version-matched regression additions only for
revised contracts while rejecting original-case removal or rewriting. Email replay
selects 40/40 current fixtures across 12 profiles and verifies 56 stored request
digests; 23 offline email tests pass, including page/catalog parity and exact
positive-integer contract-version checks. These are
author-labelled development checks, not held-out accuracy or mailbox qualification.

No site rendering, push, or deployment is claimed for this local checkpoint.

### Auto-performance AP03 v2 clarification (wave 12)

All eight auto-performance contracts, required fields, consumer boundaries, 32 v1
fixtures and receipts, and eight pattern pages were source-reviewed. A bounded Jev
wording review marked AP03 criteria meaning as an uncertain review lead; host review
confirmed that v1 required fitment text to name drivetrain while its positive fixture
did not. The v1 label still matched Jev, demonstrating why receipt agreement alone is
not a contract-to-evidence audit.

AP03 v2 clarifies the reading of unqualified category fitment versus explicit
conditions and adds AP03-5 (unresolved drivetrain) and AP03-6 (vague nonempty text).
All original AP03 fixture states and expected labels are preserved, v1
catalog/fixture/summary snapshots remain available, and the evaluator rejects
fixture removal or state/expectation rewrites during a versioned revision. Six
uncached v2 Jev cases matched 6/6; the initial v1 screen remains 32/32 and the
current selected collection is 34/34. AP03-6's `unknown` answer has confidence 0.37,
below the 0.8 review floor, so the follow-up remains mandatory. The evaluator verifies
38 historical/current request digests; all 19 auto-performance tests, exact question
JSON parity on 8/8 pages, and all 65 repository check commands passed in the final
pre-commit run (`wave12-final-checks-precommit.json`). A fresh post-commit run will
bind repository-wide results to the committed source revision.

This is a synthetic contract repair, not physical fitment confirmation, production
qualification, calibration evidence, site rendering, or deployment. The Jekyll site
could not be rendered locally because this checkout has no Gemfile or `jekyll`
executable.

### Call-control profile source review (wave 11)

All ten `controls/` question contracts and their 40 synthetic fixture states were
reviewed against the declared consumer boundaries. The offline evaluator verifies
all 40 stored request digests; 28/30 design labels and 10/10 separately authored
challenge labels match. All ten pattern pages reproduce their catalog question
JSON exactly. The 12 call-control unit tests pass.

CT03-3 remains a preserved disagreement (`unknown` expected; Jev selected
`drops_an_action`, confidence 0.72). The described consumer has a deterministic
preflight that returns `unknown` for an absent or empty `commands` field, so this
screening result is not evidence to infer a missing action from empty input. CT07-2
also remains a preserved disagreement (`not_a_complement` expected; Jev selected
`exact_complement`, confidence 0.56); the authored example demonstrates a realistic
co-occurrence, so CT07 remains provisional rather than relabeling the case after
inference. No contract defect was confirmed from these receipts and no contract was
changed in this wave. This is synthetic development evidence, not runtime or
production qualification.

Local checks: `python3 controls/evaluate.py`,
`python3 -m unittest discover -s controls -p 'test_*.py'`, and a read-only
catalog-to-page exact-JSON parity check (10/10) pass. See
`controls/evaluation.md` and `controls/results/overlap-review.json` for the
preserved screen and pre-inference overlap review. The catalog remains marked
provisional where its recorded evidence requires it.

### H05 co-occurring defect repair (wave 09)

The original H05 Choice contract had no outcome for two independently demonstrated defects, while its pure consumer proposed one targeted repair for any recognized single label. A bounded Jev question-contract check selected `forces_single_or_unspecified` at 0.97 confidence. Its consumer-route answer (0.86) was accompanied by an evidence check of 0.59 and therefore remained `needs_review`; host inspection of `iterations/01/evaluate.py` confirmed the branch behavior.

H05 is now version 2 with `multiple_demonstrated_defects`; the consumer routes that label to failure review instead of selecting one repair. The duplicate, non-measurable success metric was replaced with fresh-case baseline, preserved-regression, and multi-defect review-rate measures. The four historical H05 v1 fixtures and receipts remain unchanged. Six uncached v2 synthetic cases match 6/6 across every label, including independently evidenced criterion overlap plus cross-question dependency. One state-mismatch result has confidence 0.78, so the consumer retains it for review. Iteration 1 now replays 142/142 request hashes and passes 42 local tests. This is a development screen, not independent or production evidence. See `iterations/01/results/h05-v2-screen.json` and `../../docs/lessons-learned.md`.

### Iteration 4 flagged-contract overlap repair (wave 08)

All 13 original Iteration 4 overlap flags were source-inspected. Ten are Choice
contracts with overlapping or nested labels and are now version 2: B22, B25, E23,
E24, E26, L19, L20, L21, L24 and H40. B23, B26 and H33 have no Choice question,
so the label-overlap check did not apply; they were source-confirmed as not applicable.

The first v2 synthetic screen's four misses are preserved in
`iterations/04/results/overlap-v2-first-pass.json` (41/45). The current v2 screen
matches 46/46 independently authored cases, covering every current label, and the
86-fixture current selection matches 86/86. The initial v1 screen and its misses
remain unchanged. A v1 Jev pair screen covered 64 pairs; the current v2 pair review
covers 77, with the model selecting only `disjoint` or `precedence_resolved`.
L20's first pair review still records an unresolved verbatim/typed overlap; its
refinement and the new explicit `mixed_output_obligations` priority are retained in
the audit record. Pair outputs are advisory screening, not a proof of semantic
disjointness. L24's underspecified boundary remains low-confidence and review-only.

Local verification: `python3 iterations/04/evaluate.py` and
`python3 -m unittest discover -s iterations/04 -p 'test_*.py' -v` pass (13 tests).
No public-site build or deployment was performed. The whole-pattern goal remains
active: unflagged patterns, other iterations, foundational guides and kernel/tooling
still need proportionate source review and tests.

### H24 availability safety repair (wave 06)

V1 returned burden 0.04 at confidence 0.94 with no burden evidence and proposed score
composition. H24 now includes a separate availability Noul and a code-owned provisional
0.8 gate; unavailable/uncertain burden ignores the Score and returns review. A named
veto still takes precedence. The first v2 screen's three misses are retained; one
bounded v3 refinement matches 6/7 cases and 27/28 intervals. The negated-resource case
is still held at availability 0.66 rather than silently accepted or relabeled.
Current historical selection remains 61/61, with 86/86 question checks. Three other
iteration-three contract repairs remain (L17/L18/H28), along with H24's conservative
availability limitation, the thirteen iteration-four flags, H05, unflagged review,
foundational guides and kernel/tooling. This is a local tested safety repair, not
production qualification or deployment.

### Iteration 03 versioned repairs (wave 05)

B19/E18/H22/H26/H27 are repaired at v2. Twenty-four frozen cases (ten unchanged
regressions and fourteen development boundaries) matched; thirty option-pair checks
selected disjoint/precedence-resolved, with all uncertainty retained. Originals bind
Git `f600346`, and no original state or label was changed. The evaluator verifies
the revised questions and exact receipts before selecting new historical receipts.
Four confirmed iteration-three repairs remain: L17, L18, H24 and H28. Thirteen
original iteration-four flags remain unreviewed; H05, unflagged source review,
foundational guides and kernel/tooling remain outstanding. Local-only checkpoint.

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
recovery policy was subsequently addressed in wave 09; top-level presence checks still
do not establish nested semantic sufficiency, provenance or response-to-state binding.

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
