"""Build the public pattern finder and the shared catalog counts from source JSON."""

import html
import json
import re
from pathlib import Path

from build_collection_pages import pattern_url


ROOT = Path(__file__).resolve().parents[1]
AREAS = (
    ("Research catalogs", "research", [ROOT / "iterations" / f"{i:02d}" / "catalog.json" for i in range(1, 5)]),
    ("Email", "email", [ROOT / "email/catalog.json"]),
    ("Bug hunting", "bug-hunting", [ROOT / "bug-hunting/catalog.json"]),
    ("People and AI", "people-ai", [ROOT / "human-ai/catalog.json"]),
    ("Domain collections", "domain", sorted(ROOT.glob("*/collection.json"))),
)


def relative_url(path):
    return "{{ '" + path + "' | relative_url }}"


def source_groups():
    groups = []
    for area_label, area_slug, sources in AREAS:
        for source in sources:
            folder = source.parent
            catalog = json.loads((folder / "catalog.json").read_text())
            meta = json.loads(source.read_text()) if source.name == "collection.json" else None
            if meta:
                label = meta["short"]
                summary = json.loads((folder / "results/summary.json").read_text())
                provisional = set(summary["provisional_patterns"])
            elif area_slug == "research":
                label = "Research iteration " + folder.name.lstrip("0")
                provisional = set()
            else:
                label = {"email": "Email", "bug-hunting": "Bug hunting", "people-ai": "People and AI"}[area_slug]
                provisional = set()
                if area_slug == "bug-hunting":
                    provisional = {"BH41"}
                elif area_slug == "people-ai":
                    summary = json.loads((folder / "results/summary.json").read_text())
                    provisional = set(summary["provisional_patterns"])
            date = catalog.get("created_date") or catalog.get("created_at") or catalog.get("date") or ""
            groups.append({"area": area_slug, "area_label": area_label, "slug": folder.relative_to(ROOT).as_posix(),
                           "label": label, "patterns": catalog["patterns"], "provisional": provisional, "date": date})
    return groups


def build():
    groups = source_groups()
    ids = [p["id"] for group in groups for p in group["patterns"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate pattern ID in catalog source")
    skill = (ROOT / "skills/jev-question-kernel-catalog/SKILL.md").read_text()
    version_match = re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', skill, re.MULTILINE)
    if not version_match:
        raise ValueError("kernel version missing from skill metadata")
    metadata = {"total_profiles": len(ids), "source_catalogs": len(groups),
                "domain_collections": sum(group["area"] == "domain" for group in groups),
                "domain_profiles": sum(len(group["patterns"]) for group in groups if group["area"] == "domain"),
                "kernel_version": version_match.group(1), "catalog_date": max(group["date"] for group in groups)}
    data_dir = ROOT / "_data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "catalog_summary.json").write_text(json.dumps(metadata, indent=2) + "\n")

    lines = ["---", "layout: default", "title: Find a pattern",
             "description: Search all published Jev question profiles by task, collection, question type, and review flag.",
             "permalink: /catalog/", "kicker: 'All %d question profiles'" % len(ids), "---", "",
             "# Find a pattern", "",
             "Search by the judgment your workflow needs. Each profile links to its required evidence, exact JSON, follow-up, and evaluation. The three foundational guides are [on the home page]({{ '/' | relative_url }}) and are counted separately.", "",
             "**Provisional** means a recorded screening disagreement. Other profiles still need review before use; research iterations keep their review states on their own evaluation pages.", "",
             '<div class="finder-controls" role="search" aria-label="Filter question patterns">',
             '  <label>Search questions<input id="pattern-search" type="search" placeholder="Try refund, RFI, citation…" autocomplete="off"></label>',
             '  <label>Area<select id="pattern-area"><option value="">All areas</option>']
    for area_label, area_slug, _ in AREAS:
        lines.append('    <option value="%s">%s</option>' % (area_slug, html.escape(area_label)))
    lines += ['  </select></label>', '  <label>Collection<select id="pattern-collection"><option value="">All collections</option>']
    for group in groups:
        lines.append('    <option value="%s">%s</option>' % (html.escape(group["slug"]), html.escape(group["label"])))
    lines += ['  </select></label>',
              '  <label>Question type<select id="pattern-type"><option value="">All types</option><option value="choice">Choice</option><option value="score">Score</option><option value="noul">Noul</option></select></label>',
              '  <label>Review flag<select id="pattern-review"><option value="">All profiles</option><option value="provisional">Explicitly provisional</option></select></label>',
              '  <button id="pattern-clear" type="button">Clear filters</button>', '</div>', '',
              '<p id="pattern-count" role="status" aria-live="polite">%d patterns shown</p>' % len(ids),
              '<p id="pattern-empty" class="callout" hidden>No patterns match those filters. Try fewer terms or clear the filters.</p>', '',
              '<section aria-labelledby="all-patterns-heading">', '  <h2 id="all-patterns-heading">All patterns</h2>', '  <div class="pattern-grid">']
    for group in groups:
        for p in group["patterns"]:
            types = sorted({q.get("type", "").lower() for q in p.get("questions", {}).values()} - {""})
            if not types or not set(types).issubset({"choice", "score", "noul"}):
                raise ValueError("unknown question type in " + p["id"])
            description = p.get("purpose") or p.get("value") or p.get("benefit") or "Read the question contract and evaluation."
            flagged = p["id"] in group["provisional"]
            lines += ['    <article class="pattern-card" data-area="%s" data-collection="%s" data-types="%s" data-review="%s">' %
                      (group["area"], html.escape(group["slug"]), " ".join(types), "provisional" if flagged else ""),
                      '      <div class="pattern-meta"><span>%s</span><span>%s</span>%s</div>' %
                      (html.escape(group["label"]), html.escape(" / ".join(types).title()),
                       '<span class="provisional-tag">Provisional</span>' if flagged else ""),
                      '      <h3><a href="%s">%s · %s</a></h3>' % (relative_url(pattern_url(p["id"])), html.escape(p["id"]), html.escape(p["title"])),
                      '      <p>%s</p>' % html.escape(description), '    </article>']
    lines += ['  </div>', '</section>', '',
              '[Kernel and question design]({{ "/kernel/" | relative_url }}) · [Domain collection results]({{ "/collections/" | relative_url }}) · [Source and skills](https://github.com/Seabass-up/jev-workflow-patterns)',
              '<script src="{{ "/assets/catalog.js" | relative_url }}?v=20260923a" defer></script>', '']
    finder = ROOT / "catalog"
    finder.mkdir(exist_ok=True)
    (finder / "index.md").write_text("\n".join(lines))
    print(json.dumps(metadata))


if __name__ == "__main__":
    build()
