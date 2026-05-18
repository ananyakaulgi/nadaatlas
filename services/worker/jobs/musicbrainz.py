"""
MusicBrainz ingestion job.

Uses the `musicbrainzngs` library (synchronous) wrapped in asyncio.to_thread()
so the event loop is never blocked.
"""
from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

import musicbrainzngs
import structlog

from config import WorkerSettings
from jobs.base import BaseIngestionJob

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Tradition → MusicBrainz tag mapping
# ---------------------------------------------------------------------------

TRADITION_TAG_MAP: dict[str, list[str]] = {
    "Hindustani Classical": ["hindustani classical", "north indian classical", "raga"],
    "Carnatic": ["carnatic", "south indian classical", "carnatic music"],
    "Qawwali": ["qawwali", "sufi music"],
    "West African Griot": ["griot", "west african", "kora"],
    "Japanese Gagaku": ["gagaku", "japanese traditional", "koto"],
    "Chinese Classical": ["chinese classical", "guqin", "erhu"],
    "Korean Traditional": ["korean traditional", "pansori", "gayageum"],
    "Gamelan": ["gamelan", "indonesian traditional"],
    "Arabic Maqam": ["arabic maqam", "maqam", "arabic classical"],
    "Persian Classical": ["persian classical", "dastgah", "radif"],
    "Turkish Makam": ["turkish makam", "ottoman classical"],
    "Flamenco": ["flamenco"],
    "Fado": ["fado"],
    "Nordic Folk": ["nordic folk", "scandinavian folk"],
    "Celtic": ["celtic", "irish traditional", "scottish traditional"],
    "Balkan": ["balkan", "balkan folk"],
    "Blues": ["blues", "delta blues"],
    "Jazz": ["jazz"],
    "Brazilian Samba": ["samba", "bossa nova", "choro"],
    "Argentine Tango": ["tango", "argentine tango"],
    "Reggae": ["reggae", "dancehall"],
    "Andean": ["andean", "cumbia", "huayno"],
}

# Source tier for MusicBrainz data (authoritative)
_SOURCE_TIER = 1


