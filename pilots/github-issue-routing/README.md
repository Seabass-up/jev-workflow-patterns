# Public GitHub issue-title shadow pilot

This exploratory pilot asks whether a narrow Jev contract can plan `bug_queue`,
`enhancement_queue`, or `human_review` from public GitHub CLI issue titles. It makes
**no GitHub issue changes**. Repository `bug` and `enhancement` labels are
independent comparison targets, not adjudicated ground truth. Some enhancement
issues describe malfunctioning existing behavior; disagreement may reflect label
policy or missing body context rather than a model error.

Two 24-case samples were frozen before their respective provider calls: the
first 12 eligible closed non-PR issues in each exclusive label query from API
page 1, then the same rule on page 2, created before 2026-09-01 UTC. The API
was queried on 2026-09-24. Candidate titles from page 1 had been previewed
while checking source availability, so `sample-frozen.json` and `pilot.json`
are a **development screen**, not held-out evidence. Page 2 titles were not
previewed before `sample-held-out.json` was committed at `d49b618`, and the
question and policy remained unchanged; `pilot-held-out.json` is the separate
held-out replay. No case overlaps between the samples. Only the title is used
as state. Mixed `bug`+`enhancement` labels, PRs, and titles containing an email
address or obvious credential string were excluded. No issue body, author
identity, or repository label was sent to TypeSafe. The source JSON records
the issue URL, title, creation timestamp, labels, expected route, and baseline.

The baseline was frozen before inference: lower-case title matching. Bug cues are
`crash`, `panic`, `fail`, `error`, `bug`, `broken`, `incorrect`, `wrong`, `ignore`,
`missing`, `doesn't`, `does not`, `cannot`, `can't`, `unable`, `not found`, `empty`,
`silently`, `unexpected`, `lose`, `throttle`, `flash`, or `still requires`; bug
has precedence. Otherwise, titles beginning with `add`, `allow`, `support`,
`enable`, `make`, `update`, `show`, `tell`, or `ability` route to enhancement.
Other titles route to human review. This is a deliberately simple, useful baseline,
not a trivial all-review comparator.

Predeclared consumer thresholds are in `consumer.py`: selected Choice probability
at least 0.80, Choice confidence at least 0.50, and a corroborating Noul at least
0.70 for bug or at most 0.30 for enhancement. Everything else goes to review.
The predeclared *exploratory* pass gate is at least 24 held-out cases, at most one
automatic label disagreement, at most 25% review, and at least one more match than
the baseline. These limits are not an operational risk calibration.

The development screen had 15 matches versus 14 baseline matches, four reviews,
and five automatic label disagreements versus the limit of one. The unpreviewed
sample had 7 matches versus 4 baseline matches, **17 reviews** versus the 25%
limit, and zero automatic label disagreements. Its held-out gate **failed**.
Run `python3 pilots/github-issue-routing/verify_pilot.py` to verify both
preserved results. Reproduce the held-out gate check with:

```sh
python3 skills/jev-question-kernel-catalog/scripts/qualify_workflow.py \
  pilots/github-issue-routing/contract.json \
  pilots/github-issue-routing/pilot-held-out.json \
  pilots/github-issue-routing/consumer.py --require-sample-checks
```

This checks typed response binding and planned dispositions only. It does not
verify label quality, representativeness beyond this selection, downstream action,
or production accuracy. A failed gate stays failed; do not tune on either
inspected sample and still call it fresh held-out evidence.
