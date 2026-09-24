---
layout: default
title: Jev Workflow Patterns
description: Find focused Jev question contracts and code-controlled workflow guides for business, engineering, and AI systems.
permalink: /
kicker: A practical pattern catalog
---

<div class="hero">
  <h2>Make the question precise. Keep the workflow under code control.</h2>
  <p>Jev evaluates the text and structured state you provide, then returns typed judgments. This catalog helps you choose a narrow question, supply the evidence it needs, and decide what code should do with the answer.</p>
  <div class="action-links">
    <a href="{{ '/catalog/' | relative_url }}">Find a pattern</a>
    <a class="secondary" href="{{ '/kernel/' | relative_url }}">Build a question</a>
  </div>
</div>

## Start with the work you need to do

<div class="card-grid">
  <section class="card">
    <span class="tag">Browse</span>
    <h3><a href="{{ '/catalog/' | relative_url }}">Search all {{ site.data.catalog_summary.total_profiles }} question profiles</a></h3>
    <p>Filter by area, collection, question type, or a provisional review flag. Every result links to its question contract and evaluation context.</p>
  </section>
  <section class="card">
    <span class="tag">Design</span>
    <h3><a href="{{ '/kernel/' | relative_url }}">Use the Jev Question Kernel</a></h3>
    <p>Specify the decision, required state, answer space, uncertainty path, follow-up, and tests before using a judgment in software.</p>
  </section>
  <section class="card">
    <span class="tag">Compare</span>
    <h3><a href="{{ '/collections/' | relative_url }}">Review domain collections</a></h3>
    <p>See the synthetic screen results and provisional patterns for {{ site.data.catalog_summary.domain_collections }} newer collections.</p>
  </section>
</div>

## Popular starting points

- [Email]({{ '/email/' | relative_url }}): interpret requests, commitments, dates, quoted history, and drafts.
- [Bug hunting]({{ '/bug-hunting/' | relative_url }}): ask about a specific failure condition, then reproduce it independently.
- [People and their AI helpers]({{ '/human-ai/' | relative_url }}): preserve learning, authorship, understandable instructions, and practical handoffs.
- [Business, engineering, LLM, and harness research catalogs]({{ '/iterations/04/' | relative_url }}): start with Iteration 4 and follow links to the three earlier iterations and their evaluations.

## Three foundational workflow guides

These guides are separate from the {{ site.data.catalog_summary.total_profiles }} question profiles.

<div class="card-grid">
  <section class="card">
    <span class="tag">Bounded retrieval</span>
    <h3><a href="{{ '/patterns/evidence-directed-allowlist-controller/' | relative_url }}">Evidence-directed allowlist controller</a></h3>
    <p>Ask a fixed question, then fetch from a caller-approved source catalog only if evidence remains missing.</p>
  </section>
  <section class="card">
    <span class="tag">Source lineage</span>
    <h3><a href="{{ '/patterns/lineage-aware-corroboration/' | relative_url }}">Lineage-aware corroboration</a></h3>
    <p>Count independent origins rather than repeated copies while retaining contradictions for review.</p>
  </section>
  <section class="card">
    <span class="tag">Selective reuse</span>
    <h3><a href="{{ '/patterns/dependency-dag-selective-recomputation/' | relative_url }}">Dependency-DAG selective recomputation</a></h3>
    <p>Rerun only judgments affected by changed inputs or upstream answers.</p>
  </section>
</div>

## What the evidence means

<div class="callout warning">
  <p>Published screens use synthetic examples. A matching label checks an authored case; it does not establish production accuracy, calibration, safety, legal compliance, or a real-world benefit. Provisional profiles retain their disagreements. Code and responsible people own permissions, exact checks, and consequential actions.</p>
</div>

The <a href="{{ '/discovery/' | relative_url }}">discovery intake</a> records new candidates before promotion. The <a href="https://github.com/Seabass-up/jev-workflow-patterns">public repository</a> contains skill files, fixtures, evaluation receipts, and the source history. For Jev's supported primitives and API, see the <a href="https://docs.typesafe.ai/llms.txt">official TypeSafe documentation index</a>.

<p class="catalog-release"><strong>Catalog:</strong> {{ site.data.catalog_summary.total_profiles }} question profiles across {{ site.data.catalog_summary.source_catalogs }} catalogs · <strong>Kernel skill:</strong> v{{ site.data.catalog_summary.kernel_version }} · <strong>Catalog data date:</strong> {{ site.data.catalog_summary.catalog_date }} · <a href="https://github.com/Seabass-up/jev-workflow-patterns/commits/main/">Source history</a></p>
