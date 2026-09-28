# Audit-pending research contracts — checkpoint 2026-09-28

Kernel **2.9.0** adds 19 exact question contracts and one separately counted
composition from Research Jev Patterns at
`cb69774a6a9669ff412511094bebb387b382d008`. Each working admission is
`ACCEPTED_RESEARCH` with a **pending project-wide audit**. The kernel exposes them
only as `AUDIT_PENDING` read-only research choices. The broader research goal is
paused and incomplete. Importing these files does not resume it.

The [manifest](../assets/research-working/manifest.json) pins all bundled bytes
and 222 source Git objects, including consumers and research receipts. The
[unaltered working admission list](../assets/research-working/admissions.json)
retains each result, attribution and limitation. Frozen contract files still carry
their original pre-screen status (sometimes `CANDIDATE` or
`CANDIDATE_UNTESTED`); later acceptance comes from the separate receipt-derived
admissions, never an edit to those frozen files. JP-017's original contract title
also differs from its later listing title; both are preserved.

The ten [v0.2.0 research-edition adapters](research-edition.md) remain byte-identical
at their older checkpoint. These 19 additions and AP-C01 are separate from the
390-profile catalog. Historical requalifications do not establish new semantic
operations, novelty or cross-domain applicability.

## Select the narrow question

| Exact selector | Question to adapt | Consumer boundary |
| --- | --- | --- |
| [JP-001@4](../assets/research-working/contracts/JP-001.v4.json) | Does the supplied target establish one documented prerequisite? | Check actual target facts and exact predicates before any method decision. |
| [JP-017@1](../assets/research-working/contracts/JP-017.v1.json) | Do two records establish the same named test condition? | Only a matched condition can reach a code-owned numeric preview; verify IDs, units and tolerance separately. |
| [JP-019@1](../assets/research-working/contracts/JP-019.v1.json) | Is the actor's stated commitment firm, conditional or tentative? | Preserve exact wording; no task creation or real intent/completion claim. |
| [JP-021@2](../assets/research-working/contracts/JP-021.v2.json) | Does this meeting item record a decision, discussion or deferral? | Index the note; do not turn a recorded decision into work completion. |
| [JP-023@2](../assets/research-working/contracts/JP-023.v2.json) | Does a documented capability support one task requirement? | Keep prerequisites and remaining requirements separate; no whole-method fit. |
| [JP-025@1](../assets/research-working/contracts/JP-025.v1.json) | Does the candidate manifest declare a closed or expandable scope? | Code verifies the actual allowed universe; this answer alone cannot establish no-match. |
| [JP-026@1](../assets/research-working/contracts/JP-026.v1.json) | Does the adaptation hypothesis make a measurable prediction? | Name a testable quantity; do not claim the adaptation works. |
| [JP-027@1](../assets/research-working/contracts/JP-027.v1.json) | Does a review comment assert a defect, ask for discussion or state a style preference? | Human blocking markers override the model; no dismissal or merge decision. |
| [JP-028@1](../assets/research-working/contracts/JP-028.v1.json) | Does the described test directly check the changed behavior? | Rank candidates for inspection; no permission to skip tests. |
| [JP-031@1](../assets/research-working/contracts/JP-031.v1.json) | What kind of failure-origin evidence is stated? | Route investigation; retain mixed evidence and do not infer root cause. |
| [JP-033@1](../assets/research-working/contracts/JP-033.v1.json) | What stated difference separates two reviews of the same artifact? | Preview a request for common scope, facts or criterion priority; do not resolve truth or send a request. |
| [JP-035@1](../assets/research-working/contracts/JP-035.v1.json) | Which one of three supplied spans directly answers the question? | Copy the verified exact span, or preview a bounded search expansion. |
| [JP-036@1](../assets/research-working/contracts/JP-036.v1.json) | Do adjacent rubric levels state a checkable distinction? | Flag wording; exact numeric thresholds go to code, and no grade is assigned. |
| [JP-038@1](../assets/research-working/contracts/JP-038.v1.json) | Does a written runbook step check the named prerequisite before acting? | Preview an omission/order/override warning; do not assert the live condition holds. |
| [JP-039@1](../assets/research-working/contracts/JP-039.v1.json) | Does the proposed change address the demonstrated causal operation? | Ask for code and regression verification; an aligned proposal is not a verified fix. |
| [JP-040@1](../assets/research-working/contracts/JP-040.v1.json) | Which described source could answer one named evidence gap? | Preview a source request; actual retrieval and permissions remain host-owned. |
| [JP-042@1](../assets/research-working/contracts/JP-042.v1.json) | Does the proposed metric measure the full stated outcome? | Flag proxy gaps or opposing incentives; measurement and policy stay with the host. |
| [JP-045@1](../assets/research-working/contracts/JP-045.v1.json) | Where does this written preprocessing plan fit its parameters? | Inspect fit calls and sample lineage separately; no executed leakage verdict. |
| [JP-046@1](../assets/research-working/contracts/JP-046.v1.json) | Do written before/after results differ for one scenario and observer? | Preserve the scenario and unverified-evidence banner; no executable equivalence claim. |

