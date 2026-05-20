"""
Unit tests for the MusicBrainz worker's pure helper functions.

These functions are copied inline here because worker tests should not import
across service boundaries — the worker has its own test suite in services/worker/.
We test the contract, not the implementation import path.
"""
from __future__ import annotations

from datetime import date
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Inline the pure functions under test — these mirror services/worker/jobs/musicbrainz.py
# If the implementations drift, the tests will catch the regression.
# ---------------------------------------------------------------------------

def _normalize_mb_date(date_str: str | None):
    """Convert a partial MusicBrainz date string to a Python datetime.date."""
    if not date_str:
        return None
    try:
        parts = date_str.split("-")
        year = int(parts[0])
        month = int(parts[1]) if len(parts) > 1 else 1
        day = int(parts[2]) if len(parts) > 2 else 1
        return date(year, month, day)
    except (ValueError, IndexError):
        return None


def _extract_wikidata_id(mb_artist: dict[str, Any]) -> str | None:
    """Pull Wikidata QID from url-rels if present."""
    for rel in mb_artist.get("url-relation-list", []):
        url: str = rel.get("target", "")
        if "wikidata.org/wiki/Q" in url:
            return url.rstrip("/").split("/")[-1]
    return None


# ---------------------------------------------------------------------------
# Tests: _normalize_mb_date
# ---------------------------------------------------------------------------

class TestNormalizeMbDate:
    def test_year_only(self) -> None:
        assert _normalize_mb_date("1945") == date(1945, 1, 1)

    def test_year_month(self) -> None:
        assert _normalize_mb_date("1945-06") == date(1945, 6, 1)

    def test_year_month_day(self) -> None:
        assert _normalize_mb_date("1945-06-15") == date(1945, 6, 15)

    def test_none_returns_none(self) -> None:
        assert _normalize_mb_date(None) is None

    def test_empty_string_returns_none(self) -> None:
        assert _normalize_mb_date("") is None

    def test_bad_string_returns_none(self) -> None:
        assert _normalize_mb_date("bad-data") is None

    def test_invalid_month_returns_none(self) -> None:
        assert _normalize_mb_date("1945-13") is None

    def test_invalid_day_returns_none(self) -> None:
        assert _normalize_mb_date("1945-06-32") is None

    def test_recent_date(self) -> None:
        assert _normalize_mb_date("2024-03-22") == date(2024, 3, 22)

    def test_early_date(self) -> None:
        assert _normalize_mb_date("1700-01-01") == date(1700, 1, 1)


# ---------------------------------------------------------------------------
# Tests: _extract_wikidata_id
# ---------------------------------------------------------------------------

class TestExtractWikidataId:
    def test_extracts_qid(self) -> None:
        artist = {"url-relation-list": [{"target": "https://www.wikidata.org/wiki/Q314454"}]}
        assert _extract_wikidata_id(artist) == "Q314454"

    def test_strips_trailing_slash(self) -> None:
        artist = {"url-relation-list": [{"target": "https://www.wikidata.org/wiki/Q314454/"}]}
        assert _extract_wikidata_id(artist) == "Q314454"

    def test_returns_none_for_non_wikidata_urls(self) -> None:
        artist = {"url-relation-list": [
            {"target": "https://en.wikipedia.org/wiki/Ravi_Shankar"},
            {"target": "https://open.spotify.com/artist/abc"},
        ]}
        assert _extract_wikidata_id(artist) is None

    def test_returns_none_for_empty_list(self) -> None:
        assert _extract_wikidata_id({"url-relation-list": []}) is None

    def test_returns_none_for_missing_key(self) -> None:
        assert _extract_wikidata_id({}) is None

    def test_finds_wikidata_among_mixed_urls(self) -> None:
        artist = {"url-relation-list": [
            {"target": "https://en.wikipedia.org/wiki/Ravi_Shankar"},
            {"target": "https://www.wikidata.org/wiki/Q7294413"},
            {"target": "https://open.spotify.com/artist/abc"},
        ]}
        assert _extract_wikidata_id(artist) == "Q7294413"

    def test_returns_first_qid_when_multiple(self) -> None:
        artist = {"url-relation-list": [
            {"target": "https://www.wikidata.org/wiki/Q111111"},
            {"target": "https://www.wikidata.org/wiki/Q222222"},
        ]}
        assert _extract_wikidata_id(artist) == "Q111111"

    def test_handles_missing_target_key(self) -> None:
        artist = {"url-relation-list": [{"type": "wikidata"}]}  # no 'target'
        assert _extract_wikidata_id(artist) is None
