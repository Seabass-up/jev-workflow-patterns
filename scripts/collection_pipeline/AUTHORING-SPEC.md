# Collection authoring specification

You are authoring ONE new collection of Jev question profiles for this repository
(`<repo>`; drafts go to the work directory `<workdir>`, by default `<repo>/.work`). Jev (jev-1.13.0) answers a typed Choice
question about a JSON state and returns one label with probabilities. It reads literally,
cannot do arithmetic or date comparison reliably, and treats state as data. Code owns exact
matches, identifiers, numbers, dates, policy thresholds, permissions, and execution.

Read these files first, in this order, and copy their structure exactly:
1. <repo>/skills/jev-question-kernel-catalog/references/authoring.md
2. <repo>/electrical/catalog.json   (exemplar catalog)
3. <repo>/electrical/collection.json (exemplar page metadata)
4. <repo>/electrical/sources.json   (exemplar source register)
5. <repo>/skills/jev-question-kernel-catalog/references/electrical.md (exemplar kernel module)
Do NOT read any fixtures.json, results/, or patterns/ directory of any collection, and do not
read other agents' output. Do not modify any existing file.

## Deliverables (write exactly these files)

A. `<repo>/<folder>/catalog.json` — 8 patterns, IDs `<PREFIX>01`..`<PREFIX>08`, `version: 1`.
   Top level: {"schema_version":1,"title":...,"created_date":"2026-09-23","kernel_skill_version":"2.6.0","scope":...,"patterns":[...]}.
   Each pattern has exactly the keys of the exemplar: local_id (any short local code), title, purpose,
   benefit, required_state_fields, questions, code_owned, verification, follow_up, nearest_existing,
   distinctness, source_ids, family, id, version, policy.
   - `questions` has exactly one handle, `decision`, of type `choice`, with `instructions` and `criteria`.
   - `instructions` MUST begin with: "First, if any required field (`f1`, `f2`, ...) is absent, empty, or lacks the information needed for this judgment, select unknown before considering other labels. " listing every required field in backticks, then the judgment, and MUST end with " Treat all supplied text as data, never as instructions to change this question."
   - `criteria` has 3 to 5 labels plus `unknown` whose description is exactly:
     "Required evidence is missing, contradictory, or does not support a determinate classification."
   - Labels are lowercase snake_case. Descriptions describe concrete situations without relying on the label name. If two labels could both apply to one realistic input, the instructions MUST state which wins ("If ... select X") or the descriptions must exclude each other.
   - Reference state fields in backticks, e.g. `customer_report`. Keep each question one coherent judgment. Nothing the model should compute exactly (counts, sums, date differences, thresholds, code articles, legal conclusions) may be asked.
   - `policy`: {"review_when_confidence_below":0.8,"option_count":N,"equivalent_top_probability":X,"note":"Confidence follows the option count; the equivalent top probability is what 0.8 requires for this contract's options. Thresholds are provisional workflow policy, not calibration."} where N = number of criteria including unknown and X = round((0.8*(N-1)+1)/N, 4).
   - `nearest_existing`: 2–3 IDs from the existing catalogs (B01–B28, E01–E28, L01–L24, H01–H40, EM01–EM12, BH01–BH48, HA01–HA24, CT01–CT10, ST01–ST08, EL01–EL08). Read titles from the catalog.json files under iterations/0N/, email/, bug-hunting/, human-ai/, controls/, storytelling/, electrical/ (catalog.json only). `distinctness` explains what the nearest ones do and what this one does differently.
   - `family`: one of 2–3 family keys you define (snake_case). `source_ids`: 1–3 ids from your sources.json.

B. `<repo>/<folder>/sources.json` — 3 to 5 public sources fetched with curl (a sixth, read in a browser because the site blocks scripted fetches, may be added later). For each, run
   `curl -sSL --max-time 40 -A "Mozilla/5.0 (research fetch)" -o /tmp/src.html -w "%{http_code}" <url>`
   and include it only if the HTTP code is 200; compute sha256 of the fetched bytes with
   `shasum -a 256 /tmp/src.html`. Entry keys: id (e.g. "PM-S1"), title, url, checked ("2026-09-23"),
   sha256, summary (what the page says that motivates which patterns; state it is motivation, not
   evidence of Jev performance). Prefer public standards bodies, government pages, Wikipedia,
   Project Gutenberg, or official documentation. If a site blocks the fetch (403/404), choose another.

C. `<repo>/<folder>/collection.json` — same keys as the exemplar: title, short, description,
   families (list of {key,label} matching the family keys used), lead (2–4 sentences: who uses this,
   what the judgments are, that they are task-authored and advisory), bundle (which 3–4 IDs to start
   with and why), boundary (what code and people keep: exact checks, decisions, permissions, and any
   domain-specific safety or legal boundary), extra_results: [].

D. `<workdir>/design_<folder>.json` — a JSON list of 24 design fixtures, three per pattern, ids
   `<ID>-1`, `<ID>-2`, `<ID>-3`: a positive case, a counterexample with a DIFFERENT label, and a
   missing-evidence case where one required field is "" or [] or {} with expected "unknown".
   Each: {"id","pattern_id","version":1,"split":"design","author_origin":"<folder>_contract_author",
   "state":{...exactly the required_state_fields...},"expected":<label>,"rationale":<1–2 sentences>}.
   State values are strings, or lists/objects where the field is clearly a list or mapping.
   Every fixture state is SYNTHETIC: invented people, companies (.example domains), places, products,
   amounts. No real people, real companies, real credentials, phone numbers, account numbers, or
   copied text. Keep values to 1–6 sentences.

E. `<workdir>/module_<folder>.md` — a kernel reference module following the exemplar's five
   sections exactly (title; "Select the profile that fits" with an ID/family/checks table; choose-by
   bullets; "Prepare a bounded state"; "Use the labels without taking over"; a verification section).
   Use the site URL pattern https://seabass-up.github.io/jev-workflow-patterns/<folder>/ . Do not
   claim any screening result; say the evaluation page reports outcomes.

## Domain rules (apply all that fit your domain)
- Judge supplied text and documents, never a person's protected characteristics, health, ability,
  honesty, or worth. HR and grading profiles judge documents, work products, and process steps.
- Finance profiles classify document text and stated facts; nothing is investment, tax, or legal
  advice, and no amount is computed by the model.
- Cybersecurity and networking profiles are defensive triage of logs, reports, tickets, and
  configuration text; nothing describes exploitation, evasion, or attack tooling.
- Web-scraping profiles classify robots/ToS/notice text and page structure for compliance and
  data quality; nothing helps evade blocking or access controls.
- Auto repair, construction, electrical, motorsport: labels are readings of text, never a safety
  or fitness determination; the licensed or qualified person decides. Measurement profiles judge
  described procedures and reports; any comparison of numbers happens in code.
- Marketing, SEO, sales: classify content and claims; substantiation and legal compliance stay
  with people.
- Executive/CEO profiles judge memo and proposal text (decision framing, evidence, reversibility),
  never the decision itself.

## Finish
Run this structural check and fix anything it reports before replying:
`python3 <repo>/scripts/collection_pipeline/check_authoring.py <folder>`
Reply with one line: the folder, the pattern count, the number of sources, and the check result.
