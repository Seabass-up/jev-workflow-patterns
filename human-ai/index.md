---
layout: default
title: "24 Jev Patterns for People and Their AIs"
description: "Research-inspired question contracts for learning, everyday services, and human–AI teamwork."
permalink: /human-ai/
kicker: "21 primary sources · 24 profiles · kernel 2.3.0"
---

# Help the person, not just finish the output

A helpful AI should preserve the work a person wants to do, ask a useful clarification, provide usable recovery instructions, and distinguish fluent answers from explanations. These 24 profiles turn those needs into bounded text judgments. They are task-authored adaptations of research and design guidance—not official TypeSafe patterns, globally novel discoveries, or proven interventions.

Each profile includes exact Choice JSON, named evidence, a bounded follow-up, three design examples, one separately authored challenge, and a proposed independent verification method. The complete collection now contains 204 question profiles (120 research, 12 email, 48 bug-hunting, and these 24); three foundational guides remain separate.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Research method]({{ '/human-ai/research/' | relative_url }}) · [Primary sources]({{ '/human-ai/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/human-ai/evaluation/' | relative_url }})

## What the screen established

After four one-time service-error recoveries, **69/72 design cases and 23/24 challenge cases** matched their prewritten labels: 92/96 overall. All 96 successful request digests replay. HA06, HA10, HA17, and HA21 remain provisional. No semantic disagreement was rerun, tuned away, or relabeled. All other profiles are synthetic-screened candidates, not qualified production components.

The independent challenge author saw each question contract but not its original examples or model results. This is a stronger author-separation check than recycling the design examples, but not independent human labeling, a representative test set, or proof of improved learning, accessibility, satisfaction, or task success.

## Learning and clear explanations

| ID | Question pattern | Intended use |
| --- | --- | --- |
| HA01 | [Retrieval exercise gives away its own answer]({{ '/human-ai/patterns/ha01/' | relative_url }}) | Keeps a tutor from mistaking copying a displayed answer for an independent recall attempt. |
| HA02 | [Worked-example blank practices the wrong skill]({{ '/human-ai/patterns/ha02/' | relative_url }}) | Prevents practice that asks a learner to copy an incidental detail while leaving the intended reasoning fully supplied. |
| HA03 | [Teaching analogy reverses the intended relationship]({{ '/human-ai/patterns/ha03/' | relative_url }}) | Stops a memorable example from teaching the opposite of the intended concept. |
| HA04 | [Feedback judges the person instead of the work]({{ '/human-ai/patterns/ha04/' | relative_url }}) | Helps AI tutors revise feedback into something the person can use without labeling their ability. |
| HA05 | [Two speakers use the same term in different senses]({{ '/human-ai/patterns/ha05/' | relative_url }}) | Allows the assistant to clarify vocabulary before arguing about a conclusion the speakers do not share. |
| HA06 · provisional | [Instruction has more than one plausible referent]({{ '/human-ai/patterns/ha06/' | relative_url }}) | Helps people and assistants avoid acting on the wrong file or object while following instructions. |
| HA07 | [Figurative instruction lacks a literal explanation]({{ '/human-ai/patterns/ha07/' | relative_url }}) | Prompts a plainer alternative without assuming anything about a reader's identity or ability. |
| HA08 | [Self-explanation states a mechanism or merely repeats a fact]({{ '/human-ai/patterns/ha08/' | relative_url }}) | Helps an AI tutor choose whether to ask for a causal link, without treating fluent paraphrase as demonstrated explanation. |

## Everyday services and understandable assistance

