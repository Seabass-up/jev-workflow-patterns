# Lessons learned

## 2026-09-22 — Choice confidence depends on option count

- **Component:** Kernel skill 2.3.0, CI receipt checks, and the introduction review in `discovery/introduction-review/`.
- **Observation:** Stored jev-1.13.0 Choice confidence follows `(n × top probability − 1) / (n − 1)` within 0.020 across all 447 preserved answers (2–6 options). The confidence page presents this only as a three-option approximation. Score confidence does not follow it; an even split between extreme levels had confidence 0.
- **Consequence:** 53 Iteration 1–2 patterns share a 0.8 floor across 2–6 options, so the floor demands top probabilities from 0.833 to 0.90. Adding a no-match option raises confidence at the same top probability. Historical contracts, thresholds, and receipts were left unchanged.
- **Repair:** Added `check_confidence.py` with eight tests. It checks stored Choice confidence against probabilities and converts thresholds between option counts. Added threshold guidance to the authoring module and a receipt check plus returned-model-version drift trigger to the evaluation module. CI runs the checker over every preserved receipt and replays the discovery measurements.
- **Verification:** 17 kernel helper tests pass; the checker reports 0 failures over 456 Choice answers, including 9 from a fresh 18-question duplicate screen (request digest `25754fc54d748f8ef0f810b31a2f4bc74648e1a7f5d0335bc9e0cda5236c8d50`, 6,383 input tokens, 762 ms). Measurements replay from 25 hash-pinned inputs.
- **Review correction:** PR review found that the latency replay merged deliberate repeat calls sharing a request digest (481 calls, not 473), that the exact-after-rounding count used the wrong test (351 answers are within 0.005, not 267), and that the checker skipped incomplete Choice answers. Latency now keys on digest plus observation time, the rounding statistic tests the 0.005 interval, incomplete answers fail the check, candidate evidence strings get the privacy tripwires, and sources.json records old and new digests for the ten Iteration 4 pages.
- **Limits:** The formula is an observed approximation on one model version, not the provider's definition; 16 of 447 differences exceed what two-decimal rounding of both stored values can explain. Consistency is not correctness. The nine candidates are unscreened designs, and the duplicate screen compared only reviewer-chosen shortlists. A later kernel review found the screen's overlap Score asked two hops and lacked an insufficient-description outcome.
- **Prevention:** Store each confidence threshold with the option set it was tuned on, and recheck the relationship after any model or API change.

## 2026-09-22 — Portable Jev Question Kernel v2

- **Symptom:** The shared skill indexed only Iteration 3 and referenced a file outside its installable folder. It could not carry its core guide when installed alone.
- **Cause:** The catalog skill was packaged around the repository layout and a single historical iteration.
- **Repair:** Kept the existing skill name and added local authoring, evidence/provenance, evaluation/drift, and domain references covering all four catalogs. Added separate contract/fixture examples and a standard-library structural checker. Repeated identical calls are explicitly allowed for bounded repeatability audits; ordinary drill-down retains its evidence dependency rule.
- **Verification scope:** The helper tests version binding, expectation coverage, invalid intervals, required state, candidate labels, and transport construction. Passing structural checks does not establish semantic quality or performance. The historical research fixtures and four-cycle completion state are unchanged.
- **Local results:** Nine helper tests and the example structural check passed, including from a copied standalone skill folder. Skill Creator validation passed using an isolated uv environment with PyYAML because the existing interpreters lacked that validator dependency. The helper itself requires only Python's standard library. GitHub CI now runs the kernel checks and verifies the rendered kernel/home links alongside the 136 iteration pages.
- **Jev consultation:** A two-question design check returned coherent (confidence 0.97) and resolved repeat-audit exception (1.0), model jev-1.13.0, request digest `1cdab42a2e606ec00b0ab17fcd08efa9aa03f3363d3773c881f949b420e8f494`; 605 input/90 output tokens and 430.191 ms. This was advisory design review, not a live test of the new example contract.
- **Prevention:** Package required guidance inside the skill and distinguish structural validation, semantic evaluation, and installed/runtime status.

## 2026-09-23 — Bug-hunting screen preserves uncertainty and service failures

