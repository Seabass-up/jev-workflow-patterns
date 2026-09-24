# SEO profiles

Use this module for classifying the text an SEO or content team reviews at scale:
search queries, title tags, internal link anchors, meta descriptions, backlink
context, FAQ entries, page change records, and query-to-page assignments. A label
is a reading of text. Counts, lengths, rankings, rel-attribute parsing, and any
search engine's rules stay with code and people.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/seo/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| SE01, SE08 | Query intent and topic fit | Intent a query expresses; whether a page's primary subject is the target query's |
| SE02, SE04, SE06, SE07 | On-page content | Title describes the page; description summarizes or teases; FAQ answer addresses its question; change is content or technical |
| SE03, SE05 | Links | Internal anchor describes its destination; backlink context is editorial, disclosed, user-submitted, or a listing |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/seo/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/seo/catalog.json).
The evaluation page reports the screening outcomes; a small synthetic check is not
qualification for a real site.

Choose by what the label feeds:

- SE01 and SE08 feed a query-to-page map. Code owns the keyword list, volumes, and
  the mapping from intent to page type; a broader, narrower, or different label goes
  to the content planner.
- SE02, SE04, and SE06 feed a review list per template. Code measures length and
  duplicates exactly; the editor decides the rewrite and substantiates any claim.
- SE03 and SE05 feed link review. Code crawls, resolves redirects, and parses rel
  attributes exactly; the label groups contexts and never decides whether a link is
  valuable, harmful, or compliant.
- SE07 feeds a change log that code aligns with analytics. The label never says a
  change caused a ranking movement.

## Prepare a bounded state

Supply the query, title, description, anchor, or answer text unchanged, and a
code-extracted summary of the page or destination where the contract asks for one.
Several contracts state a precedence order: a brand query that also asks to complete
an action, a description that both mismatches and teases, a link context that carries
a disclosure, and a change that is both content and technical. Keep those sentences
when adapting. Before inference, code validates `required_state_fields` and returns a
local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label decides whether a practice complies with a search engine's policies, whether
a claim is substantiated, whether a link should be removed or disavowed, or why traffic
changed. Send only authorized site and export text through the approved provider path;
keep account identifiers, customer data, and credentials out of the state.

## Verify against the team's own review decisions

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/seo/evaluation/)
reports the design and challenge outcomes. Before use, compare labels with an
analyst's intent tags, an editor's title and description reviews, manual backlink
context tags, and the content team's own change categories. Measure teases labeled
as summaries and sponsored contexts labeled as editorial first.
