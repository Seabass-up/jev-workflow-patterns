# Jev Workflow Patterns

Public documentation pages, foundational Codex skills, and growing synthetic-screened question catalogs for composing Jev's typed judgments into bounded application workflows.

The project site is built from Markdown with GitHub Pages and GitHub Actions. The skills directory contains three foundational skills plus Jev Question Kernel v2, covering authoring, evidence/provenance, evaluation/drift, domain profiles, and email profiles with portable references, example JSON, and a structural checker. Iteration directories retain their historical contracts, synthetic receipts, and demonstration controllers. This is not a TypeSafe SDK or production runtime library.

## Pages

- [Twelve email question patterns](https://seabass-up.github.io/jev-workflow-patterns/email/)
- [Email evaluation and preserved misses](https://seabass-up.github.io/jev-workflow-patterns/email/evaluation/)

- [Jev Question Kernel v2](https://seabass-up.github.io/jev-workflow-patterns/kernel/)
- [Pattern discovery intake](https://seabass-up.github.io/jev-workflow-patterns/discovery/)
- [TypeSafe introduction review and pattern candidates](https://seabass-up.github.io/jev-workflow-patterns/discovery/introduction-review/)

- [Iteration 1: 20 useful questions plus 10 experimental harness designs](https://seabass-up.github.io/jev-workflow-patterns/iterations/01/)
- [Iteration 1 evaluation and preserved failures](https://seabass-up.github.io/jev-workflow-patterns/iterations/01/evaluation/)
- [Iteration 2: 30 versioned question patterns](https://seabass-up.github.io/jev-workflow-patterns/iterations/02/)
- [Iteration 2 evaluation and preserved failures](https://seabass-up.github.io/jev-workflow-patterns/iterations/02/evaluation/)
- [Iteration 3: 30 new question patterns and catalog skill](https://seabass-up.github.io/jev-workflow-patterns/iterations/03/)
- [Iteration 3 evaluation and preserved failures](https://seabass-up.github.io/jev-workflow-patterns/iterations/03/evaluation/)
- [Iteration 4: final 30 question patterns](https://seabass-up.github.io/jev-workflow-patterns/iterations/04/)
- [Iteration 4 evaluation, v2 repairs, and raw synthetic receipts](https://seabass-up.github.io/jev-workflow-patterns/iterations/04/evaluation/)

- [Evidence-directed allowlist controller](https://seabass-up.github.io/jev-workflow-patterns/patterns/evidence-directed-allowlist-controller/)
- [Lineage-aware corroboration](https://seabass-up.github.io/jev-workflow-patterns/patterns/lineage-aware-corroboration/)
- [Dependency-DAG selective recomputation](https://seabass-up.github.io/jev-workflow-patterns/patterns/dependency-dag-selective-recomputation/)

## Use the skills

The foundational patterns have dedicated skills. All four catalogs share the [Jev Question Kernel v2 skill](skills/jev-question-kernel-catalog/SKILL.md), whose existing folder name remains compatible. Copy the entire skill folder through a compatible skill installation workflow; its modules, examples, and helper are self-contained. The website does not install it or change harness settings.

## Boundaries

The email extension adds 12 profiles to the existing 120 research questions, with
the email module packaged in kernel skill version 2.1.0. Initial screening matched
34/36; two versioned missing-input refinements matched 6/6 reruns and select 36/36
current fixtures. All 42 live screening receipts remain replayable. No mailbox
connection or email action is installed or authorized by the catalog.

Patterns found while using Jev in other work are recorded as candidates in
`discovery/candidates.json` and checked by `discovery/check_candidates.py`. The
introduction review supplies the first nine, with an advisory Jev duplicate screen
and offline measurements of preserved receipts. Candidates have no contracts,
fixtures, or screening receipts and do not activate a fifth iteration.

The iteration catalog is a separate evidence track from the three foundational patterns. Iteration 4's initial 58/60 screen preserves both misses; four v2 reruns selected 60/60 current synthetic fixtures. See each iteration's exact versions, failures and scope; these are not production-accuracy claims.

Jev returns typed, advisory judgments. Application code retains control of source access, evidence freshness, deterministic validation, budgets, caching, escalation, and actions. Confidence thresholds are workflow policy, not universal correctness guarantees. Read each pattern's limitations before adapting it.

No license is included in this repository. Ask the owner before reusing or redistributing these materials.
