# Changelog

All notable changes to this project are listed here.

## [Unreleased]

### Added
- Release workflow that creates a GitHub Release from a version tag.

## [0.1.0]

### Added
- BM25 keyword search over Markdown files, using only the Python standard library.
- Command line tool: `python -m course_search "query" --folder notes/`.
- Unit tests for the ranking, the index, and the command line tool.
- GitHub Actions CI on Python 3.11 and 3.12.
