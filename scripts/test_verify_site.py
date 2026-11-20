import tempfile
from pathlib import Path
import unittest
from verify_site import check_local_link


class ProjectLinkTests(unittest.TestCase):
    def test_missing_base_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "omits project base"):
                check_local_link(Path(folder), "source.html", "/human-ai/")

    def test_missing_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "broken internal link"):
                check_local_link(Path(folder), "source.html", "/jev-workflow-patterns/human-ai/")

    def test_existing_target_and_external_links(self):
        with tempfile.TemporaryDirectory() as folder:
            site = Path(folder)
            (site / "index.html").touch()
            check_local_link(site, "source.html", "/jev-workflow-patterns/")
            check_local_link(site, "source.html", "https://example.org/unrelated/")
            check_local_link(site, "source.html", "//example.org/unrelated/")
            check_local_link(site, "source.html", "#heading")

    def test_relative_and_same_site_links_resolve_from_rendered_page(self):
        with tempfile.TemporaryDirectory() as folder:
            site = Path(folder)
            page = site / "iterations/01/evaluation/index.html"
            guide = site / "kernel/guide/index.html"
            guide.parent.mkdir(parents=True)
            guide.touch()
            check_local_link(site, page, "../../../kernel/guide/?view=all#heading")
            check_local_link(site, page, "https://seabass-up.github.io/jev-workflow-patterns/kernel/guide/")
            for link in ("../../skills/authoring.md", "../missing/", "/jev-workflow-patterns/missing.js",
                         "//seabass-up.github.io/jev-workflow-patterns/missing/"):
                with self.subTest(link=link), self.assertRaisesRegex(ValueError, "broken internal link"):
                    check_local_link(site, page, link)


if __name__ == "__main__":
    unittest.main()
