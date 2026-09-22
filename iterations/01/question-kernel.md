---
layout: default
title: "The Jev question-design kernel"
description: "A reusable way to ask a narrow question, inspect uncertainty and request the missing evidence."
permalink: /iterations/01/question-kernel/
---

## Recommended kernel: Decision → Evidence → Judgment → Gate → Follow-up

1. **Name the downstream decision.** What will the software show, select or ask next? “Give me good JSON” is not an operational objective.
2. **Supply the smallest sufficient evidence packet.** Name the target, source, version, relevant text and constraints. Missing information stays missing. Do not send secrets or unnecessary private records.
3. **Ask a bounded judgment.** Choice for one label; Noul for each independently true/false condition; Score for one ordered dimension. Define complete, distinguishable answer criteria.
4. **Validate and gate in code.** Validate the answer shape and allowed values; apply provisional uncertainty handling, source freshness and authority checks. A valid JSON object can still express a wrong judgment.
5. **Drill into the missing fact.** Map the uncertainty or missing field to a specific question or authorized evidence read, merge the new evidence into a versioned state, and re-ask only affected judgments within a budget.

State is evidence; questions describe the judgment. Independent questions can be batched, but do not consume one another's results. A dependent step needs a later request or deterministic composition. See the [state guide](https://docs.typesafe.ai/concepts/state) and [question guide](https://docs.typesafe.ai/primitives).

## Worked example: dispatch readiness

Bad: “Is this request good enough? Return JSON.”

Better: independently ask whether the supplied request identifies a consistent location, a concrete task, and a stated access arrangement. Then code chooses the first missing detail:

```text
Missing location → Which property and unit is the work for?
Missing symptom → What is not working, or what work is requested?
Missing access → Who will admit the crew, or what is the entry arrangement?
Uncertain/conflicting answer → Review the exact conflicting or unclear evidence.
All three supplied → Verify the location, schedule and access before dispatch.
```

The [B02 contract]({{ '/iterations/01/patterns/b02/' | relative_url }}) explicitly prevents a missing location from contaminating the separate access judgment. A resident role can be an arrangement without a personal name. A hopeful “maybe someone will be there” is not a confirmed arrangement; a stated arrangement is still not proof of actual entry.

## A reusable host-owned contract

```json
{
  "decision_id": "dispatch-detail-review",
  "purpose": "Choose the next useful clarification",
  "state": {
    "request": "At Cedar Court Unit C, repair the broken switch. Access is not arranged."
  },
  "required_source_checks": ["current request", "same work item", "authorized access to record"],
  "question_contract": "Use B02 version 2 from catalog.json",
  "uncertainty_policy": "Review uncertain consumed answers; do not invent missing data",
  "follow_up_order": ["location", "symptom", "access"],
  "maximum_follow_ups": 2,
  "allowed_effect": "draft clarification only",
  "success_measure": "Fewer clarification turns without falsely treating a request as ready"
}
```

This is **application metadata**, not the TypeSafe HTTP request schema. The provider request contains `model`, `state` and `questions`; the host keeps expected labels, permissions, test results and follow-up limits out of model input. See the [HTTP API](https://docs.typesafe.ai/api).

## Questions to ask about every question

- Could two answer descriptions fit the same evidence?
- Can “unknown,” “not supplied,” “none fits” or “conflicting” be represented?
- Does the question ask for something the evidence actually contains?
- Are separate dimensions accidentally influencing each other?
- Would an exact lookup, calculation, schema test or rule be better?
- Does the response describe a claim, or has the real-world event actually been verified?
- What precise additional fact could change the answer?
- What will the application do when the provider fails or the answer is uncertain?
- Which representative negative case would prove this design is not useful?

Choice/Score confidence measures concentration, not correctness or permission; Noul is the probability of yes, not intensity. Thresholds must be evaluated on the intended domain. [TypeSafe confidence](https://docs.typesafe.ai/confidence) and the [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13) explain why code still owns precise operations.
