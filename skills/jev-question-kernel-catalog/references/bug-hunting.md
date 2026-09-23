# Bug-hunting profiles

Use this module to select focused questions for an authorized code review, bug hunt,
or proposed-repair check. It supplements authoring, evidence, and evaluation;
it does not authorize implementation, scans of third-party targets, or a release.

## Choose by failure mechanism

The [48 profiles](https://seabass-up.github.io/jev-workflow-patterns/bug-hunting/)
are grouped as follows. Read the applicable page and its screening limits:

| IDs | Family | Typical evidence |
| --- | --- | --- |
| BH01–BH06 | Concurrency/lifecycle | Owners, callbacks, interleavings, cancellation, lock order |
| BH07–BH12 | Persistence/cache | Transactions, versions, cache scopes, checkpoints, migrations |
| BH13–BH18 | API/data contracts | Null/empty meaning, units, timezones, pagination, normalization |
| BH19–BH24 | UI/interaction | State transitions, submit handlers, focus, keyboard, IME, row identity |
| BH25–BH30 | Resources/performance | Cleanup, queues, retries, blocking work, query counts, telemetry |
| BH31–BH36 | Trust boundaries | Object access, paths, redirects, command args, redaction, revocation |
| BH37–BH42 | Tests/builds/releases | Assertions, mocks, async tests, isolation, imports, artifact identity |
| BH43–BH48 | LLM/agent workflows | Retrieved instructions, call binding, citations, constraints, receipts, loop budgets |

Profiles can overlap and several defects can coexist. Select the smallest relevant
set, not a single winner from all bug categories and not all 48 on every file.
Existing engineering/harness catalogs have related mechanisms; do not claim novelty.

## Assemble connected evidence

Bind the checkout and exact source revision. Include the behavioral contract,
surrounding implementation, callers/callees, guards, relevant tests, and failure path.
For ordering bugs include owner identities and event sequence. For boundaries include
both sides of the boundary. Keep missing context explicit; do not infer an absent guard
from a truncated snippet. Preserve counterevidence and source pointers outside pruning.

Required semantic fields are `contract` and `evidence`. Reject missing required
context locally or report unresolved. Only authorized, minimized source excerpts go
to the approved provider; never credentials or unrelated private history.

Each sample question uses handle `decision`. Give batched questions unique handles,
retain full instructions, and supply the shared state they need. Same-call questions
cannot use one another's answers. Separate unrelated source packets.

## Interpret without promoting evidence

- `risk_supported`: retain a candidate and perform the page's independent check.
  Low confidence does not erase a potentially high-impact lead.
- `counterevidence`: retain a relevant guard or contradictory trace for this path.
  It is not an all-clear and cannot veto an independently reproduced defect.
- `insufficient`: retrieve the specifically missing source or report unresolved.
  Source mismatch, stale state, and provider failure also stay unresolved, separately.

A proposed default follow-up budget is one retrieval plus one re-evaluation when new
evidence exists. Stop unresolved if evidence is unavailable. Repetition without new
evidence is not verification; declared repeatability audits are a separate experiment.

Host code owns exact paths, identities, quantities, clocks, hashes and enforcement.
Jev does not run tests or produce patches. Use applicable security-review procedures
for actual security-sensitive investigations; a model judgment cannot establish
authorization, exploitability, or a prompt-injection boundary.

## Verify and communicate

For a candidate record preserve: pattern/version, file/location, revision, condition,
contract versus observed behavior, evidence IDs, Jev verdict/confidence, missing
context, and next deterministic check. These are host-assembled fields, not additional
model-generated response fields.

Report candidate, source-verified, reproduced, fixed, and verified-fixed distinctly.
Run isolated reproductions or appropriate exact checks; after authorized fixes run
regressions and the relevant broader suite. A proposed recipe is not an executed test.

The catalog's three examples per pattern are textual synthetic scenarios, not
executed faulty/fixed programs or held-out accuracy. BH41 has an unresolved
counterexample disagreement and remains provisional. Read the
[evaluation](https://seabass-up.github.io/jev-workflow-patterns/bug-hunting/evaluation/)
before operational use. Publication does not install these profiles in a harness.
