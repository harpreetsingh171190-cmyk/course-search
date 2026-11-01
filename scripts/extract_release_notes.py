#!/usr/bin/env python3
"""Print the release notes for one version from CHANGELOG.md.

Usage: python scripts/extract_release_notes.py v1.0.0

It looks for a "## [1.0.0]" section. If that is missing, it uses the
"## [Unreleased]" section. If neither exists, it prints a short fallback
line. It always exits with 0, so a release is never blocked by the notes.

Standard library only.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"
FALLBACK = "See CHANGELOG.md for the list of changes."
SECTION = re.compile(r"^## \[(.+?)\]\s*$", re.MULTILINE)


def find_section(text: str, name: str) -> str | None:
    """Return the body under '## [name]' up to the next '## ' heading."""
    for match in SECTION.finditer(text):
        if match.group(1).strip().lower() == name.lower():
            start = match.end()
            nxt = re.search(r"^## ", text[start:], re.MULTILINE)
            end = start + nxt.start() if nxt else len(text)
            return text[start:end].strip()
    return None


def release_notes(text: str, version: str) -> str:
    clean = version.lstrip("v")
    body = find_section(text, clean) or find_section(text, "Unreleased")
    return body or FALLBACK


def main() -> int:
    version = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    text = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
    print(release_notes(text, version))
    return 0


if __name__ == "__main__":
    sys.exit(main())
