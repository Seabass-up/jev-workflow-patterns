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

Together these collections contain 230 question profiles. The three foundational
workflows below are counted separately.

The [three foundations](https://seabass-up.github.io/jev-workflow-patterns/) retain
their dedicated skills for evidence-directed retrieval, lineage-aware corroboration,
and dependency-DAG recomputation. Historical contracts and results remain versioned.
