# Authoring a consumable question

Start with the decision the application needs, who consumes it, and what evidence
could change it. "Analyze this customer" needs decomposition; "which supplied
service category is requested in `message.text`?" has a consumer.

Choose Choice for competing branches, separate Nouls for independently applicable
properties, or Score with concrete ordered levels. Define each option without relying
on its name. If a score lacks enough evidence to mean anything, add an independent
availability question and ignore the score when absent. A low score must not silently
mean both "low severity" and "unknown severity."

Give the model relevant context for negation, quoted material, dates, identities,
and competing claims. Have code construct candidates before selection; record what
coverage was checked and what may still be missing. A schema validator cannot certify
candidate completeness. Put known arithmetic, exact IDs, dates, and string copying
in code. Use structured instructions or criteria when contrasts need more detail.

## Local authoring envelope

Use `../assets/contract-example.json`. Record:

- `contract_id` and positive integer `version`;
- `consumer`: the precise downstream use;
- `required_state_fields`: top-level fields the helper checks;
- `request`: state and complete typed questions;
- `uncertainty_policy`: ambiguity, missing evidence, and service failure behavior;
- `code_owned_checks`: specific checks required by this task;
- `follow_up`: trigger, new evidence, maximum calls, and stop condition;
- `evaluation_scope`: what the tests establish.

These metadata fields are for the application. Do not upload the whole envelope.
Source IDs/revisions needed for the judgment may appear in state; expectations,
credentials, and unrelated records do not. Define precedence where it changes the
result: missing source, contradictory evidence, no matching label, or unresolved intent.

## Asking for more detail

Suppose the first Choice identifies a delivery issue but no delivery event is supplied.
Code retrieves authorized event history, then asks whether it supports delay, failed
access, or insufficient evidence. Record the triggering answer and source revision.
If the events were already in the original state, batch the useful independent
questions in the first request.

Set a maximum number of follow-ups and a stop condition before calling. Stop when
evidence is unavailable, the consumer's decision is resolved, or the budget is exhausted.
Rewording until a preferred label appears is not evidence.

Use L23 primitive fit, L20 fidelity, and L22 directness through
[profiles.md](profiles.md). Directness and source support are distinct judgments.

Official references: [questions](https://docs.typesafe.ai/primitives),
[structured criteria](https://docs.typesafe.ai/primitives/advanced), and
[state](https://docs.typesafe.ai/concepts/state).
