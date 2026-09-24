# Jev Workflow Patterns

Public documentation pages, foundational Codex skills, and growing synthetic-screened question catalogs for composing Jev's typed judgments into bounded application workflows.

The project site is built from Markdown with GitHub Pages and GitHub Actions. The skills directory contains three foundational skills plus Jev Question Kernel v2, covering authoring, evidence/provenance, evaluation/drift, domain profiles, and email profiles with portable references, example JSON, and a structural checker. Iteration directories retain their historical contracts, synthetic receipts, and demonstration controllers. This is not a TypeSafe SDK or production runtime library.

## Pages

- [Find a pattern across the full catalog](https://seabass-up.github.io/jev-workflow-patterns/catalog/) — search and filter all published question profiles
- [All pattern collections](https://seabass-up.github.io/jev-workflow-patterns/collections/) — hub with screen results
- [Project management](https://seabass-up.github.io/jev-workflow-patterns/project-management/)
- [Marketing](https://seabass-up.github.io/jev-workflow-patterns/marketing/)
- [Construction](https://seabass-up.github.io/jev-workflow-patterns/construction/)
- [Finance](https://seabass-up.github.io/jev-workflow-patterns/finance/)
- [Executive](https://seabass-up.github.io/jev-workflow-patterns/executive/)
- [SEO](https://seabass-up.github.io/jev-workflow-patterns/seo/)
- [Auto repair](https://seabass-up.github.io/jev-workflow-patterns/auto-repair/)
- [Auto performance](https://seabass-up.github.io/jev-workflow-patterns/auto-performance/)
- [Motorsport](https://seabass-up.github.io/jev-workflow-patterns/motorsport/)
- [Grading](https://seabass-up.github.io/jev-workflow-patterns/grading/)
- [Human resources](https://seabass-up.github.io/jev-workflow-patterns/human-resources/)
- [Logistics](https://seabass-up.github.io/jev-workflow-patterns/logistics/)
- [Logistics routing](https://seabass-up.github.io/jev-workflow-patterns/logistics-routing/)
- [Networking](https://seabass-up.github.io/jev-workflow-patterns/networking/)
- [Cybersecurity](https://seabass-up.github.io/jev-workflow-patterns/cybersecurity/)
- [Web data](https://seabass-up.github.io/jev-workflow-patterns/web-scraping/)
- [Contracts](https://seabass-up.github.io/jev-workflow-patterns/legal-contracts/)
- [Real estate](https://seabass-up.github.io/jev-workflow-patterns/real-estate/)
- [Sales](https://seabass-up.github.io/jev-workflow-patterns/sales/)
- [Data quality](https://seabass-up.github.io/jev-workflow-patterns/data-quality/)

- [10 call-control profiles](https://seabass-up.github.io/jev-workflow-patterns/controls/) · [evaluation](https://seabass-up.github.io/jev-workflow-patterns/controls/evaluation/)
- [8 storytelling profiles](https://seabass-up.github.io/jev-workflow-patterns/storytelling/) · [evaluation](https://seabass-up.github.io/jev-workflow-patterns/storytelling/evaluation/)
- [8 electrical-contracting profiles](https://seabass-up.github.io/jev-workflow-patterns/electrical/) · [evaluation](https://seabass-up.github.io/jev-workflow-patterns/electrical/evaluation/)

- [24 human–AI collaboration profiles](https://seabass-up.github.io/jev-workflow-patterns/human-ai/)
- [Human–AI evaluation: design and independent challenge cases](https://seabass-up.github.io/jev-workflow-patterns/human-ai/evaluation/)
- [Human–AI research method](https://seabass-up.github.io/jev-workflow-patterns/human-ai/research/)
- [Human–AI primary sources](https://seabass-up.github.io/jev-workflow-patterns/human-ai/sources/)

- [48 bug-hunting profiles across eight failure families](https://seabass-up.github.io/jev-workflow-patterns/bug-hunting/)
- [Bug-hunting evaluation and preserved disagreement](https://seabass-up.github.io/jev-workflow-patterns/bug-hunting/evaluation/)

- [Twelve email question patterns](https://seabass-up.github.io/jev-workflow-patterns/email/)
- [Email evaluation and preserved misses](https://seabass-up.github.io/jev-workflow-patterns/email/evaluation/)

- [Jev Question Kernel v2](https://seabass-up.github.io/jev-workflow-patterns/kernel/)
- [Question-to-consumer qualification walkthrough](https://seabass-up.github.io/jev-workflow-patterns/kernel/qualification/)
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

The foundational patterns have dedicated skills. The four research catalogs and the email, bug-hunting, and human–AI collections share the [Jev Question Kernel v2 skill](skills/jev-question-kernel-catalog/SKILL.md), whose existing folder name remains compatible. Copy the entire skill folder through a compatible skill installation workflow; its modules, examples, and helper are self-contained. The website does not install it or change harness settings.

The [human–AI module](skills/jev-question-kernel-catalog/references/human-ai.md)
is packaged in skill version 2.3.0. Its external catalog links are optional
reference material; an installed copy does not require this entire repository.

## Build another collection

The scripts that built the domain collections are under
[`scripts/collection_pipeline/`](scripts/collection_pipeline/README.md): an authoring
specification, a structural checker, the pre-inference overlap pass, the live screen,
the assembly step that writes results and pages, and the source support check. The
live steps use the local `jev-workflows` bridge; nothing in the repository holds a
credential. Drafts and challenge cases go in a git-ignored work directory.
The historical collection pipeline uses one Choice per profile. For a mixed
Choice/Noul/Score contract, start with the kernel's portable contract format and
the [side-effect-free qualification guide](skills/jev-question-kernel-catalog/references/qualification.md)
instead of forcing several independent judgments into one label.

`python3 scripts/build_catalog.py` regenerates the complete finder and shared
catalog counts from the thirty source catalogs. `python3 scripts/build_collection_pages.py --hub`
regenerates the newer-collection overview. The Pages workflow checks both outputs
for drift before building the site.

## Boundaries

Kernel skill version 2.6.0 adds twenty domain collections (160 profiles) authored
against one written specification, each checked for option overlap before its
fixtures were frozen, screened with three design cases and one separately authored
challenge per pattern, and replayed by a shared evaluator. Domain boundaries are
stated in every collection: HR and grading judge documents and work, never people;
finance is document classification, not advice; cybersecurity and networking are
defensive triage; web data collection is compliance and quality, not evasion;
automotive, construction, and measurement labels are readings of text with every
numeric comparison and safety or fitness determination left to qualified people
and code. The [collections hub](https://seabass-up.github.io/jev-workflow-patterns/collections/)
lists each screen result and provisional patterns.

Kernel skill version 2.5.0 adds three collections with 26 profiles: call controls
(38/40 synthetic cases matched; CT03 and CT07 provisional), storytelling (27/32;
ST04, ST05, ST08 provisional), and electrical contracting (32/32). That brings the
question profiles to 230. Every disagreement is preserved unchanged. Electrical labels
are readings of text, never electrical determinations; the jurisdiction's rules,
exact ratings, the official inspection result, and on-site licensed judgment govern.

Kernel skill version 2.3.0 adds 24 human–AI profiles to the 120 research,
12 email, and 48 bug-hunting profiles: 204 question profiles in total.
The three foundational guides are counted separately. The human–AI screen
separates 72 design cases from 24 independently authored synthetic challenge
cases; see its evaluation for results and disagreements. Neither a synthetic
match nor the motivating research establishes Jev benefit or production accuracy.
Consuming code must return `unknown` for missing required inputs before inference. These
profiles do not infer learner traits or diagnoses, authorize actions, or confer
authority to change memory.

Kernel skill version 2.2.0 introduced the bug-hunting module and 48 profiles.
Its screen matches 143/144 authored text
scenarios after two service-error recoveries. BH41 retains an unresolved
counterexample disagreement. These are not 48 executed bug reproductions.

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

Released under the [MIT License](LICENSE).
