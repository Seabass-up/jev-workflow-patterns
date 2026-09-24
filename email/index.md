---
layout: default
title: Twelve Jev Email Patterns
description: Typed email judgments with explicit uncertainty, bounded follow-up, and synthetic test receipts.
permalink: /email/
kicker: 12 email profiles · introduced in kernel v2.1
---

# Better questions for email workflows

These 12 profiles help Jev distinguish the meaning of email evidence before a person or application decides what to do. They supplement the 120 research-catalog questions; the three foundational workflow guides remain separate. No mailbox integration or sending capability is installed by this catalog.

| ID | Pattern | Useful answer |
| --- | --- | --- |
| EM01 | [Who is being asked to reply?]({{ '/email/patterns/em01/' | relative_url }}) | Prioritize requests directed to the mailbox owner without treating every CC as an assignment. |
| EM02 | [Current request or quoted history?]({{ '/email/patterns/em02/' | relative_url }}) | Prevent old quoted instructions from becoming new tasks. |
| EM03 | [Material change in a thread]({{ '/email/patterns/em03/' | relative_url }}) | Surface a new instruction or changed fact without treating repeated wording as progress. |
| EM04 | [Firm commitment or tentative intent]({{ '/email/patterns/em04/' | relative_url }}) | Identify promised work while preserving conditions and tentative statements. |
| EM05 | [What does the date mean?]({{ '/email/patterns/em05/' | relative_url }}) | Separate requested deadlines from estimates and references to past events. |
| EM06 | [Scheduling response meaning]({{ '/email/patterns/em06/' | relative_url }}) | Distinguish accepting an offered slot from proposing a different one. |
| EM07 | [Attachment delivery claim]({{ '/email/patterns/em07/' | relative_url }}) | Detect whether a sender claims a file is attached, linked, or still forthcoming. |
| EM08 | [Does the draft answer this request?]({{ '/email/patterns/em08/' | relative_url }}) | Check a draft against each explicit request item before a person approves it. |
| EM09 | [Who is waiting on whom?]({{ '/email/patterns/em09/' | relative_url }}) | Identify which side has the next stated step in a thread. |
| EM10 | [Meaning of an automatic response]({{ '/email/patterns/em10/' | relative_url }}) | Keep absence notices and transport reports from being mistaken for substantive replies. |
| EM11 | [Invoice question or dispute?]({{ '/email/patterns/em11/' | relative_url }}) | Route invoice emails to explanation, correction, or payment-status review. |
| EM12 | [Close, reopen, or keep waiting?]({{ '/email/patterns/em12/' | relative_url }}) | Recognize when a reply withdraws a request or reopens it with unresolved work. |

## Use them with the kernel

[Start with the kernel]({{ '/kernel/' | relative_url }}) and its [portable email module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/email.md). Each pattern has named state fields, exact Choice instructions and labels, an unknown outcome, code-owned controls, a drill-down plan, and three frozen examples.

For an incoming scheduling email, EM01 identifies the requested respondent, EM05 classifies a candidate date's meaning, and EM06 interprets the proposed slot response. They can run independently in one request if code builds one state containing all required context. Rename their question handles to `reply_owner`, `date_role`, and `slot_response` to avoid overwriting the shared example handle `decision`. Each still needs its full instructions. None sees another question's answer.

For a draft reply, evaluate each original request item with EM08. An `answered` label means the draft addresses the request; it does not prove the answer is true, authorized, or delivered. Use the kernel's evidence module for factual support.

## Evidence before inference

Code must bind the actual message, mailbox, thread revision, recipient identities, and any attachment inventory. Keep current text separate from quoted history; treat uncertain segmentation as uncertain evidence. Do not treat a copied recipient as the responsible owner, an attachment claim as an actual file, an automatic acknowledgment as a human response, or a reported resolution as verified completion.

Unknown, conflicts, stale evidence, and low confidence belong in a review path. Choose confidence thresholds against your own labeled data and error costs, not the numbers in this small screen. Confidence is a distribution summary, not permission or proof.

## Test evidence

Initial versions matched **34/36** synthetic fixtures. EM07 and EM08 confused empty evidence with a negative category. Explicit missing-input precedence in v2 matched all six targeted reruns, giving a selected current set of **36/36**. All **42** request/response bindings are replayable; original misses remain published.

[Evaluation and limitations]({{ '/email/evaluation/' | relative_url }}) · [Catalog JSON]({{ '/email/catalog.json' | relative_url }}) · [Fixtures]({{ '/email/fixtures.json' | relative_url }}) · [Sources]({{ '/email/sources/' | relative_url }})

The screen uses synthetic English text only. It is not a held-out accuracy, calibration, security, deliverability, or financial/legal qualification. These are task-authored adaptations, not claims of global novelty. Reading or installing the skill does not authorize inbox access, labels, forwarding, sending, payment, or closure.
