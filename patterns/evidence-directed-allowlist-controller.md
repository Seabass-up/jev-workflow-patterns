---
layout: default
title: Evidence-directed allowlist controller
description: A bounded follow-up loop that uses Jev to choose among caller-approved evidence sources only when the current answer is unresolved.
permalink: /patterns/evidence-directed-allowlist-controller/
kicker: Bounded extension · evidence acquisition
---

This pattern answers a question with current evidence first. Only if that typed answer remains uncertain does the workflow ask Jev which already-approved source is most likely to resolve the remaining uncertainty. Application code fetches that source, verifies its identity and revision, and asks the fixed target question again.

This is deliberately described as a **bounded extension** of follow-up and retrieval guidance, not as a claim that evidence expansion itself is unprecedented.

## When to use it

Use it when there is a small, finite catalog of permitted sources and one or more may resolve a specific judgment. Examples include checking a current order record, an approved policy, or a versioned internal reference.

Do not use it as open-ended web search. Jev does not invent URLs, tools, search terms, source authority, or permission to retrieve. A person or separately authorized retrieval component must define the candidate catalog first.

## State and question contract

Keep the business task and acquired evidence in named fields. Give the first request the facts already available, not a summary of documents Jev has not seen. Ask one narrow target question, with an explicit answer space.

Example target request:

```json
{
  "state": {
    "task": {
      "question": "Do the supplied records establish that the same order was charged twice?",
      "order_id": "ORD-104",
      "observed_charge_count": 1
    },
    "acquired_evidence": []
  },
  "questions": {
    "duplicate_charge": {
      "type": "noul",
      "instructions": "Do the supplied facts establish two captured charges for the same order?"
    }
  }
}
```

A Noul is the probability that the answer is yes. A probability close to 0 or 1 can be decisive under a workflow policy; a value near 0.5 is unresolved. Choose thresholds from representative, labeled cases and the consequences of a wrong decision.

Only an unresolved target justifies a second, dependent request. The routing request must receive the latest target answer and a code-built list of remaining source choices:

```json
{
  "state": {
    "task": {"question": "Does this order have a duplicate captured charge?", "order_id": "ORD-104"},
    "latest_target_answer": {"type": "noul", "noul": 0.52},
    "already_acquired_source_ids": [],
    "available_evidence_sources": [
      {"source_id": "charge_ledger", "description": "Captured charges for order ORD-104"}
    ],
    "evidence_so_far": []
  },
  "questions": {
    "next": {
      "type": "choice",
      "instructions": "Which single listed source is most likely to resolve the remaining question? Choose only a listed label; do not invent or fetch sources.",
      "criteria": {
        "charge_ledger": "The versioned charge ledger for this order.",
        "ask_user": "The task needs clarification from the user.",
        "no_more_evidence": "No permitted source is likely to resolve the uncertainty."
      }
    }
  }
}
```

The JSON shows the question shape, not a complete application request wrapper for every SDK. See TypeSafe's [state](https://docs.typesafe.ai/concepts/state), [Choice](https://docs.typesafe.ai/primitives/choice), [Noul](https://docs.typesafe.ai/primitives/noul), and [confidence](https://docs.typesafe.ai/confidence) docs for current SDK/API contracts.

## Output contract

The controller returns an application-level status, not a new Jev primitive:

| Status | Meaning |
| --- | --- |
| `answered` | The fixed target question met the caller's resolution rule. This is not permission to perform an action. |
| `needs_user` | Jev selected the explicit clarification route. |
| `needs_review` | No source was selected, routing confidence was inadequate, or a selection was invalid. |
| `budget_exhausted` | The bounded rounds ended while the target remained unresolved. |
| `evidence_fetch_failed` | The caller's fetch failed or timed out. |
| `stale_or_invalid_evidence` | Returned source identity/revision did not match the caller's catalog. |
| `evidence_byte_budget_exceeded` / `state_byte_budget_exceeded` | The evidence or resulting request exceeded its size budget. |
| `inference_failed` | The bridge failed or returned an unusable typed answer. |

The result retains completed rounds, exact revision-bound evidence, and the last target/routing result where available. Downstream code still owns any real-world action.

## Code-controlled loop

1. Validate a fixed target question against the initial task state and ask it once.
2. Stop immediately if the target answer is resolved under the caller's policy.
3. Build Choice criteria from the remaining caller-owned source catalog plus `ask_user` and `no_more_evidence`.
4. Check the routing answer type, confidence floor, and source ID. Reject unknown, repeated, or escape labels that were not declared as such.
5. Fetch only the chosen catalog entry, under a deadline. Require exact returned `source_id` and `revision`, nonempty text, then project the result to exactly `{ "source_id", "revision", "text" }` before any fetched content reaches Jev. Do not forward headers, credentials, or arbitrary adapter metadata. Measure the evidence byte budget after this projection.
6. Re-ask the same target question with the new evidence. Stop on resolution, explicit stop, uncertainty, failure, staleness, or budget.

The prototype bounds the source catalog at 253 items, the round count to 1–5, evidence to 8,000 bytes by default (12,000 maximum), and each fetch deadline to at most 10 seconds. The 0.8 target and routing confidence floors are local example defaults, not universal Jev settings.

## Safety and failure handling

- Treat retrieved text as untrusted evidence, not instructions. A question wording alone is not prompt-injection protection.
- Keep fetch URLs, credentials, authorization and revision authority in ordinary code.
- Normalize each fetch result to the three-field evidence contract before it is appended to the model state. The local prototype was tightened to do this; custom fetch adapters should still return only the intended excerpt and never include credentials or unrelated metadata.
- A failed or low-confidence routing result must not trigger a guessed fetch. Escalate or stop.
- A matching revision proves only that the result matches the caller's declared catalog entry; it does not prove the catalog is authoritative.
- Test decisive initial answers, unresolved answers, stop labels, invalid labels, stale revisions, timeouts, oversized evidence, and bridge failures.

## Skill

Use [`jev-evidence-directed-retrieval`](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-evidence-directed-retrieval/SKILL.md) when you need to implement, adapt, or review this bounded follow-up pattern in an application.

## Related TypeSafe guidance

[System One](https://docs.typesafe.ai/concepts/system-one) · [State](https://docs.typesafe.ai/concepts/state) · [Choice](https://docs.typesafe.ai/primitives/choice) · [Noul](https://docs.typesafe.ai/primitives/noul) · [Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing) · [Re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
