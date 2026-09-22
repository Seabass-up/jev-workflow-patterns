---
layout: default
title: "Iteration 1 — 30 useful Jev question patterns"
description: "20 business, engineering and LLM patterns, plus 10 experimental harness designs, with exact contracts and preserved test failures."
permalink: /iterations/01/
kicker: "Research cycle 1 · 2026-09-22"
---

Start with a **question contract**, not a request to “give me good JSON.” Specify the decision the caller will make, supply the evidence that could change it, define mutually understandable answer choices, and decide what happens when the evidence is missing or contradictory. Jev provides the bounded semantic judgment; code controls the workflow.

This collection contains **7 business + 7 engineering + 6 LLM patterns, and 10 additional harness designs**. Every entry includes exact question JSON, a synthetic example, useful follow-ups, deterministic responsibilities, primary references and test status.

## Start with these pilots

1. **B02 — Missing dispatch details:** ask for the first missing location, symptom or access detail.
2. **E02 — Requirement/test coverage:** catch tests that run relevant code without asserting the requested result.
3. **L02 — Claim/citation fit:** flag unsupported qualifiers before an LLM answer is delivered.
4. **B06 — Quote/requirement comparison:** surface omissions and explicit exclusions for a reviewer.
5. **E06 — Installation/test/acceptance separation:** keep reported progress from being promoted to verified acceptance.
6. **H03 — Unresolved-branch handoff:** prevent a summary from turning an open hypothesis into a finding.

This order is a practical judgment about a narrow outcome, reviewability and consequence—not measured ROI. Pilot in shadow mode on authorized, independently labeled real examples before taking operational actions. **H01 is on hold for grounding redesign:** its “plausibility” question accepted invented meanings of “Do it.”

## The 20 core patterns

