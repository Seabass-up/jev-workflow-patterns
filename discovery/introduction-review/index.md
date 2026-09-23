---
layout: default
title: "TypeSafe introduction review: pattern candidates"
description: "A detailed review of the TypeSafe introduction and its linked pages, measured against preserved Jev receipts, with nine pattern candidates and an advisory duplicate screen."
permalink: /discovery/introduction-review/
kicker: "Discovery · candidates for a possible Iteration 5"
---

# What the introduction adds to the catalog

Reviewed 2026-09-22. This page records a review of the TypeSafe
[introduction](https://docs.typesafe.ai/introduction) and every page it links to,
plus official pages this repository had not cited before. Claims were checked against
the preserved Jev receipts in this repository.

<div class="callout warning">
  <p><strong>Candidates, not a catalog.</strong> Nothing here has question contracts, frozen fixtures, or screening receipts. This is not an activated iteration: the four-iteration loop state is unchanged. The candidates need the usual contract, fixture, and live-screen cycle before any of them becomes a pattern.</p>
</div>

## What was new to read

The ten pages Iteration 4 hashed returned identical SHA-256 values (both digests are
recorded for each), and the index was still 16,013 characters. The documentation has not changed since then, and all 18
cookbooks are already cited by Iterations 1–4. The unmined material was the
introduction and its neighbours: quick start, AI primer, coding agents, the
[build guide](https://docs.typesafe.ai/concepts/how-to-build-with-system-one), models,
the agent skill page, and the smart-home demo. Hashes for every page read are in
[sources.json]({{ '/discovery/introduction-review/sources.json' | relative_url }}).

## The introduction's claims against preserved receipts

Measurements replay offline from 25 hash-pinned receipt and catalog files:
[measurements.json]({{ '/discovery/introduction-review/measurements.json' | relative_url }}).

| Claim | What the receipts show |
| --- | --- |
| Adding questions barely changes response time | **Supported.** Across 481 uncached calls, latency does not correlate with question count (r = −0.02). A 30-question, 9,294-token request took 486 ms; single-question calls had a median of 540 ms. |
| Most queries complete in about 100 ms (build guide) | **Not what this client sees.** Client-observed time, including network, had a median of 547 ms and a 90th percentile of 777 ms. Budget real-time paths on observed time. |
| More questions do not cause context rot | **True only for questions.** The [Jev 1.13 limitations page](https://docs.typesafe.ai/model-jaggedness/jev-1.13) says irrelevant *state* costs accuracy. Cap state size, not question count. |
| Ask many questions in one request (build guide) | **Not yet exercised here.** 413 of 481 calls (86%) asked one question. Batch invariance on these fixtures is untested. |

## Choice confidence depends on option count

The [confidence page](https://docs.typesafe.ai/confidence) shows
`(3 × largest probability − 1) / 2` as an approximation for three options. Generalized
to `(n × top probability − 1) / (n − 1)`, it matches all 447 stored Choice answers
(2–6 options) within 0.020. 351 are consistent with two-decimal rounding of the
formula (within 0.005) and 431 are within 0.01. The quick-start example (0.85 across
three options) gives 0.775, which the page reports as 0.78. Sixteen differences exceed
what rounding both the confidence and the top probability can explain, so treat the
formula as a close observed approximation, not the provider's definition.

Consequences for existing patterns:

- **A flat threshold is not one standard.** 53 Iteration 1–2 patterns use a 0.8
  floor across Choice questions with 2–6 options. That floor requires a top
  probability of 0.90 (2 options), 0.867 (3), 0.85 (4), 0.84 (5), or 0.833 (6).
- **Adding a no-match option makes the gate easier to pass.** At a top probability of
  0.85, three options give 0.775 confidence and four give 0.80.
- **Confidence ignores the runner-up.** Whether the remaining probability sits on an
  option with the same downstream action is visible only in the probabilities.

Score confidence does not follow this form. Across 74 unique Score answers it differs
by up to 0.333; an even split between the two extreme levels,
`[0.48, 0, 0.02, 0.5]`, has confidence 0. No simple variance or entropy form fitted.

**Applied now:** Kernel skill 2.2.0 adds
[`check_confidence.py`](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/scripts/check_confidence.py),
which checks stored Choice confidence against probabilities and converts thresholds
between option counts. CI runs it over every preserved receipt. The
[authoring](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/authoring.md)
and [evaluation](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/evaluation.md)
modules carry the threshold and model-version guidance. Historical catalogs and
their thresholds are unchanged.

## Nine candidates and their screen

A single Jev call compared each candidate with a reviewer-chosen shortlist of the
nearest prior patterns: one Choice for the nearest, one Score for overlap. It used 18
questions, 6,383 input tokens, and 762 ms. Every flagged overlap was then checked by
reading the prior pattern. The receipt, including where host judgment differs from
Jev, is in
[duplicate-screen.json]({{ '/discovery/introduction-review/duplicate-screen.json' | relative_url }}).

| ID | Candidate | Source | Jev nearest | Disposition |
| --- | --- | --- | --- | --- |
| C1 | Confidence gate adjusted for option count | Confidence page, receipts | none close (0.79) | **Lead candidate** |
| C2 | Tool-call trace audit split between code and Jev | Build guide | E23 (0.81) | Retain as a composition of L04 and E23; lower priority |
| C3 | Compound-request split and re-ask | Smart-home demo | none close (0.62; H28 0.30) | Retain |
| C4 | Email phishing signals with veto | Build guide | H24 (0.99) | Reclassify as an email profile that applies H24 |
| C5 | Language-aware confidence gate | Models page | none close (0.84) | Retain |
| C6 | Model-alias movement canary | Models page | H35 (0.49) / H21 (0.35) | Fold into kernel evaluation guidance (done) |
| C7 | Label bootstrap from several reasoning models | Build guide | none close (0.82) | Retain, adjacent to H38 |
| C8 | Question packer under two context limits | Models page | none close (0.72), overlap unclear | Fold into H28 as concrete limits |
| C9 | Question/negation ambiguity probe | Limitations page | none close (0.90) | Retain as experimental |

The screen is advisory. Shortlists were chosen by the reviewer, so Jev could not find a
closer pattern omitted from them. This is not a prior-art or novelty search.

**Kernel review of the screen questions.** Checked afterwards against the kernel's
authoring module, the screen has four design defects:

- The overlap Score asks Jev to find the closest listed pattern and then rate it. That
  is two hops; ask one question per candidate–pattern pair and take the maximum in code.
- Choice options name a pattern ID and title, while its description sits only in
  state. Point each option at its `shortlists.Cn.<ID>.purpose` path.
- There is no outcome for descriptions too thin to compare, so thin evidence can
  read as `none_close`. Add an explicit insufficient-description option.
- No uncertainty policy was declared before the call; every disposition came from
  review afterwards. A repeated screen needs a declared contract and thresholds
  stated with their option counts.

A version 2 screen should fix these and keep this receipt as version 1.

## Candidate details

### C1 · Confidence gate adjusted for option count

**Mechanism.** Code stores each threshold with the option set it was tuned on,
converts it to the implied top probability, and re-tunes when options change. Where
options share a downstream action, code sums their probabilities before gating.
**Jev judges** the unchanged Choice. **Screen first:** paired contracts that differ
only by an added `insufficient` option, and cases whose runner-up shares or does not
share the winner's action. **Delta:** H11 falls back to a taxonomy parent and H32
audits agreement across repeats; neither normalizes thresholds by option count.

### C2 · Tool-call trace audit split between code and Jev

**Mechanism.** The build guide decomposes a weather trace into nine yes/no questions.
Six are exact checks the limitations page assigns to code: call/result ID match, two
schema conformance checks, coordinate equality, date equality, and unit equality.
**Code owns** those plus the missing result for the second call. **Jev judges** only
whether each tool suits the request and whether a free-text argument refers to the
requested entity. **Delta:** E23 judges field pairing inside one assembled record; L04
selects a handler before a call. The new element is the partition over a multi-call
trace.

### C3 · Compound-request split and re-ask

**Mechanism.** A yes/no question detects several distinct actions. An LLM splits the
request, code caps the number of commands, and Jev checks that the commands jointly
cover the request and add nothing. Each command then goes through the ordinary routing
questions; multi-action execution needs confirmation. **Delta:** H28 batches
independent questions; it neither splits a request nor checks split coverage.

### C4 · Email phishing signals (email profile)

**Mechanism.** Separate questions for credential request, unexpected reward, time
pressure, the organization a display name claims, and the destination link text
claims. Code parses the sender and link domains. **Why a veto:** in the build guide's
weighted composite, a credential request alone scores 0.45. That lands in the
0.4–0.6 human-review band instead of quarantine. H24's non-compensable veto fixes
this, so C4 is an email-domain application of H24.

### C5 · Language-aware confidence gate

**Mechanism.** Code detects input language before inference. Non-English input gets
stricter thresholds, review, or a translate-then-ask path that keeps the translation
as provenance. **Source:** the models page states English accuracy is best and asks
for extra attention to confidence elsewhere. **Screen first:** matched English and
non-English fixtures; the email evaluation notes no non-English set was tested.

### C7 · Label bootstrap from several reasoning models

**Mechanism.** When no labels exist, several reasoning models label a sample. Code
keeps agreed labels with provenance, measures label noise on a small human-labelled
holdout, and only then trains on Jev probability features. **Delta:** H38 governs
feature provenance and holdout evaluation but assumes labels exist. Evaluate Jev
against labels produced under a different framing from the questions.

### C9 · Question/negation ambiguity probe (experimental)

**Mechanism.** At design time only, ask a proposition and its literal negation as two
yes/no questions. A large departure of their sum from one may flag wording for a
literal rewrite. The limitations page reports 0.72 + 0.47 = 1.19 for one ticket and
warns the pair need not be comparable. Validate that large departures actually
predict wording defects before using the probe; it is never a runtime correctness signal.

### Folded refinements

- **C6:** a changed returned `model` version is now a drift trigger in the kernel
  evaluation module: hold threshold-gated automation, rerun frozen fixtures,
  re-qualify, and pin the versioned ID where thresholds were tuned.
- **C8:** the models page gives two limits, 64k tokens for state plus all questions
  and 32k for state plus the single longest question. They are concrete values for
  the budget H28 already leaves to code. Record them per model version.

## Other notes from the reviewed pages

- The agent skill page recommends taking the highest-probability option without a
  threshold when only the best option matters. For statistical algorithms, use
  probabilities rather than confidence.
- Choice accepts at most 255 options; Score accepts 2–10 levels. Pricing is per input
  token; output is free.
- The confidence page promises a later cookbook on alternative confidence measures.
  It was not published at review time.

## Reproduce

```sh
python3 discovery/introduction-review/measure.py
python3 skills/jev-question-kernel-catalog/scripts/check_confidence.py iterations email discovery
```

[Measurement script](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/discovery/introduction-review/measure.py)
· [Sources]({{ '/discovery/introduction-review/sources.json' | relative_url }})
· [Duplicate screen]({{ '/discovery/introduction-review/duplicate-screen.json' | relative_url }})
· [Kernel]({{ '/kernel/' | relative_url }})

These are measurements of synthetic screening receipts from jev-1.13.0. They are not
accuracy, calibration, or production latency claims, and the candidates carry no
novelty claim.
