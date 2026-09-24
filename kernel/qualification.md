---
layout: default
title: Qualify a Jev question through its consumer
description: Replay typed Jev answers through side-effect-free consumer code and compare planned dispositions with a baseline.
permalink: /kernel/qualification/
kicker: Kernel v2.7 · shadow replay
---

# Test the decision the application would actually make

A matching label is not enough. The application may use several answers, apply
thresholds, fall back to review, or make an error after Jev has returned. The
qualification kit checks the planned disposition from a **trusted,
side-effect-free consumer** against a separately assigned expectation and the
existing baseline. It cannot send a message, issue a refund, or certify that any
real-world action happened.

The [portable qualification guide](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/qualification.md)
has the sample format and commands. The [mixed contract](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/mixed-contract-example.json)
asks one Choice, one Noul, and one Score over the same named state; the
[example consumer](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/mixed-consumer-example.py)
uses those answers to select a review queue. Its [pilot record](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/assets/mixed-pilot-example.json)
contains three observed Jev 1.13.0 responses to invented messages and one
missing-input case stopped before inference.

The four example dispositions matched their authored expectations; the
baseline dispositions matched one. This is a **synthetic demonstration**, not
a held-out performance estimate. The demo's thresholds have not been calibrated
for any real support operation.

## What a real pilot still needs

Freeze representative, authorized cases and independent labels before inference.
Declare the cost of each error and an allowed review rate, then compare the
consumer's planned actions with the current workflow. Inspect provider failures,
invalid output, contradictory evidence, language differences, and near-boundary
cases. Verify any consequential action and its outcome separately. The replay
reports `held_out_as_declared` only when the caller supplies held-out cases;
it cannot prove that the split or labels were independent.

The historical collection generator remains Choice-only. New mixed-primitive
contracts should start with the portable kernel contract format, rather than
forcing independent truths or ordered judgments into an exclusive Choice label.

[Back to the kernel]({{ '/kernel/' | relative_url }}) ·
[Find a profile]({{ '/catalog/' | relative_url }})
