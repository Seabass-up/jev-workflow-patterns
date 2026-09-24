---
layout: default
title: Public issue-title routing pilot
description: A frozen, held-out shadow replay failed its automatic-disagreement gate.
permalink: /kernel/qualification/public-issue-pilot/
kicker: Kernel qualification · two observed samples · failed gate
---

# A public shadow pilot that did not pass

We tested a frozen question contract and side-effect-free consumer against two
24-title samples from closed public [GitHub CLI issues](https://github.com/cli/cli/issues).
Each sample has twelve issues with the repository's `bug` label and twelve with
`enhancement`; mixed-label issues and PRs were excluded. Only issue titles were
sent to Jev, with no label or expected answer in the provider state. The pilot
did not read private records, change GitHub issues, or make a downstream action.

The first sample, contract, keyword baseline, thresholds, and pass limits were
frozen in [commit `a1ff667`](https://github.com/Seabass-up/jev-workflow-patterns/commit/a1ff667bec15bd9fc878e2e1cbe63acfe9b7a329)
before inference. But candidate titles had been previewed while checking source
availability, so this is a **development screen**, not held-out evidence. A
second, non-overlapping sample was selected from a different API page with
no title preview and frozen in [commit `d49b618`](https://github.com/Seabass-up/jev-workflow-patterns/commit/d49b6185f705660e0d7f15c4ef53d7d1bc3d01a9)
before inference. The contract, baseline, thresholds, and limits stayed unchanged.

| Shadow result | Development screen | Unpreviewed held-out sample | Frozen limit |
| --- | ---: | ---: | ---: |
| Jev matches to repository labels | 15 / 24 | 7 / 24 | Gain ≥ 1 over baseline |
| Keyword baseline matches | 14 / 24 | 4 / 24 | — |
| Jev automatic label disagreements | 5 | 0 | ≤ 1 |
| Jev human review | 4 / 24 | 17 / 24 | ≤ 25% |
| Invalid or failed responses | 0 | 0 | 0 |

The development screen exceeded the automatic-disagreement limit. Jev routed five
`enhancement`-labeled titles to the bug queue: [#14208](https://github.com/cli/cli/issues/14208),
[#14153](https://github.com/cli/cli/issues/14153),
[#14118](https://github.com/cli/cli/issues/14118),
[#14055](https://github.com/cli/cli/issues/14055), and
[#13862](https://github.com/cli/cli/issues/13862). Several of their titles and
bodies describe broken behavior or use a “Describe the bug” template while the
repository labels them `enhancement`. This exposes a target-definition mismatch,
not a reason to tune Jev to disagree with the wording.

The unpreviewed sample had **zero** automatic label disagreements but sent
**17 of 24** titles to review, exceeding the frozen 25% ceiling. Several titles
were one-word strings or unrelated links. Review is sensible for those inputs,
but the sample also shows that a bare `bug`/`enhancement` repository label does
not make every title a valid automatic-routing case. The held-out gate **failed**.
No post-result threshold, label, or sample change was made.

The [contract and fixed policy](https://github.com/Seabass-up/jev-workflow-patterns/tree/main/pilots/github-issue-routing)
use one Choice and one Noul, with an `unclear` option and a human-review fallback.
The [development receipts](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/pilots/github-issue-routing/pilot.json)
and [held-out receipts](https://github.com/Seabass-up/jev-workflow-patterns/blob/main/pilots/github-issue-routing/pilot-held-out.json)
record 48 `jev-1.13.0` responses bound to exact states and questions. The bridge
estimated $0.001077468 for those calls and reported 32.45 seconds of summed
request elapsed time, not the wall-clock time of the four-at-a-time runs. One
earlier model/digest smoke call is excluded.

Repository labels are **not adjudicated gold labels** and are not necessarily
a consistent semantic bug-versus-feature taxonomy. The small, balanced,
title-only samples are not representative of another team's work or all GitHub
CLI issues. The failure blocks this exact title-only policy from automatic
routing; it does not estimate Jev's general bug-classification accuracy. A next
study should define the target with human reviewers, screen eligibility before
sampling, settle ambiguous cases before inference, and use a new held-out set
with an authorized, privacy-screened body excerpt if titles alone are
insufficient. Neither inspected sample can become fresh held-out evidence.

Run `python3 pilots/github-issue-routing/verify_pilot.py` at the repository root
to recheck both samples, baselines, exact receipts, and the deliberately failed
held-out gate. The [source and selection records](https://github.com/Seabass-up/jev-workflow-patterns/tree/main/pilots/github-issue-routing)
retain the issue URLs and label snapshots.
The broader [qualification guide]({{ '/kernel/qualification/' | relative_url }})
explains what shadow replay does and does not prove.
