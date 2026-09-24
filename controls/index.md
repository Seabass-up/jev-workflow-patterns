---
layout: default
title: "Call controls: patterns around a Jev call"
description: "Ten question contracts for preparing a request, consuming an answer, checking contract quality, and reading message signals."
permalink: /controls/
kicker: "10 profiles · 38/40 labels matched · kernel 2.5.0"
---

# Call controls

The code around a Jev call decides most of what a workflow does with an answer: whether to split a request first, whether a runner-up label would have led somewhere else, whether two options of a contract can both apply. These ten contracts give that code bounded judgments to use. They were promoted from the [discovery intake]({{ '/discovery/' | relative_url }}) after the introduction review; they are task-authored compositions, not official TypeSafe patterns.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/controls/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/controls/evaluation/' | relative_url }})

## What the screen established

**28/30 design cases and 10/10 challenge cases** matched their prewritten labels: 38/40 overall. CT03, CT07 remain provisional. All 40 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Preparing the request

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CT03 · provisional | [Split commands cover the request without additions]({{ '/controls/patterns/ct03/' | relative_url }}) | Lets code trust a language-model split before each command is routed and executed separately. |
| CT04 | [Request contains more than one distinct action]({{ '/controls/patterns/ct04/' | relative_url }}) | Prevents a router from executing only the first action of a compound request or forcing a single handler to interpret several. |
| CT05 | [Translation preserves what the question needs]({{ '/controls/patterns/ct05/' | relative_url }}) | Lets a translate-then-ask path fail closed when the translation changed negation, quantities, parties, or requests that the downstream question relies on. |

## Consuming the answer

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CT01 | [Runner-up label leads to the same consumer outcome]({{ '/controls/patterns/ct01/' | relative_url }}) | Lets code gate on the probability mass that actually changes the outcome instead of a flat confidence threshold that ignores where the remaining probability went. |
| CT02 | [Free-text tool argument targets the requested entity]({{ '/controls/patterns/ct02/' | relative_url }}) | Catches an agent calling the right tool for the wrong place, record, or file while code keeps every exact check. |

## Contract quality

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CT06 | [Labeler rationales apply the definition the same way]({{ '/controls/patterns/ct06/' | relative_url }}) | Keeps a bootstrapped training label from counting as agreement when the labelers agreed by coincidence under different interpretations. |
| CT07 · provisional | [Negation pair is a true complement]({{ '/controls/patterns/ct07/' | relative_url }}) | Stops a design-time probe from comparing two propositions that can both be true or both be false and reading the mismatch as model inconsistency. |
| CT08 | [Two Choice options overlap]({{ '/controls/patterns/ct08/' | relative_url }}) | Finds label overlap before inference, the defect that pre-inference review found by hand in nine human-AI contracts. |

## Message signals

| ID | Question pattern | Intended use |
| --- | --- | --- |
| CT09 | [What a message asks the recipient to do with a credential]({{ '/controls/patterns/ct09/' | relative_url }}) | Supplies the one phishing signal that should veto delivery rather than average into a spam score, while leaving legitimate reset instructions alone. |
| CT10 | [Link text claims a destination its host does not match]({{ '/controls/patterns/ct10/' | relative_url }}) | Flags disguised links using the organization registry code already holds, without asking the model to parse URLs. |

## Start with a small bundle

For an agent that executes tool calls, start with CT04 (compound detection), CT03 (split coverage), and CT02 (argument target). For a router with a review band, add CT01 (runner-up outcome). Before freezing any new contract, run CT08 over its option pairs; this collection ran it on itself before its own fixtures were written.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

These labels never authorize an action. Code keeps thresholds recorded with their option counts, exact identifiers and equality checks, split caps, credential and link policy, and every execution decision. A veto label such as CT09's disclose_credential feeds a code-owned rule, not an automatic action.

[Exact catalog]({{ '/controls/catalog.json' | relative_url }}) · [40 frozen fixtures]({{ '/controls/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/controls.md)
