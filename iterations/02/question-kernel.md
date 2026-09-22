---
layout: default
title: "Iteration 2 Question Kernel"
description: "A practical kernel for asking Jev precise, testable JSON questions and drilling down safely."
permalink: /iterations/02/question-kernel/
kicker: "Question design · State, typed judgment, code-owned control"
---

[← Iteration 2 catalog]({{ '/iterations/02/' | relative_url }}) · [Evaluation]({{ '/iterations/02/evaluation/' | relative_url }}) · [Sources]({{ '/iterations/02/sources/' | relative_url }})

# The question kernel: turn a vague ask into a typed, testable judgment

The right Jev question is not “what should we do?” It is a small judgment that code can inspect, combine with deterministic checks, and escalate when evidence is missing. Jev sees one state and evaluates each question independently; if a later judgment depends on an earlier answer, make that sequence explicit in code.

## Eight required parts

| Part | Ask yourself | Good outcome |
| --- | --- | --- |
| Subject | What exact record, claim, field, or proposal is being judged? | One named decision target. |
| Evidence | Which facts, documents, candidates, and revisions may support it? | A compact named JSON state. |
| Judgment | Is this a closed choice, a bounded score, or a probability? | Choice, Score, or Noul with a reason to use it. |
| Criteria | What does every label mean, including absence or conflict? | Mutually useful labels with an explicit insufficient/no-match path. |
| Exclusions | What must the model not decide? | Authority, date math, identity, policy enforcement, and actions remain outside. |
| Follow-up | What happens for each result or low confidence? | Clarify, retrieve, preserve, review, or make a non-executing proposal. |
| Code controls | Which facts require deterministic checks? | IDs, revisions, offsets, calendars, permissions, thresholds, writes. |
| Test set | What ordinary, missing, conflict, and outside cases prove the boundary? | Frozen synthetic or independently labeled fixtures. |

## A reusable JSON shape

~~~json
{
  "state": {
    "subject": "named item being judged",
    "evidence": "only relevant facts and source excerpts",
    "candidates": "caller-bounded candidates when selection is needed",
    "source_revision": "caller-verified revision identifier when available"
  },
  "questions": {
    "decision": {
      "type": "choice",
      "instructions": "Name the relationship to judge and the exclusions.",
      "criteria": {
        "supported": "Explicit evidence supports the named relationship.",
        "contradicted": "Explicit evidence establishes the incompatible relationship.",
        "insufficient": "Evidence is absent, vague, conflicting, or cannot establish it."
      }
    }
  }
}
~~~

The expected label belongs in a test fixture outside the submitted state. Never put the answer, an authority claim, a secret, or a command to act into the state and then ask the model to validate it.

## Drill-down sequence

~~~text
1. Bound the object and the evidence.
2. Ask one coarse, closed judgment.
3. If it is sufficient and within policy, run deterministic code checks.
4. If it is missing, contradictory, or low-confidence, ask a smaller follow-up question
   against a caller-approved subset of evidence.
5. Preserve the original question, result, revision, and failure evidence.
6. Escalate to a human or a reasoning model when the next step cannot be bounded.
~~~

Do not fake dependency by putting two dependent questions in one request. For example, first select a source span or date expression, then let code validate offsets or resolve calendar arithmetic before asking any later judgment.

## Primitive selection

- **Choice**: choose one well-defined route, category, candidate ID, or evidentiary status. Include no-match, ambiguous, or insufficient where the state can fail to establish a label.
- **Score**: rate a bounded ordinal continuum only when the caller can explain what each level means and how it will be used. Keep the score advisory.
- **Noul**: estimate whether a narrowly defined proposition is supported. Treat middle values as uncertainty, not as a silent yes/no.

## State design rules

- Prefer a JSON object with descriptive fields over a long blended string.
- Provide only the content needed for the decision, along with the source revision or candidate IDs when relevant.
- Separate task request, binding constraints, reference material, and quoted third-party text. H15 audits this role separation but is not a security boundary.
- Give the model candidate IDs or spans when code already found them. H13 and H14 show why code should still verify calendar inputs and offsets.
- Include the stated effect if you want a severity judgment. H19 showed that severity must not be invented from an action alone.

## The minimum drill-down policy

A useful implementation has a non-model policy table:

| Jev result | Caller-owned next step |
| --- | --- |
| Clear, high-confidence bounded answer | Run deterministic validation, then make a proposal for approved handling. |
| No match or insufficient | Ask for the missing fact, expand a caller-approved candidate set, or retain the broader category. |
| Contradiction | Preserve both sides and route to an approved verifier or human. |
| Low confidence or middle Noul probability | Review; do not silently collapse uncertainty into a label. |
| Material change after a plan was drafted | Discard the pending proposal and replan from a verified state snapshot. |
| Any action, permission, financial, privacy, or external consequence | Require the separate authority and verification path regardless of the typed answer. |

The [30 patterns]({{ '/iterations/02/' | relative_url }}) are concrete variants of this kernel. The [evaluator]({{ '/iterations/02/evaluate.py' | relative_url }}) demonstrates how to bind a receipt to state and questions while keeping controller outputs non-executing.
