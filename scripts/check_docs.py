"""Check repository Markdown links, local images and GitHub-style heading anchors.

Uses only the standard library; it does not fetch external URLs or load settings.
Historical commands and plain-text source paths are not executable documentation.
"""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import os
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "node_modules", "artifacts", "staticfiles", ".agents", ".codex", "__pycache__"}


def prose(text):
    """Exclude fenced code while preserving source line numbers."""
    fence = None
    lines = []
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append("")
        else:
            lines.append("" if fence else line)
    return "\n".join(lines)


def slug(text):
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", unescape(text)).lower()
    text = re.sub(r"[^\w\-\s]", "", text)
    return text.replace(" ", "-")


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.headings = []
        self.heading = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if key in attrs:
                self.links.append((self.getpos()[0], attrs[key]))
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        if re.fullmatch(r"h[1-6]", tag):
            self.heading = (self.getpos()[0], [])

    def handle_data(self, data):
        if self.heading is not None:
            self.heading[1].append(data)

    def handle_endtag(self, tag):
        if re.fullmatch(r"h[1-6]", tag) and self.heading is not None:
            self.headings.append((self.heading[0], "".join(self.heading[1])))
            self.heading = None


def document(text):
    text = prose(text)
    html = HTMLReferences()
    html.feed(text)
    headings = list(html.headings)
    links = list(html.links)
    lines = text.splitlines()
    for number, line in enumerate(lines, 1):
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            headings.append((number, heading.group(1)))
        elif number > 1 and re.fullmatch(r" {0,3}(?:=+|-+)\s*", line):
            previous = lines[number - 2].strip()
            if previous and not previous.startswith(("|", "#")):
                headings.append((number - 1, previous))
        definition = re.match(r"^\s*\[([^\]]+)\]:\s*<?([^\s>]+)>?", line)
        if definition:
            links.append((number, definition.group(2)))
        link_line = re.sub(r"(`+).*?\1", "", line)
        for match in re.finditer(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)", link_line):
            links.append((number, match.group(1).strip("<>")))
    anchors = set(html.ids)
    for _, heading in sorted(headings):
        base = slug(heading)
        anchor = base
        count = 0
        while anchor in anchors:
            count += 1
            anchor = f"{base}-{count}"
        anchors.add(anchor)
    return links, anchors


def markdown_files(root):
    for directory, children, files in os.walk(root):
        children[:] = [name for name in children if name not in EXCLUDED]
        for name in files:
            if name.endswith(".md"):
                yield Path(directory) / name


def check(root=ROOT):
    files = sorted(markdown_files(root))
    parsed = {path.resolve(): document(path.read_text(encoding="utf-8-sig")) for path in files}
    errors = []
    count = 0
    for path, (links, _) in parsed.items():
        for line, target in links:
            try:
                parts = urlsplit(unescape(target))
            except ValueError:
                errors.append(f"{path.relative_to(root)}:{line}: invalid target {target}")
                continue
            if parts.scheme or parts.netloc:
                continue
            count += 1
            local = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not local.is_relative_to(root.resolve()) or not local.exists():
                errors.append(f"{path.relative_to(root)}:{line}: missing local target {target}")
            elif parts.fragment and local.suffix.lower() == ".md":
                anchors = parsed.get(local, ([], set()))[1]
                if unquote(parts.fragment) not in anchors:
                    errors.append(f"{path.relative_to(root)}:{line}: missing heading {target}")
    for error in errors:
        print(error)
    print(f"Checked {len(files)} Markdown files and {count} local links/images; {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(check())