- **Component:** New BH01–BH48 question profiles and their replay/evidence-status helper.
- **Observed:** Two initial calls returned HTTP 529; BH41-2 returned insufficient at 0.35 confidence against an author expectation of counterevidence. The provider's internal causes are unknown.
- **Handling, not a provider repair:** Retained all original results, made one bounded recovery attempt per service error, and kept BH41 provisional without changing its label or question. Both service recoveries succeeded; this does not establish a permanent availability fix.
- **Verification:** 146 screening attempts yielded 144 successful responses; 143/144 selected labels match. All 144 successful request digests replay. Sixteen offline evaluator/status-mapping tests pass; the 48 proposed reproduction recipes were not executed.
- **Prevention and limits:** Separate service failure, missing evidence, model disagreement and observed runtime behavior. Low-confidence leads remain candidates; counterevidence is not bug-free and stale evidence cannot promote a finding. See [the complete evaluation](../bug-hunting/evaluation.md).

## 2026-09-22 — Email missing-input precedence and confidence validation

- **Component:** Email profiles EM07/EM08 and the email receipt evaluator.
- **Symptom:** Initial screening matched 34/36. Empty evidence selected no_document_claim (EM07) and omitted (EM08) rather than unknown. The first evaluator also rejected valid receipts because it equated confidence with the chosen category probability.
- **Confirmed cause/boundary:** The two question contracts did not explicitly prioritize missing input over negative categories. The model's internal cause is unknown. The evaluator assumption contradicted TypeSafe's documented confidence-as-distribution-summary contract.
- **Repair:** Versioned EM07/EM08 to v2 with explicit missing-input precedence, preserving original state, labels, contracts and receipts. Validate confidence independently from category probability. Recommend deterministic required-field preflight before operational inference.
- **Verification:** Six targeted live reruns matched 6/6; current selection matches 36/36. The evaluator verifies 42 request digests and preserves both initial misses. Thirteen offline tests and Skill Creator validation pass; the original low-confidence miss is explicitly accepted as a valid but incorrect response in a regression test. See [email evaluation](../email/evaluation.md).
- **Prevention and limits:** Freeze expectations outside provider inputs; preserve misses and version repairs. Do not infer source completeness from a negative label or equate different statistics. These are synthetic design checks, not held-out accuracy, mailbox integration, or delivery verification. Public deployment is checked separately.

## 2026-09-22 — Iteration 4 literal precedence and numeric-boundary repairs

