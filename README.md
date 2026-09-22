# Jev Workflow Patterns

Public documentation pages, three foundational Codex skills, and a growing synthetic-screened question catalog for composing Jev's typed judgments into bounded application workflows.

The project site is built from the Markdown pages in this repository with GitHub Pages and GitHub Actions. The `skills/` directory contains the three foundational installable skill sources. Iteration directories add question contracts, synthetic fixtures/receipts, and pure demonstration controllers. This is not a TypeSafe SDK or a maintained production runtime library.

## Pages

- [Iteration 1: 20 useful questions plus 10 experimental harness designs](https://seabass-up.github.io/jev-workflow-patterns/iterations/01/)
- [Iteration 1 evaluation and preserved failures](https://seabass-up.github.io/jev-workflow-patterns/iterations/01/evaluation/)

- [Evidence-directed allowlist controller](https://seabass-up.github.io/jev-workflow-patterns/patterns/evidence-directed-allowlist-controller/)
- [Lineage-aware corroboration](https://seabass-up.github.io/jev-workflow-patterns/patterns/lineage-aware-corroboration/)
- [Dependency-DAG selective recomputation](https://seabass-up.github.io/jev-workflow-patterns/patterns/dependency-dag-selective-recomputation/)

## Use the skills

Each pattern has a self-contained Codex skill under `skills/<skill-name>/SKILL.md`. Use the skill with a compatible Codex skill installation workflow; the site does not install anything into a visitor's environment.

## Boundaries

The iteration catalog is a separate evidence track from the three foundational patterns. Initial core screening matched 76/81 fixtures, targeted refinement 15/15, and harness screening 38/40. See each iteration's exact versions, failures and scope; these are not production-accuracy claims.

Jev returns typed, advisory judgments. Application code retains control of source access, evidence freshness, deterministic validation, budgets, caching, escalation, and actions. Confidence thresholds are workflow policy, not universal correctness guarantees. Read each pattern's limitations before adapting it.

No license is included in this repository. Ask the owner before reusing or redistributing these materials.
