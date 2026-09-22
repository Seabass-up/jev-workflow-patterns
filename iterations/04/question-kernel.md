---
layout: default
title: "Iteration 4 · Question Kernel"
description: "A practical checklist for asking Jev the right JSON question."
permalink: /iterations/04/question-kernel/
kicker: "Iteration 4 · authoring guide"
---

[← Iteration 4 catalog]({{ '/iterations/04/' | relative_url }}) · [Evaluation]({{ '/iterations/04/evaluation/' | relative_url }}) · [Sources]({{ '/iterations/04/sources/' | relative_url }})

# The final question kernel

“Crap in, crap out” is useful shorthand, but the repair is specific: a Jev request needs the exact evidence, a literal semantic decision, an answer space that code can consume, and a declared uncertainty route. JSON typing makes an interface predictable; it does not make a judgment true.

## Before you send state

1. **Name the decision.** Ask for one decision whose output has a specific consumer. Do not ask Jev to “analyze” a record.
2. **Name the evidence fields.** Use a small JSON object and tell the question which named relationship matters. Do not hide needed context in a prose blob or send irrelevant records.
3. **Let code find and bind candidates.** Regexes, parsers, IDs, exact quote search, source revisions, arithmetic, dates, and schemas belong in code. Jev selects/interprets supplied candidates; it cannot choose an omitted value.
4. **Choose the primitive by meaning.** Choice is one bounded label; Score is degree on a concrete ordered rubric; Noul is one independently useful yes/no condition. Use a composite only when code needs more than one independent fact.
5. **Make boundaries literal.** Put negations, exclusions, ambiguity, conflicts, and no-evidence behavior in instructions/criteria. If an explanation of “what we really meant” appears after a miss, that explanation belongs in the next contract version.

## The JSON contract

Every usable question page includes these parts:

| Contract part | What it prevents |
| --- | --- |
| named required state fields | silent context loss or unsupported comparison |
| complete instructions | accidental reliance on an opaque question ID |
| concrete closed criteria | vague labels and forced guesses |
| explicit unknown/no-match choice where needed | a false forced selection |
| separate expectations outside state | label leakage into a synthetic screen |
| code-owned controller | treating probability as authority or an action |
| frozen boundary fixtures | a happy-path-only prompt that regresses silently |

## Drill down only when it changes the state

Batch independent questions over one immutable state. Make a second call only when the first result tells code what evidence to fetch, which candidates to construct, or which explicit subset requires a detailed check. Preserve the original decision, source revision, question version, probabilities/confidence, and the reason a second pass was needed.

Good drill-down: a broad taxonomy controller retains candidate paths, then code builds a detailed subtree state for the selected paths. Bad drill-down: asking the same vague question again until the answer is desirable.

## Keep code in control

Use code for numerical work, dates, IDs, candidate membership, source version binding, thresholds, caching, authorization, state mutation, communications, and verification. Confidence expresses answer distribution concentration; it is not correctness, permission, authentication, or completion.

See [the evaluation]({{ '/iterations/04/evaluation/' | relative_url }}) for the frozen-fixture and receipt boundary, and [the sources]({{ '/iterations/04/sources/' | relative_url }}) for the official TypeSafe mechanisms that informed these contracts.
