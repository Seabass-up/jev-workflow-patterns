# Web data collection profiles

Use this module for classifying the text a team that collects public web data handles:
policy excerpts from robots files and terms of use, page excerpts, extracted values
against field definitions, operator notices, records against a personal-data exclusion
policy, page diffs, record pairs, and page kinds. A label is a reading of text. Request
behavior, rate policy, legal review, exact matching, and contact with site operators
stay with people and code. Nothing here helps evade blocking, rate limits, or access
controls.

## Select the profile that fits

The [8 profiles](https://seabass-up.github.io/jev-workflow-patterns/web-scraping/)
are optional examples:

| IDs | Family | Useful checks |
| --- | --- | --- |
| WS01, WS04, WS05 | Permissions and notices | Policy excerpt against a described use; operator notice to collectors; personal data the policy excludes |
| WS02, WS06, WS08 | Page structure | Target record type present; structural versus content-only change; item, listing, or navigation page |
| WS03, WS07 | Record quality | Extracted value carries the field's meaning; two records describe one entity |

Each question is at
`https://seabass-up.github.io/jev-workflow-patterns/web-scraping/patterns/<lowercase-id>/`
with contracts in the
[catalog JSON](https://seabass-up.github.io/jev-workflow-patterns/web-scraping/catalog.json).
The evaluation page reports the screening outcomes; a small synthetic screen is not
qualification for a real collection program.

Choose by what the label feeds:

- WS01 feeds an onboarding decision before any request is made. Code performs the
  exact robots path and user-agent match; `forbids` halts, and
  `permits_with_conditions` goes to legal review. The label is not a legal conclusion.
- WS04 feeds a halt. Code stops collection on `stop_request` and `contact_operator`
  and never retries, changes client identity, or takes another route to the content;
  a person decides whether to contact the operator.
- WS05 feeds a storage gate under the team's own written policy and its recorded
  revision. The model applies that policy, never a law.
- WS06 feeds maintenance routing. Code confirms the label with a real extractor run
  against the current snapshot before anyone edits a template.
- WS07 proposes a merge that code performs under the dataset's rules after exact
  identifier checks. `variant_of_same` is kept apart from a true duplicate.
- WS02 and WS08 feed extractor routing. Code chooses canonical URLs and never
  follows sign-in or access-restricted pages.

## Prepare a bounded state

Supply the policy excerpt, notice, page excerpt, or record text unchanged, the field
or record-type definition from the collection schema, the extractor's field list with
where each field is read, and the exclusion policy text with its revision. Several
contracts state a precedence order for inputs that fit two labels (a permission with
a condition, a stop notice with a contact route, allowed with excluded personal data,
structure with values, a variant against a different entity); keep those sentences
when adapting. Keep raw markup excerpts short and limited to the elements the fields
are read from. Before inference, code validates `required_state_fields` and returns a
local `unknown` for absent or empty evidence.

## Use the labels without taking over

No label grants permission, concludes a legal question, sets a request rate, executes
a merge, or selects a canonical URL. A notice halts collection, and only a person
reopens it. Send only authorized page text through the approved provider path; keep
personal data out of the state except where WS05 is judging whether to exclude it,
and hold those records from storage until a person reviews them.

## Verify against the team's own reviews

The [evaluation](https://seabass-up.github.io/jev-workflow-patterns/web-scraping/evaluation/)
reports design and challenge outcomes. Before use, compare labels with the compliance
reviewer's readings of the same excerpts, the crawl owner's handling of halted fetches,
the privacy reviewer's marks, the maintainer's dispositions of change alerts, and a
hand-adjudicated set of record pairs. Measure missed stop notices, missed excluded
personal data, and false merges first.
