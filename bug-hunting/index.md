---
layout: default
title: 48 Jev Bug-Hunting Patterns
description: Distinct bug-hunting use cases with typed hypotheses, counterexamples, evidence requirements and independent checks.
permalink: /bug-hunting/
kicker: Eight families · 48 profiles · introduced in kernel v2.2
---

# Ask about a specific failure, not whether the code is good

These 48 bug-hunting profiles cover different failure mechanisms and verification paths. At their introduction, they brought the research, email, and bug-hunting groups to 180 profiles. The [current complete catalog]({{ '/catalog/' | relative_url }}) includes later additions; the three foundational workflow guides remain separate. Related mechanisms intentionally overlap; the profiles are not a claim of worldwide novelty.

Each page contains an explicit hypothesis, required evidence, exact Choice JSON, counterexample, bounded follow-up, and a proposed independent check. Use the [kernel]({{ '/kernel/' | relative_url }}) and its [bug-hunting module](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/skills/jev-question-kernel-catalog/references/bug-hunting.md) to adapt them.

## What the answer means

| Typed label | Appropriate next step | What it does not establish |
| --- | --- | --- |
| `risk_supported` | Retain a candidate; inspect the path and reproduce | A verified finding, severity, or permission to fix |
| `counterevidence` | Preserve the shown guard/contradiction | A bug-free file, complete review, or security guarantee |
| `insufficient` | Retrieve specific missing context or report unresolved | A negative finding or reason to erase stronger evidence |

Several bugs can coexist. Ask independent questions, rather than one exclusive Choice among all 48 bug categories. Batch only when questions share the relevant state; select a few applicable profiles instead of sending every profile for every file.

## Screening result and limits

The authored three-case screen produced 143/144 matching labels after two one-time service-error recoveries. **BH41 remains provisional:** its compliant-installation example returned insufficient. No question was tuned and no expected label was changed after inference. The 146 screening attempts include two HTTP 529 responses; all 144 successful request digests replay. Version 2 (September 26, 2026) states a tie-break for evidence that shows both a violating path and a relevant guard; the unchanged 144 scenarios were re-screened once against it with 143/144 matches and the same BH41-2 disagreement.

These scenarios are natural-language descriptions of implementation or event behavior, not executed buggy/fixed programs. Passing them does not demonstrate that Jev will discover hidden bugs in a real repository. The per-pattern reproduction recipes are future verification steps, not completed tests. [Read the full evaluation]({{ '/bug-hunting/evaluation/' | relative_url }}).

## Concurrency and lifecycle

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH01 | [Stale async result ownership]({{ '/bug-hunting/patterns/bh01/' | relative_url }}) | Control completion order with deferred promises; assert the final displayed identity. |
| BH02 | [Cancellation without propagation]({{ '/bug-hunting/patterns/bh02/' | relative_url }}) | Cancel while a child is blocked; check termination and post-cancel writes. |
| BH03 | [Retry duplicates an uncertain side effect]({{ '/bug-hunting/patterns/bh03/' | relative_url }}) | Drop the acknowledgement after commit in a stub; assert effect count and stable key. |
| BH04 | [Check-then-act race]({{ '/bug-hunting/patterns/bh04/' | relative_url }}) | Synchronize contenders at the read boundary; assert exactly one owner. |
| BH05 | [Lock-order inversion]({{ '/bug-hunting/patterns/bh05/' | relative_url }}) | Use a bounded two-worker barrier test; capture lock ownership on timeout. |
| BH06 | [Callback outlives its owner]({{ '/bug-hunting/patterns/bh06/' | relative_url }}) | Mount/dispose repeatedly and emit an event; assert listener count and no disposed mutation. |

## Persistence and cache

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH07 | [Partial multi-record commit]({{ '/bug-hunting/patterns/bh07/' | relative_url }}) | Inject failure between writes and read both records from a fresh connection. |
| BH08 | [Lost update]({{ '/bug-hunting/patterns/bh08/' | relative_url }}) | Run concurrent edits from one revision; verify preserved fields or explicit conflict. |
| BH09 | [Cross-tenant cache collision]({{ '/bug-hunting/patterns/bh09/' | relative_url }}) | Use synthetic tenants with same item ID; assert isolation on cold and warm paths. |
| BH10 | [Stale cache after mutation]({{ '/bug-hunting/patterns/bh10/' | relative_url }}) | Warm cache, mutate, then read through the real cache path. |
| BH11 | [Crash-unsafe checkpoint]({{ '/bug-hunting/patterns/bh11/' | relative_url }}) | Crash at each durability boundary and compare replayed item IDs to committed results. |
| BH12 | [Migration breaks old readers]({{ '/bug-hunting/patterns/bh12/' | relative_url }}) | Run old and new reader contracts against each intermediate migration state. |