## Required state

These are field names, not permission or truth checks. Read the complete selected
contract for the expected nested shape, precedence, sources and consumer behavior.
For example, JP-025 has a structured selection request and candidate manifest;
JP-035 requires three source-bound spans; JP-040 has exactly three catalog entries
with distinct source IDs, revisions and descriptions.

| Contract | Required state fields |
| --- | --- |
| JP-001@4 | `procedure`, `documented_prerequisite`, `target_evidence` |
| JP-017@1 | `condition_dimension`, `comparison_rule`, `record_a_condition_text`, `record_b_condition_text` |
| JP-019@1 | `actor`, `action`, `current_body` |
| JP-021@2 | `note_item` |
| JP-023@2 | `task_requirement`, `documented_capability` |
| JP-025@1 | `selection_request`, `candidate_manifest` |
| JP-026@1 | `hypothesis_statement` |
| JP-027@1 | `review_comment`, `attached_hunk` |
| JP-028@1 | `changed_behavior`, `test_description` |
| JP-031@1 | `failure_evidence` |
| JP-033@1 | `shared_context`, `review_a`, `review_b` |
| JP-035@1 | `question`, `candidates.s1`, `candidates.s2`, `candidates.s3` |
| JP-036@1 | `criterion_name`, `lower_level_description`, `higher_level_description` |
| JP-038@1 | `runbook_step`, `precondition` |
| JP-039@1 | `reproduced_cause`, `proposed_change` |
| JP-040@1 | `evidence_gap`, `source_catalog` |
| JP-042@1 | `user_goal`, `success_metric`, `stated_consequence` |
| JP-045@1 | `evaluation_context`, `preprocessing_operation`, `plan_text`, `source_note` |
| JP-046@1 | `declared_refactor`, `scenario`, `observer_boundary`, `before_behavior`, `after_behavior` |

Source identity, revision, digest, membership and permissions are host-owned
preflight checks. Do not rely on a model to authenticate them. Keep missing and
conflicting evidence visible. Validate the exact request/response binding, answer
shape and selected contract's probability floor before considering any preview.
JP-027 and JP-028 use 0.80 in this source screen; the other imported questions use
0.85. Those floors are research policies, not measured correctness probabilities.
Retain original thresholds in replay; a new policy needs separate evaluation.

The source consumers differ and are **not bundled as production adapters**.
Several depend on frozen fixture registries and source archives. JP-017's
synthetic adapter in particular lacks real record ID/revision/hash enforcement;
a real application must implement and test that binding before any numeric
preview. The import checker cannot supply it. Source preflight and consumer
paths are recorded per contract in the manifest.

## Load deliberately; never silently upgrade a held version

Run from the complete skill folder with Python 3:

```sh
python3 scripts/check_research_working_import.py
python3 scripts/check_research_working_import.py --show JP-001@4 --allow-audit-pending
python3 scripts/check_research_working_import.py --show-composition AP-C01@1 --allow-audit-pending
python3 scripts/check_research_working_import.py --source-root "/path/to/Research Jev Patterns"
python3 -m unittest discover -s scripts -p 'test_research_working_import.py'
```

The default command prints inventory and integrity metadata. Displaying a contract
requires both an exact `ID@version` and the audit-pending acknowledgement.
`JP-001`, `JP-001@2`, `JP-001@3`, unknown versions and held candidates are
rejected; no fallback to another version occurs. The acknowledgement records a
caller's choice of research evidence limits, not a grant of user/action authority.
The output envelope carries status, source commit, admission evidence and consumer
boundary together with the unchanged contract.

The source check reads **Git blobs at the pinned commit**, not mutable working
files or the current source HEAD. It runs no research builder, provider call or
consumer. A changed manifest, bundled contract, receipt summary, extra file or
symlink is rejected. The manifest digest is anchored in the checked-in loader;
hashes detect local drift under a trusted copy, not authenticity or malicious
changes to the loader itself.

For code reuse, add the skill's `scripts` directory to the caller's import path:

