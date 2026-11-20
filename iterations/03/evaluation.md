---
layout: default
title: "Iteration 3 Evaluation"
description: "Preserved synthetic Jev receipts, question revisions, fixture correction, and offline integrity checks."
permalink: /iterations/03/evaluation/
kicker: "Evaluation · frozen fixtures and versioned contract repair"
---

[← Iteration 3 catalog]({{ '/iterations/03/' | relative_url }}) · [Question kernel]({{ '/iterations/03/question-kernel/' | relative_url }}) · [Raw summary]({{ '/iterations/03/results/summary.json' | relative_url }}) · [Kernel authoring guide](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/authoring.md)

# Evaluation: preserve the initial miss, repair only the demonstrated boundary

This is a small synthetic contract screen. It asks whether deliberately clear,
synthetic states produce the intended typed answer under the exact question contract.
It does not measure production accuracy, calibration, security, legal compliance,
real-world authority, or global novelty.

## Result timeline

| Stage | Requests | Fixture matches | Question checks | What happened |
| --- | ---: | ---: | ---: | --- |
| Initial frozen v1 screen | 61 | 58 / 61 | 81 / 84 | Three semantic/fixture boundaries missed; all raw receipts remain public. |
| Targeted refinement | 6 | 6 / 6 | 17 / 17 | E16 and L14 were versioned; one H24 fixture was clarified and rerun. |
| Original selected-contract checkpoint | 61 | 61 / 61 | 84 / 84 | Selection before the later local review revisions below. |
| L17/L18/H28 v2 review | 18 | 17 / 18 | 17 / 18 | One L17 incomplete-description case missed; the original v2 request and expected label are preserved. |
| Bounded L17 v3 refinement | 6 | 6 / 6 | 6 / 6 | Same six L17 states and expectations; one uncached refinement, no relabeling. |
| Current selected synthetic contracts | 73 | 73 / 73 | 98 / 98 | L17 v3, L18/H28 v2, and the previously selected fixtures. |

The 67 live synthetic calls used 33,989 billed input tokens, 4,281 output tokens, and
an estimated provider cost of $0.001427538. Those are observed historical receipts, not
a price quote or a claim about a production workload.

## H24 availability safety repair — 2026-09-26

The v1 baseline returned burden Score 0.04/confidence 0.94 on an explicitly unstated
burden and proposed computing the weighted score. The consumer now requires a separate
`burden_available` Noul at the provisional 0.8 threshold; it ignores the burden Score
when availability is low and preserves the named-veto path first. Missing required
top-level state still fails closed before semantic consumption.

Two original regression states and their three original Score/veto intervals are
preserved; the new availability intervals are additional expectations, not relabels.
Five development cases exercise absent, unrelated, conflicting, negated-resource and
veto-plus-absent burden. The v2 screen matched 4/7 cases (25/28 intervals). One bounded
v3 refinement clarified qualitative availability and independent fit/veto semantics:
6/7 cases and 27/28 intervals match, with every v2 miss preserved and no state,
threshold or expected interval changed. The negated-resource case remains at
availability 0.66, so code returns review rather than its frozen calculation proposal.
Do not call this a perfect screen or qualified availability classifier.

## L17, L18 and H28 precedence review — 2026-09-26

The first v2 review covers six unchanged L17/L18/H28 regressions and twelve frozen
development boundaries. L17 returned document_editor with confidence 0.99 when one
offered skill description was explicitly unavailable, despite an expected
insufficient-evidence label. That raw miss is preserved in
[pattern-review-v2.json]({{ '/iterations/03/results/pattern-review-v2.json' | relative_url }}).
The confirmed contract gap was that v2 did not say an undescribed candidate prevents
choosing among the shortlist. L17 v3 adds that explicit rule; one uncached re-screen of
the exact same six states matched 6/6, including the incomplete-description case.
No states or expected labels changed. The consumer proposes review/expansion for that
answer rather than loading a skill.

L18 v2 distinguishes requested work shape from missing answer values: chained work,
external retrieval and exact calculation take precedence over a bounded comparison or
single-item judgment. H28 v2 handles incomplete evidence first, then stale/unverifiable
state, explicit over-budget evidence, dependencies, and finally batchability. Jev does
not calculate limits; the controller proposes a code-owned snapshot/budget check before
any batching.

The v2 CT08-style screen covered 31 option pairs (all selected disjoint/precedence
resolved; seven had confidence below 0.8). The L17 v3 check covered its 15 pairs (all
selected disjoint; six below 0.8). These low-confidence judgments remain visible and
advisory; they were not retried until they passed. The [pair-review receipts]({{ '/iterations/03/results/pattern-review-pair-review-v2.json' | relative_url }})
and [L17 v3 pair review]({{ '/iterations/03/results/pattern-review-pair-review-v3.json' | relative_url }})
retain the exact requests and responses.

