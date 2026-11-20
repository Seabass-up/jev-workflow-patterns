# Whole-catalog review — local checkpoint

Goal: review every pattern, test it, repair confirmed defects, and commit locally.
No push, pull request, publication, or deployment is included.

## Coverage established

- 390 profiles in 30 catalogs, plus three foundational workflow guides.
- `baseline.json`: all 65 existing offline replay/test commands passed.
- `validator-repair.json`: all 65 commands passed after the iteration-01 validator repair and inventory tests.
- Each profile row binds its complete source contract with a SHA-256 and identifies its current version.
- Whole-contract advisory screening now covers all 390 profiles in 113 uncached Jev requests, with exact request/response binding checked by `scripts/verify_semantic_review.py`. It flagged 44 profiles for host review. No provider failures occurred.
- Source dispositions cover all 44 profiles originally flagged by the advisory screen across waves 01–09, including versioned repairs, source-refuted flags, and checks that did not apply to non-Choice contracts. The two wave-01 follow-ups (H05's co-occurring-defect contract and L01's required-state consumer boundary) are resolved locally. The initial `semantic-coverage.json` remains a frozen screen inventory: 346 profiles were unflagged in that baseline, not a current remaining-work count. Separate source-review waves below have since covered email, call controls, auto repair/performance, motorsport, construction, cybersecurity, legal contracts, finance, and data quality. Three foundations, remaining profiles, and kernel/tooling still need proportionate review because screening can miss defects.
- The 12 cases matched their frozen expectations. HA22's combined-target `unknown` answer has confidence 0.70, retained as uncertainty rather than promoted to confident automation. These are development screens, not independent held-out cases.
- `semantic-and-boundary-coverage.json` is the verified screen/behavior receipt summary; `host-triage-wave01.json` records source conclusions and measured usage. Semantic screening is not calibration evidence, production qualification, or approval of every question contract.

## Confirmed repair

Iteration 01 previously accepted a Choice response missing its probability distribution and passed it to the typed-signal proposal. The repaired validator checks full Choice/Score distribution coverage, finite values, bounded rounding tolerance, and maximum-Choice consistency. Regression tests cover malformed and missing distributions. All 136 historical iteration-01 request bindings still replay. See `jev-validator-candidate.json` for the low-confidence Jev triage output that preceded deterministic reproduction and `../../docs/lessons-learned.md` for the repair lesson.

## Resumption

### Finance FN01–FN08 source and page review (wave 18)

All eight finance contracts, required fields, criteria, code-owned boundaries,
follow-ups, source notes, frozen fixtures, saved Jev receipts, and pages were
reviewed. The evaluator verifies all 32 successful request digests; all 24 design
and 8 challenge cases still match, with no provider failures or provisional
patterns. Five saved source-support checks and the 72-pair overlap review were
reused. Their source review dates from September 23; FN-S3 (Net D) was marked as
changed since its prior source record and was not live-refreshed in this wave.

The low-confidence overlap leads for FN07 and FN08 were reviewed with one uncached
Jev request over two synthetic boundaries, without sending expected labels. Jev
favored conditional approval for the contingent sign-off case (probability 0.98)
and inconsistent for a memo with a matching counterparty but different purpose
(probability 0.67); the conflict-rule question for FN08 favored the stated
inconsistent rule (0.97). Host review found the existing wording adequate for
these specific cases, so both v1 contracts and all expectations remain unchanged.
The request and results are preserved in ../2026-09-27/wave18-finance-review.json.

Confirmed the same missing-field documentation overclaim as wave 17: all eight
pages stated that code already returns unknown, although this collection contains
no consumer or preflight implementation. Reworded them as a future consumer-code
requirement and added a test that checks both exact page/catalog JSON parity and
this boundary across all eight pages. All 13 finance tests pass. The legal and
finance page repairs are documented together in ../../docs/lessons-learned.md.