| ID | Area | Question pattern | Expected practical value |
| --- | --- | --- | --- |
| B01 | business | [Route the current business request]({{ '/iterations/01/patterns/b01/' | relative_url }}) | Reduce transfers between billing, service and estimating queues. |
| B02 | business | [Find the missing dispatch detail]({{ '/iterations/01/patterns/b02/' | relative_url }}) | Ask one useful follow-up before dispatch rather than exchange several vague messages. |
| B03 | business | [Classify an invoice dispute for review]({{ '/iterations/01/patterns/b03/' | relative_url }}) | Send a dispute to the reviewer who can resolve its actual issue. |
| B04 | business | [Compare a requested change with approved scope]({{ '/iterations/01/patterns/b04/' | relative_url }}) | Flag likely added or excluded work before it becomes an undocumented scope change. |
| B05 | business | [Distinguish a firm commitment from an intention]({{ '/iterations/01/patterns/b05/' | relative_url }}) | Keep hoped-for or contingent promises out of a confirmed commitments list. |
| B06 | business | [Check one vendor requirement against a quote]({{ '/iterations/01/patterns/b06/' | relative_url }}) | Expose missing or conflicting inclusions before accepting a quotation. |
| B07 | business | [Review possible duplicate work records]({{ '/iterations/01/patterns/b07/' | relative_url }}) | Reduce double counting while preserving records of genuinely separate visits. |
| E01 | engineering | [Score reported operational impact]({{ '/iterations/01/patterns/e01/' | relative_url }}) | Prioritize review by the described functional impact rather than emotionally strong wording. |
| E02 | engineering | [Check whether a test covers a requirement]({{ '/iterations/01/patterns/e02/' | relative_url }}) | Find tests that exercise the relevant behavior but fail to assert the required outcome. |
| E03 | engineering | [Assess a described interface change against a consumer]({{ '/iterations/01/patterns/e03/' | relative_url }}) | Flag behavior changes that a schema-only check may miss. |
| E04 | engineering | [Choose the next diagnostic evidence source]({{ '/iterations/01/patterns/e04/' | relative_url }}) | Collect the evidence most likely to distinguish the immediate failure before attempting a fix. |
| E05 | engineering | [Separate requirement changes from editorial revisions]({{ '/iterations/01/patterns/e05/' | relative_url }}) | Focus review on wording changes that alter obligations or permitted behavior. |
| E06 | engineering | [Distinguish installation, testing and acceptance evidence]({{ '/iterations/01/patterns/e06/' | relative_url }}) | Keep an installation report from silently becoming a tested or accepted completion record. |
| E07 | engineering | [Check a proposed repair against the reproduced failure]({{ '/iterations/01/patterns/e07/' | relative_url }}) | Catch changes that hide a symptom while leaving the confirmed failure mechanism untouched. |
| L01 | llm | [Rank answer evidence while preserving counterevidence]({{ '/iterations/01/patterns/l01/' | relative_url }}) | Reduce irrelevant LLM context while keeping passages that challenge the question's premise. |
| L02 | llm | [Check a claim against its cited context]({{ '/iterations/01/patterns/l02/' | relative_url }}) | Flag citations that are present but do not actually support the claim. |
| L03 | llm | [Verify an extracted value's meaning and entity]({{ '/iterations/01/patterns/l03/' | relative_url }}) | Catch schema-valid extraction errors where a copied value belongs to the wrong person or field. |
| L04 | llm | [Select an available tool handler]({{ '/iterations/01/patterns/l04/' | relative_url }}) | Keep simple calculations and lookups out of a large reasoning call while respecting actual tool availability. |
| L05 | llm | [Choose the clarification that unlocks a useful answer]({{ '/iterations/01/patterns/l05/' | relative_url }}) | Convert vague LLM requests into a specific target, success condition and compatible constraint set. |
| L06 | llm | [Classify a proposed memory update]({{ '/iterations/01/patterns/l06/' | relative_url }}) | Avoid overwriting a remembered fact with unrelated or conflicting new evidence. |

## The 10 experimental harness designs

“New” means a proposed Jev composition added to this catalog. Clarification, loop detection, compaction, failure classification and notification policies all have prior art. This is **not** a claim of global novelty.

| ID | Harness design | What it changes |
| --- | --- | --- |
| H01 | [Proceed only when ambiguous interpretations share a safe next read]({{ '/iterations/01/patterns/h01/' | relative_url }}) | Avoid interrupting the user when unresolved meaning cannot change the next permitted evidence-gathering step. |
| H02 | [Detect semantic stalls against the unresolved question]({{ '/iterations/01/patterns/h02/' | relative_url }}) | Catch rephrased evidence loops that do not produce diagnostic progress. |
| H03 | [Keep unresolved branches unresolved during handoff]({{ '/iterations/01/patterns/h03/' | relative_url }}) | Prevent a compacted summary from silently turning a hypothesis into a finding. |
| H04 | [Route reviewer disagreement by what would resolve it]({{ '/iterations/01/patterns/h04/' | relative_url }}) | Avoid majority voting when reviewers are judging different facts, subjects or preferences. |
| H05 | [Repair the demonstrated question defect, not the whole prompt]({{ '/iterations/01/patterns/h05/' | relative_url }}) | Turn a failed Jev judgment into a bounded, auditable repair target. |
| H06 | [Keep illustrative values out of real tool arguments]({{ '/iterations/01/patterns/h06/' | relative_url }}) | Catch an LLM copying a sample path or record value from documentation into a real operation. |
| H07 | [Notify only when a change matters to the user's next decision]({{ '/iterations/01/patterns/h07/' | relative_url }}) | Reduce repetitive status messages while preserving completion, blockers and changed risks. |
| H08 | [Prefer a diagnostic check that separates competing hypotheses]({{ '/iterations/01/patterns/h08/' | relative_url }}) | Spend the next tool call on evidence that could actually change the diagnosis. |
| H09 | [Separate required work from attractive scope expansion]({{ '/iterations/01/patterns/h09/' | relative_url }}) | Keep an agent's step budget focused on the accepted outcome. |
| H10 | [Reopen recommendations whose premise is undermined]({{ '/iterations/01/patterns/h10/' | relative_url }}) | Keep previously delivered advice from silently surviving contradictory new evidence. |

## Evidence and reusable artifacts

- [Evaluation, failures and limitations]({{ '/iterations/01/evaluation/' | relative_url }})
- [Question-design kernel and follow-up policy]({{ '/iterations/01/question-kernel/' | relative_url }})
- [Primary sources and bounded novelty comparison]({{ '/iterations/01/sources/' | relative_url }})
- [Machine-readable current catalog]({{ '/iterations/01/catalog.json' | relative_url }})
- [Frozen contracts and fixtures by screen]({{ '/iterations/01/screens.json' | relative_url }})
- [Source directory, raw receipts and offline tests](https://github.com/Seabass-up/jev-workflow-patterns/tree/main/iterations/01)

The initial core screen matched **76/81** fixtures; targeted refinement matched **15/15** (8 reused cases and 7 new diagnostic cases); the harness screen matched **38/40**. All **136** request digests were independently recomputed against the preserved state and question contract. These are small author-labeled synthetic checks, not production accuracy or calibration.
