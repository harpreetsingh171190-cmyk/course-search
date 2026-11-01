"""Command line tool: index a folder of Markdown files and search it."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .bm25 import BM25Index


def build_index(folder: Path) -> BM25Index:
    index = BM25Index()
    for path in sorted(folder.rglob("*.md")):
        index.add(str(path.relative_to(folder)), path.read_text(encoding="utf-8"))
    return index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search Markdown notes with BM25.")
    parser.add_argument("query", help="words to search for")
    parser.add_argument("--folder", type=Path, default=Path("."), help="folder with .md files")
    parser.add_argument("--limit", type=int, default=5, help="maximum results to show")
    args = parser.parse_args(argv)

    if not args.folder.is_dir():
        print(f"Error: folder not found: {args.folder}", file=sys.stderr)
        return 2

    index = build_index(args.folder)
    results = index.search(args.query, limit=args.limit)
    if not results:
        print("No matches found.")
        return 0
    for rank, result in enumerate(results, 1):
        print(f"{rank}. {result.doc_id} (score {result.score:.2f})")
        print(f"   {result.snippet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
