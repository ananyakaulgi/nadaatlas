"""
Wikidata enrichment job.

Queries the Wikidata SPARQL endpoint to find musician entities and
cross-reference them with artists already in our database.
"""
from __future__ import annotations

import time
import uuid
from typing import Any

import structlog

from config import WorkerSettings
from http_client import ResilientHttpClient
from jobs.base import BaseIngestionJob

logger = structlog.get_logger(__name__)

_SPARQL_ACCEPT = "application/sparql-results+json"


class WikidataIngestionJob(BaseIngestionJob):
    """Sync Wikidata entity IDs and enrich artist metadata via SPARQL."""

    # ── SPARQL query constant ─────────────────────────────────────────────────

    MUSICIAN_SPARQL_QUERY: str = """
SELECT ?musician ?musicianLabel ?nativeLabel ?mbid ?born ?died ?countryLabel ?instrumentLabel WHERE {
  ?musician wdt:P106 wd:Q639669 .  # occupation: musician
  OPTIONAL { ?musician wdt:P434 ?mbid }  # MusicBrainz ID
  OPTIONAL { ?musician wdt:P569 ?born }
  OPTIONAL { ?musician wdt:P570 ?died }
  OPTIONAL { ?musician wdt:P27 ?country }
  OPTIONAL { ?musician wdt:P1303 ?instrument }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
}
LIMIT 1000
"""

    def __init__(self, db_session_factory: Any, settings: WorkerSettings) -> None:
        super().__init__(db_session_factory, settings)
        self._sparql_url = settings.wikidata_sparql_url
        self._log = logger.bind(job="WikidataIngestionJob")

    # ── Entry point ───────────────────────────────────────────────────────────

    async def run(self) -> None:
        """Main job: sync Wikidata IDs for known artists, then enrich."""
        start = time.monotonic()
        self._log.info("job_start")
        processed = 0

        try:
            processed = await self.sync_wikidata_ids()
        except Exception:
            self._log.exception("wikidata_sync_failed")

        elapsed_ms = round((time.monotonic() - start) * 1000)
        self._log.info(
            "job_complete",
            duration_ms=elapsed_ms,
            records_processed=processed,
        )

    # ── SPARQL query helper ───────────────────────────────────────────────────

    async def query(self, sparql: str) -> list[dict[str, Any]]:
        """
        Execute a SPARQL query against the Wikidata Query Service.
        Returns a list of result-binding dicts (each key → {"type", "value"}).
        """
        # Rate-limit at 0.5 req/s to be polite to the public endpoint
        async with ResilientHttpClient(
            base_url="",
            rate_limit_per_second=0.5,
            timeout=60.0,
        ) as client:
            data = await client.get(
                self._sparql_url,
                params={"query": sparql, "format": "json"},
                headers={"Accept": _SPARQL_ACCEPT},
            )

        bindings: list[dict[str, Any]] = (
            data.get("results", {}).get("bindings", [])
        )
        return bindings

    # ── Sync logic ────────────────────────────────────────────────────────────

    async def sync_wikidata_ids(self) -> int:
        """
        Two-pass sync:
        1. For artists with a wikidata_id set → run enrichment from Wikidata data.
        2. For artists with musicbrainz_id but no wikidata_id → query Wikidata
           to find and store the matching entity.
        Returns total count of artists touched.
        """
        processed = 0

        # Pass 1: enrich artists that already have wikidata_id
        enriched = await self._enrich_artists_with_wikidata_id()
        processed += enriched

        # Pass 2: discover wikidata_id for artists that only have musicbrainz_id
        discovered = await self._discover_wikidata_ids_via_mbid()
        processed += discovered

        return processed

    async def _enrich_artists_with_wikidata_id(self) -> int:
        """Query Wikidata for artists whose wikidata_id we already know."""
        artists = await self._fetch_artists_with_wikidata_id()
        if not artists:
            return 0

        self._log.info(
            "enriching_artists_with_wikidata_id", count=len(artists)
        )
        processed = 0

        for row in artists:
            artist_id: uuid.UUID = row["id"]
            qid: str = row["wikidata_id"]
            try:
                sparql = self._build_entity_query(qid)
                bindings = await self.query(sparql)
                if bindings:
                    await self._apply_wikidata_enrichment(artist_id, bindings[0])
                    processed += 1
            except Exception:
                self._log.exception(
                    "enrich_wikidata_error",
                    artist_id=str(artist_id),
                    qid=qid,
                )

        return processed

    async def _discover_wikidata_ids_via_mbid(self) -> int:
        """For artists missing wikidata_id, query Wikidata by MusicBrainz ID."""
        artists = await self._fetch_artists_missing_wikidata_id()
        if not artists:
            return 0

        self._log.info(
            "discovering_wikidata_ids", count=len(artists)
        )
        processed = 0

        for row in artists:
            artist_id: uuid.UUID = row["id"]
            mb_id: str = row["musicbrainz_id"]
            try:
                sparql = self._build_mbid_lookup_query(mb_id)
                bindings = await self.query(sparql)
                if bindings:
                    binding = bindings[0]
                    qid = self._extract_qid(binding.get("musician", {}).get("value", ""))
                    if qid:
                        await self._store_wikidata_id(artist_id, qid)
                        await self._apply_wikidata_enrichment(artist_id, binding)
                        processed += 1
            except Exception:
                self._log.exception(
                    "discover_wikidata_error",
                    artist_id=str(artist_id),
                    mb_id=mb_id,
                )

        return processed

    # ── SPARQL query builders ─────────────────────────────────────────────────

    @staticmethod
    def _build_entity_query(qid: str) -> str:
        return f"""
SELECT ?musician ?musicianLabel ?nativeLabel ?mbid ?born ?died ?countryLabel ?instrumentLabel WHERE {{
  BIND(wd:{qid} AS ?musician)
  OPTIONAL {{ ?musician wdt:P434 ?mbid }}
  OPTIONAL {{ ?musician wdt:P569 ?born }}
  OPTIONAL {{ ?musician wdt:P570 ?died }}
  OPTIONAL {{ ?musician wdt:P27 ?country }}
  OPTIONAL {{ ?musician wdt:P1303 ?instrument }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }}
}}
LIMIT 1
"""

    @staticmethod
    def _build_mbid_lookup_query(mb_id: str) -> str:
        return f"""
SELECT ?musician ?musicianLabel ?nativeLabel ?mbid ?born ?died ?countryLabel ?instrumentLabel WHERE {{
  ?musician wdt:P434 "{mb_id}" .
  OPTIONAL {{ ?musician wdt:P569 ?born }}
  OPTIONAL {{ ?musician wdt:P570 ?died }}
  OPTIONAL {{ ?musician wdt:P27 ?country }}
  OPTIONAL {{ ?musician wdt:P1303 ?instrument }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }}
}}
LIMIT 1
"""

    @staticmethod
    def _extract_qid(entity_url: str) -> str | None:
        """Extract QID (e.g. 'Q12345') from a Wikidata entity URL."""
        if "/Q" in entity_url:
            return entity_url.rstrip("/").split("/")[-1]
        return None

    def _binding_value(self, binding: dict[str, Any], key: str) -> str | None:
        """Safely extract string value from a SPARQL binding dict."""
        entry = binding.get(key)
        if entry and isinstance(entry, dict):
            return entry.get("value")
        return None

    # ── DB helpers ────────────────────────────────────────────────────────────

    async def _fetch_artists_with_wikidata_id(self) -> list[dict[str, Any]]:
        from sqlalchemy import text

        stmt = text(
            "SELECT id, wikidata_id FROM artists WHERE wikidata_id IS NOT NULL LIMIT 500"
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return [{"id": row[0], "wikidata_id": row[1]} for row in result]

    async def _fetch_artists_missing_wikidata_id(self) -> list[dict[str, Any]]:
        from sqlalchemy import text

        stmt = text(
            """
            SELECT id, musicbrainz_id
            FROM artists
            WHERE wikidata_id IS NULL
              AND musicbrainz_id IS NOT NULL
            LIMIT 500
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return [{"id": row[0], "musicbrainz_id": row[1]} for row in result]

    async def _store_wikidata_id(self, artist_id: uuid.UUID, qid: str) -> None:
        from sqlalchemy import text

        stmt = text(
            "UPDATE artists SET wikidata_id = :qid, updated_at = now() WHERE id = :id"
        )
        async with self._session_factory() as session:
            await session.execute(stmt, {"qid": qid, "id": artist_id})
            await session.commit()

    async def _apply_wikidata_enrichment(
        self, artist_id: uuid.UUID, binding: dict[str, Any]
    ) -> None:
        """Write Wikidata-sourced fields back to the artist row (COALESCE — never overwrite)."""
        from sqlalchemy import text

        born = self._binding_value(binding, "born")
        died = self._binding_value(binding, "died")
        country_label = self._binding_value(binding, "countryLabel")

        stmt = text(
            """
            UPDATE artists SET
                born        = COALESCE(:born, born),
                died        = COALESCE(:died, died),
                nationality = COALESCE(:nationality, nationality),
                updated_at  = now()
            WHERE id = :id
            """
        )
        async with self._session_factory() as session:
            await session.execute(
                stmt,
                {
                    "born": born,
                    "died": died,
                    "nationality": country_label,
                    "id": artist_id,
                },
            )
            await session.commit()

        self._log.debug(
            "wikidata_enrichment_applied",
            artist_id=str(artist_id),
            has_born=born is not None,
        )
