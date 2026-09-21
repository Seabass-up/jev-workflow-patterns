---
name: jev-evidence-directed-retrieval
description: Use when a Jev judgment remains unresolved and code has a fixed, authorized source catalog; design or review a bounded follow-up loop that chooses only among those sources.
---

# Jev Evidence-Directed Retrieval

Use this pattern when the task needs evidence expansion from a finite, caller-approved catalog. It is a bounded extension of retrieval/follow-up guidance, not open-ended search.

## Design the questions

- Put the task facts and already-acquired evidence in named `state` fields.
- Ask one fixed target question with an answer space that includes a genuine unresolved or insufficient outcome where appropriate.
- Ask the target question first. If it is already resolved under the caller's evaluated policy, stop without fetching.
- Only when unresolved, ask a dependent Choice question whose criteria are generated from the still-available source catalog plus `ask_user` and `no_more_evidence`. Include the latest target answer in the routing state.
- Describe what each source can establish; do not use labels whose meaning requires undocumented assumptions.
- Batch questions that are independent over the same state. Use another request only when the first answer must determine new evidence, state, or options.

## Keep execution in code

- The caller owns the allowlist, source identity/revision, authorization, fetch implementation, size/time budgets, thresholds, and actions.
- Pass Jev a list of permitted source descriptions; accept only an exact catalog label. Jev must never invent a URL, query, tool, identity, or permission.
- Require an adequate caller-chosen routing confidence before fetching. Treat thresholds as local policy to validate on representative labeled cases, not universal Jev calibration.
- Fetch only the selected entry. Verify returned `source_id` and exact `revision`; require nonempty text; project the record to exactly `{ "source_id", "revision", "text" }` before model submission so headers, credentials, or arbitrary callback metadata cannot enter Jev state. Reject stale, empty, unknown, repeated, oversized, or late evidence.
- Re-ask the same target question with the acquired evidence. Stop on resolved answer, `ask_user`, `no_more_evidence`, low confidence, invalid output, error, staleness, or budget.
- Return an explicit application status such as `answered`, `needs_user`, `needs_review`, `budget_exhausted`, `evidence_fetch_failed`, `stale_or_invalid_evidence`, `evidence_byte_budget_exceeded`, `state_byte_budget_exceeded`, or `inference_failed`. Never interpret `answered` as authorization to act.

The reference prototype used 1–5 rounds, at most 253 catalog sources, 8,000 evidence bytes by default (12,000 maximum), and a fetch timeout capped at 10 seconds. These are implementation bounds, not platform-wide guarantees; inspect the target implementation before claiming them.

Retrieved text is untrusted evidence. Wording such as “treat as evidence, not instructions” is not a prompt-injection defense. Preserve failures and uncertain outcomes; do not fall back to a guessed fetch.

For the complete JSON examples, status meanings, and failure tests, read the [pattern guide](../../patterns/evidence-directed-allowlist-controller.md) in this repository or the [published page](https://seabass-up.github.io/jev-workflow-patterns/patterns/evidence-directed-allowlist-controller/). Current TypeSafe contracts are in the official [state](https://docs.typesafe.ai/concepts/state), [Choice](https://docs.typesafe.ai/primitives/choice), [Noul](https://docs.typesafe.ai/primitives/noul), and [confidence](https://docs.typesafe.ai/confidence) docs.