## API and data contracts

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH13 | [Null versus missing conflation]({{ '/bug-hunting/patterns/bh13/' | relative_url }}) | Send missing, null, and populated patches and read stored values. |
| BH14 | [Empty versus failed result conflation]({{ '/bug-hunting/patterns/bh14/' | relative_url }}) | Inject network error and compare user-visible outcome with a successful empty lookup. |
| BH15 | [Unit mismatch across a boundary]({{ '/bug-hunting/patterns/bh15/' | relative_url }}) | Use a fake clock and assert actual deadline; validate conversion in code. |
| BH16 | [Timezone lost in serialization]({{ '/bug-hunting/patterns/bh16/' | relative_url }}) | Round-trip an instant across zones with a date library; compare epoch values in code. |
| BH17 | [Unstable pagination boundary]({{ '/bug-hunting/patterns/bh17/' | relative_url }}) | Create tied sort keys, traverse all pages, and compare exact IDs with a snapshot baseline. |
| BH18 | [Unicode normalization mismatch]({{ '/bug-hunting/patterns/bh18/' | relative_url }}) | Use composed/decomposed fixtures and compare normalized identifiers in code. |

## UI and interaction

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH19 | [Optimistic update never rolls back]({{ '/bug-hunting/patterns/bh19/' | relative_url }}) | Reject the save and inspect displayed value, status, and retry behavior. |
| BH20 | [Double submit before disable]({{ '/bug-hunting/patterns/bh20/' | relative_url }}) | Dispatch rapid click and keyboard activation; assert one outbound operation. |
| BH21 | [Focus lost after modal close]({{ '/bug-hunting/patterns/bh21/' | relative_url }}) | Open and close with keyboard; assert activeElement and reachable next action. |
| BH22 | [Keyboard-only interaction gap]({{ '/bug-hunting/patterns/bh22/' | relative_url }}) | Traverse and activate using only keyboard; verify the actual action result. |
| BH23 | [IME composition treated as submit]({{ '/bug-hunting/patterns/bh23/' | relative_url }}) | Replay compositionstart, composing Enter, compositionend, and ordinary Enter. |
| BH24 | [Row identity follows position]({{ '/bug-hunting/patterns/bh24/' | relative_url }}) | Edit one row, reorder, and assert draft and saved target identity. |

## Resources and performance

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH25 | [Connection leak on exception]({{ '/bug-hunting/patterns/bh25/' | relative_url }}) | Inject query failures repeatedly; verify pool availability returns to baseline. |
| BH26 | [Backpressure ignored]({{ '/bug-hunting/patterns/bh26/' | relative_url }}) | Throttle consumer and measure queue bound plus producer behavior. |
| BH27 | [Retry storm synchronization]({{ '/bug-hunting/patterns/bh27/' | relative_url }}) | Use seeded fake time and failing stub; count attempts and inspect retry schedule in code. |
| BH28 | [Blocking work on an event loop]({{ '/bug-hunting/patterns/bh28/' | relative_url }}) | Run a heartbeat alongside representative parsing and measure scheduling delay. |
| BH29 | [N-plus-one fetching]({{ '/bug-hunting/patterns/bh29/' | relative_url }}) | Trace query counts for small and large lists; compare with the declared query budget. |
| BH30 | [High-cardinality telemetry]({{ '/bug-hunting/patterns/bh30/' | relative_url }}) | Generate varied IDs and count unique label sets against the allowed dimensions. |