- **Component:** Iteration 4 H37 citation controller and H38 feature-evaluation controller.
- **Symptom:** The frozen initial screen matched 58/60 fixtures. H37 selected `contradicts` when code had already established that the claimed quote was missing; H38 selected `insufficient` when asked to infer that a lower RMSE was an improvement.
- **Confirmed cause:** H37 did not make the code-owned missing-quote condition a priority branch. H38 asked Jev to perform a numeric comparison, contrary to the documented numeric-boundary rule. Neither miss involved private data or an operational action.
- **Repair:** Versioned H37 and H38 to contract version 2. H37 now selects `quote_missing` first whenever deterministic exact lookup reports a missing quote. H38 now asks only whether revisions, held-out split, metric, and validity are bound; deterministic code calculates metric direction and difference.
- **Verification:** The initial 60 raw request digests remain preserved. Four targeted V2 calls (both H37 and H38 fixtures) matched 4/4; final selection matches 60/60 current fixtures and 60/60 current question checks. The offline evaluator and six pure tests pass.
- **Published verification:** [Actions run 35732787172](https://github.com/Seabass-up/jev-workflow-patterns/actions/runs/35732787172) passed all 66 Iteration 1–4 tests, Jekyll build, and 136 rendered iteration-page/link checks for source commit `9184e6201ac0ab5391d5b92197bcff0130e57ca9`. All 39 scoped public endpoints returned HTTP 200; the served Iteration 4 catalog and summary SHA-256 values match the local artifacts, and the served final-acceptance receipt contains 60 receipts. [Publication receipt](../iterations/publications/04.json). GitHub's Ubuntu 26 migration notice is a future runner-image notice, not a present failure. These checks do not claim visual acceptance, production accuracy, calibration, security, legal compliance, novelty, or operational integration.
- **Prevention:** State priority branches literally in the question, and move arithmetic/metric interpretation into code before the semantic call.

## 2026-09-22 — Iteration 4 generated-page and negative-schema test integrity

- **Component:** Iteration 4 page emitter and evaluator test helper.
- **Symptom:** The first generated pattern pages had YAML front matter indented by four spaces, so Jekyll would not recognize it. Separately, the test helper attempted to round `NaN` before the validator could exercise its malformed-score failure path.
- **Confirmed cause:** Dynamic Markdown fragments defeated `dedent`'s shared margin. The helper constructed a synthetic score from the invalid value rather than mutating the final typed response.
- **Repair:** Normalized exactly one template margin after interpolation, regenerated all 35 Jekyll pages, and changed the negative test to build a valid response then assign `NaN` directly to its score.
- **Verification:** Ruby parsed front matter for all 35 Jekyll pages; `git diff --check`, receipt replay, and the Iteration 4 six-test suite pass.
- **Prevention:** Parse generated front matter before screening or staging, and mutate the exact response field under a negative-schema test rather than relying on a convenience helper's value transformation.

## 2026-09-22 — Iteration 3 standalone evaluator test import path

- **Component:** Iteration 3 synthetic receipt tests.
- **Symptom:** The standalone unittest module invocation could not import the colocated evaluate.py, even though the evaluator itself passed and GitHub discovery would place the iteration directory on the module path.
- **Confirmed cause:** The test module relied on unittest discovery's working-directory/import behavior rather than declaring its local module path.
- **Repair:** Added the test file's own directory to sys.path before importing the local evaluator. No provider receipt, fixture, or question contract changed.
- **Verification:** The evaluator replayed 67 request-digest bindings and selected 61/61 current fixtures before the repair; the standalone command and discovery command are rerun after this entry.
- **Published verification:** [Actions run 35728767306](https://github.com/Seabass-up/jev-workflow-patterns/actions/runs/35728767306) passed the Iteration 1–3 suites, Jekyll build, and 102 rendered iteration-page/link checks for source commit `c56955f50f3b769a0fd08d23e953856ebe2da66b`. All 38 scoped public Iteration 3 endpoints returned HTTP 200, the served catalog SHA-256 matches the local artifact, and the shared public skill was reachable as raw GitHub content. The Mac lacked a local Jekyll/Gemfile path, so the successful exact-current Actions run is the rendered-site check. GitHub's Ubuntu 26 migration notice is a future runner-image notice, not a present failure. [Publication receipt](../iterations/publications/03.json). These checks do not claim visual acceptance, production accuracy, calibration, or operational integration.
- **Prevention:** Iteration test modules should establish their colocated evaluator import path explicitly so direct and discovery invocation exercise the same code.
- **Follow-up formatting repair:** Staging's whitespace check found one extra blank line at the end of every generated Iteration 3 pattern page. The page emitter appended both a terminal content newline and a terminal patch line. Removed the redundant lines with a scoped patch, then refreshed the iteration checksum manifest and reran the whitespace check. Future generated-page patches should inspect the final two lines before staging.

## 2026-09-22 — Iteration 2 contract-version and negative-schema test integrity

- **Component:** Iteration 2 catalog generation and Iteration 2 test evaluator.
- **Symptom:** A broad text patch briefly marked three untouched contracts as version 2 because their prior-pattern anchors overlapped with the intended targets. Separately, the invalid-probability test appeared to cover None, but the synthetic-response helper replaced None with its default valid Noul value.
- **Confirmed cause:** The first version update used insufficiently specific textual context; the test helper deliberately used None as its sentinel for use-default, so passing None did not reach the validator. Neither issue affected a provider call or production data.
- **Repair:** Restored E12/L10/L12 to version 1 and assigned version 2 only to B08/E13/L11/H11/H19; L09 subsequently moved to version 3 after its own documented refinement. Content review later corrected H19's stale message wording to its named proposed_action field and moved H19 to version 3 with four fresh synthetic receipts. Updated the negative-schema test to construct a valid response and then assign None directly to the Noul field.
- **Verification:** The Iteration 2 unittest discovery command passed 20 tests; the Iteration 2 evaluator reproduced 168 request-digest bindings and selected 134/134 current fixtures with 147/147 current question checks. Publication/deployment verification remains pending at this entry.
- **Prevention:** Version every altered contract with pattern-specific context, then assert the complete changed-version set before a live rerun. In negative tests, mutate the final value under test rather than using a helper parameter whose sentinel behavior can bypass the invalid case.
- **Published verification:** [Actions run 35724928016](https://github.com/Seabass-up/jev-workflow-patterns/actions/runs/35724928016) passed both iteration suites, Jekyll build, and 68 rendered iteration-page/link checks for source commit 86735a60f6364e19be29c90507ee5b46728a4820. All 38 checked public Iteration 2 URLs returned HTTP 200; the served catalog SHA-256 matches the local artifact, and H19 is served at contract version 3. [Publication receipt](../iterations/publications/02.json). These checks do not claim visual acceptance or production performance.

## 2026-09-22 — Iteration 1 question contracts and guarded controllers

- **Symptom:** Initial core screening matched 76/81 fixtures. Courtesy/no-action messages overlapped with clarification; three explicit access arrangements fell below the declared yes range. A vague editor target also disagreed with its author-assigned label. Harness screening matched 38/40; H01 assigned high probability to invented meanings of “Do it.”
- **Confirmed cause/boundary:** B01's written criteria overlapped. B02's wording suggested a personal name requirement and left cross-dimension independence unclear; the model's internal cause is unknown. L05's fixture target was genuinely underspecified. H01 demonstrates that plausibility does not establish an actual task target.
- **Repair:** Versioned B01/B02 questions, preserving initial contracts, labels and failures. Added caller-owned target binding and exact authorized read/argument checks to the H01 demonstration controller; H01 remains held for grounding redesign. Preserved L05/H09 disputed labels instead of silently relabeling them.
- **Verification:** 15 targeted live checks matched (8 regression + 7 new diagnostic cases). 136/136 raw request hashes reproduce from frozen state/questions. 31 offline tests passed, including the actual H01 high-probability failure being blocked with an unbound target. The first offline test's mistaken all-branches-labeled assumption was corrected to allow only explicitly unused E01 impact scores.
- **Prevention:** Separate no request from unresolved intent, separate evidence dimensions, freeze expected labels, and never treat model plausibility/confidence as grounding or authority. Production integration and domain qualification remain unperformed. See [the full evaluation](../iterations/01/evaluation.md).
- **Published verification:** [Actions run 35720398125](https://github.com/Seabass-up/jev-workflow-patterns/actions/runs/35720398125) passed the same 31 tests, 136 request bindings and 34 built-page/link checks for source commit `4ee6ca204b66b42783166dcd1680717922459aa6`. All 38 checked public URLs returned HTTP 200, including the 30 new pattern pages and the three earlier pages; the served catalog's SHA-256 matches the local artifact. [Publication receipt](../iterations/publications/01.json). These checks do not claim visual acceptance.

## 2026-09-21 — GitHub Pages workflow runtime compatibility

- **Component:** `.github/workflows/pages.yml`.
- **Symptom:** The first successful Pages deployment carried Node.js 20 deprecation warnings even though its build and deploy jobs passed.
- **Confirmed cause:** The workflow used older major releases of the checkout, configure-pages, upload-pages-artifact, and deploy-pages actions. The composite upload action also bundled an older Node 20 upload-artifact runtime.
- **Repair:** Updated to `actions/checkout@v7`, `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, and `actions/deploy-pages@v5`. Kept deployment restricted to the `main` branch and kept build/deploy permissions scoped to their jobs.
- **Verification:** GitHub Actions run [35657662378](https://github.com/Seabass-up/jev-workflow-patterns/actions/runs/35657662378) completed both build and deploy successfully for commit `e89ec7e82906b3bc077c339040f7f3c9667b280b`. The Node.js 20 warnings disappeared. The index and all three pattern URLs, plus all three raw skill files, returned HTTP 200. GitHub still reports that `ubuntu-latest` is scheduled to move to Ubuntu 26 on October 19, 2026; this is a future runner-image notice, not a current build failure.
- **Prevention:** When a successful workflow emits runtime warnings, inspect both direct actions and composite-action dependencies, update to supported majors, then verify a real build, deployment, and served output. Do not suppress an obsolete runtime warning as a substitute for upgrading.