The full pre-commit and post-commit audits each pass 65/65 checks across 390
profiles and 30 catalogs. The post-commit snapshot binds to local code commit
14d9684 in ../2026-09-27/wave18-postcommit-checks.json; the review and pre-commit
receipt are beside it. All examples are synthetic: this is not finance advice,
held-out performance, live ledger/approval verification, or consumer qualification.
No Jekyll render, push, or deployment was performed; the overall goal remains
active.

### Data Quality DQ01–DQ08 and shared preflight-claim repair (wave 19)

Reviewed all eight Data Quality contracts, named evidence, criteria and precedence,
code-owned boundaries, follow-ups, source notes, frozen fixtures, saved Jev
responses, and pattern pages. The evaluator verifies all 32 successful request
digests: 21/24 design cases and 8/8 separately authored challenge cases match
(29/32 overall); DQ03 and DQ06 remain provisional. Preserved all three design
disagreements without changing questions or labels: DQ03-3 (`unknown` expected;
`fits_sibling_entry` observed at 0.32), DQ06-2 (`admits_two_readings` expected;
`single_reading` at 0.42), and DQ06-3 (`unknown` expected; `circular_or_empty` at
0.92). Contract inspection supports the frozen unknown expectations for the empty
required fields in DQ03-3 and DQ06-3; DQ06-2's missing discount/tax basis matches
the contract's two-readings example. No question defect was confirmed.

The existing source-support receipt is dated September 23: DQ-S1, S2, S3, and S5
were marked changed since the recorded text; S4 was unchanged. Sources were not
refreshed because this repair concerns unsupported claims about local runtime
behavior, not the source summaries or Jev performance.

Tracing the page claim to `scripts/build_collection_pages.py` found 193 additional
generated pattern pages with the false statement that code already performs a
missing-field gate. Corrected the shared template and only that sentence in the
193 pages, plus added a generator regression and Data Quality exact page/catalog
JSON and consumer-boundary tests. Legal and Finance's 16 earlier corrections
remain covered. No contract, version, fixture, or receipt changed. The Data Quality
evaluator verifies 32 request digests and all 13 tests pass; the new generator test
passes. The 65-command pre-commit audit passes across 390 profiles and 30 catalogs
at base commit `2cf9479`; the post-commit audit passes 65/65 and binds to code
commit `d4e4d39` in `../2026-09-27/wave19-postcommit-checks.json`. The pre-commit
receipt is `../2026-09-27/wave19-final-checks-precommit-locked.json`; detailed
Data Quality dispositions are in `../2026-09-27/wave19-data-quality-review.json`.

This is a documentation-generator correction and synthetic pattern review, not a
live consumer test, source refresh, production qualification, or held-out accuracy
claim. No Jekyll rendering, push, or deployment was performed; the goal remains
active.

### Legal contracts LC01–LC08 source review and page-claim repair (wave 17)

All eight legal-contract patterns, their complete question JSON, required fields,
criteria, code-owned boundaries, follow-ups, source notes, frozen fixtures, saved
receipts, and pages were reviewed. The existing evaluator verifies all 32 successful
request digests. The original screen remains 31/32: all eight challenge cases match,
while LC02-3 remains a preserved miss (`unknown` expected; Jev chose
`obligation_on_party_a`, confidence 0.38) because `party_b` is empty. LC02 remains
provisional; no contract or fixture expectation was changed.

Confirmed a documentation overclaim on all eight pages: they described a required
missing-field gate as already-executed deterministic behavior, but the legal-contract
collection contains no consumer or preflight implementation. Reworded the statements
as a future consumer-code requirement and made the implementation limit explicit.
A regression checks both exact catalog/page question JSON parity and this boundary on
all eight pages; all 13 legal-contract tests pass. One uncached Jev wording check
supported the distinction (original statement: existing behavior, 0.78 probability;
revision: clear requirement, not verified runtime behavior, 1.00). This was advisory;
the repository inspection established the missing implementation.

