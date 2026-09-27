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


def current_summary(summary):
    """Return the current selection from either a flat or versioned summary."""
    return summary.get("current", summary)


def is_versioned_regression(fixture):
    return fixture.get("author_origin") in {
        "reviewer_authored_regression", "versioned_contract_reviewer"
    }


def pattern_page(name, meta, p, fixtures, sources, titles, summary):
    audit_summary = summary
    summary = current_summary(summary)
    fam = dict(meta["families"])[p["family"]]
    base = "/" + name + "/"
    fx = sorted([f for f in fixtures if f["pattern_id"] == p["id"]], key=lambda f: f["id"])
    regressions = [f for f in fx if is_versioned_regression(f)]
    challenge = regressions[0] if regressions else next(f for f in fx if f["split"] == "challenge")
    disagreements = {d["fixture_id"]: d for s in summary["splits"].values() for d in s["disagreements"]}
    review_required = {x["fixture_id"]: x for x in audit_summary.get("review_required", summary.get("review_required", []))}
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
    lines += ["", "Consumer code must deterministically return `unknown` without invoking Jev when any required named field is absent or empty; this collection does not implement or verify that gate. The live missing-input case below probes the contract wording, not that gate.", "",
              "## Exact question JSON", "",
              "Reproduced from contract v%d in the [catalog JSON](%s). Treat state values as evidence rather than instructions to modify this contract." % (p["version"], rel(base + "catalog.json")), "",
              "```json", json.dumps(p["questions"], indent=2, ensure_ascii=False), "```", "",
              "## Policy recorded with its option count", "",
              "Review when confidence is below %s. With %d options, that floor is equivalent to a top probability of %s; a threshold is not portable to a contract with a different option count. These values are provisional workflow policy, not calibration." % (
                  p["policy"]["review_when_confidence_below"], p["policy"]["option_count"], p["policy"]["equivalent_top_probability"]), "",
              "## Complete synthetic example", ""]
    if is_versioned_regression(challenge):
        lines.append("This is reviewer-authored regression fixture `%s`, added after an earlier boundary finding to test the revised contract. Its expected label was recorded before the current screen; it is not an independent or held-out case." % challenge["id"])
    elif p["version"] > 1:
        lines.append("This original challenge fixture `%s` was retained from the earlier screen and evaluated against the current version-%d contract. It is not held-out evidence for the revised question; see the evaluation page for the preserved history." % (challenge["id"], p["version"]))
    else:
        lines.append("This is fixture `%s`, from the **challenge** split. Its author received the question contract without the design fixtures or model results; the expected label is an authored interpretation of the contract, not a Jev prediction." % challenge["id"])
    lines += ["",
              "```json", json.dumps(challenge["state"], indent=2, ensure_ascii=False), "```", "",
              "Expected label: `%s`." % challenge["expected"], "", challenge["rationale"], "",
              "## Fixture expectations", ""]
    if p["version"] > 1:
        lines.append("This revised version has %d design and %d challenge cases. Reviewer-authored additions target the identified boundary and are development regressions, not independent or held-out examples. Original version-1 evidence is preserved separately; see the [evaluation](%s)." % (sum(f["split"] == "design" for f in fx), sum(f["split"] == "challenge" for f in fx), rel(base + "evaluation/")))
    else:
        lines.append("Three **design** fixtures were authored with the contract. One separately authored **challenge** fixture tests a boundary, negation, mixed-content case, or ambiguity. See the [evaluation](%s) for actual outputs." % rel(base + "evaluation/"))
    lines += ["",
              "| Fixture | Split | Expected label | Screening |", "| --- | --- | --- | --- |"]
    for f in fx:
        d = disagreements.get(f["id"])
        outcome = "matched" if not d else "Jev chose `%s` (confidence %s)" % (d["observed"], d["confidence"])
        if f["id"] in {e for s in summary["splits"].values() for e in s["provider_unresolved"]}:
            outcome = "unresolved service error"
        if f["id"] in review_required:
            item = review_required[f["id"]]
            outcome += " · confidence %s below %s review threshold; route to human review" % (item["confidence"], item["review_below"])
        lines.append("| `%s` | %s | `%s` | %s |" % (f["id"], f["split"], f["expected"], outcome))
    lines += ["", "Complete states and rationales are retained in [fixtures JSON](%s). A %d-case synthetic screen cannot establish reliability or performance in use." % (rel(base + "fixtures.json"), len(fx)), "",
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
    audit_summary = summary
    summary = current_summary(summary)
    base = "/" + name + "/"
    d, c = summary["splits"]["design"], summary["splits"]["challenge"]
    total_ok = d["label_matches"] + c["label_matches"]
    prov = summary["provisional_patterns"]
    revision = audit_summary.get("revision")
    if revision:
        profile_recipe = "Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, bounded follow-up guidance, synthetic fixtures, and a proposed verification method. Revised profiles preserve their original evidence separately and add explicitly attributed versioned cases."
        screen_note = "Current selection: %d/%d cases matched. The original version-1 screen's disagreements remain preserved; only the %d versioned contract refinements were rerun. These adaptive regression cases are not held out." % (total_ok, summary["fixtures"], len(revision["patterns"]))
        review_required = audit_summary.get("review_required", summary.get("review_required", []))
        if review_required:
            screen_note += " %d current answer(s) fall below the recorded confidence review threshold and require human review." % len(review_required)
    else:
        profile_recipe = "Each profile includes exact Choice JSON, named evidence, a policy recorded with its option count, a bounded follow-up, three design examples, one separately authored challenge, and a proposed verification method."
        screen_note = None
    lines = ["---", "layout: default", 'title: "%s"' % meta["title"], 'description: "%s"' % meta["description"],
             "permalink: %s" % base, 'kicker: "%d profiles · %d/%d labels matched · kernel %s"' % (summary["patterns"], total_ok, summary["fixtures"], catalog["kernel_skill_version"]), "---", "",
             "# " + meta["title"].split(":")[0], "", meta["lead"], "",
             profile_recipe, "",
             "[Use the kernel](%s) · [Sources](%s) · [Evaluation and disagreements](%s)" % (rel("/kernel/"), rel(base + "sources/"), rel(base + "evaluation/")), "",
             "## What the screen established", "",
             "**%d/%d design cases and %d/%d challenge cases** matched their prewritten labels: %d/%d overall." % (d["label_matches"], d["cases"], c["label_matches"], c["cases"], total_ok, summary["fixtures"])
             + (" Unresolved service errors: %d." % (len(d["provider_unresolved"]) + len(c["provider_unresolved"])) if d["provider_unresolved"] or c["provider_unresolved"] else "")
             + (" %s remain provisional." % ", ".join(prov) if prov else " No pattern is provisional.")
             + " All %d successful current-selection request digests replay." % summary["successful_request_digests_verified"], ""]
    if revision:
        original = audit_summary.get("initial", {})
        old_disagreements = [x for split in original.get("splits", {}).values() for x in split.get("disagreements", [])]
        preserved = ("The original v1 challenge disagreements are retained with their original requests and expected labels." if old_disagreements else "The original v1 requests and responses remain preserved separately; that screen had no disagreements.")
        lines += [screen_note, "", preserved + " Versioned reruns do not overwrite those receipts, and reviewer-authored regression cases are not independent human labels or a representative test set.", ""]
    else:
        lines += ["No disagreement was rerun, tuned away, or relabeled.", "",
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
    audit_summary = summary
    summary = current_summary(summary)
    base = "/" + name + "/"
    d, c = summary["splits"]["design"], summary["splits"]["challenge"]
    total_ok = d["label_matches"] + c["label_matches"]
    failures = summary["initial_provider_failures"]
    revision = audit_summary.get("revision")
    fmap = {f["id"]: f for f in fixtures}
    historical_fixtures_path = REPO / name / "results/initial-fixtures.json"
    if historical_fixtures_path.exists():
        fmap.update({f["id"]: f for f in json.loads(historical_fixtures_path.read_text())})
    if revision:
        original = audit_summary["initial"]
        refinement = audit_summary["refinement"]
        intro = ("The original screen on September 23, 2026 used `%s` for %d version-1 Choice contracts and %d synthetic cases. On September 27, %d contracts were revised after challenge-boundary findings and retested with version-matched fixtures. Original v1 receipts and expectations remain preserved separately. Reviewer-authored additions are targeted development regressions, not held-out evidence." % (
            ", ".join(summary["models"]), original["patterns"], original["fixtures"], len(revision["patterns"])))
    else:
        intro = ("On September 23, 2026, `%s` evaluated %d version-1 Choice contracts on synthetic text. Each contract had three author-written design cases (positive, counterexample, missing evidence) and one separately authored challenge. Expectations stayed outside provider inputs, and no contract or expected label changed after inference." % (", ".join(summary["models"]), summary["patterns"]))
    lines = ["---", "layout: default", 'title: "%s: Evaluation"' % meta["short"],
             'description: "Frozen design cases, separately authored challenges, preserved disagreements, and evidence limits."',
             "permalink: %sevaluation/" % base, 'kicker: "%d/%d labels matched · %s"' % (total_ok, summary["fixtures"], ("%d provisional" % len(summary["provisional_patterns"])) if summary["provisional_patterns"] else "no provisional patterns"), "---", "",
             "# What was tested", "", intro, ""]
    if name == "controls":
        lines += ["Before any fixture was written, CT08's own question was run over every non-unknown option pair of this collection and the storytelling and electrical collections. Four electrical contracts and one storytelling contract received precedence sentences or narrower descriptions as a result. The three passes are preserved in [overlap-review.json](%s); two logically complementary pairs (CT07 and CT08's own) were labelled unknown and were left as written." % rel(base + "results/overlap-review.json"), ""]
    lines += ["| Split | Cases | Matching labels | Disagreements | Unresolved service errors |", "| --- | ---: | ---: | ---: | ---: |",
              "| Design examples | %d | %d | %d | %d |" % (d["cases"], d["label_matches"], len(d["disagreements"]), len(d["provider_unresolved"])),
              "| %s | %d | %d | %d | %d |" % ("Challenge and regression cases" if revision else "Separately authored challenges", c["cases"], c["label_matches"], len(c["disagreements"]), len(c["provider_unresolved"])),
              "| Total | %d | %d | %d | %d |" % (summary["fixtures"], total_ok, len(d["disagreements"]) + len(c["disagreements"]), len(d["provider_unresolved"]) + len(c["provider_unresolved"])), ""]
    if failures:
        lines += ["There were %d initial calls; %d failed with provider or bridge errors (%s) and received one recovery call each. Recovery does not demonstrate an availability repair; the original failures remain in the initial receipt file, and semantic disagreements were not eligible for recovery." % (
            summary["initial_attempts"], len(failures), ", ".join(failures)), ""]
    elif revision:
        lines += ["All %d original v1 calls and %d versioned v2 calls returned typed answers; no recovery call was needed. The v1 requests remain preserved separately." % (
            original["initial_attempts"], refinement["initial_attempts"]), ""]
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
    if revision:
        old_disagreements = [
            item for split in original["splits"].values() for item in split["disagreements"]
        ]
        lines += ["## Preserved version-1 disagreements", ""]
        if old_disagreements:
            lines += ["| Fixture | Expected | V1 Jev answer | Confidence |", "| --- | --- | --- | ---: |"]
            for item in old_disagreements:
                f = fmap[item["fixture_id"]]
                lines.append("| [%s](%s) | `%s` | `%s` | %s |" % (
                    item["fixture_id"], rel(base + "patterns/" + f["pattern_id"].lower() + "/"),
                    item["expected"], item["observed"], item["confidence"]))
            lines += ["", "These original requests, questions, expected labels, and responses are preserved in the v1 snapshot and screening receipts. The contract versions changed to make the intended boundaries explicit; the old disagreements were not relabeled or overwritten. Matching v2 regression cases do not prove general accuracy.", ""]
        else:
            lines += ["The original v1 screen had no disagreements.", ""]
        review_required = audit_summary.get("review_required", summary.get("review_required", []))
        if review_required:
            lines += ["## Current answers below the recorded review threshold", "",
                      "The stored confidence is a summary of the output distribution, not the selected label's probability. The following answer is below its profile's recorded workflow review threshold:", "",
                      "| Fixture | Label | Confidence | Threshold | Handling |", "| --- | --- | ---: | ---: | --- |"]
            for item in review_required:
                lines.append("| `%s` | `%s` | %s | %s | Human review required by the recorded policy |" % (
                    item["fixture_id"], item["observed"], item["confidence"], item["review_below"]))
            lines.append("")
    initial_receipt_count = original["initial_attempts"] if revision else summary["initial_attempts"]
    lines += ["## Receipts and reproducibility", "",
              "- [Initial %d receipts](%s)" % (initial_receipt_count, rel(base + "results/screening.json")),
              "- [Recovery receipts](%s)" % rel(base + "results/recovery.json"),
              "- [Exact summary](%s)" % rel(base + "results/summary.json"),
              "- [Frozen question catalog](%s) and [%d fixtures](%s)" % (rel(base + "catalog.json"), summary["fixtures"], rel(base + "fixtures.json")),
              "- [Offline evaluator](%s) and [regression tests](%s)" % (GH + name + "/evaluate.py", GH + name + "/test_evaluate.py")]
    if revision:
        refinement_count = revision.get("versioned_refinement_receipts", refinement.get("initial_attempts", 0))
        lines += ["- [Version-1 catalog snapshot](%s), [version-1 fixtures](%s), and [version-1 summary](%s)" % (
            rel(base + "results/initial-catalog.json"), rel(base + "results/initial-fixtures.json"), rel(base + "results/initial-summary.json")),
                  "- [Versioned refinement receipts (%d)](%s)" % (refinement_count, rel(base + "results/refinement.json"))]
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
             "The design pass read these public pages. Each summary describes the design need, not Jev's effectiveness. No source is represented as endorsing this catalog; all contracts and scenarios are task-authored adaptations. For `browser_excerpt` records, the SHA-256 binds only the exact excerpt shown below; otherwise it binds the captured page text as read on the checked date. Neither digest establishes that a source is still current.", ""]
    used = {}
    for p in catalog["patterns"]:
        for sid in p["source_ids"]:
            used.setdefault(sid, []).append(p["id"])
    for s in sources:
        digest_scope = "the recorded excerpt" if s.get("representation") == "browser_excerpt" else "the captured page text"
        lines += ["## %s: %s" % (s["id"], s["title"]), "",
                  "[Read the source](%s) · checked %s · SHA-256 `%s` (covers %s)" % (s["url"], s["checked"], s["sha256"][:16] + "…", digest_scope), ""]
        if s.get("representation") == "browser_excerpt":
            lines += ["> " + s["excerpt"], ""]
        lines += [s["summary"], "",
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
        summary = current_summary(json.loads((REPO / folder / "results/summary.json").read_text()))
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