The side-effect-free controller replay passes for all 18 v2 cases and all six L17 v3
cases. The selected current set is 73/73 fixtures and 98/98 question checks. This does
not establish representative accuracy, calibration, global shortlist completeness, or
production qualification. See the [v1 archive]({{ '/iterations/03/results/pattern-review-pre-review-contracts.json' | relative_url }}),
[v2 frozen revision cases]({{ '/iterations/03/results/pattern-review-revision-v2.json' | relative_url }}),
and [v3 L17 cases]({{ '/iterations/03/results/l17-v3-revision-fixtures.json' | relative_url }}).

The preserved pre-review replay binds 105 fixture-screen receipts, five prior
option-pair requests and the v1 baseline probe. That earlier selection contained
61/61 fixtures and 86/86 checkpoint question checks (including two additional
availability questions), while separately reporting the open development miss and
6/7 consumer matches. The later L17/L18/H28 review and current 73-fixture selection
are reported above; no action or deployment is performed.

## Initial misses and repairs

| Pattern / fixture | Initial observation | Repair and evidence boundary |
| --- | --- | --- |
| E16 configuration conflict | The v1 wording returned insufficient when the state gave incompatible values and said both must control without a resolution. | Contract v2 explicitly classifies that stated condition as explicit_conflict; both E16 fixtures were rerun. |
| L14 neutral question | A neutral “does the policy permit” query received a high premise-conflict Noul despite no affirmative premise. | Contract v2 explicitly says a neutral question does not assert permission/truth/availability; all three L14 fixtures were rerun. |
| H24 limited-fit veto fixture | A “limited fit” synthetic state received score 0.63, just outside its author-assigned 0–0.6 bin. | The fixture now states no fit, which is the intended low-score boundary. The original receipt remains intact and the clarified state was rerun under the unchanged H24 v1 contract. |

Making a final synthetic regression set perfect after inspecting misses does not establish
generalization. Production use needs independently adjudicated, representative data,
predeclared consequence policy, and calibration against the target workflow.

## Receipt integrity

### Local review revision — 2026-09-26

B19/E18/H22/H26/H27 are now v2 with explicit missing-evidence and overlapping-label
precedence. The five original v1 contracts and ten original fixtures are preserved
and verified against Git source `f600346`. Ten unchanged regression cases plus fourteen
frozen development boundaries matched 24/24 in one uncached screen. All thirty CT08
option-pair judgments selected disjoint/precedence-resolved; some were low-confidence
and remain advisory rather than qualification. The evaluator binds all 91 fixture
receipts plus five pair-review requests, rejects changed originals or unbound revised
cases, and keeps the final selection at 61/61 fixtures and 84/84 question checks.
The historical cost above describes only the original 67 calls, not this added screen.
No production behavior, authority, merge, retry permission or deployment is established.

The offline evaluator verifies:

- response shapes match the exact Choice, Score, or Noul question contract;
- every request digest binds model, synthetic state, and question JSON;
- expected labels never enter submitted state;
- stored observed values and match flags recompute from raw typed output;
- every final fixture is linked to the current contract version and exact current state;
- pure controllers return review, calculation, expansion, or verification proposals only.

Run locally:

~~~text
python3 iterations/03/evaluate.py
python3 -m unittest discover -s iterations/03 -p 'test_*.py' -v
~~~

[Initial raw receipts]({{ '/iterations/03/results/initial-screen.json' | relative_url }}) · [Refinement raw receipts]({{ '/iterations/03/results/refinement-screen.json' | relative_url }}) · [Final receipt selection]({{ '/iterations/03/results/final-acceptance.json' | relative_url }}) · [Offline evaluator]({{ '/iterations/03/evaluate.py' | relative_url }})
## 2026-09-26 local controller evidence preflight

The advisory `plan` API now requires `state=...` as a keyword argument. Omission,
missing top-level required fields, nulls, whitespace-only strings and empty arrays
or objects return `review / missing_required_state` before model answers are used.
This repairs the previous API's inability to inspect required evidence. Iteration 1's
mandatory policy-alert override remains independent of model/evidence availability.

This is a structural presence check only: nonempty records may still be false,
stale, contradictory or incomplete internally. It does not authenticate a response,
validate nested schemas, or grant authority. Providers should also be called only
after preflight. Branch tests use explicitly supplied synthetic evidence, not proof
of real-world source grounding. Cross-iteration negative tests exercise all 120
profiles in `scripts/test_iteration_state_preflight.py`; historical question
contracts, fixtures and provider receipts are unchanged. Local repair, not deployment.
