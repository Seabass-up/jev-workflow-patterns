# Collection pipeline

The scripts that built the domain collections, in the order they run. They need
Python 3 and, for the live steps, the local `jev-workflows` bridge (its path comes
from `JEV_WORKFLOWS_CLI`; the API key stays in the macOS Keychain and is never read
here). Drafts, challenge cases, and browser page records live in a work directory
(`JEV_PATTERNS_WORKDIR`, default `<repo>/.work`, git-ignored).

This historical pipeline supports one Choice answer per profile. For a new
workflow that needs independent Nouls, ordered Scores, or a mixed batch, use the
portable kernel contract and [qualification guide](../../skills/jev-question-kernel-catalog/references/qualification.md).
The authoring specification now compares proposed patterns against all current
collection catalogs; ID validation is dynamic, but semantic novelty remains a
review judgment.

| Step | Script | Needs Jev | What it does |
| --- | --- | --- | --- |
| 1. Author | [AUTHORING-SPEC.md](AUTHORING-SPEC.md) | no | The specification an author (person or agent) follows: contract shape, missing-field precedence, option-count policy, sources with hashes, page metadata, 24 design fixtures, a kernel module draft. |
| 2. Check | `check_authoring.py <folder> [kernel_version]` | no | Structural check of the authored catalog, sources, metadata, design fixtures, and module, with synthetic-content tripwires. |
| 3. Overlap | `overlap_check.py <folder> ["note"]` | yes | Runs the CT08 question over every non-unknown option pair before any fixture is frozen; appends the pass to `<folder>/results/overlap-review.json`. Add precedence sentences where it finds real co-occurrence, then rerun. |
| 4. Challenge | (separate author) | no | A second author who sees only `catalog.json` writes one challenge case per pattern to `<workdir>/challenge_<folder>.json`. |
| 5. Assemble | `finish_collection.py merge <folder>` | no | Merges design and challenge cases into `fixtures.json` and validates them. |
| 6. Screen | `finish_collection.py screen <folder>` | yes | One uncached call per fixture without a receipt into `results/screening.json`, then one recovery call per provider failure into `results/recovery.json`. Append-only: a stored receipt is never replaced, each receipt is saved before the next call, and a receipt that no longer matches its fixture or contract stops the run. Once screened, `merge` refuses to change `fixtures.json`. |
| 7. Finish | `finish_collection.py finish <folder>` | no | Writes `results/summary.json`, installs the evaluator wrappers, copies the kernel module into the skill, and builds the pages. |
| 8. Sources | `source_support.py <folder> ... [--run-id NAME]` | yes | Refetches each source, selects the excerpt with the most distinct summary keywords in code, and asks Jev whether the summary describes the page; writes `results/source-review.json`, or `results/source-review-NAME.json` for a later run. Reviews are never overwritten. Drift is true or false only when the recorded and observed hashes cover the same representation (raw bytes or displayed text); otherwise it is null. |

After step 7, rebuild the hub with `python3 scripts/build_collection_pages.py --hub`
and add a `{"label": "Source support review", "path": "results/source-review.json"}`
entry to the collection's `extra_results` once step 8 has run.

## Pages that block scripted fetches

Some sites return 403 or 404 to `curl`, and some render their text with script so a
fetch contains only a title. Read those pages in a real browser, hash the main text
as displayed, and record them in `<workdir>/browser/pages.json` as
`{"<key>": {"url": ..., "sha256_of_text": ..., "excerpt": ...}}`; `source_support.py`
uses the excerpt in place of a fetch and marks the receipt `browser`. Say so in the
source entry's `fetch_method` (mention the displayed text) so the recorded hash is
compared only with another displayed-text hash. A page whose extracted text is only a
title is unread.

## What the pipeline does not do

It does not decide that a contract is good, that a source is authoritative, or that a
screen qualifies a pattern for use. Disagreements are preserved, never tuned away;
provisional patterns keep them on the evaluation page. Every step that talks to Jev
records the exact request and response.
