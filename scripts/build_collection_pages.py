"""Generate Jekyll pages for a pattern collection from its frozen catalog, fixtures, sources, and summary.

Usage: python3 scripts/build_collection_pages.py <collection> [<collection> ...]
Reads <collection>/collection.json for titles, families, and boundary text. Prefix
routes for cross-collection links are in PREFIX_URL; add a prefix when a collection is added.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GH = "https://github.com/Seabass-up/jev-workflow-patterns/blob/main/"
RAW = "https://raw.githubusercontent.com/Seabass-up/jev-workflow-patterns/main/"

def load_meta(name):
    """Collection metadata lives in <collection>/collection.json."""
    doc = json.loads((REPO / name / "collection.json").read_text())
    return {"title": doc["title"], "short": doc["short"], "description": doc["description"],
            "families": [(f["key"], f["label"]) for f in doc["families"]],
            "lead": doc["lead"], "bundle": doc["bundle"], "boundary": doc["boundary"],
            "extra_results": [(x["label"], x["path"]) for x in doc.get("extra_results", [])]}


PREFIX_URL = {"EM": "/email/patterns/", "BH": "/bug-hunting/patterns/", "HA": "/human-ai/patterns/"}
for _folder in sorted(p.parent.name for p in Path(__file__).resolve().parents[1].glob("*/collection.json")):
    _catalog = json.loads((Path(__file__).resolve().parents[1] / _folder / "catalog.json").read_text())
    if _catalog["patterns"]:
        PREFIX_URL[_catalog["patterns"][0]["id"][:2]] = "/" + _folder + "/patterns/"


def all_titles():
    titles = {}
    for path in [*sorted(REPO.glob("iterations/[0-9][0-9]/catalog.json")), *sorted(REPO.glob("*/collection.json")),
                 *[REPO / f"{c}/catalog.json" for c in ("email", "bug-hunting", "human-ai")]]:
        if path.name == "collection.json":
            path = path.with_name("catalog.json")
        for p in json.loads(path.read_text())["patterns"]:
            titles[p["id"]] = p["title"]
    return titles


def pattern_url(pid):
    prefix = pid[:2]
    if prefix in PREFIX_URL:
        return PREFIX_URL[prefix] + pid.lower() + "/"
    letter, number = pid[0], int(pid[1:])
    per = {"B": 7, "E": 7, "L": 6, "H": 10}[letter]
    return "/iterations/%02d/patterns/%s/" % ((number - 1) // per + 1, pid.lower())


def rel(path):
    return "{{ '" + path + "' | relative_url }}"


def link(pid, titles):
    return "[%s: %s](%s)" % (pid, titles.get(pid, pid), rel(pattern_url(pid)))


def pattern_page(name, meta, p, fixtures, sources, titles, summary):
    fam = dict(meta["families"])[p["family"]]
    base = "/" + name + "/"
    fx = sorted([f for f in fixtures if f["pattern_id"] == p["id"]], key=lambda f: f["id"])
    challenge = next(f for f in fx if f["split"] == "challenge")
    disagreements = {d["fixture_id"]: d for s in summary["splits"].values() for d in s["disagreements"]}
    provisional = p["id"] in summary["provisional_patterns"]
    lines = ["---", "layout: default", 'title: "%s — %s"' % (p["id"], p["title"].replace('"', "'")),
             'description: "%s"' % p["purpose"].replace('"', "'"), "permalink: %spatterns/%s/" % (base, p["id"].lower()),
             'kicker: "%s · %s%s"' % (meta["short"], fam, " · provisional" if provisional else ""), "---", "",
             "# %s — %s" % (p["id"], p["title"]), "",
             "[%s catalog](%s) · [Evaluation and limitations](%s) · [Kernel reference module](%s)" % (
                 meta["short"], rel(base), rel(base + "evaluation/"), RAW + "skills/jev-question-kernel-catalog/references/%s.md" % name), "",
             p["purpose"], "",
             "This is a proposed, bounded text judgment. Consult the [evaluation record](%s) for observed results; the fixture labels below are intended outputs." % rel(base + "evaluation/"), ""]
    if provisional:
        lines += ["<div class=\"callout warning\"><p><strong>Provisional.</strong> At least one screening case disagreed with its authored label or did not complete. The disagreement is preserved on the evaluation page; neither the contract nor the label was changed after inference.</p></div>", ""]
    lines += ["## Proposed benefit", "", p["benefit"], "",
              "This is a proposed benefit, not an observed outcome. All fixtures on this page are synthetic.", "",
              "## Required named state", "", "Supply the following named fields as the evidence packet:", ""]
    lines += ["- `%s`" % f for f in p["required_state_fields"]]
    lines += ["", "Code deterministically returns `unknown` without invoking Jev when any required named field is absent or empty; the model is not the required-field gate. The live missing-input case below probes the contract wording, not that gate.", "",
              "## Exact question JSON", "",
              "Reproduced from the frozen [catalog JSON](%s). Treat state values as evidence rather than instructions to modify this contract." % rel(base + "catalog.json"), "",
              "```json", json.dumps(p["questions"], indent=2, ensure_ascii=False), "```", "",
              "## Policy recorded with its option count", "",
              "Review when confidence is below %s. With %d options, that floor is equivalent to a top probability of %s; a threshold is not portable to a contract with a different option count. These values are provisional workflow policy, not calibration." % (
                  p["policy"]["review_when_confidence_below"], p["policy"]["option_count"], p["policy"]["equivalent_top_probability"]), "",
              "## Complete synthetic example", "",
              "This is fixture `%s`, from the **challenge** split. Its author received the question contract without the design fixtures or model results; the expected label is an authored interpretation of the contract, not a Jev prediction." % challenge["id"], "",
              "```json", json.dumps(challenge["state"], indent=2, ensure_ascii=False), "```", "",
              "Expected label: `%s`." % challenge["expected"], "", challenge["rationale"], "",
              "## All four fixture expectations", "",
              "Three **design** fixtures were authored with the contract. One separately authored **challenge** fixture tests a boundary, negation, mixed-content case, or ambiguity. See the [evaluation](%s) for actual outputs." % rel(base + "evaluation/"), "",
              "| Fixture | Split | Expected label | Screening |", "| --- | --- | --- | --- |"]
    for f in fx:
        d = disagreements.get(f["id"])
        outcome = "matched" if not d else "Jev chose `%s` (confidence %s)" % (d["observed"], d["confidence"])
        if f["id"] in {e for s in summary["splits"].values() for e in s["provider_unresolved"]}:
            outcome = "unresolved service error"
        lines.append("| `%s` | %s | `%s` | %s |" % (f["id"], f["split"], f["expected"], outcome))
    lines += ["", "Complete states and rationales are retained in [fixtures JSON](%s). A four-case synthetic screen cannot establish reliability or performance in use." % rel(base + "fixtures.json"), "",
              "## Code-owned responsibilities", "", p["code_owned"], "",
              "The judgment is advisory. Code and the responsible person retain control of exact identifiers, data access, state changes, and consequential verification.", "",
              "## Bounded follow-up", "", p["follow_up"], "",
              "## Verification recipe", "", p["verification"], "",
              "This describes required verification work, not checks already performed.", "",
              "## Source inspiration", ""]
    smap = {s["id"]: s for s in sources}
    for sid in p["source_ids"]:
        s = smap[sid]
        lines.append("- [%s](%s) (%s). %s" % (s["title"], s["url"], sid, s["summary"]))
    lines += ["", "These sources motivate the design problem and its boundaries. They do not demonstrate Jev performance on this question.", "",
              "## Nearest existing patterns and distinctness", ""]
    lines += ["- " + link(n, titles) for n in p["nearest_existing"]]
    lines += ["", p["distinctness"], "",
              "[Back to %s](%s) · [Evaluation and limitations](%s)" % (meta["short"], rel(base), rel(base + "evaluation/")), ""]
    return "\n".join(lines)


def index_page(name, meta, catalog, fixtures, summary, titles):
    base = "/" + name + "/"
    d, c = summary["splits"]["design"], summary["splits"]["challenge"]
    total_ok = d["label_matches"] + c["label_matches"]
    prov = summary["provisional_patterns"]
    lines = ["---", "layout: default", 'title: "%s"' % meta["title"], 'description: "%s"' % meta["description"],
             "permalink: %s" % base, 'kicker: "%d profiles · %d/%d labels matched · kernel %s"' % (summary["patterns"], total_ok, summary["fixtures"], catalog["kernel_skill_version"]), "---", "",
             "# " + meta["title"].split(":")[0], "", meta["lead"], "",
             "Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method.", "",
             "[Use the kernel](%s) · [Sources](%s) · [Evaluation and disagreements](%s)" % (rel("/kernel/"), rel(base + "sources/"), rel(base + "evaluation/")), "",
             "## What the screen established", "",
             "**%d/%d design cases and %d/%d challenge cases** matched their prewritten labels: %d/%d overall." % (d["label_matches"], d["cases"], c["label_matches"], c["cases"], total_ok, summary["fixtures"])
             + (" Unresolved service errors: %d." % (len(d["provider_unresolved"]) + len(c["provider_unresolved"])) if d["provider_unresolved"] or c["provider_unresolved"] else "")
             + (" %s remain provisional." % ", ".join(prov) if prov else " No pattern is provisional.")
             + " All %d successful request digests replay. No disagreement was rerun, tuned away, or relabeled." % summary["successful_request_digests_verified"], "",
             "The challenge author saw each contract but not its design examples or model results. That is an author-separation check, not independent human labeling, a representative test set, or a measure of benefit in use.", ""]
    for key, label in meta["families"]:
        lines += ["## " + label, "", "| ID | Question pattern | Intended use |", "| --- | --- | --- |"]
        for p in catalog["patterns"]:
            if p["family"] != key:
                continue
            tag = " · provisional" if p["id"] in prov else ""
            lines.append("| %s%s | [%s](%s) | %s |" % (p["id"], tag, p["title"], rel(base + "patterns/" + p["id"].lower() + "/"), p["benefit"]))
        lines.append("")
    lines += ["## Start with a small bundle", "", meta["bundle"], "",
              "Batch questions only when their required evidence belongs to one coherent state. Every fixture in this screen was a separate request.", "",
              "## Keep the boundary explicit", "", meta["boundary"], "",
              "[Exact catalog](%s) · [%d frozen fixtures](%s) · [Kernel module](%s)" % (rel(base + "catalog.json"), summary["fixtures"], rel(base + "fixtures.json"), GH + "skills/jev-question-kernel-catalog/references/%s.md" % name), ""]
    return "\n".join(lines)


def evaluation_page(name, meta, catalog, fixtures, summary, initial, recovery):
    base = "/" + name + "/"
    d, c = summary["splits"]["design"], summary["splits"]["challenge"]
    total_ok = d["label_matches"] + c["label_matches"]
    failures = summary["initial_provider_failures"]
    fmap = {f["id"]: f for f in fixtures}
    lines = ["---", "layout: default", 'title: "%s: Evaluation"' % meta["short"],
             'description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."',
             "permalink: %sevaluation/" % base, 'kicker: "%d/%d labels matched · %s"' % (total_ok, summary["fixtures"], ("%d provisional" % len(summary["provisional_patterns"])) if summary["provisional_patterns"] else "no provisional patterns"), "---", "",
             "# What was tested", "",
             "On September 23, 2026, `%s` evaluated %d version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference." % (", ".join(summary["models"]), summary["patterns"]), ""]
    if name == "controls":
        lines += ["Before any fixture was written, CT08's own question was run over every non-unknown option pair of this collection and the storytelling and electrical collections. Four electrical contracts and one storytelling contract received precedence sentences or narrower descriptions as a result. The three passes are preserved in [overlap-review.json](%s); two logically complementary pairs (CT07 and CT08's own) were labelled unknown and were left as written." % rel(base + "results/overlap-review.json"), ""]
    lines += ["| Split | Cases | Matching labels | Disagreements | Unresolved service errors |", "| --- | ---: | ---: | ---: | ---: |",
              "| Design examples | %d | %d | %d | %d |" % (d["cases"], d["label_matches"], len(d["disagreements"]), len(d["provider_unresolved"])),
              "| Separately authored challenges | %d | %d | %d | %d |" % (c["cases"], c["label_matches"], len(c["disagreements"]), len(c["provider_unresolved"])),
              "| Total | %d | %d | %d | %d |" % (summary["fixtures"], total_ok, len(d["disagreements"]) + len(c["disagreements"]), len(d["provider_unresolved"]) + len(c["provider_unresolved"])), ""]
    if failures:
        lines += ["There were %d initial calls; %d failed with provider or bridge errors (%s) and received one recovery call each. Recovery does not demonstrate an availability repair; the original failures remain in the initial receipt file, and semantic disagreements were not eligible for recovery." % (
            summary["initial_attempts"], len(failures), ", ".join(failures)), ""]
    else:
        lines += ["All %d initial calls returned a typed answer; no recovery call was needed." % summary["initial_attempts"], ""]
    dis = d["disagreements"] + c["disagreements"]
    lines += ["## Preserve the disagreements", ""]
    if dis:
        lines += ["| Fixture | Split | Expected | Jev chose | Reported confidence | Consequence |", "| --- | --- | --- | --- | ---: | --- |"]
        for x in dis:
            f = fmap[x["fixture_id"]]
            lines.append("| [%s](%s) | %s | `%s` | `%s` | %s | Pattern remains provisional |" % (
                x["fixture_id"], rel(base + "patterns/" + f["pattern_id"].lower() + "/"), f["split"], x["expected"], x["observed"], x["confidence"]))
        lines += [""]
        for x in dis:
            f = fmap[x["fixture_id"]]
            lines.append("- %s: %s" % (x["fixture_id"], f["rationale"]))
        lines += ["", "These are disagreements against authored expectations, not automatically proven model defects. Confidence summarizes the output distribution and follows the option count; it is not the chosen label's probability and not a correctness guarantee.", ""]
    else:
        lines += ["Every case matched its authored label. A full match on %d synthetic cases is a small design check, not evidence of accuracy in use." % summary["fixtures"], ""]
    lines += ["## Receipts and reproducibility", "",
              "- [Initial %d receipts](%s)" % (summary["initial_attempts"], rel(base + "results/screening.json")),
              "- [Recovery receipts](%s)" % rel(base + "results/recovery.json"),
              "- [Exact summary](%s)" % rel(base + "results/summary.json"),
              "- [Frozen question catalog](%s) and [%d fixtures](%s)" % (rel(base + "catalog.json"), summary["fixtures"], rel(base + "fixtures.json")),
              "- [Offline evaluator](%s) and [regression tests](%s)" % (GH + name + "/evaluate.py", GH + name + "/test_evaluate.py")]
    for label, path in meta["extra_results"]:
        lines.append("- [%s](%s)" % (label, rel(base + path)))
    lines += ["", "Run from the repository root with Python 3:", "", "```sh", "python3 %s/evaluate.py" % name,
              "python3 -m unittest discover -s %s -p 'test_*.py' -v" % name, "```", "",
              "The evaluator checks exact state/question/version binding, request hashes, model identity, answer and probability coverage, the consistency of each stored confidence with its probabilities, fixture splits, source references, and recovery eligibility. A retained known disagreement does not fail CI; changing or hiding it does.", "",
              "Successful fixture responses report %s input tokens and %s output tokens. The local bridge estimates their total cost at $%s. That is an estimate, not an invoice, and excludes design-review calls and any billing for failed calls." % (
                  format(summary["reported_input_tokens"], ","), format(summary["reported_output_tokens"], ","), summary["reported_bridge_estimated_cost_usd"]), "",
              "## What remains untested", "",
              "There is one small synthetic challenge per pattern, no random sample, repeatability experiment, human-label agreement study, calibration assessment, subgroup assessment, or integration with a real workflow. Pattern-specific verification recipes are proposed next steps, not completed experiments.", "",
              "Before adoption, independently label representative authorized examples, choose the cost of each error, assess abstention and false positives, and measure the actual outcome. Keep deterministic missing-evidence and action controls outside the model.", "",
              "[Back to the collection](%s)" % rel(base), ""]
    return "\n".join(lines)


def sources_page(name, meta, catalog, sources):
    base = "/" + name + "/"
    lines = ["---", "layout: default", 'title: "%s: Sources"' % meta["short"],
             'description: "Public pages that motivated the question designs, with the digest of each page as read."',
             "permalink: %ssources/" % base, 'kicker: "%d sources · inspiration, not a performance claim"' % len(sources), "---", "",
             "# Inspiration, not a performance claim", "",
             "The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. The SHA-256 binds the page text as fetched on the listed date, not a claim that the page is unchanged since.", ""]
    used = {}
    for p in catalog["patterns"]:
        for sid in p["source_ids"]:
            used.setdefault(sid, []).append(p["id"])
    for s in sources:
        lines += ["## %s: %s" % (s["id"], s["title"]), "",
                  "[Read the source](%s) · checked %s · SHA-256 `%s`" % (s["url"], s["checked"], s["sha256"][:16] + "…"), "", s["summary"], "",
                  "Used by: " + (", ".join("[%s](%s)" % (pid, rel(base + "patterns/" + pid.lower() + "/")) for pid in used.get(s["id"], [])) or "no pattern directly"), ""]
    lines += ["Full digests are in [sources.json](%s)." % rel(base + "sources.json"), "", "[Back to the collection](%s)" % rel(base), ""]
    return "\n".join(lines)


def generate(name):
    meta = load_meta(name)
    root = REPO / name
    catalog = json.loads((root / "catalog.json").read_text())
    fixtures = json.loads((root / "fixtures.json").read_text())
    sources = json.loads((root / "sources.json").read_text())
    summary = json.loads((root / "results/summary.json").read_text())
    initial = json.loads((root / "results/screening.json").read_text())
    recovery = json.loads((root / "results/recovery.json").read_text())
    titles = all_titles()
    for p in catalog["patterns"]:
        (root / "patterns" / (p["id"].lower() + ".md")).write_text(pattern_page(name, meta, p, fixtures, sources, titles, summary))
    (root / "index.md").write_text(index_page(name, meta, catalog, fixtures, summary, titles))
    (root / "evaluation.md").write_text(evaluation_page(name, meta, catalog, fixtures, summary, initial, recovery))
    (root / "sources.md").write_text(sources_page(name, meta, catalog, sources))
    print(name, "pages written:", len(catalog["patterns"]) + 3)


def hub_page():
    """Write collections/index.md listing every collection with its screen result."""
    rows = []
    for meta_path in sorted(REPO.glob("*/collection.json")):
        folder = meta_path.parent.name
        meta = load_meta(folder)
        catalog = json.loads((REPO / folder / "catalog.json").read_text())
        summary = json.loads((REPO / folder / "results/summary.json").read_text())
        d, c = summary["splits"]["design"], summary["splits"]["challenge"]
        prov = ", ".join(summary["provisional_patterns"]) or "none"
        ids = catalog["patterns"][0]["id"] + "–" + catalog["patterns"][-1]["id"]
        rows.append('  <article class="collection-card"><h2><a href="%s">%s</a></h2><dl>'
                    '<div><dt>IDs</dt><dd>%s</dd></div><div><dt>Profiles</dt><dd>%d</dd></div>'
                    '<div><dt>Synthetic labels matched</dt><dd>%d/%d</dd></div>'
                    '<div><dt>Provisional</dt><dd>%s</dd></div></dl></article>' %
                    (rel("/" + folder + "/"), meta["short"], ids, summary["patterns"],
                     d["label_matches"] + c["label_matches"], summary["fixtures"], prov))
    total = sum(json.loads((p.parent / "catalog.json").read_text())["patterns"].__len__() for p in REPO.glob("*/collection.json"))
    lines = ["---", "layout: default", 'title: "Pattern collections"',
             'description: "Every domain collection built on the kernel: contracts, fixtures, live screens, evaluators, and modules."',
             "permalink: /collections/", 'kicker: "%d collections · %d profiles"' % (len(rows), total), "---", "",
             "Each collection reports its synthetic screen result and any provisional profiles. Every profile has an explicit `unknown`, frozen fixtures, preserved receipts, and an evaluation page. These screens do not qualify a real workflow.", "",
             "[Find a pattern across all {{ site.data.catalog_summary.total_profiles }} question profiles]({{ '/catalog/' | relative_url }}). The count below covers this newer format; four research catalogs, email, bug hunting, and human–AI keep their own pages.", "",
             '<div class="collection-grid">', *rows, '</div>', "",
             "New patterns found while using Jev enter through the [discovery intake]({{ '/discovery/' | relative_url }}).", ""]
    (REPO / "collections").mkdir(exist_ok=True)
    (REPO / "collections/index.md").write_text("\n".join(lines))
    print("hub written:", len(rows), "collections,", total, "profiles")


if __name__ == "__main__":
    if sys.argv[1:] == ["--hub"]:
        hub_page()
    else:
        for name in sys.argv[1:]:
            generate(name)
