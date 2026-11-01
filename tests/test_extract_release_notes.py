"""Tests for the release notes extractor. No network needed."""

import extract_release_notes as ern

CHANGELOG_TEXT = """# Changelog

## [Unreleased]

### Added
- Something new.

## [1.0.0]

### Added
- First stable release.

## [0.1.0]

### Added
- Early version.
"""


def test_finds_the_matching_version_section():
    notes = ern.release_notes(CHANGELOG_TEXT, "v1.0.0")
    assert "First stable release." in notes
    assert "Early version." not in notes


def test_version_without_v_prefix_also_works():
    assert "First stable release." in ern.release_notes(CHANGELOG_TEXT, "1.0.0")


def test_falls_back_to_unreleased_when_version_is_missing():
    notes = ern.release_notes(CHANGELOG_TEXT, "v9.9.9")
    assert "Something new." in notes


def test_returns_fallback_when_changelog_is_empty():
    assert ern.release_notes("", "v1.0.0") == ern.FALLBACK
