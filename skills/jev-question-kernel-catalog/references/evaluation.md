# Evaluation, regression, and drift

Use this module for new reusable contracts, observed failures, and changes that
could invalidate prior evidence. Ordinary invocation does not need a fresh benchmark.

## Freeze cases before inference

Store fixture `state` and `expected` as siblings. Build provider inputs from only
fixture state plus frozen contract questions. Review semantic label leakage: a
key-name check cannot catch an answer embedded in prose. Include ordinary cases and
relevant missing evidence, negation, conflicts, candidate omissions, and near-label overlap.

Define expected Choice labels, Noul acceptance intervals, or Score intervals before
testing. Demo thresholds are examples; evaluate thresholds for the task's consequences.
Where review is expected, separately test that consuming code produces that disposition.
The bundled helper checks label/interval forms, not consumer behavior.
For a side-effect-free test of the consuming decision code, use
[qualification.md](qualification.md) and its shadow replay. It does not execute
or verify the eventual external action.

## Preserve replay evidence

For authorized synthetic/public fixtures, retain exact request/response, canonical
serialization convention and request digest, contract version, model identifier,
client settings, timestamp, fixture ID, expectation, errors, and result. Follow
existing retention policy for private material. A digest cannot reconstruct missing data.

Run `scripts/check_confidence.py` over stored receipts. A Choice confidence that
disagrees with its probabilities indicates a transcription error or a changed
provider definition; either suspends threshold evidence until reviewed. The check
establishes internal consistency only, not correctness.

Preserve initial misses alongside refinements. Investigate missing context, ambiguous
labels, question wording, composition, and provider errors without inventing a
model-internal cause. Version meaningful contract changes. Change labels only for
documented labeling errors, preserving the old fixture version. Rerun affected and
relevant regression cases.

## Repeatability and held-out work

Ordinary drill-down changes evidence or candidates. A repeat audit deliberately repeats
the same request within a predeclared sample and cost budget. Disable caching or label
cached samples; cached responses are not fresh replicates. Preserve every sample and
error. Compute agreement, abstention, and threshold crossings in code. Agreement does
not prove correctness; correlated samples are not independent truth evidence.

Refined synthetic fixtures are regression evidence. Estimate performance on new inputs
with a separately held-out, representative labeled set and a simpler baseline. Measure
errors, review rate, cost, latency, and consequential consumer failures. Do not describe
repeatedly tuned fixture results as production accuracy.

## Research-transfer lessons

The [research-edition supplement](research-edition.md) preserves a JP-002
historical-public-record development pilot, not a production qualification. Apply
its replay lessons when checking another saved screen:

- Compare the response's recorded request digest with a fresh canonical digest of
  the exact model, state and complete questions. Hashes detect a mismatch; they do
  not authenticate the source or prove the provider produced the response.
- Recompute baseline outputs, per-case dispositions, every aggregate and the final
  gate from frozen inputs. Do not trust a saved `passed` flag or aggregate alone.
- Bind each emitted preview to its case, exact target, source revision/hash and
  historical date. Validate unique/full case coverage and absence of review previews.
- Keep label accuracy, high-probability outputs, actual consumer previews, and review
  counts separate. A host veto can send a high-probability answer to review.
- Test request substitution, baseline/aggregate tampering and source/preview drift.
  A replay repair should be additive when the original inference packet is frozen;
  keep the original miss or failure and verify the repaired checker locally.
- Count a route once, state which boundaries are actually public versus synthetic,
  and compare with a suitable target-aware code baseline. Same-author fresh cases
  and independent model agreement are not independently authored or specialist labels.

## Drift decision

Compare question semantics/version, model or resolved alias, preprocessing, source
schema, candidate generation, population/language, consumer policy, and evaluation
split. Record changes and decide whether prior evidence still supports the intended use.
Retain the last qualified revision and route uncertain adoption to review. This module
does not automatically retrain, alter thresholds, or promote a contract.

Log the versioned `model` returned with every answer. A floating alias such as
`jev-latest` can move without a client change; when the returned version differs from
the qualified one, hold threshold-gated automation and rerun frozen fixtures before
re-qualifying. Pin the versioned ID where thresholds were tuned against it.

Use H31/H32 repeat audits, H35 canaries, H39 boundary fixtures, and H40 feature drift
through [profiles.md](profiles.md).

Official references: [confidence](https://docs.typesafe.ai/confidence),
[Noul consistency](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook), and
[Choice consistency](https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook).
