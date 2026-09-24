# Domain profiles

Choose by state relationship, typed output, consumer, and limitation. Similar nouns
alone do not establish a match. Four research catalogs total 120 patterns:

| Catalog | Business | Engineering | LLM | Harness |
| --- | --- | --- | --- | --- |
| [Iteration 1](https://seabass-up.github.io/jev-workflow-patterns/iterations/01/) | B01–B07 | E01–E07 | L01–L06 | H01–H10 |
| [Iteration 2](https://seabass-up.github.io/jev-workflow-patterns/iterations/02/) | B08–B14 | E08–E14 | L07–L12 | H11–H20 |
| [Iteration 3](https://seabass-up.github.io/jev-workflow-patterns/iterations/03/) | B15–B21 | E15–E21 | L13–L18 | H21–H30 |
| [Iteration 4](https://seabass-up.github.io/jev-workflow-patterns/iterations/04/) | B22–B28 | E22–E28 | L19–L24 | H31–H40 |

Each catalog's JSON is at `catalog.json`; each pattern is at
`patterns/<lowercase-id>/`, for example
[H37](https://seabass-up.github.io/jev-workflow-patterns/iterations/04/patterns/h37/).
Read the chosen page and evaluation before adapting it. If offline, use the bundled
modules/example and mark uninspected external patterns as unverified.

- **Business:** interpret request, obligation, purchase, churn, or contact-preference
  evidence. Identity, payments, disclosure, and delivery remain with existing controls.
- **Engineering:** assess code context, test realism, configuration, extraction, or
  trace relations. Verify findings with source and reproductions.
- **LLM/RAG:** distinguish work type, fidelity, directness, answerability, and support.
  L21/H36 risk judgments cannot establish prompt-injection safety.
- **Harness:** select compositions required by actual dependencies: batching,
  retrieval, candidate binding, repeat audits, or drift checks.

An additional [email catalog](https://seabass-up.github.io/jev-workflow-patterns/email/)
adds EM01–EM12: twelve email-specific profiles with three synthetic cases each.
Read the local [email module](email.md) for source boundaries, question-handle
composition, draft coverage, and action controls. These supplement rather than
replace the four historical catalogs.

The [bug-hunting catalog](https://seabass-up.github.io/jev-workflow-patterns/bug-hunting/)
adds BH01–BH48 across eight failure families. Read the local
[bug-hunting module](bug-hunting.md) for evidence packets, candidate status,
counterevidence, and verification boundaries. Its scenarios are textual, not
executed reproductions; BH41 retains an unresolved counterexample disagreement.

The [human–AI catalog](https://seabass-up.github.io/jev-workflow-patterns/human-ai/)
adds HA01–HA24: eight learning-material profiles, eight communication/service
profiles, and eight decision/collaboration profiles. Read the local
[human–AI module](human-ai.md) for material-level judgments, explicit user agency,
missing-input preflight, and human-takeover boundaries. Its screen separates
72 design cases from 24 independently authored synthetic challenge cases.
Research sources motivate the use cases; they do not establish Jev benefit.

Three further collections were added in skill version 2.5.0:

- The [call-controls catalog](https://seabass-up.github.io/jev-workflow-patterns/controls/)
  adds CT01–CT10 for the code around a call: request preparation, answer consumption,
  contract quality, and message signals. Read the local [controls module](controls.md).
  CT03 and CT07 are provisional.
- The [storytelling catalog](https://seabass-up.github.io/jev-workflow-patterns/storytelling/)
  adds ST01–ST08 for manuscript text: structure, consistency, and craft. Read the local
  [storytelling module](storytelling.md). ST04, ST05, and ST08 are provisional.
- The [electrical catalog](https://seabass-up.github.io/jev-workflow-patterns/electrical/)
  adds EL01–EL08 for service calls, permits and inspections, and materials. Read the
  local [electrical module](electrical.md). Its labels never replace licensed judgment.

Skill version 2.6.0 adds twenty domain collections of eight profiles each, built
with the same contract shape, a pre-inference overlap pass, separately authored
challenge cases, and preserved screens. Every profile records its review floor with
its option count. Read the local module before adapting one; provisional profiles
keep their disagreements on each collection's evaluation page.

| Collection | IDs | Module |
| --- | --- | --- |
| [Project management](https://seabass-up.github.io/jev-workflow-patterns/project-management/) | PM01–PM08 | [project-management.md](project-management.md) |
| [Marketing](https://seabass-up.github.io/jev-workflow-patterns/marketing/) | MK01–MK08 | [marketing.md](marketing.md) |
| [Construction](https://seabass-up.github.io/jev-workflow-patterns/construction/) | CN01–CN08 | [construction.md](construction.md) |
| [Finance](https://seabass-up.github.io/jev-workflow-patterns/finance/) | FN01–FN08 | [finance.md](finance.md) |
| [Executive](https://seabass-up.github.io/jev-workflow-patterns/executive/) | CE01–CE08 | [executive.md](executive.md) |
| [SEO](https://seabass-up.github.io/jev-workflow-patterns/seo/) | SE01–SE08 | [seo.md](seo.md) |
| [Auto repair](https://seabass-up.github.io/jev-workflow-patterns/auto-repair/) | AR01–AR08 | [auto-repair.md](auto-repair.md) |
| [Auto performance](https://seabass-up.github.io/jev-workflow-patterns/auto-performance/) | AP01–AP08 | [auto-performance.md](auto-performance.md) |
| [Motorsport](https://seabass-up.github.io/jev-workflow-patterns/motorsport/) | MR01–MR08 | [motorsport.md](motorsport.md) |
| [Grading](https://seabass-up.github.io/jev-workflow-patterns/grading/) | GR01–GR08 | [grading.md](grading.md) |
| [Human resources](https://seabass-up.github.io/jev-workflow-patterns/human-resources/) | HR01–HR08 | [human-resources.md](human-resources.md) |
| [Logistics](https://seabass-up.github.io/jev-workflow-patterns/logistics/) | LG01–LG08 | [logistics.md](logistics.md) |
| [Logistics routing](https://seabass-up.github.io/jev-workflow-patterns/logistics-routing/) | LR01–LR08 | [logistics-routing.md](logistics-routing.md) |
| [Networking](https://seabass-up.github.io/jev-workflow-patterns/networking/) | NW01–NW08 | [networking.md](networking.md) |
| [Cybersecurity](https://seabass-up.github.io/jev-workflow-patterns/cybersecurity/) | CY01–CY08 | [cybersecurity.md](cybersecurity.md) |
| [Web data](https://seabass-up.github.io/jev-workflow-patterns/web-scraping/) | WS01–WS08 | [web-scraping.md](web-scraping.md) |
| [Contracts](https://seabass-up.github.io/jev-workflow-patterns/legal-contracts/) | LC01–LC08 | [legal-contracts.md](legal-contracts.md) |
| [Real estate](https://seabass-up.github.io/jev-workflow-patterns/real-estate/) | RE01–RE08 | [real-estate.md](real-estate.md) |
| [Sales](https://seabass-up.github.io/jev-workflow-patterns/sales/) | SA01–SA08 | [sales.md](sales.md) |
| [Data quality](https://seabass-up.github.io/jev-workflow-patterns/data-quality/) | DQ01–DQ08 | [data-quality.md](data-quality.md) |

Together these collections contain 390 question profiles. The three foundational
workflows below are counted separately.

The [three foundations](https://seabass-up.github.io/jev-workflow-patterns/) retain
their dedicated skills for evidence-directed retrieval, lineage-aware corroboration,
and dependency-DAG recomputation. Historical contracts and results remain versioned.
