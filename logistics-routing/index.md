---
layout: default
title: "Logistics routing: patterns for stops, windows, and driver reports"
description: "Eight question contracts for routing text: access constraints in address notes, window expressions, stop instructions, driver-reported deviation causes, reschedule requests, hazardous or temperature-controlled declarations, multi-stop sequence constraints, and address candidates."
permalink: /logistics-routing/
kicker: "8 profiles · 30/32 labels matched · kernel 2.6.0"
---

# Logistics routing

A dispatch desk and its routing software read free text all day: an address note with a gate code or dock hours, a customer asking for a window, a stop note that bans box trucks, a driver explaining why stop six came after stop nine. These eight contracts classify that text so code can file it, extract the expression, or encode the rule. They are synthetic, task-authored designs and their labels are advisory. Distance, time, capacity, and sequencing are computed in code, and the model never chooses a route.

Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.

[Use the kernel]({{ '/kernel/' | relative_url }}) · [Sources]({{ '/logistics-routing/sources/' | relative_url }}) · [Evaluation and disagreements]({{ '/logistics-routing/evaluation/' | relative_url }})

## What the screen established

**24/24 design cases and 6/8 challenge cases** matched their prewritten labels: 30/32 overall. LR03, LR04 remain provisional. All 32 successful request digests replay. No disagreement was rerun, tuned away, or relabeled.

The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.

## Stops and addresses

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LR01 | [Access constraint stated in an address note]({{ '/logistics-routing/patterns/lr01/' | relative_url }}) | Surfaces appointment, hours, and entry-code requirements before the route is built, while code keeps the exact code, the hours comparison, and the booking. |
| LR03 · provisional | [Kind of direction a stop instruction gives the driver]({{ '/logistics-routing/patterns/lr03/' | relative_url }}) | Catches vehicle restrictions that change the assignment before dispatch, instead of leaving them buried in free text the driver reads on arrival. |
| LR06 | [Hazardous or temperature-controlled declaration in order text]({{ '/logistics-routing/patterns/lr06/' | relative_url }}) | Flags declarations to reconcile with the product master before a vehicle and driver are assigned, without letting the model classify goods for regulatory purposes. |
| LR08 | [How many places an address text names]({{ '/logistics-routing/patterns/lr08/' | relative_url }}) | Stops a stop from being geocoded to the wrong one of two places the customer mentioned, and routes multi-place text to a choice or a split in code. |

## Windows and sequence

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LR02 | [Kind of time constraint in a delivery-window request]({{ '/logistics-routing/patterns/lr02/' | relative_url }}) | Separates reading the customer's timing language from calendar arithmetic, which stays in code with the time zone and the route capacity. |
| LR05 | [Reschedule request proposes a time, defers, or cancels]({{ '/logistics-routing/patterns/lr05/' | relative_url }}) | Starts the right flow, confirmation, options, or cancellation, from the message itself while the calendar and availability stay in code. |
| LR07 | [Sequence constraint stated in a multi-stop request]({{ '/logistics-routing/patterns/lr07/' | relative_url }}) | Keeps customer-stated precedence from being lost when stops are entered, while the solver, not the model, computes the sequence. |

## Driver reports

| ID | Question pattern | Intended use |
| --- | --- | --- |
| LR04 · provisional | [Cause a driver's report gives for a route deviation]({{ '/logistics-routing/patterns/lr04/' | relative_url }}) | Codes the day's deviations consistently for the log and the re-plan trigger, without treating the driver's account as verified fact. |

## Start with a small bundle

Start with LR01 (access constraint), LR03 (stop instruction kind), and LR08 (address candidates) when stops are entered, with exact codes, fleet dimensions, and geocoding in code. Add LR02 (window kind) and LR05 (reschedule intent) at the calendar, where code copies the verbatim expression and resolves it. LR07 (sequence constraint) and LR06 (goods declaration) join once the solver and the product master are wired in.

Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.

## Keep the boundary explicit

A label is a reading of text, not a routing decision. Code computes distance, time, capacity, and stop sequence, resolves every date and time expression, matches vehicle restrictions against exact fleet data, stores codes and contact details as exact strings, and measures delays from telematics. The product master and the carrier's regulatory and driver-qualification rules classify hazardous and temperature-controlled goods; LR06 only flags what the order text declares. The dispatcher's own adjustment and the customer's confirmation override any label.

[Exact catalog]({{ '/logistics-routing/catalog.json' | relative_url }}) · [32 frozen fixtures]({{ '/logistics-routing/fixtures.json' | relative_url }}) · [Kernel module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/logistics-routing.md)