class MusicBrainzIngestionJob(BaseIngestionJob):
    """Ingest artist and album data from MusicBrainz."""

    def __init__(self, db_session_factory: Any, settings: WorkerSettings) -> None:
        super().__init__(db_session_factory, settings)
        musicbrainzngs.set_useragent(
            settings.musicbrainz_app_name,
            settings.musicbrainz_app_version,
            settings.musicbrainz_contact,
        )
        self._log = logger.bind(job="MusicBrainzIngestionJob")

    # ── Entry point ───────────────────────────────────────────────────────────

    async def run(self) -> None:
        """Full ingestion cycle: iterate all tradition tags."""
        start = time.monotonic()
        total_processed = 0
        self._log.info("job_start")

        for tradition, tags in TRADITION_TAG_MAP.items():
            # Derive region from the first tag as a heuristic; base class handles mapping
            region = await self._region_for_tradition(tradition)
            # Ensure the tradition row exists
            await self.upsert_tradition(name=tradition, region=region)

            for tag in tags:
                try:
                    count = await self.ingest_artists_by_tag(
                        mb_tag=tag, tradition=tradition, region=region
                    )
                    total_processed += count
                except Exception:
                    self._log.exception(
                        "tag_ingest_error", tradition=tradition, tag=tag
                    )

        elapsed_ms = round((time.monotonic() - start) * 1000)
        self._log.info(
            "job_complete",
            duration_ms=elapsed_ms,
            records_processed=total_processed,
        )

    # ── Core ingestion methods ────────────────────────────────────────────────

    async def ingest_artists_by_tag(
        self,
        mb_tag: str,
        tradition: str,
        region: str,
        limit: int = 100,
    ) -> int:
        """
        Search MusicBrainz for artists matching `mb_tag`, then upsert each one.
        Returns the number of artists processed.
        """
        self._log.info("ingest_artists_by_tag_start", tag=mb_tag, tradition=tradition)

        # musicbrainzngs is synchronous — offload to thread pool
        search_result: dict[str, Any] = await asyncio.to_thread(
            musicbrainzngs.search_artists,
            tag=mb_tag,
            limit=limit,
        )

        artists = search_result.get("artist-list", [])
        processed = 0

        for artist_stub in artists:
            mb_id: str = artist_stub.get("id", "")
            if not mb_id:
                continue

            try:
                full: dict[str, Any] = await asyncio.to_thread(
                    musicbrainzngs.get_artist_by_id,
                    mb_id,
                    includes=[
                        "recordings",
                        "release-groups",
                        "tags",
                        "url-rels",
                    ],
                )
                artist_data = full.get("artist", {})
                mapped = self._map_artist(
                    artist_data,
                    tradition=tradition,
                    region=region,
                )
                artist_id = await self.upsert_artist(mapped)
                await self.ingest_albums_for_artist(mb_id)
                processed += 1
                self._log.debug(
                    "artist_ingested",
                    artist_id=str(artist_id),
                    mb_id=mb_id,
                    name=mapped.get("name"),
                )
            except musicbrainzngs.ResponseError:
                self._log.exception("mb_response_error", mb_id=mb_id)
            except Exception:
                self._log.exception("artist_ingest_error", mb_id=mb_id)

        self._log.info(
            "ingest_artists_by_tag_done",
            tag=mb_tag,
            tradition=tradition,
            artists_found=len(artists),
            artists_processed=processed,
        )
        return processed

    async def ingest_albums_for_artist(self, musicbrainz_id: str) -> None:
        """
        Fetch release-groups for an artist and upsert album records.
        """
        try:
            result: dict[str, Any] = await asyncio.to_thread(
                musicbrainzngs.browse_release_groups,
                artist=musicbrainz_id,
                limit=100,
            )
        except musicbrainzngs.ResponseError:
            self._log.exception(
                "mb_browse_release_groups_error", mb_id=musicbrainz_id
            )
            return

        release_groups = result.get("release-group-list", [])
        for rg in release_groups:
            await self._upsert_album(rg, artist_musicbrainz_id=musicbrainz_id)

    # ── Mapping helpers ───────────────────────────────────────────────────────

    def _map_artist(
        self,
        mb_artist: dict[str, Any],
        tradition: str,
        region: str,
    ) -> dict[str, Any]:
        """Convert a MusicBrainz artist dict to our DB schema dict."""
        life_span = mb_artist.get("life-span", {})
        area = mb_artist.get("begin-area") or mb_artist.get("area") or {}
        country_code: str = mb_artist.get("country", "")

        return {
            "name": mb_artist.get("name"),
            "name_sort": mb_artist.get("sort-name"),
            "name_native": None,  # enriched later by wikipedia job
            "musicbrainz_id": mb_artist.get("id"),
            "wikidata_id": self._extract_wikidata_id(mb_artist),
            "spotify_id": None,  # enriched later by spotify job
            "born": life_span.get("begin"),
            "died": life_span.get("end") if life_span.get("ended") else None,
            "birth_place": area.get("name"),
            "nationality": country_code or None,
            "musical_tradition": tradition,
            "image_url": None,
            "biography_short": None,
            "biography": None,
            "source_tier": _SOURCE_TIER,
        }

    def _extract_wikidata_id(self, mb_artist: dict[str, Any]) -> str | None:
        """Pull Wikidata QID from url-rels if present."""
        for rel in mb_artist.get("url-relation-list", []):
            url: str = rel.get("target", "")
            if "wikidata.org/wiki/Q" in url:
                return url.rstrip("/").split("/")[-1]
        return None

    async def _upsert_album(
        self,
        rg: dict[str, Any],
        artist_musicbrainz_id: str,
    ) -> None:
        """Upsert a release-group as an album record."""
        from sqlalchemy import text

        stmt = text(
            """
            INSERT INTO albums (
                id,
                title,
                release_date,
                album_type,
                musicbrainz_id,
                artist_musicbrainz_id,
                updated_at
            ) VALUES (
                gen_random_uuid(),
                :title,
                :release_date,
                :album_type,
                :musicbrainz_id,
                :artist_musicbrainz_id,
                now()
            )
            ON CONFLICT (musicbrainz_id) DO UPDATE SET
                title                 = EXCLUDED.title,
                release_date          = COALESCE(EXCLUDED.release_date, albums.release_date),
                album_type            = COALESCE(EXCLUDED.album_type, albums.album_type),
                artist_musicbrainz_id = EXCLUDED.artist_musicbrainz_id,
                updated_at            = now()
            """
        )
        async with self._session_factory() as session:
            await session.execute(
                stmt,
                {
                    "title": rg.get("title"),
                    "release_date": rg.get("first-release-date"),
                    "album_type": rg.get("primary-type"),
                    "musicbrainz_id": rg.get("id"),
                    "artist_musicbrainz_id": artist_musicbrainz_id,
                },
            )
            await session.commit()

    # ── Helpers ───────────────────────────────────────────────────────────────

    async def _region_for_tradition(self, tradition: str) -> str:
        """
        Best-effort region derivation for a tradition name.
        Falls back to 'Global' for cross-regional traditions.
        """
        _TRADITION_REGION: dict[str, str] = {
            "Hindustani Classical": "South Asia",
            "Carnatic": "South Asia",
            "Qawwali": "South Asia",
            "West African Griot": "West Africa",
            "Japanese Gagaku": "East Asia",
            "Chinese Classical": "East Asia",
            "Korean Traditional": "East Asia",
            "Gamelan": "Southeast Asia",
            "Arabic Maqam": "Middle East & North Africa",
            "Persian Classical": "Middle East & North Africa",
            "Turkish Makam": "Middle East & North Africa",
            "Flamenco": "Western Europe",
            "Fado": "Western Europe",
            "Nordic Folk": "Northern Europe",
            "Celtic": "Western Europe",
            "Balkan": "Eastern Europe",
            "Blues": "North America",
            "Jazz": "Global",
            "Brazilian Samba": "South America",
            "Argentine Tango": "South America",
            "Reggae": "Caribbean",
            "Andean": "South America",
        }
        return _TRADITION_REGION.get(tradition, "Global")
