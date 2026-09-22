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

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value:
                self.links.append(value)


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
    pages.extend([site / "index.html", site / "kernel" / "index.html"])
    for page in pages:
        if not page.is_file():
            raise ValueError("missing page: " + str(page))
        parser = Links()
        text = page.read_text()
        if "{{" in text or "{%" in text:
            raise ValueError("unrendered template in " + str(page))
        parser.feed(text)
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path.startswith(BASE):
                continue
            target = site / unquote(parsed.path[len(BASE):])
            if parsed.path.endswith("/"):
                target /= "index.html"
            if not target.is_file():
                raise ValueError("broken internal link from " + str(page) + ": " + link)
    if not pages:
        raise ValueError("no iteration pages found")
    return {"iteration_pages_verified": iteration_count,
            "email_pages_verified": email_count,
            "kernel_and_home_pages_verified": 2}


if __name__ == "__main__":
    print(json.dumps(verify(Path(sys.argv[1]))))
