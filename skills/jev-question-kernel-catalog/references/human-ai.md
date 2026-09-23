# Human–AI collaboration profiles

Use this module for bounded checks of learning materials, service communication,
and collaboration with a person. The object of judgment is supplied text and its
relationship to an explicit task—not the person's intelligence, motivation,
disability, personality, diagnosis, or worth.

## Select the relationship that needs checking

The [24 profiles](https://seabass-up.github.io/jev-workflow-patterns/human-ai/)
are optional examples, not a checklist to run on every interaction:

| IDs | Family | Useful checks |
| --- | --- | --- |
| HA01–HA08 | Learning materials | Answer leakage, worked-example skill fit, analogy mapping, feedback target, term meaning, referents, literal instructions, self-explanation |
| HA09–HA16 | Communication and service | Up-front requirements, repeated questions, error recovery, optionality, stated communication constraints, resumption, feedback scope, capability promises |
| HA17–HA24 | Decisions and collaboration | Retained user work, correction subject, disclosed tradeoffs, missing human context, outcome metrics, explanation targets, comparison parity, human takeover |

Read the selected page's exact instructions, labels, required fields, and limits.
Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/human-ai/patterns/<lowercase-id>/`.
The [catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/human-ai/catalog.json)
contains the versioned question contracts. If these external pages are unavailable,
use the local [authoring](authoring.md) and [evaluation](evaluation.md) guidance;
do not claim an uninspected profile is validated.

Choose between nearby questions by their consumer:

- HA14 reorients a returning person to a saved checkpoint; HA24 transfers a task
  from an AI to a person who needs the stopping state and a concrete next step.
- HA18 identifies what the person is correcting; HA15 checks the proposed scope
  of that feedback's consequences. Neither may silently update a lasting preference.
- HA19 checks whether a recommendation reveals a relevant sacrifice; HA23 checks
  whether the named alternatives are compared on consistent criteria and evidence.
- HA08 classifies the content of a supplied explanation. It does not establish
  mastery, assign a grade, or justify a claim about the learner.

## Prepare a bounded, explicit state

Bind the exact material, its revision, and the current user request. Preserve
qualifications such as “for this item,” “do not write it for me,” and “this is only
a draft.” Describe missing context explicitly; do not invent the user's intent.
For a rendered experience, capture what the person could actually see, not only
the intended template. Keep answer keys distinct from learner-visible content.

Before inference, code validates `required_state_fields` and returns a local
`unknown` for absent, null, or schema-defined empty required evidence. Do not rely
on Jev to implement this guard, and do not treat valid `0` or `false` as missing.
Record the local reason separately from a model-generated answer. A deliberately
missing-input model test must be identified as such; it is not the production path.

Send only authorized, minimized material through the approved provider path.
The presence of a relevant observation does not authorize transmitting private
context. Identify a user observation as reported until independently verified.
Do not upload student records, health information, credentials, or bulk personal
history as a side effect of choosing a profile.

Each catalog sample uses the handle `decision`. Give batched questions unique
handles such as `ha18_correction` and `ha15_scope`, retain the full question
instructions, and supply the state fields both need. Batch only independent
questions over a coherent state; one answer cannot feed another in the same call.

## Use the labels without taking over

Use a result to focus a review or draft one bounded improvement. It does not prove
that learning happened, that the person understood, that a service became
accessible, or that a recommendation is best. Research inspiration and synthetic
label agreement are not demonstrated Jev benefit.

Preserve explicit user choices. Do not replace a human-selected task with more
automation merely because Jev predicts it is useful. Correction, explanation,
and comparison labels do not authorize edits, communication, publication, memory
updates, or external actions. Source access, actual capabilities, permissions,
numeric checks, state transitions, and outcome verification remain in code.

Keep unknown results, disagreements, stale inputs, and provider failures visible.
Do not map them to a favorable or negative answer. A default follow-up is one
targeted retrieval or clarification and at most one re-evaluation with new evidence;
stop unresolved when the needed evidence is unavailable. Respect a user's request
to stop without consulting a model.

## Verify the human-facing outcome

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/human-ai/evaluation/)
separates 72 design cases from 24 independently authored synthetic challenge cases.
Keep the two tracks separate, retain original expectations and misses, and do not
present their aggregate as a held-out real-world accuracy or efficacy estimate.
The [research](https://seabass-up.github.io/jev-workflow-patterns/human-ai/research/)
and [sources](https://seabass-up.github.io/jev-workflow-patterns/human-ai/sources/)
explain the motivating evidence and bounded prior-pattern comparison.

Before operational use, test the actual consumer. For example, inspect the visible
exercise for leaked answers; verify an error message against the real form rule;
or observe whether a person can resume from the handoff without duplicating work.
Measure the intended outcome separately from model agreement. Do not infer learner
traits, diagnoses, or preferences from those observations. Preserve current
contracts, source revisions, independent review, and real user feedback without
claiming that publication installed the module in a running harness.