| ID | Question pattern | Intended use |
| --- | --- | --- |
| HA09 | [Disclose the needed document before the person starts]({{ '/human-ai/patterns/ha09/' | relative_url }}) | Can flag journeys that surprise people with requirements after they have invested effort. |
| HA10 · provisional | [Do not ask for the same answer again in different words]({{ '/human-ai/patterns/ha10/' | relative_url }}) | Can reduce avoidable repetition without suppressing legitimate change checks or new information. |
| HA11 | [Does an error message tell the person how to recover?]({{ '/human-ai/patterns/ha11/' | relative_url }}) | Can distinguish actionable recovery instructions from merely announcing that an error occurred. |
| HA12 | [Optional information must not sound compulsory]({{ '/human-ai/patterns/ha12/' | relative_url }}) | Can flag wording that pressures people to disclose optional information or hides a required field. |
| HA13 | [Match a help route to the person's stated communication constraint]({{ '/human-ai/patterns/ha13/' | relative_url }}) | Can prevent sending a person back to a channel they have already said they cannot use. |
| HA14 | [Reorient the person when they resume an interrupted task]({{ '/human-ai/patterns/ha14/' | relative_url }}) | Can reduce confusion about what is already done and what remains without asking the person to remember the whole journey. |
| HA15 | [Keep one-off feedback from becoming a permanent preference]({{ '/human-ai/patterns/ha15/' | relative_url }}) | Can flag unintended personalization, such as treating 'not this suggestion' as 'never suggest this again'. |
| HA16 | [Do not promise a capability the assistant does not have]({{ '/human-ai/patterns/ha16/' | relative_url }}) | Can prevent users from relying on a draft-only or read-only assistant to perform an action it cannot carry out. |

## Human–AI teamwork and control

| ID | Question pattern | Intended use |
| --- | --- | --- |
| HA17 · provisional | [Preserve the work the person wants to do]({{ '/human-ai/patterns/ha17/' | relative_url }}) | Support creative ownership and participation instead of equating help with maximum automation. |
| HA18 | [What is the user correcting?]({{ '/human-ai/patterns/ha18/' | relative_url }}) | Avoid changing the task goal in response to a formatting complaint, or treating a corrected fact as a mere stylistic preference. |
| HA19 | [Does a recommendation disclose its tradeoff?]({{ '/human-ai/patterns/ha19/' | relative_url }}) | Give the person a real choice instead of presenting one option's advantage as if it has no relevant cost. |
| HA20 | [Surface human context absent from the AI packet]({{ '/human-ai/patterns/ha20/' | relative_url }}) | Make useful human-only observations available for collaboration while avoiding guesses about unstated context. |
| HA21 · provisional | [Does the success metric measure the user's outcome?]({{ '/human-ai/patterns/ha21/' | relative_url }}) | Keep assistants optimized for useful completion rather than impressive-looking counts. |
| HA22 | [Which explanation does the person need?]({{ '/human-ai/patterns/ha22/' | relative_url }}) | Answer the question they actually asked without inventing internal reasoning or overloading them with irrelevant model detail. |
| HA23 | [Are alternatives compared on the same basis?]({{ '/human-ai/patterns/ha23/' | relative_url }}) | Make side-by-side choices easier to assess without claiming objective neutrality or deciding which alternative is best. |
| HA24 | [Can the person resume after the AI stops?]({{ '/human-ai/patterns/ha24/' | relative_url }}) | Let the person continue from the actual stopping point instead of reconstructing what the assistant did or repeating completed work. |

## Start with a small bundle

For an AI tutor, try HA01 (answer disclosure), HA02 (the skill actually practiced), and HA08 (mechanism versus repetition). For a frustrating form, try HA09 (prerequisites), HA11 (recovery instructions), and HA12 (optional input wording). For human–AI collaboration, try HA15 (feedback scope), HA18 (correction target), and HA24 (usable takeover notes).

Batch questions only when their required evidence belongs to the same coherent state. Distinct fixtures in this screen were separate requests. Select the questions that can change a specific next step; do not send all 24 for every conversation.

## Keep the boundary explicit

Before operational inference, code must validate the required fields and bind source identities/revisions. Missing required evidence deterministically returns `unknown`; the live missing-input cases here deliberately probe the question wording, not replace that gate. Preserve originals, contradictions and uncertainty. A label is not permission to edit, send, save a preference, assess a learner, or disclose a person's information.

These patterns examine supplied content and explicit constraints, not intelligence, personality, disability, diagnoses, emotional state, hidden motives, or a person's worth. Claims in state remain claims until independently verified. The cited guidance motivates the use cases; it has not tested Jev.

[Exact catalog]({{ '/human-ai/catalog.json' | relative_url }}) · [96 frozen fixtures]({{ '/human-ai/fixtures.json' | relative_url }}) · [Kernel human–AI module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/human-ai.md)