The full pre-commit and post-commit audits each pass 65/65 checks across 390 profiles
and 30 catalogs. The post-commit snapshot binds to local code commit `69b2f47` in
`../2026-09-27/wave17-postcommit-checks.json`; the review and pre-commit receipt are
beside it. `../../docs/lessons-learned.md` records the repair. These are synthetic question
screens, not legal advice, held-out performance, a live consumer test, or production
qualification. No Jekyll rendering, push, or deployment was performed; the broader
pattern-review goal remains active.

### Cybersecurity CY01–CY08 source and contract review (wave 16)

All eight cybersecurity contracts, required fields, criteria, code-owned
responsibilities, verification recipes, follow-ups, source references, pattern pages
and frozen fixtures were reviewed. Existing Jev source-support, option-overlap and
32-case screening receipts were reused. The original screen is 31/32 (24/24 design,
7/8 challenge); CY02-4 remains the sole disagreement (not_accounted_for expected,
partly_accounted_for observed at confidence 0.9).

A focused uncached Jev contract-fit judgment favored the frozen CY02-4 expectation
(probability 0.91, confidence 0.88); host review confirmed the completed
prior-evening change does not produce the 03:40 activity in the same period. The
disagreement is preserved as a model miss, not used to tune or relabel. Two further
boundary probes considered edition matching in CY03 and partial evidence in CY04.
Neither established a defect: CY03 keeps exact identifier matching with code (the
integration must confirm edition handling before consequence), and CY04's existing
not-stated label can cover a required condition set that is not fully established.
The patterns remain v1; no contract or fixture expectation changed.

Added a regression test asserting that each of the eight pattern pages embeds the
exact question JSON in its catalog. The cybersecurity evaluator validates all 32
saved request digests and exact summary replay; all 13 tests pass. Evidence and
limits are recorded in ../2026-09-27/wave16-cybersecurity-review.json. The full
pre-commit audit passes 65/65 checks across 390 profiles and 30 catalogs
(../2026-09-27/wave16-final-checks-precommit-locked.json). No lesson entry was
fabricated because this review did not produce a confirmed repair. After local code
commit cc858ca, the post-commit audit again passes 65/65 checks across 390 profiles
and 30 catalogs (../2026-09-27/wave16-postcommit-checks.json). The whole-pattern
goal remains active; no site deployment or push.

### Construction CN05 v2 list-bound clarification (wave 15)

All eight construction question contracts, required state, source notes, consumer
boundaries, fixture history, stored screening receipts, and pattern pages were
reviewed. CN05 v1's purpose and named list defined project-policy routing, but its
instructions also made any active exposure a stop-work condition outside the supplied
list. A bounded Jev review favored aligning the label to the complete list (top
probability 0.91, confidence 0.89); its scope-mismatch diagnosis was lower confidence
(0.58, confidence 0.44) and was treated as advisory. CN05 is now v2: list-matched
conditions are `stop_work_condition`; other deficiencies, including actively exposed
unlisted hazards, are `hazard_to_correct` for human review. This does not say a
condition is safe or decide work stoppage or urgency.

All four v1 fixture states and expectations remain unchanged. Seven uncached v2
reviewer-authored development cases matched 6/7. CN05-7 remains a disagreement
(`unknown` expected for an empty list; Jev selected `positive_no_deficiency`, confidence
0.95); the described deterministic preflight is not implemented or verified against a
live consumer. The original v1 CN05-4 disagreement is also retained. Current selection
is 34/35 across 35 cases; the offline evaluator validates all 39 historical/refinement
request digests. All 24 construction tests pass, including current/archived separation,
receipt integrity, immutable fixture history, and exact question JSON parity for all
eight pages. Full-catalog pre-commit and post-commit checks are recorded in
`../2026-09-27/` after completion. See `../2026-09-27/wave15-construction-review.json`
and `../../docs/lessons-learned.md`.

