# Qualify a question through its consumer

Use this module after authoring and synthetic regression checks, before treating a
profile as suitable for a real workflow. It supplies an **offline shadow replay**:
record a versioned request and typed response, pass the response through a trusted,
side-effect-free copy of the consuming decision logic, and compare its planned
disposition with an independently assigned label and the current baseline.

The portable example uses one Choice, one Noul, and one Score in the same request:
`assets/mixed-contract-example.json`, `assets/mixed-fixtures-example.json`,
`assets/mixed-pilot-example.json`, and `assets/mixed-consumer-example.py`.
Its four cases are synthetic demonstrations, **not** held-out cases or evidence of
production accuracy. Its two thresholds and baseline labels are illustrative.

## Prepare a real shadow pilot

1. Name the decision consumer, allowed dispositions, review fallback, model ID,
   contract revision, and source-data boundary. Make a side-effect-free adapter
   exposing `decide(state, answers) -> disposition`. Review the adapter as ordinary
   code; the replay imports and executes it. It must not send messages, pay, publish,
   mutate records, or call tools. Keep actual action permissions outside Jev.
2. Freeze a representative, authorized, independently labeled sample **before**
   inference. Use `split: "held_out"` only for cases not used to author or tune the
   question, thresholds, or adapter. Record the existing baseline disposition and
   expected disposition separately. Resolve label disagreements with people before
   checking model answers. Preserve the sample's population, time window, language,
   source revisions, and exclusions. Keep private records under their actual
   retention policy; the public example must remain synthetic.
3. Run code-owned preflight. Missing or empty top-level `required_state_fields`
   must return the declared review disposition **without a provider call**. For
   nonempty cases, capture the exact contract, state, versioned model, response,
   request digest, elapsed time, and estimated cost. A response copied from a
   different state, question, or model is invalid. The tool checks these bindings
   and typed answer coverage before invoking the adapter.
4. Define a risk-based sample gate before reading results, for example maximum
   automatic errors and review fraction. Count errors, review, baseline matches,
   provider/schema failures, and consumer exceptions. Inspect every error and
   boundary case, not just the aggregate. Test any consequential effect in the
   real application separately: this replay checks planned dispositions, not
   delivery or a completed external action.

## Run the example

From the installed skill folder, with Python 3:

```sh
python3 scripts/check_contract.py assets/mixed-contract-example.json assets/mixed-fixtures-example.json
python3 scripts/qualify_workflow.py assets/mixed-contract-example.json assets/mixed-pilot-example.json assets/mixed-consumer-example.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The pilot JSON has `contract_id`, `version`, versioned `model`,
`review_disposition`, `allowed_dispositions`, and `cases`. Each case has `id`, `split`, `state`,
`expected_disposition`, `baseline_disposition`, and `receipt`. A receipt contains
the canonical `request_sha256` plus the unmodified provider `response`; the
exact request is reconstructed from the frozen contract, case state, and model.
For preflight-missing cases, `receipt` is null. Real held-out samples also need
`sample_limits.min_held_out_cases`, `sample_limits.max_automatic_errors`,
`sample_limits.max_review_fraction`, and
`sample_limits.min_match_gain_over_baseline`. Set these before inference based on
the workflow's error cost and sample design; the example does not choose them.
`--require-sample-checks` makes the command fail if a held-out sample misses its
declared limits; it fails on the synthetic example because no held-out sample exists.

The output says `synthetic_demo_only` or `held_out_as_declared`. The latter is a
**caller declaration**, not a verified independent split or a production approval.
No sample gate replaces human review of representativeness, privacy, error costs,
subgroup/language performance, or the actual action and outcome path. Model aliases
may move; pin and log the resolved version when thresholds have been tuned.
The request digest detects a mismatch between stored request and response; it
does not authenticate the source or prove that the provider produced the response.
The bundled Choice-confidence consistency approximation is checked only for
`jev-1.13.0`; a later model needs its own threshold and consistency review.

## Add boundary tests before adoption

At minimum, include absent/empty evidence, negation, quoted history, contradictory
sources, a relevant candidate omitted from an option set, near-overlapping labels,
unrelated state, malformed or missing typed answers, and a provider failure. Use
the relevant subset for the actual task; do not ask Jev to perform arithmetic,
date comparison, exact identity checks, or permission enforcement. Keep original
misses and repeat with a new contract version after meaningful changes.

Official references: [primitives](https://docs.typesafe.ai/primitives),
[confidence](https://docs.typesafe.ai/confidence), and
[Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13).
