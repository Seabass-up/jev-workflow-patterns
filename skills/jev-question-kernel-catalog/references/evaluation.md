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

## Preserve replay evidence

For authorized synthetic/public fixtures, retain exact request/response, canonical
serialization convention and request digest, contract version, model identifier,
client settings, timestamp, fixture ID, expectation, errors, and result. Follow
existing retention policy for private material. A digest cannot reconstruct missing data.

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

## Drift decision

Compare question semantics/version, model or resolved alias, preprocessing, source
schema, candidate generation, population/language, consumer policy, and evaluation
split. Record changes and decide whether prior evidence still supports the intended use.
Retain the last qualified revision and route uncertain adoption to review. This module
does not automatically retrain, alter thresholds, or promote a contract.

Use H31/H32 repeat audits, H35 canaries, H39 boundary fixtures, and H40 feature drift
through [profiles.md](profiles.md).

Official references: [confidence](https://docs.typesafe.ai/confidence),
[Noul consistency](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook), and
[Choice consistency](https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook).