This is a synthetic question-contract repair, not site-specific safety policy,
independent human agreement, live queue/notification verification, or production
qualification. Local code commit `6043e1d` is verified by the post-commit snapshot:
all 65 repository checks pass across 390 profiles and 30 catalogs
(`../2026-09-27/wave15-postcommit-checks.json`). The evidence/lessons follow-up is
recorded locally; the whole-pattern goal remains active, with no public build, push,
or deployment.

### Motorsport MR04 v2 clarification (wave 14)

All eight motorsport profiles, their question contracts, source notes, consumer
boundaries, fixtures, stored receipts, and pattern pages were reviewed. Seven profiles
remain unchanged. The initial v1 screen still replays 31/32, including the preserved
MR04-4 disagreement (`observation` expected; Jev chose `conformance_claim` at
confidence 0.4). Host review confirmed the wording gap: v1 did not explicitly say
that a measured value accompanied by an applicable limit, without a stated relation,
remains an observation; the numeric comparison belongs in code.

MR04 is now version 2 with that boundary explicit. Its four original cases and
expectations are preserved, and MR04-5/6 add reviewer-authored challenge cases for
the distinction between adjacent value/limit evidence and an explicit conformance
claim. Six uncached v2 Jev calls match 6/6. The current selection uses 28 unchanged
v1 receipts and six v2 receipts: 34/34 labels match, with 38 historical/refinement
request digests verified. The new evaluator rejects version skips, contract edits
without a version increment, and removed or rewritten fixtures. All 22 motorsport
tests pass, including exact question JSON parity on MR04's page. The full pre-commit
final pre-commit audit passes 65/65 commands across 390 profiles and 30 catalogs
(`wave14-final-checks-precommit-final.json`). Detailed receipts and limits are in
`wave14-motorsport-review.json`; the repair lesson is in
`../../docs/lessons-learned.md`.

This is a synthetic contract clarification, not a real measurement or compliance
decision, production qualification, or independent test set. Local commit and
post-commit verification are complete: `wave14-postcommit-checks.json` records all
65 checks passing against commit `d5fed5f`. The broader pattern-review goal remains
active; no push or deployment has occurred.

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
pre-commit run (`wave12-final-checks-precommit.json`). The post-commit snapshot
(`wave12-postcommit-checks.json`) binds all 65 checks, across 390 profiles and 30
catalogs, to code commit `37d3ca6`.

This is a synthetic contract repair, not physical fitment confirmation, production
qualification, calibration evidence, site rendering, or deployment. The Jekyll site
could not be rendered locally because this checkout has no Gemfile or `jekyll`
executable.

### Auto-repair profile source review (wave 13)

All eight auto-repair contracts, required fields, four frozen fixture states per
profile, source notes, page-level code/people boundaries, follow-up limits, and
verification recipes were inspected. Each v1 contract still matches its frozen
whole-contract Jev screen; exact question JSON matches the catalog on all eight
pages. The recorded Jev screening set replays 32/32 (24 design and 8 separately
authored challenge cases), with no provider failures; all 12 collection tests pass.

The earlier whole-contract and option-pair screens retained several low-confidence
overlap judgments; the exact outputs remain preserved. Host review confirmed that
AR01, AR03, AR04, AR05, AR06, and AR08 state how to resolve the specific pairs in
their questions and examples. A new, uncached AR05 boundary case
combined an independent maker brand with an explicitly remanufactured previously
used core. Jev selected `remanufactured` at confidence 1.0, matching the host-frozen
expectation; the expected label was not sent. The request/response and both verified
hashes are retained in `wave13-auto-repair-review.json`. This single development
check is not independent labeling or qualification. No source-confirmed defect was
found, so no contract or fixture was changed; low-confidence signals remain visible.

The source-support receipts refer to pages checked September 23 and were not
live-refreshed in this wave. Their sources motivate the designs and do not establish
Jev performance or current regulatory advice. No real repair-order action,
authorization, warranty determination, website rendering, push, or deployment was
performed.

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
