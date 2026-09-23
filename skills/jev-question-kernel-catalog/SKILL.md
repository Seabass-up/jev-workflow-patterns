---
name: jev-question-kernel-catalog
description: Design, adapt, or evaluate Jev typed question contracts, including evidence binding, targeted follow-up, regression fixtures, and drift checks. Use when a workflow needs dependable JSON judgments from Jev.
metadata:
  version: "2.4.0"
---

# Jev Question Kernel v2

One entry point for authoring and checking Jev question contracts. Keep the existing
skill name for compatibility. Four research catalogs supply 120 examples, with
12 email, 48 bug-hunting, and 24 human–AI collaboration profiles: 204 in total,
separate from the three foundational workflow guides.
Their synthetic results do not qualify a new application automatically.

## Select the work needed

Read only the references relevant to the task:

| Need | Reference | Deliverable |
| --- | --- | --- |
| Create or repair a question; choose a primitive; design drill-down | [Authoring](references/authoring.md) | Versioned request, consumer, uncertainty policy, and follow-up plan |
| Check an extraction, quotation, association, or claim against sources | [Evidence and provenance](references/evidence.md) | Exact preflight results, bounded semantic checks, and unresolved evidence |
| Test a contract, investigate disagreement, or assess a change | [Evaluation and drift](references/evaluation.md) | Frozen fixtures, receipts, failure report, and reevaluation decision |
| Find a domain example | [Domain profiles](references/profiles.md) | Smallest matching pattern with its version and limitations |
| Interpret email evidence or assess a draft against a request | [Email profiles](references/email.md) | Typed advisory labels with mailbox and action boundaries |
| Hunt a specific failure mechanism or check a proposed bug | [Bug-hunting profiles](references/bug-hunting.md) | Source-bound candidates, counterevidence, and independent verification recipes |
| Improve learning materials, service communication, or collaboration with a person | [Human–AI profiles](references/human-ai.md) | Bounded checks of supplied material, explicit preferences, and practical handoffs—not judgments about the person |

For a new contract intended for repeated workflow use, combine authoring with a
proportionate evaluation. Existing qualified contracts need reevaluation when their
meaning, evidence assumptions, model, or consuming policy changes. Ordinary invocation
does not require repeating a benchmark.

## Shared rules

- Work backward from the JSON consumer to one coherent semantic judgment per
  question. Use Choice for competing labels, Score for a concrete ordered dimension,
  and Noul for probability of one proposition. A Noul near 0.5 is uncertainty, not
  medium intensity; it has no separate confidence field.
- State supplies relevant evidence. Prefer named fields when relationships matter;
  strings remain suitable for simple inputs. Instructions must carry the complete
  question because its ID is only a code handle. Define exclusions and missing or
  conflicting evidence behavior explicitly. Do not turn unknown evidence into false.
- Batch independent questions over the same state. Dependent requests follow after
  code constructs required evidence or candidates. Declared repeatability experiments
  are a separate, budgeted use of repeated identical requests.
- Code owns exact matches, candidate membership, IDs, revisions, calculations, dates,
  policy thresholds, permissions, execution, and outcome verification. Model results
  remain advisory. Confidence neither authenticates a source nor grants authority.
- Send only task-authorized material through the existing approved provider path.
  Keep credentials server-side and out of templates and receipts. On provider failure,
  return the error and use the declared fallback; never synthesize a passing result.
- Preserve question versions and original misses. Freeze expectations outside provider
  inputs. Report model judgment, code checks, and observed outcome separately.

## Start a contract

Copy [the contract example](assets/contract-example.json) and
[fixture example](assets/fixtures-example.json) into the user's scoped project.
These are local authoring envelopes, **not TypeSafe API payloads**. Only the request's
`state` and `questions` belong in the provider call; the configured client owns
model/settings. Fixture inputs replace `request.state`; expectations never enter it.

Run the portable structural check from the installed skill folder:

```sh
python3 scripts/check_contract.py assets/contract-example.json assets/fixtures-example.json
python3 scripts/check_confidence.py RECEIPT_JSON_OR_DIRECTORY
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`check_confidence.py` checks stored Choice confidence against its probabilities and
converts a confidence threshold into the top probability it requires for a given
option count. Consistency is not correctness.

The helper checks the local authoring envelope shape shown in the two examples
(`contract_id`, `request`, `consumer`, `uncertainty_policy`, `evaluation_scope`). The
published iteration and email catalogs use a different `catalog.json` pattern shape and
are validated by their own `evaluate.py` receipt checks, not by this helper.
The helper catches selected packaging/schema mistakes. It does not prove semantic
clarity, privacy, candidate completeness, authenticity, or accuracy. Review those
against source material and consuming code using the relevant module.

Before API integration, refresh the relevant official
[TypeSafe documentation](https://docs.typesafe.ai/llms.txt) and installed SDK schema.
Local bridge limits must not be presented as provider-wide limits.
