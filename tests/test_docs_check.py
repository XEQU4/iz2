"""Documentation checker cases that matter when preserving moved reports."""

from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from tempfile import TemporaryDirectory
from unittest import TestCase

from scripts.check_docs import check, document


class DocumentationCheckTests(TestCase):
    def test_visible_heading_text_and_collision_anchors(self):
        _, anchors = document("# [Quick start](README.md)\n# Foo\n# Foo\n# Foo-1\n")
        self.assertEqual(anchors, {"quick-start", "foo", "foo-1", "foo-1-1"})

    def test_code_examples_are_not_links_or_headings(self):
        links, anchors = document("`[example](missing.md)`\n```md\n# Hidden\n[x](absent.md)\n```\n# Visible\n")
        self.assertEqual(links, [])
        self.assertEqual(anchors, {"visible"})

    def test_html_and_setext_headings(self):
        links, anchors = document('<h1>IZ2</h1>\nStart here\n----------\n<img src="image.png">\n')
        self.assertEqual(anchors, {"iz2", "start-here"})
        self.assertEqual(links, [(4, "image.png")])

    def test_moved_files_images_and_encoded_fragments(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "archive").mkdir()
            (root / "archive" / "report.md").write_text("# Данные\n", encoding="utf-8")
            (root / "image.png").write_bytes(b"image placeholder")
            (root / "README.md").write_text(
                '[Report](archive/report.md#%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5)\n'
                '![Screenshot](image.png)\n', encoding="utf-8",
            )
            with redirect_stdout(StringIO()):
                self.assertFalse(check(root))

    def test_broken_targets_fail_without_network_or_settings(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text(
                '# Start\n[Missing](#absent)\n[File](missing.md)\n'
                '[External](https://example.invalid/)\n', encoding="utf-8",
            )
            output = StringIO()
            with redirect_stdout(output):
                self.assertTrue(check(root))
            self.assertIn("2 errors", output.getvalue())