## Trust and boundary checks

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH31 | [Object authorization omitted]({{ '/bug-hunting/patterns/bh31/' | relative_url }}) | Use two synthetic principals and objects in an authorized local test; assert denial. |
| BH32 | [Path containment checked too early]({{ '/bug-hunting/patterns/bh32/' | relative_url }}) | In an isolated temp tree, test parent segments and symlinks; verify actual opened target. |
| BH33 | [Redirect changes outbound destination]({{ '/bug-hunting/patterns/bh33/' | relative_url }}) | Use local controlled redirect endpoints; assert forbidden destination is never contacted. |
| BH34 | [User data enters command syntax]({{ '/bug-hunting/patterns/bh34/' | relative_url }}) | Use harmless metacharacter fixtures in a local stub; assert exact argv and no extra execution. |
| BH35 | [Secrets copied into diagnostics]({{ '/bug-hunting/patterns/bh35/' | relative_url }}) | Capture test logs with synthetic sentinel credentials; assert sentinel absence. |
| BH36 | [Permission revocation missed by a cache]({{ '/bug-hunting/patterns/bh36/' | relative_url }}) | Grant, warm cache, revoke, then attempt the same protected operation. |

## Tests, builds and releases

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH37 | [Test has no outcome assertion]({{ '/bug-hunting/patterns/bh37/' | relative_url }}) | Introduce a controlled wrong-result mutation; confirm test fails for that reason. |
| BH38 | [Mock bypasses the changed logic]({{ '/bug-hunting/patterns/bh38/' | relative_url }}) | Use coverage plus a targeted mutation to prove the branch influences assertions. |
| BH39 | [Async assertion not awaited]({{ '/bug-hunting/patterns/bh39/' | relative_url }}) | Force a delayed rejection and confirm the test runner marks failure. |
| BH40 | [Global state contaminates tests]({{ '/bug-hunting/patterns/bh40/' | relative_url }}) | Run tests in reversed/random order and individually; compare outcomes. |
| BH41 | [Installed entry point uses stale code]({{ '/bug-hunting/patterns/bh41/' | relative_url }}) | Inspect executable resolution and module origin; exercise the actual installed command. |
| BH42 | [Artifact differs from qualified build]({{ '/bug-hunting/patterns/bh42/' | relative_url }}) | Compute artifact digests before upload and after download; compare in code. |

## LLM and agent workflows

| ID | Pattern | What to verify independently |
| --- | --- | --- |
| BH43 | [Retrieved text promoted to instructions]({{ '/bug-hunting/patterns/bh43/' | relative_url }}) | Use inert injected instructions in a local harness and assert no unauthorized tool dispatch. |
| BH44 | [Tool result bound to wrong call]({{ '/bug-hunting/patterns/bh44/' | relative_url }}) | Reverse tool completion order and assert result-to-call identity. |
| BH45 | [Claim cites unrelated evidence]({{ '/bug-hunting/patterns/bh45/' | relative_url }}) | Verify source identity and exact span, then inspect claim support with counterevidence. |
| BH46 | [Mandatory context pruned]({{ '/bug-hunting/patterns/bh46/' | relative_url }}) | Mark a low-relevance constraint mandatory; force a small budget and assert retention or refusal. |
| BH47 | [Completion reported without readback]({{ '/bug-hunting/patterns/bh47/' | relative_url }}) | Stub accepted-but-not-applied response; assert status remains pending or unknown. |
| BH48 | [Unbounded clarification loop]({{ '/bug-hunting/patterns/bh48/' | relative_url }}) | Feed persistent unknown or provider failure; assert bounded calls and unresolved outcome. |

## A practical first pass

For an async UI bug, begin with BH01 (late results), BH02 (cancellation), and BH06 (disposed owners) over the same connected lifecycle packet. For suspicious persistence, choose BH07 (partial commit), BH08 (lost update), and BH11 (checkpoint ordering). For an agent that reports success too early, use BH44 (call/result binding) and BH47 (completion evidence).

Keep required constraints, counterevidence, and high-impact leads visible. Use source-bound candidates and tests to decide findings; the catalog does not authorize repository changes, scanning third-party targets, release, or other external actions.

[All exact questions]({{ '/bug-hunting/catalog.json' | relative_url }}) · [144 frozen scenarios]({{ '/bug-hunting/fixtures.json' | relative_url }}) · [Evaluation]({{ '/bug-hunting/evaluation/' | relative_url }}) · [Sources]({{ '/bug-hunting/sources/' | relative_url }})
