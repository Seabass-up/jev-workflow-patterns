# Research edition: ten source-bound task adapters

Use this module when one of the tasks below fits the supplied evidence and an
application-owned, side-effect-free consumer. Kernel 2.8.0 imports ten contracts
from **Research Jev Patterns**, checkpoint
`48a8b4569a9ce5b17ce1119d63179e84a2990ae6` (2026-09-27), without changing their
bytes, questions, thresholds, or versions. JP-011 uses **v2**; the other nine use v1.
These are attributed research adaptations, not ten newly invented primitives.
They supplement the existing 390-profile catalog; do not inflate its count.

The source's v0.2.0 master list admits them for bounded advisory trials. Each
matched 12/12 development and 6/6 same-author fresh challenge labels. Fresh cases
were frozen before inference, but were **not independently authored**. Independent
model label review is not specialist validation. None is production-qualified.

The checkpoint records a **paused, incomplete** research goal, a pending wider
audit, and twelve older release-manifest mismatches in its committed source tree.
This is an import from that exact checkpoint, not a replay or re-release of the
entire research edition. Later research work does not silently update this bundle.
Loading it neither resumes research nor changes any goal status.

Contents: [task routing](#choose-the-actual-task) ·
[consumer boundaries](#apply-the-contract-without-weakening-its-consumer) ·
[excluded entries](#held-and-working-entries-stay-separate) ·
[JP-002 transfer](#jp-002-public-transfer-useful-evidence-bounded-claims) ·
[coverage](#coverage-is-a-discovery-index) · [local checks](#check-the-installed-copy-locally).

## Choose the actual task

Read the complete linked contract, not just this routing table. The
[manifest](../assets/research-edition/manifest.json) records exact source paths,
SHA-256 hashes, source consumer locations, versions, admission status, and limits.

| Contract | Evidence needed | Bounded answer and consumer |
| --- | --- | --- |
| [JP-002 v1](../assets/research-edition/contracts/JP-002.v1.json) — evidence stage | `record` names the target work item and relevant dated evidence | `planned`, `performed`, `tested`, `accepted`, `unknown`; annotate the record's documented stage, not real-world completion |
| [JP-003 v1](../assets/research-edition/contracts/JP-003.v1.json) — diagnostic observation | `record` contains two hypotheses, both explicit predictions, and the proposed observation | `separates`, `does_not_separate`, `unknown`; annotate information value without running a test |
| [JP-004 v1](../assets/research-edition/contracts/JP-004.v1.json) — negative evidence | `record` supplies the absence claim, scope, observation, coverage and stated detection capability | `absence_supported`, `coverage_insufficient`, `contradicted`, `unknown`; annotate support within the stated scope |
| [JP-005 v1](../assets/research-edition/contracts/JP-005.v1.json) — exact-copy selection | `document`, `field_role`, `candidate_spans`, source revision and document SHA-256 | Select `s1`/`s2`/`s3`, `not_found`, or `unknown`; code copies only an exact validated span |
| [JP-007 v1](../assets/research-edition/contracts/JP-007.v1.json) — entity relation | `entity_type`, `record_a`, `record_b` | `same_entity`, `related_but_distinct`, `different_entities`, `unknown`; annotate the relation, never merge records |
| [JP-008 v1](../assets/research-edition/contracts/JP-008.v1.json) — block role | `block` and functional `context` | `heading`, `list_item`, `body`, `unknown`; produce an escaped local formatting preview |
| [JP-010 v1](../assets/research-edition/contracts/JP-010.v1.json) — change impact | `old_contract`, `new_contract`, and this `consumer`'s stated dependencies | `breaking`, `compatible`, `unknown`; annotate impact for this consumer, not deployment approval |
| [JP-011 v2](../assets/research-edition/contracts/JP-011.v2.json) — benefit preview | `proposal_effect`, code-owned `effort_units` and `blocked_by_host` | Availability Choice plus 0–2 benefit Score; code gates the evidence and computes the provisional preview |
| [JP-012 v1](../assets/research-edition/contracts/JP-012.v1.json) — feedback structure | `feedback_comment` about submitted student work | `concrete_next_step`, `generic_advice`, `asks_a_question`, `evaluation_only`, `unknown`; annotate structure, not correctness or the student's ability |
| [JP-013 v1](../assets/research-edition/contracts/JP-013.v1.json) — study assignment | `methods_excerpt` plus exact `source_record` identity/revision/excerpt/hash | `investigator_randomized`, `investigator_nonrandom`, `observed_or_external`, `unknown`; annotate the reported mechanism, not causality or study quality |

## Apply the contract without weakening its consumer

1. Bind a small, task-authorized evidence packet to exact source IDs, revisions and
   hashes. Keep expected labels, admission metadata and review commentary outside
   provider state. Missing required evidence is a host preflight review outcome;
   it is not a request to infer a default answer.
2. Use the **complete** `request.questions` object. Supply the task's own state;
   the embedded examples are not a caller's evidence. Preserve exclusions and
   precedence. Pin/log `jev-1.13.0` for the historical thresholds; another model,
   wording, candidate set or consumer policy needs versioned reevaluation.
3. Implement and locally test the application's consumer before use. These imports
   bundle contracts and guidance, **not executable research consumers or the full
   fixture/receipt archive**. Source consumer paths and hashes in the manifest are
   provenance, not imports to execute. Follow [qualification](qualification.md)
   for a new side-effect-free adapter and its boundary tests.
4. Code checks the response envelope, exact question/label coverage, model and
   request digest, finite values, probability shape and source binding. `unknown`,
   `not_found`, invalid input/output, service failure, or insufficient probability
   routes to review. The frozen Choice annotation floor is top probability 0.85,
   **not confidence 0.85** and not 85% demonstrated correctness. Preserve a source
   consumer's thresholds when reproducing its results; changed validation is a
   versioned application integration, not a silent historical repair.
5. Return a source-bound read-only annotation or preview. Permissions, identity,
   calculations, safety, sending, merging, publishing and outcome verification stay
   in code and with authorized people. No imported result can authorize an action.

Special consumer boundaries:

- **JP-002:** missing/conflicting target evidence wins before stage ranking.
  Otherwise explicit acceptance outranks tested, performed and planned. A failed
  completed test is still `tested`; passing an acceptance test, receiving a package,
  or planning acceptance does not establish recipient acceptance. For multi-item
  records, bind each preview to the exact target and historical source date.
- **JP-003/004:** require the predictions or coverage evidence; do not supply missing
  scientific assumptions. JP-004 checks unknown first, then explicit detection
  (`contradicted`) before insufficient coverage. Criterion key order is not priority.
- **JP-005:** validate unique candidate IDs, membership, source hash, and exact
  start/end/text agreement before copying. The frozen Python consumer uses zero-based,
  end-exclusive character indexes; define equivalent indexing in another runtime.
  Candidate omission is `not_found`, not permission to invent a new span or value.
- **JP-007/008:** parent/child entities remain related-but-distinct even with distinct
  legal IDs. Preserve block text and escape it before the `h2`, `li`, or `p` preview;
  the label establishes neither whole-document hierarchy nor safe publication.
- **JP-010:** unknown takes precedence for missing/ambiguous/conflicting behavioral
  evidence; otherwise one violated stated dependency is `breaking`.
- **JP-011:** never use Score alone. Availability must be `available` at probability
  >= 0.85. Code requires `blocked_by_host` to be a Boolean and `effort_units` to be a
  nonnegative integer (not a Boolean). A host veto returns review. Validate the 0–2
  Score and its distribution; the frozen consumer also requires its largest bucket
  probability >= 0.85. Its exact preview is
  `round(benefit_score - 0.2 * effort_units, 6)`, **not benefit divided by effort**.
  Zero effort is permitted. The formula is illustrative, not a universal business
  priority or value model. Unknown availability never becomes zero benefit.
- **JP-012:** preserve the precedence concrete next step → generic advice → question
  → evaluation only, after missing-evidence handling. This labels existing feedback;
  it does not generate feedback, assess kindness, or qualify coaching in another domain.
- **JP-013:** require a nonempty methods excerpt and matching `source_record.excerpt`,
  nonempty `source_id`/`source_revision`, and SHA-256 of that exact UTF-8 excerpt.
  Use the repaired consumer-v2 boundary, including empty-content rejection. Random
  sampling, measurement order or analysis order is not random exposure assignment.

JP-010/011/012 retain template Noul threshold keys even though these selected
contracts have no Noul question. Some shared `code_owned_checks` are also broader
than an individual adapter. Preserve frozen bytes; use the relevant source consumer
and the guards above, not those incidental keys, to understand executed behavior.

## Held and working entries stay separate

The v0.2.0 exclusions are **JP-001** (disputed applicability precedence), **JP-006**
(seven useful outputs below an eight-output gate), **JP-009** (four useful outputs
and a fresh interval disagreement), and **JP-014 v2** (11/12 after one clarification;
no fresh challenge). They are not selectable contracts in this bundle.

**JP-017** is recorded separately as source `ACCEPTED_RESEARCH`, with its wider
audit `PENDING`. Its 12/12 development and 8/8 same-author challenge results do not
place it in the frozen admitted ten. Its contract is not imported. Later held
JP-015/016/018 leads also remain outside this edition; four is the v0.2.0 hold count,
not a claim that only four candidates were ever held. Do not retry or promote them
because a kernel lookup cannot supply a suitable admitted contract.

## JP-002 public transfer: useful evidence, bounded claims

The preserved pilot used six historical NASA/DOE/USGS interpretations and six
synthetic controls. One frozen call matched **12/12 labels**, producing **nine
read-only previews, three reviews, five public previews and zero wrong previews**.
Blind Codex/Grok label agreement is recorded. This is development-screen evidence
for existing JP-002, not a new master-list entry or independent domain qualification.

The public subset contained neither explicit recipient acceptance nor unresolved
conflict; those boundaries were synthetic. The code comparator abstained on every
multi-item public record. A target-aware baseline and appropriate specialist review
remain needed; do not claim Jev beats all deterministic alternatives. Preserve the
source dates rather than presenting historical stages as current status.

The additive verifier checked the canonical request digest against the preserved
response, reconstructed the baseline and all gate counts, bound each preview to
its target/source, and checked the pre-inference commit chronology. It did not
rewrite the frozen request, response or expected labels. Four adversarial tests
exercise those replay boundaries. Apply these practices through the
[evaluation module](evaluation.md#research-transfer-lessons).

## Coverage is a discovery index

At this checkpoint: **155 arXiv routes in eight groups; 22 with an individual mixed
transfer screen, 133 without one, zero individually domain-validated**. All 155
remain `UNSCREENED` for specialist/domain validation. The occupation index covers
50 occupations and 211 rated task statements, with 114 Jev route advisories.
A category, job title or route is not a validated pattern. Future work starts from
a concrete agent task, evidence packet and consumer, then checks operation overlap.

## Check the installed copy locally

From the complete skill folder:

```sh
python3 scripts/check_research_import.py
python3 scripts/check_research_import.py --show JP-011
python3 -m unittest discover -s scripts -p 'test_research_import.py'
```

If the original research repository is available, add `--source-root PATH` to
compare every recorded source file with the pinned Git object. This checks the
requested checkpoint even when that repository has newer commits; it does not
rebuild its catalogs, alter its worktree, or make an inference call.

These checks validate import bytes, identities, exclusions and packaging only.
The raw research contracts have several original envelope shapes, so do not pass
all of them straight to `check_contract.py` or `qualify_workflow.py`. Create an
explicit application adapter using those tools' documented schema, preserving
the original contract provenance and separately testing the actual consumer.

To reproduce historical labels or gates, use the original frozen fixtures,
receipts and source consumers in the research repository, not this small bundle.
Hashes are integrity references, not proof of trustworthy authorship or model
accuracy. No local test here completes the research audit or authorizes deployment.
