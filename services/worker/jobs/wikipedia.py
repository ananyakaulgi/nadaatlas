"""
Wikipedia enrichment job.

Fetches biographies and native-script artist names from Wikipedia.
Uses the `wikipedia-api` library (synchronous) wrapped in asyncio.to_thread().
"""
from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

import structlog
import wikipediaapi

from config import WorkerSettings
from jobs.base import BaseIngestionJob

logger = structlog.get_logger(__name__)

# Languages whose Wikipedia titles are in a non-Latin script and should be
# stored as name_native.
_NON_LATIN_SCRIPT_LANGS: frozenset[str] = frozenset(
    ["hi", "ja", "zh", "ko", "ar", "fa", "ta", "ru", "bn", "te", "kn", "ml", "gu", "pa", "ur"]
)


class WikipediaIngestionJob(BaseIngestionJob):
    """Enrich artists and traditions with Wikipedia biography data."""

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
        """Enrich all artists that have a wikipedia_slug but missing biography."""
        start = time.monotonic()
        processed = 0
        self._log.info("job_start")

        artists = await self._fetch_artists_needing_enrichment()
        for row in artists:
            artist_id: uuid.UUID = row["id"]
            slug: str = row["wikipedia_slug"]
            try:
                await self.enrich_artist_from_wikipedia(
                    artist_id=artist_id,
                    wikipedia_slug=slug,
                    languages=self._languages,
                )
                processed += 1
            except Exception:
                self._log.exception(
                    "enrich_error",
                    artist_id=str(artist_id),
                    slug=slug,
                )

        elapsed_ms = round((time.monotonic() - start) * 1000)
        self._log.info(
            "job_complete",
            duration_ms=elapsed_ms,
            records_processed=processed,
        )

    # ── Core enrichment methods ───────────────────────────────────────────────

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

    async def ingest_tradition_article(
        self,
        tradition_name: str,
        wikipedia_slug: str,
    ) -> None:
        """
        Fetch the Wikipedia article for a musical tradition and update its
        description in the musical_traditions table.
        """
        wiki = self._wikis.get("en")
        if wiki is None:
            self._log.warning(
                "no_english_wiki_client", tradition=tradition_name
            )
            return

        page: wikipediaapi.WikipediaPage = await asyncio.to_thread(
            wiki.page, wikipedia_slug
        )
        if not page.exists():
            self._log.warning(
                "tradition_article_not_found",
                tradition=tradition_name,
                slug=wikipedia_slug,
            )
            return

        description = page.summary or page.text[:1000] if page.text else None
        await self.upsert_tradition(
            name=tradition_name,
            region="Global",  # caller can override; upsert won't blank existing region
            description=description,
        )
        self._log.info(
            "tradition_article_ingested",
            tradition=tradition_name,
            slug=wikipedia_slug,
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
