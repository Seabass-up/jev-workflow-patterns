---
layout: default
title: "Human–AI Pattern Sources"
description: "Primary guidance and original research used to motivate the question designs."
permalink: /human-ai/sources/
kicker: "Checked September 23, 2026"
---

# Inspiration, not a performance claim

The research passes inspected these 21 primary pages or papers. Evidence summaries describe the design need, not Jev's effectiveness. W3C cognitive-accessibility supplemental patterns are guidance, not themselves WCAG conformance requirements; the error-suggestion understanding page is explanatory guidance, not a full compliance test. Original studies are bounded by their own populations and tasks.

No source is represented as endorsing this catalog. All question contracts and scenarios are task-authored adaptations. Sources are checked as of the listed date, not continuously monitored.

## HL-S1: Organizing Instruction and Study to Improve Student Learning

[Read the primary source](https://ies.ed.gov/ncee/wwc/PracticeGuide/1) · checked 2026-09-23

IES recommends retrieval practice, worked-example/problem alternation, linking concrete with abstract representations, and deep explanatory questions. These educational recommendations inspire question designs; they do not evaluate Jev.

Used by: [HA01]({{ '/human-ai/patterns/ha01/' | relative_url }}), [HA02]({{ '/human-ai/patterns/ha02/' | relative_url }}), [HA03]({{ '/human-ai/patterns/ha03/' | relative_url }}), [HA08]({{ '/human-ai/patterns/ha08/' | relative_url }})

## HL-S2: Use Clear Words

[Read the primary source](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o3p01-clear-words/) · checked 2026-09-23

W3C supplemental guidance recommends explaining jargon and uncommon or application-specific meanings. This motivates detecting an explicitly demonstrated vocabulary mismatch, without inferring disability or reading level.

Used by: [HA05]({{ '/human-ai/patterns/ha05/' | relative_url }})

## HL-S3: Explain Implied Content

[Read the primary source](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o3p12-implicit-explained/) · checked 2026-09-23

W3C recommends nearby explanations for implied or ambiguous material, including metaphors. The proposed pattern checks supplied text only, not reader traits or emotional states.

Used by: [HA07]({{ '/human-ai/patterns/ha07/' | relative_url }})

## HL-S4: What might the content of effective feedback look like in the classroom?

[Read the primary source](https://d2tic4wvo1iusb.cloudfront.net/production/eef-guidance-reports/feedback/Effective_Feedback_Task__Subject_and_Self-regulation_Strategies.pdf) · checked 2026-09-23

EEF distinguishes feedback directed at work, subject processes, or self-regulation from general comments about a person's characteristics. It notes boundaries between productive categories can blur; the proposed question does not force those subcategories.

Used by: [HA04]({{ '/human-ai/patterns/ha04/' | relative_url }})

## HL-S5: Separate Each Instruction

[Read the primary source](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o3p09-separated-instructions/) · checked 2026-09-23

W3C recommends clear separated steps with necessary information included. The referent-ambiguity question is a task-authored specialization of this clarity need, not an explicit W3C test.

Used by: [HA06]({{ '/human-ai/patterns/ha06/' | relative_url }})

## HC-S1: GOV.UK Design System: Start using a service

[Read the primary source](https://design-system.service.gov.uk/patterns/start-using-a-service/) · checked 2026-09-23

The start point should explain what the service does, provide information needed before starting, offer resumption when relevant, and list documents or information needed to complete the process. This motivates checking when a prerequisite is disclosed; it does not validate an AI classifier.

Used by: [HA09]({{ '/human-ai/patterns/ha09/' | relative_url }}), [HA14]({{ '/human-ai/patterns/ha14/' | relative_url }})

## HC-S2: GOV.UK Design System: Question pages

[Read the primary source](https://design-system.service.gov.uk/patterns/question-pages/) · checked 2026-09-23

The guidance says to ask only needed questions, mark optional information, explain why questions are asked, accept uncertainty when valid, and avoid asking for the same information repeatedly within a journey. Patterns apply to known process rules rather than guessing whether personal data is necessary.

Used by: [HA10]({{ '/human-ai/patterns/ha10/' | relative_url }}), [HA12]({{ '/human-ai/patterns/ha12/' | relative_url }})

## HC-S3: W3C WAI: Understanding SC 3.3.3 Error Suggestion

[Read the primary source](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html) · checked 2026-09-23

The explanation distinguishes notifying a user of an input error from providing an appropriate known correction. Suggestions may be withheld if they would jeopardize security or the content's purpose. The proposed pattern checks semantic correction guidance only, not complete WCAG conformance.

Used by: [HA11]({{ '/human-ai/patterns/ha11/' | relative_url }})

## HC-S4: W3C WAI: Provide Human Help

[Read the primary source](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o7p01-human-help/) · checked 2026-09-23

The guidance recommends reachable human help through a mechanism the person prefers, with few steps and without complex menu navigation. The proposed pattern uses an explicitly stated interaction constraint and a supplied support route, never a disability or diagnosis inference.

Used by: [HA13]({{ '/human-ai/patterns/ha13/' | relative_url }})

## HC-S5: W3C WAI: Provide Feedback

[Read the primary source](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o4p10-status-feedback/) · checked 2026-09-23

The guidance recommends explaining the state of each process step. Feedback can orient a returning or interrupted user by showing what happened and where they are in a multi-step process. Actual task status must still come from verified application state.

Used by: [HA14]({{ '/human-ai/patterns/ha14/' | relative_url }})

## HC-S6: Microsoft Research: Guidelines for human-AI interaction design

[Read the primary source](https://www.microsoft.com/en-us/research/blog/guidelines-for-human-ai-interaction-design/) · checked 2026-09-23

The researchers' official summary describes capability disclosure, efficient correction, granular feedback, consequences of user actions, and global controls. It reports that the guidelines were developed and tested for graphical products, not a Jev effectiveness benchmark or blanket voice-interface result.

Used by: [HA15]({{ '/human-ai/patterns/ha15/' | relative_url }}), [HA16]({{ '/human-ai/patterns/ha16/' | relative_url }})

## HC-S7: GOV.UK Design System: Contact a department or service team

[Read the primary source](https://design-system.service.gov.uk/patterns/contact-a-department-or-service-team/) · checked 2026-09-23

The pattern recommends presenting supported contact channels according to user needs, showing availability and expected waits, and avoiding personal information on public social channels. The proposed route-compatibility check does not verify staff availability or contact any service.

Used by: [HA13]({{ '/human-ai/patterns/ha13/' | relative_url }})

## HC-S8: W3C WAI: Use Clear Step-by-step Instructions

[Read the primary source](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o4p07-step-instructions/) · checked 2026-09-23

This guidance recommends complete, clearly located instructions and examples before a user needs to act, rather than introducing requirements only after an error. The patterns target content relationships; no reader ability or disability is inferred.

Used by: [HA09]({{ '/human-ai/patterns/ha09/' | relative_url }}), [HA11]({{ '/human-ai/patterns/ha11/' | relative_url }})

## HD-S1: Guidelines for Human-AI Interaction (Amershi et al., CHI 2019)

[Read the primary source](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/) · checked 2026-09-23

Original research presents18 interaction guidelines, evaluated with49 design practitioners and20 AI-infused products. Guidance motivates correction, user control, and scoped help; it does not evaluate Jev.

Used by: [HA17]({{ '/human-ai/patterns/ha17/' | relative_url }}), [HA18]({{ '/human-ai/patterns/ha18/' | relative_url }}), [HA22]({{ '/human-ai/patterns/ha22/' | relative_url }}), [HA24]({{ '/human-ai/patterns/ha24/' | relative_url }})

## HD-S2: Google PAIR: User Needs + Defining Success

[Read the primary source](https://pair.withgoogle.com/chapter/user-needs/) · checked 2026-09-23

Official design guidance distinguishes augmentation from replacing work people want to do, and warns that narrow reward functions can miss broader outcomes. These are design principles, not empirical Jev performance claims.

Used by: [HA17]({{ '/human-ai/patterns/ha17/' | relative_url }}), [HA19]({{ '/human-ai/patterns/ha19/' | relative_url }}), [HA21]({{ '/human-ai/patterns/ha21/' | relative_url }}), [HA23]({{ '/human-ai/patterns/ha23/' | relative_url }})

## HD-S3: Google PAIR: Feedback + Control

[Read the primary source](https://pair.withgoogle.com/chapter/feedback-controls/) · checked 2026-09-23

Official guidance separates explicit from implicit feedback and warns an interaction does not necessarily mean a lasting preference. It motivates precise interpretation of corrections without profiling the user.

Used by: [HA18]({{ '/human-ai/patterns/ha18/' | relative_url }})

## HD-S4: Google PAIR: Errors + Graceful Failure

[Read the primary source](https://pair.withgoogle.com/chapter/errors-failing/) · checked 2026-09-23

Official guidance describes context errors caused by assumptions about what a person wants, and says failure recovery should give the user a usable path forward. A high-confidence output may still miss the user's situation.

Used by: [HA18]({{ '/human-ai/patterns/ha18/' | relative_url }}), [HA20]({{ '/human-ai/patterns/ha20/' | relative_url }}), [HA24]({{ '/human-ai/patterns/ha24/' | relative_url }})

## HD-S5: Complementarity in Human-AI Collaboration: Concept, Sources, and Evidence (Hemmer et al., v2 2024)

[Read the primary source](https://arxiv.org/abs/2404.00029) · checked 2026-09-23

The authors identify information and capability asymmetry as distinct sources of potential collaboration gains, illustrated in two studies. The paper does not show that every human-AI team improves outcomes.

Used by: [HA20]({{ '/human-ai/patterns/ha20/' | relative_url }})

## HD-S6: Google PAIR: Explainability + Trust

[Read the primary source](https://pair.withgoogle.com/chapter/explainability-trust/) · checked 2026-09-23

Official guidance discusses what and when to explain, the limits of explanations, and calibrated trust. It motivates matching the explanation to the person's explicit question, not inventing model reasoning.

Used by: [HA19]({{ '/human-ai/patterns/ha19/' | relative_url }}), [HA22]({{ '/human-ai/patterns/ha22/' | relative_url }}), [HA23]({{ '/human-ai/patterns/ha23/' | relative_url }})

## HD-S7: Generative AI without guardrails can harm learning: Evidence from high school mathematics (Bastani et al., PNAS 2025)

[Read the primary source](https://doi.org/10.1073/pnas.2422633122) · checked 2026-09-23

An original high-school mathematics study distinguished assisted practice performance from later unaided learning; teacher-designed hint safeguards mitigated negative effects in that setting. This does not establish general tutoring effectiveness or Jev efficacy.

Used by: [HA21]({{ '/human-ai/patterns/ha21/' | relative_url }})

## HD-S8: To Trust or to Think (Buçinca, Malaya and Gajos, CSCW 2021)

[Read the primary source](https://www.eecs.harvard.edu/~kgajos/papers/2021/bucinca2021trust.shtml) · checked 2026-09-23

An original experiment found a tradeoff between overreliance reduction and participants' subjective ratings of cognitive-forcing designs. Explanations alone did not establish appropriate reliance. This is a limitation on simplistic help-quality claims, not a prescription to force extra steps.

Used by: [HA19]({{ '/human-ai/patterns/ha19/' | relative_url }}), [HA22]({{ '/human-ai/patterns/ha22/' | relative_url }})

For API semantics, start with TypeSafe's [documentation index](https://docs.typesafe.ai/llms.txt), [Choice](https://docs.typesafe.ai/primitives/choice), and [confidence](https://docs.typesafe.ai/confidence). Provider documentation defines the primitive, not the validity of these applications.

[Source register JSON]({{ '/human-ai/sources.json' | relative_url }}) · [Research method]({{ '/human-ai/research/' | relative_url }}) · [Collection]({{ '/human-ai/' | relative_url }})
