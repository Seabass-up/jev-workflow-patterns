# Public GitHub issue-title shadow pilot

This exploratory pilot asks whether a narrow Jev contract can plan `bug_queue`,
`enhancement_queue`, or `human_review` from public GitHub CLI issue titles. It makes
**no GitHub issue changes**. Maintainer-applied `bug` and `enhancement` labels are
independent comparison targets, not adjudicated ground truth. Some enhancement
issues describe malfunctioning existing behavior; disagreement may reflect label
policy or missing body context rather than a model error.

The sample is frozen before provider inference: first 12 closed non-PR issues in
each exclusive label query, ordered by GitHub's issue API creation order, created
before 2026-09-01 UTC. The API was queried on 2026-09-24. Only the title is used as
state. Exclude mixed `bug`+`enhancement` labels, PRs, and titles containing an email
address or obvious credential string. No issue body, author identity, or maintainer
label is sent to TypeSafe. `sample-frozen.json` records the source URL, title,
creation timestamp, labels, expected route, and deterministic baseline route.

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

`pilot.json` stores exact bridge receipts after the frozen commit. Reproduce with:

```sh
python3 skills/jev-question-kernel-catalog/scripts/qualify_workflow.py \
  pilots/github-issue-routing/contract.json \
  pilots/github-issue-routing/pilot.json \
  pilots/github-issue-routing/consumer.py --require-sample-checks
```

This checks typed response binding and planned dispositions only. It does not
verify label quality, representativeness beyond this selection, downstream action,
or production accuracy. A failed gate stays failed; do not tune on these cases and
still call them held out.