```python
from check_research_working_import import load_contract, question_for

envelope = load_contract("JP-001@4", allow_audit_pending=True)
contract = envelope["contract"]
request = {
    "state": {
        "procedure": "The exact documented procedure and mode",
        "documented_prerequisite": "The exact one prerequisite and input scope",
        "target_evidence": "Source-bound target observations, including gaps/conflicts",
    },
    "questions": {"prerequisite": question_for(contract)},
}
# Construction only. Bind and validate the real source packet before dispatch.
# Keep the envelope and request digest outside Jev as the consumer's evidence.
```

Only the applicable question and evidence go to Jev. Admission records, expected
labels and gate outcomes never enter the provider's question state. Each dependent
step needs newly constructed state; a shared request evaluates questions independently.
Follow the installed bridge's current limits and approved provider path.

## Algorithm applicability and discovery sequence

1. **Evidence gap:** JP-040 can preview which described source to request. The host
   decides access and retrieves it.
2. **Retrieved evidence:** JP-035 can select a uniquely answer-bearing supplied span.
   Code copies exact bytes and retains source provenance.
3. **Candidate scope:** JP-025 describes manifest coverage. Code verifies the named
   universe and every candidate ID before closing it.
4. **Capability and prerequisite:** JP-023 checks one requested capability against
   documentation. JP-001@4 checks one documented prerequisite against target
   descriptions. Keep a host-owned ledger of remaining requirements, modes and
   unresolved facts; neither check establishes full suitability.
5. **Adaptation/evaluation:** JP-026 screens measurable prediction wording, JP-017
   screens one test-condition comparison, JP-042 screens goal/metric alignment and
   JP-045 screens the stated preprocessing fit source. Actual data, exact numeric
   checks, experimental design, implementation and domain review stay external.

Use only needed steps. Reuse satisfactory judgments when their evidence and
versions still apply. This is workflow guidance assembled from the imported
contracts, not a newly screened end-to-end research result.

### JP-001@4's repaired distinction

Missing verification or a missing completion record is `unknown`. An expressly
incompatible input state can be `condition_not_met`, even when another required
input is unreported. Unresolved contradictory reports about that same target fact
are `unknown`. `condition_met` requires the entire stated prerequisite across
all named inputs for the exact mode. Per-group order alone cannot establish global
order. Preserve the unverified-target banner and require actual target checks.

Version 4's saved screen reports 12/12 development and 6/6 challenge labels, with
eight and four correct read-only previews and zero wrong nonreview routes.
Claude's missing-versus-false ambiguity was repaired before the freeze. Grok's
review timed out without a verdict; no Abacus credits were used in that wave.
These are synthetic target descriptions plus pinned official documentation.
Historical JP-001@2/@3 holds remain referenced; the old edition's JP-001@1
exclusion is unchanged.

### AP-C01@1 is a composition

[AP-C01](../assets/research-working/compositions/AP-C01.v1.json) combines
**JP-025@1 + JP-023@2**, then deterministic aggregation. Only a code-verified closed
candidate universe and a source-bound, sufficiently probable contradiction to a
hard requirement for **every candidate** can produce a scoped no-match preview.
Missing evidence, weak answers or expandable scope cannot eliminate a candidate.

The [separate composition admission note](../assets/research-working/compositions.md)
records its eight-case same-author pilot and 22 adversarial consumer tests. The
pilot is limited to the eight documented `scipy.optimize.root_scalar(method)`
options at the pinned source version; other APIs and global algorithm search are
outside its universe. No challenge split or model-over-deterministic-baseline gain
was established. No algorithm is selected or executed. AP-C01 is not a twentieth
new question primitive.

## Research status and remaining work

The [saved inventory](../assets/research-working/inventory.json) contains 29
research-accepted IDs (10 prior + 19 working), 17 currently held IDs and 406
accepted-ID pairs. The [saved audit verification](../assets/research-working/audit-verification.json)
reports 154 locally reviewed pairs and **252 unassessed contacts** (224 inherited
plus 28 new JP-001 contacts). Local review is short of the independent final
duplicate/attribution audit. All 19 additions require project-wide reconciliation
before a new audited master-list edition.

Specialist/domain validation, independently controlled consumer trials and guarded
live integration remain open. The 155 mapped arXiv routes remain unscreened for
specialist validation. The older release-manifest drift is not resolved here.
The adjacent CA01–CA04 drafts and other held leads are not admitted by this import.

Keep source version, input packet and code-owned checks in any trial record.
Respect each contract's follow-up limit: JP-017 permits zero further calls within
its frozen evaluation; other questions require genuinely new evidence and their
own bounded workflow. Never reword frozen cases to obtain a preferred answer.
