#!/usr/bin/env python3
"""Validate evidence links, local images, and placeholders in an XHS report."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs)
        elif tag == "img":
            self.images.append(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])


REQUIRED_IDS = {
    "summary",
    "evolution",
    "diagnosis",
    "assets",
    "compliance",
    "route",
    "sources",
}


def validate(path: Path):
    html = path.read_text(encoding="utf-8")
    parser = ReportParser()
    parser.feed(html)
    errors = []
    external_count = 0

    unresolved = sorted(set(re.findall(r"\[\[[^\[\]]+\]\]|\{\{[^{}]+\}\}", html)))
    if unresolved:
        preview = ", ".join(unresolved[:8])
        errors.append(f"Unresolved placeholders ({len(unresolved)}): {preview}")

    missing_sections = sorted(REQUIRED_IDS - parser.ids)
    if missing_sections:
        errors.append("Missing required section ids: " + ", ".join(missing_sections))

    for index, attrs in enumerate(parser.links, start=1):
        href = (attrs.get("href") or "").strip()
        if not href or href == "#":
            errors.append(f"Link {index} has an empty or placeholder href")
            continue
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https"}:
            external_count += 1
            rel = set((attrs.get("rel") or "").split())
            if attrs.get("target") != "_blank":
                errors.append(f"External link {index} must use target=_blank: {href}")
            if not {"noopener", "noreferrer"}.issubset(rel):
                errors.append(f"External link {index} must use rel=noopener noreferrer: {href}")
        elif parsed.scheme and parsed.scheme not in {"file"}:
            errors.append(f"Link {index} uses an unsupported scheme: {href}")

    for index, attrs in enumerate(parser.images, start=1):
        src = (attrs.get("src") or "").strip()
        if not src:
            errors.append(f"Image {index} has an empty src")
            continue
        parsed = urlparse(src)
        if not parsed.scheme and not src.startswith("data:"):
            local = (path.parent / unquote(parsed.path)).resolve()
            if not local.is_file():
                errors.append(f"Local image {index} not found: {src}")

    if external_count == 0:
        errors.append("No external evidence links found")
    return errors, external_count, len(parser.images)


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_report_links.py <report.html>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"Report not found: {path}", file=sys.stderr)
        return 2
    errors, links, images = validate(path)
    if errors:
        print("Report validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Report validation passed: {links} external links, {images} images, 7 sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
