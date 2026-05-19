"""
Wikipedia enrichment job.

Fetches biographies and native-script artist names from Wikipedia.
Also enriches musical traditions and instruments with descriptions.
Uses the `wikipedia-api` library (synchronous) wrapped in asyncio.to_thread().
Wikipedia search uses the REST API via httpx (ResilientHttpClient).
"""
from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

import structlog
import wikipediaapi

from config import WorkerSettings
from http_client import ResilientHttpClient
from jobs.base import BaseIngestionJob

logger = structlog.get_logger(__name__)

# Languages whose Wikipedia titles are in a non-Latin script and should be
# stored as name_native.
_NON_LATIN_SCRIPT_LANGS: frozenset[str] = frozenset(
    ["hi", "ja", "zh", "ko", "ar", "fa", "ta", "ru", "bn", "te", "kn", "ml", "gu", "pa", "ur"]
)

_WIKIPEDIA_API_BASE = "https://en.wikipedia.org/w/api.php"


class WikipediaIngestionJob(BaseIngestionJob):
    """Enrich artists, traditions, and instruments with Wikipedia data."""

    def __init__(self, db_session_factory: Any, settings: WorkerSettings) -> None:
        super().__init__(db_session_factory, settings)
        self._languages = settings.wikipedia_languages
        # Build one wiki client per language; they are thread-safe for reads.
        self._wikis: dict[str, wikipediaapi.Wikipedia] = {
            lang: wikipediaapi.Wikipedia(
                language=lang,
                extract_format=wikipediaapi.ExtractFormat.WIKI,
                user_agent=(
                    f"NadaAtlas/{settings.worker_version} "
                    f"(contact: {settings.musicbrainz_contact})"
                ),
            )
            for lang in self._languages
        }
        self._log = logger.bind(job="WikipediaIngestionJob")

    # ── Entry point ───────────────────────────────────────────────────────────

    async def run(self) -> None:
        """Enrich artists, traditions, and instruments via Wikipedia."""
        start = time.monotonic()
        processed = 0
        self._log.info("job_start")

        # ── 1. Artists with existing slug but no biography ────────────────────
        artists_with_slug = await self._fetch_artists_needing_enrichment()
        for row in artists_with_slug:
            artist_id: uuid.UUID = row["id"]
            slug: str = row["wikipedia_slug"]
            try:
                await self.enrich_artist_from_wikipedia(
                    artist_id=artist_id,
                    wikipedia_slug=slug,
                    languages=self._languages,
                )
                processed += 1
                await asyncio.sleep(0.5)
            except Exception:
                self._log.exception(
                    "enrich_artist_error",
                    artist_id=str(artist_id),
                    slug=slug,
                )

        # ── 2. Artists without a slug — discover then enrich ──────────────────
        artists_without_slug = await self._fetch_artists_without_slug()
        async with ResilientHttpClient(rate_limit_per_second=1.0) as http:
            for row in artists_without_slug:
                artist_id = row["id"]
                name: str = row["name"]
                try:
                    slug = await self._search_wikipedia(name, http=http)
                    if slug:
                        await self._update_artist_wikipedia_slug(artist_id, slug)
                        await self.enrich_artist_from_wikipedia(
                            artist_id=artist_id,
                            wikipedia_slug=slug,
                            languages=self._languages,
                        )
                        processed += 1
                    await asyncio.sleep(0.5)
                except Exception:
                    self._log.exception(
                        "discover_artist_slug_error",
                        artist_id=str(artist_id),
                        name=name,
                    )

        # ── 3 & 4. Traditions ─────────────────────────────────────────────────
        traditions = await self._fetch_traditions_needing_enrichment()
        async with ResilientHttpClient(rate_limit_per_second=1.0) as http:
            for row in traditions:
                tradition_id: uuid.UUID = row["id"]
                tradition_name: str = row["name"]
                slug = row["wikipedia_slug"]
                try:
                    if slug is None:
                        slug = await self._search_wikipedia(
                            f"{tradition_name} music", http=http
                        )
                    if slug:
                        await self.enrich_tradition_from_wikipedia(tradition_id, slug)
                        processed += 1
                    await asyncio.sleep(0.5)
                except Exception:
                    self._log.exception(
                        "enrich_tradition_error",
                        tradition_id=str(tradition_id),
                        name=tradition_name,
                    )

        # ── 5 & 6. Instruments ────────────────────────────────────────────────
        instruments = await self._fetch_instruments_needing_enrichment()
        async with ResilientHttpClient(rate_limit_per_second=1.0) as http:
            for row in instruments:
                instrument_id: uuid.UUID = row["id"]
                instrument_name: str = row["name"]
                slug = row["wikipedia_slug"]
                try:
                    if slug is None:
                        slug = await self._search_wikipedia(
                            f"{instrument_name} instrument", http=http
                        )
                    if slug:
                        await self.enrich_instrument_from_wikipedia(instrument_id, slug)
                        processed += 1
                    await asyncio.sleep(0.5)
                except Exception:
                    self._log.exception(
                        "enrich_instrument_error",
                        instrument_id=str(instrument_id),
                        name=instrument_name,
                    )

        elapsed_ms = round((time.monotonic() - start) * 1000)
        self._log.info(
            "job_complete",
            duration_ms=elapsed_ms,
            records_processed=processed,
        )

    # ── Search ────────────────────────────────────────────────────────────────

    async def _search_wikipedia(
        self,
        query: str,
        lang: str = "en",
        *,
        http: ResilientHttpClient,
    ) -> str | None:
        """
        Search Wikipedia for `query` and return the best-matching page title
        (suitable for use as a wikipedia_slug), or None if not found.

        Uses the Wikipedia Action API search endpoint, then verifies the page
        actually exists via the wikipediaapi client.
        """
        try:
            data = await http.get(
                _WIKIPEDIA_API_BASE,
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json",
                    "srlimit": "1",
                },
            )
            search_results = data.get("query", {}).get("search", [])
            if not search_results:
                return None
            title: str = search_results[0]["title"]
            # Verify the page exists via the wiki client
            wiki = self._wikis.get(lang)
            if wiki is None:
                return title  # fall back to returning the title unverified
            page: wikipediaapi.WikipediaPage = await asyncio.to_thread(wiki.page, title)
            if page.exists():
                return title
            return None
        except Exception:
            self._log.exception("wikipedia_search_error", query=query)
            return None

    # ── Artist enrichment ─────────────────────────────────────────────────────

    async def enrich_artist_from_wikipedia(
        self,
        artist_id: uuid.UUID,
        wikipedia_slug: str,
        languages: list[str],
    ) -> None:
        """
        Fetch Wikipedia pages for an artist across all configured languages.

        - English page → biography_short (summary) + biography (full text)
        - Non-Latin-script language page → name_native (page title)
        """
        biography_short: str | None = None
        biography: str | None = None
        name_native: str | None = None

        for lang in languages:
            wiki = self._wikis.get(lang)
            if wiki is None:
                continue

            page: wikipediaapi.WikipediaPage = await asyncio.to_thread(
                wiki.page, wikipedia_slug
            )
            if not page.exists():
                continue

            if lang == "en" and biography_short is None:
                biography_short = page.summary or None
                biography = page.text or None

            candidate_native = await self.extract_name_native(page.title, lang)
            if candidate_native and name_native is None:
                name_native = candidate_native

            # Stop once we have English bio + a native name
            if biography_short and name_native:
                break

        await self._update_artist_biography(
            artist_id=artist_id,
            biography_short=biography_short,
            biography=biography,
            name_native=name_native,
        )
        self._log.debug(
            "artist_enriched_wikipedia",
            artist_id=str(artist_id),
            slug=wikipedia_slug,
            has_bio=biography_short is not None,
            has_native_name=name_native is not None,
        )

    async def extract_name_native(self, page_title: str, language: str) -> str | None:
        """
        Return `page_title` as a native-script name when the language uses a
        non-Latin script; otherwise return None.
        """
        if language in _NON_LATIN_SCRIPT_LANGS:
            return page_title
        return None

    # ── Tradition enrichment ──────────────────────────────────────────────────

    async def enrich_tradition_from_wikipedia(
        self,
        tradition_id: uuid.UUID,
        wikipedia_slug: str,
    ) -> None:
        """
        Fetch the English Wikipedia page for a musical tradition and update its
        description and wikipedia_slug in the musical_traditions table.
        """
        wiki = self._wikis.get("en")
        if wiki is None:
            self._log.warning("no_english_wiki_client", tradition_id=str(tradition_id))
            return

        page: wikipediaapi.WikipediaPage = await asyncio.to_thread(wiki.page, wikipedia_slug)
        if not page.exists():
            self._log.warning(
                "tradition_article_not_found",
                tradition_id=str(tradition_id),
                slug=wikipedia_slug,
            )
            return

        description = (page.summary or "")[:2000] or None
        await self._update_tradition_wikipedia(tradition_id, wikipedia_slug, description)
        self._log.info(
            "tradition_enriched_wikipedia",
            tradition_id=str(tradition_id),
            slug=wikipedia_slug,
            has_description=description is not None,
        )

    # ── Instrument enrichment ─────────────────────────────────────────────────

    async def enrich_instrument_from_wikipedia(
        self,
        instrument_id: uuid.UUID,
        wikipedia_slug: str,
    ) -> None:
        """
        Fetch the English Wikipedia page for an instrument and update its
        description and wikipedia_slug in the instruments table.
        """
        wiki = self._wikis.get("en")
        if wiki is None:
            self._log.warning("no_english_wiki_client", instrument_id=str(instrument_id))
            return

        page: wikipediaapi.WikipediaPage = await asyncio.to_thread(wiki.page, wikipedia_slug)
        if not page.exists():
            self._log.warning(
                "instrument_article_not_found",
                instrument_id=str(instrument_id),
                slug=wikipedia_slug,
            )
            return

        description = (page.summary or "")[:2000] or None
        await self._update_instrument_wikipedia(instrument_id, wikipedia_slug, description)
        self._log.info(
            "instrument_enriched_wikipedia",
            instrument_id=str(instrument_id),
            slug=wikipedia_slug,
            has_description=description is not None,
        )

    # ── DB helpers ────────────────────────────────────────────────────────────

    async def _fetch_artists_needing_enrichment(self) -> list[dict[str, Any]]:
        """Return artists that have a wikipedia_slug but no biography_short yet."""
        from sqlalchemy import text

        stmt = text(
            """
            SELECT id, wikipedia_slug
            FROM artists
            WHERE wikipedia_slug IS NOT NULL
              AND biography_short IS NULL
            LIMIT 500
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return [{"id": row[0], "wikipedia_slug": row[1]} for row in result]

    async def _fetch_artists_without_slug(self) -> list[dict[str, Any]]:
        """Return artists that have no wikipedia_slug at all."""
        from sqlalchemy import text

        stmt = text(
            """
            SELECT id, name
            FROM artists
            WHERE wikipedia_slug IS NULL
              AND deleted_at IS NULL
            LIMIT 100
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return [{"id": row[0], "name": row[1]} for row in result]

    async def _fetch_traditions_needing_enrichment(self) -> list[dict[str, Any]]:
        """Return traditions that need a wikipedia slug or description."""
        from sqlalchemy import text

        stmt = text(
            """
            SELECT id, name, wikipedia_slug
            FROM musical_traditions
            WHERE deleted_at IS NULL
              AND (wikipedia_slug IS NULL OR description IS NULL)
            LIMIT 100
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return [
                {"id": row[0], "name": row[1], "wikipedia_slug": row[2]}
                for row in result
            ]

    async def _fetch_instruments_needing_enrichment(self) -> list[dict[str, Any]]:
        """Return instruments that need a wikipedia slug or description."""
        from sqlalchemy import text

        stmt = text(
            """
            SELECT id, name, wikipedia_slug
            FROM instruments
            WHERE deleted_at IS NULL
              AND (wikipedia_slug IS NULL OR description IS NULL)
            LIMIT 100
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return [
                {"id": row[0], "name": row[1], "wikipedia_slug": row[2]}
                for row in result
            ]

    async def _update_artist_biography(
        self,
        artist_id: uuid.UUID,
        biography_short: str | None,
        biography: str | None,
        name_native: str | None,
    ) -> None:
        from sqlalchemy import text

        stmt = text(
            """
            UPDATE artists SET
                biography_short = COALESCE(:biography_short, biography_short),
                biography       = COALESCE(:biography, biography),
                name_native     = COALESCE(:name_native, name_native),
                updated_at      = now()
            WHERE id = :artist_id
            """
        )
        async with self._session_factory() as session:
            await session.execute(
                stmt,
                {
                    "biography_short": biography_short,
                    "biography": biography,
                    "name_native": name_native,
                    "artist_id": artist_id,
                },
            )
            await session.commit()

    async def _update_artist_wikipedia_slug(
        self,
        artist_id: uuid.UUID,
        wikipedia_slug: str,
    ) -> None:
        from sqlalchemy import text

        stmt = text(
            """
            UPDATE artists SET
                wikipedia_slug = :wikipedia_slug,
                updated_at     = now()
            WHERE id = :artist_id
              AND wikipedia_slug IS NULL
            """
        )
        async with self._session_factory() as session:
            await session.execute(
                stmt,
                {"wikipedia_slug": wikipedia_slug, "artist_id": artist_id},
            )
            await session.commit()

    async def _update_tradition_wikipedia(
        self,
        tradition_id: uuid.UUID,
        wikipedia_slug: str,
        description: str | None,
    ) -> None:
        from sqlalchemy import text

        stmt = text(
            """
            UPDATE musical_traditions SET
                wikipedia_slug = :slug,
                description    = COALESCE(:desc, description),
                updated_at     = now()
            WHERE id = :id
            """
        )
        async with self._session_factory() as session:
            await session.execute(
                stmt,
                {"slug": wikipedia_slug, "desc": description, "id": tradition_id},
            )
            await session.commit()

    async def _update_instrument_wikipedia(
        self,
        instrument_id: uuid.UUID,
        wikipedia_slug: str,
        description: str | None,
    ) -> None:
        from sqlalchemy import text

        stmt = text(
            """
            UPDATE instruments SET
                wikipedia_slug = :slug,
                description    = COALESCE(:desc, description),
                updated_at     = now()
            WHERE id = :id
            """
        )
        async with self._session_factory() as session:
            await session.execute(
                stmt,
                {"slug": wikipedia_slug, "desc": description, "id": instrument_id},
            )
            await session.commit()
