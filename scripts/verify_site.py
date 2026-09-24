"""Verify every catalog page and its internal links in the built static site."""
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = "/jev-workflow-patterns/"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1_count = 0
        self.pattern_card_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.h1_count += 1
        if tag == "article" and "pattern-card" in dict(attrs).get("class", "").split():
            self.pattern_card_count += 1
        for key, value in attrs:
            if key in ("href", "src") and value:
                self.links.append(value)


def check_local_link(site, page, link):
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc or not parsed.path.startswith("/"):
        return
    if not parsed.path.startswith(BASE):
        raise ValueError("internal link omits project base URL from " + str(page) + ": " + link)
    target = site / unquote(parsed.path[len(BASE):])
    if parsed.path.endswith("/"):
        target /= "index.html"
    if not target.is_file():
        raise ValueError("broken internal link from " + str(page) + ": " + link)


def verify(site):
    pages = []
    for catalog_path in sorted((ROOT / "iterations").glob("[0-9][0-9]/catalog.json")):
        catalog = json.loads(catalog_path.read_text())
        folder = catalog_path.parent.name
        if len(catalog["patterns"]) != 30:
            raise ValueError("expected 30 patterns in " + folder)
        for p in catalog["patterns"]:
            page = site / "iterations" / folder / "patterns" / p["id"].lower() / "index.html"
            if not page.is_file():
                raise ValueError("missing pattern page: " + str(page))
            if p["id"] not in page.read_text():
                raise ValueError("pattern identifier not rendered: " + str(page))
            pages.append(page)
        for name in ("index.html", "evaluation/index.html", "question-kernel/index.html", "sources/index.html"):
            page = site / "iterations" / folder / name
            if not page.is_file():
                raise ValueError("missing supporting page: " + str(page))
            pages.append(page)
    iteration_count = len(pages)
    email_catalog = json.loads((ROOT / "email/catalog.json").read_text())
    if len(email_catalog["patterns"]) < 12:
        raise ValueError("expected at least twelve email profiles")
    for p in email_catalog["patterns"]:
        page = site / "email/patterns" / p["id"].lower() / "index.html"
        if not page.is_file() or p["id"] not in page.read_text():
            raise ValueError("missing email pattern or identifier: " + str(page))
        pages.append(page)
    for name in ("index.html", "evaluation/index.html", "sources/index.html"):
        pages.append(site / "email" / name)
    email_count = len(pages) - iteration_count
    bug_catalog = json.loads((ROOT / "bug-hunting/catalog.json").read_text())
    if len(bug_catalog["patterns"]) != 48:
        raise ValueError("expected 48 bug-hunting profiles")
    for p in bug_catalog["patterns"]:
        page = site / "bug-hunting/patterns" / p["id"].lower() / "index.html"
        if not page.is_file() or p["id"] not in page.read_text():
            raise ValueError("missing bug-hunting page or identifier: " + str(page))
        pages.append(page)
    for name in ("index.html", "evaluation/index.html", "sources/index.html"):
        pages.append(site / "bug-hunting" / name)
    bug_count = len(pages) - iteration_count - email_count
    human_catalog = json.loads((ROOT / "human-ai/catalog.json").read_text())
    if len(human_catalog["patterns"]) != 24:
        raise ValueError("expected 24 human-AI profiles")
    for p in human_catalog["patterns"]:
        page = site / "human-ai/patterns" / p["id"].lower() / "index.html"
        if not page.is_file() or p["id"] not in page.read_text():
            raise ValueError("missing human-AI page or identifier: " + str(page))
        pages.append(page)
    for name in ("index.html", "evaluation/index.html", "research/index.html", "sources/index.html"):
        pages.append(site / "human-ai" / name)
    human_count = len(pages) - iteration_count - email_count - bug_count
    collection_count = 0
    # Every folder with a collection.json is a pattern collection built by scripts/build_collection_pages.py.
    for meta_path in sorted(ROOT.glob("*/collection.json")):
        folder = meta_path.parent.name
        catalog = json.loads((ROOT / folder / "catalog.json").read_text())
        if len(catalog["patterns"]) < 8:
            raise ValueError("expected at least 8 %s profiles" % folder)
        for p in catalog["patterns"]:
            page = site / folder / "patterns" / p["id"].lower() / "index.html"
            if not page.is_file() or p["id"] not in page.read_text():
                raise ValueError("missing %s page or identifier: %s" % (folder, page))
            pages.append(page)
            collection_count += 1
        for name in ("index.html", "evaluation/index.html", "sources/index.html"):
            pages.append(site / folder / name)
            collection_count += 1
    pages.extend([site / "index.html", site / "kernel" / "index.html", site / "kernel" / "qualification" / "index.html",
                  site / "kernel" / "qualification" / "public-issue-pilot" / "index.html", site / "collections" / "index.html",
                  site / "catalog" / "index.html",
                  site / "discovery" / "index.html",
                  site / "discovery" / "introduction-review" / "index.html"])
    catalog_profiles = sum(len(json.loads(p.read_text())["patterns"]) for p in sorted(ROOT.glob("*/catalog.json")))
    catalog_profiles += sum(len(json.loads(p.read_text())["patterns"]) for p in sorted(ROOT.glob("iterations/[0-9][0-9]/catalog.json")))
    for page in pages:
        if not page.is_file():
            raise ValueError("missing page: " + str(page))
        parser = Links()
        text = page.read_text()
        if "{{" in text or "{%" in text:
            raise ValueError("unrendered template in " + str(page))
        parser.feed(text)
        if parser.h1_count != 1:
            raise ValueError("expected one main heading in " + str(page) + ": " + str(parser.h1_count))
        if page == site / "catalog" / "index.html" and parser.pattern_card_count != catalog_profiles:
            raise ValueError("finder does not contain every catalog profile")
        for link in parser.links:
            check_local_link(site, page, link)
    if not pages:
        raise ValueError("no iteration pages found")
    return {"iteration_pages_verified": iteration_count,
            "email_pages_verified": email_count,
            "bug_hunting_pages_verified": bug_count,
            "human_ai_pages_verified": human_count,
            "collection_pages_verified": collection_count,
            "kernel_home_hub_and_discovery_pages_verified": 8,
            "catalog_profiles_verified": catalog_profiles}


if __name__ == "__main__":
    print(json.dumps(verify(Path(sys.argv[1]))))
