---
layout: default
title: "Iteration 3 Question Kernel"
description: "How to ask Jev the right JSON question, inspect typed output, and drill down without giving up code control."
permalink: /iterations/03/question-kernel/
kicker: "Question design · precise state, bounded judgment, code gate"
---

[← Iteration 3 catalog]({{ '/iterations/03/' | relative_url }}) · [Evaluation]({{ '/iterations/03/evaluation/' | relative_url }}) · [Sources]({{ '/iterations/03/sources/' | relative_url }})

# The correct Jev question is a decision contract, not a request for advice

“Crap in, crap out” is exactly the right concern. Treat Jev as a typed decision
component. Give it compact evidence and one bounded judgment; make code own everything
that must be exact, authorized, or observable in the real world.

## Kernel: State → Decision → Criteria → Gate → Follow-up → Receipt

| Part | The question to answer before calling Jev | What belongs there |
| --- | --- | --- |
| State | What facts are actually relevant? | Named JSON fields, candidate IDs, source excerpts, and a caller-verified revision when useful. |
| Decision | What one semantic relation must be classified? | One subject and one relationship: not “what should we do?” |
| Criteria | What does every possible answer mean? | Concrete labels plus insufficient, ambiguous, conflict, or no-match where the evidence can fail. |
| Gate | What must be true before code consumes it? | Exact IDs, revisions, candidate coverage, confidence policy, and consequence policy. |
| Follow-up | What resolves uncertainty? | Ask for a missing fact, retrieve an approved source, retain conflict, or route to review. |
| Receipt | How can a result be checked later? | Exact state, questions, model, typed response, request digest, and outcome label. |

## Start from a named JSON state

~~~json
{
  "state": {
    "subject": "the one record, task, candidate pair, or passage being judged",
    "evidence": "only facts needed for that judgment",
    "candidates": "caller-bounded IDs when the question selects among options",
    "source_revision": "a caller-verified revision or snapshot identity when available"
  },
  "questions": {
    "decision": {
      "type": "choice",
      "instructions": "Name the exact relation to judge and the things Jev must not decide.",
      "criteria": {
        "supported": "The supplied state explicitly establishes the named relation.",
        "contradicted": "The supplied state explicitly establishes the incompatible relation.",
        "insufficient": "Evidence is absent, vague, conflicting, or cannot establish either relation."
      }
    }
  }
}
~~~

Expected labels belong in a test fixture outside state. Never put “the answer,” a secret,
an authority claim, an action command, or an unverified completion claim into state and
ask Jev to ratify it.

## Pick the output type by what the answer means

- **Choice** — a closed, mutually useful route or candidate. Include an insufficient/no-match branch when the candidate set or evidence may fail.
- **Noul** — one focused proposition such as “does this passage explicitly contradict the asserted premise?” Use a middle probability as uncertainty, not a silent decision.
- **Score** — an ordered concrete dimension. Define every level; keep weights and non-compensable rules in code.

All questions in one request see the same state and are evaluated independently. Put
independent companion questions together. If one answer must determine what state comes
next, make a second request after code performs the retrieval, construction, or exact
validation.

## Drill down only when the next question is genuinely narrower

~~~text
1. Name the decision target and freeze a compact state snapshot.
2. Ask the coarse judgment with an explicit insufficient/no-match outcome.
3. If evidence is clear, let code validate IDs, revisions, candidate membership,
   calculations, and any policy gate.
4. If evidence is missing or ambiguous, fetch only a caller-approved next evidence
   source, then ask a smaller follow-up about that new state.
5. If a decision needs chained reasoning, external facts, exact numeric work, or an
   authority decision, route it out of the Jev-only path.
6. Preserve the original request and every result generation rather than rewriting history.
~~~

Examples in this iteration:

- L16 asks whether a corpus contains an answer before L07-style selection can force a top candidate.
- H22 makes code verify whether a candidate universe is exhaustive before a Choice winner becomes a real-world selection.
- L13 and H27 separate semantic entity alignment from any actual link or merge.
- H24 asks atomic dimensions once, but code owns weights and the serious-veto rule.
- H29 sends arithmetic and date math to deterministic code rather than to a semantic model.

## The minimum safety and quality gate

| Typed result | Caller-owned next step |
| --- | --- |
| Clear bounded answer | Verify exact snapshot, IDs, and deterministic conditions; make only a non-executing proposal unless a separate authority path exists. |
| Insufficient, no-match, or ambiguous | Ask for the missing fact, expand a caller-approved candidate set, or retain the uncertainty. |
| Contradictory evidence | Preserve both sides in separate fields or context lanes; route to a designated verifier or reviewer. |
| Low Choice/Score confidence or middle Noul | Review or use a broader deterministic category; never silently collapse it to yes/no. |
| State changed after request | Discard/recompute from a new snapshot. |
| Financial, privacy, legal, permission, or external consequence | Require separate authority and real-world verification regardless of a Jev result. |

Use the [shared catalog skill](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/SKILL.md) for a compact implementation guide, then choose the closest concrete [Iteration 3 pattern]({{ '/iterations/03/' | relative_url }}).
