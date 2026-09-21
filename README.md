# Jev Workflow Patterns

Public documentation pages and three Codex skills for composing Jev's typed judgments into bounded application workflows.

The project site is built from the Markdown pages in this repository with GitHub Pages and GitHub Actions. The `skills/` directory contains the matching installable skill sources. This repository is documentation and agent guidance; it is not a TypeSafe SDK or a maintained runtime library.

## Pages

- [Evidence-directed allowlist controller](https://seabass-up.github.io/jev-workflow-patterns/patterns/evidence-directed-allowlist-controller/)
- [Lineage-aware corroboration](https://seabass-up.github.io/jev-workflow-patterns/patterns/lineage-aware-corroboration/)
- [Dependency-DAG selective recomputation](https://seabass-up.github.io/jev-workflow-patterns/patterns/dependency-dag-selective-recomputation/)

## Use the skills

Each pattern has a self-contained Codex skill under `skills/<skill-name>/SKILL.md`. Use the skill with a compatible Codex skill installation workflow; the site does not install anything into a visitor's environment.

## Boundaries

Jev returns typed, advisory judgments. Application code retains control of source access, evidence freshness, deterministic validation, budgets, caching, escalation, and actions. Confidence thresholds are workflow policy, not universal correctness guarantees. Read each pattern's limitations before adapting it.

No license is included in this repository. Ask the owner before reusing or redistributing these materials.
