"""
Spotify enrichment job.

Adds spotify_id and image_url to artist records using the Spotify Web API.
`spotipy` is synchronous — all calls are wrapped in asyncio.to_thread().
Token caching uses Redis to avoid redundant OAuth round-trips across restarts.
"""
from __future__ import annotations

import asyncio
import json
import time
import uuid
from typing import Any

import spotipy
import structlog
from spotipy.oauth2 import SpotifyClientCredentials

from config import WorkerSettings
from jobs.base import BaseIngestionJob

logger = structlog.get_logger(__name__)

_REDIS_TOKEN_KEY = "nadaatlas:spotify:access_token"
_SPOTIFY_RATE_LIMIT = 10  # max requests per second per Spotify docs


class SpotifyIngestionJob(BaseIngestionJob):
    """Enrich artist records with Spotify IDs and profile images."""

    def __init__(self, db_session_factory: Any, settings: WorkerSettings) -> None:
        super().__init__(db_session_factory, settings)
        self._settings = settings
        self._log = logger.bind(job="SpotifyIngestionJob")
        # Rate-limit semaphore: max 10 concurrent/sequential requests per second
        self._semaphore = asyncio.Semaphore(1)
        self._min_interval = 1.0 / _SPOTIFY_RATE_LIMIT
        self._last_request: float = 0.0
        # Lazy-initialised spotipy client
        self._sp: spotipy.Spotify | None = None

    # ── Entry point ───────────────────────────────────────────────────────────

    async def run(self) -> None:
        """Enrich all artists missing a spotify_id."""
        start = time.monotonic()
        self._log.info("job_start")
        processed = 0

        await self._ensure_client()
        artists = await self._fetch_artists_missing_spotify()

        for row in artists:
            artist_id: uuid.UUID = row["id"]
            name: str = row["name"]
            try:
                await self.enrich_artist_spotify(artist_id=artist_id, artist_name=name)
                processed += 1
            except Exception:
                self._log.exception(
                    "spotify_enrich_error", artist_id=str(artist_id), name=name
                )

        elapsed_ms = round((time.monotonic() - start) * 1000)
        self._log.info(
            "job_complete",
            duration_ms=elapsed_ms,
            records_processed=processed,
        )

    # ── OAuth token management ────────────────────────────────────────────────

    async def _get_token(self) -> str:
        """
        Return a valid Spotify access token.
        Checks Redis cache first; falls back to client-credentials flow.
        """
        try:
            import redis.asyncio as aioredis  # type: ignore[import]

            redis = aioredis.from_url(self._settings.redis_url, decode_responses=True)
            cached = await redis.get(_REDIS_TOKEN_KEY)
            if cached:
                data = json.loads(cached)
                return data["access_token"]
        except Exception:
            self._log.warning("redis_token_cache_unavailable")

        # Obtain fresh token via spotipy's CCF
        ccm = SpotifyClientCredentials(
            client_id=self._settings.spotify_client_id,
            client_secret=self._settings.spotify_client_secret,
        )
        token_info = await asyncio.to_thread(ccm.get_access_token)
        access_token: str = token_info["access_token"]
        expires_in: int = token_info.get("expires_in", 3600)

        # Cache in Redis with a small safety buffer before actual expiry
        try:
            await redis.setex(  # type: ignore[possibly-undefined]
                _REDIS_TOKEN_KEY,
                max(expires_in - 60, 1),
                json.dumps({"access_token": access_token}),
            )
        except Exception:
            pass  # Non-fatal; we'll just re-fetch next time

        return access_token

    async def _ensure_client(self) -> None:
        """Initialise the spotipy client (idempotent)."""
        if self._sp is not None:
            return
        token = await self._get_token()
        self._sp = spotipy.Spotify(auth=token)

    # ── Rate limiting ─────────────────────────────────────────────────────────

    async def _throttle(self) -> None:
        async with self._semaphore:
            now = time.monotonic()
            elapsed = now - self._last_request
            wait = self._min_interval - elapsed
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_request = time.monotonic()

    # ── Core enrichment ───────────────────────────────────────────────────────

    async def search_artist(self, name: str) -> dict[str, Any] | None:
        """
        Search Spotify for an artist by name.
        Returns a dict with spotify_id, image_url, popularity, genres on success.
        """
        assert self._sp is not None, "Call _ensure_client() first"
        await self._throttle()

        result = await asyncio.to_thread(
            self._sp.search,
            q=f"artist:{name}",
            type="artist",
            limit=1,
        )
        items = result.get("artists", {}).get("items", [])
        if not items:
            return None

        item = items[0]
        images = item.get("images", [])
        image_url: str | None = images[0]["url"] if images else None

        return {
            "spotify_id": item.get("id"),
            "image_url": image_url,
            "popularity": item.get("popularity"),
            "genres": item.get("genres", []),
        }

    async def enrich_artist_spotify(
        self, artist_id: uuid.UUID, artist_name: str
    ) -> None:
        """
        Look up an artist on Spotify and persist spotify_id + image_url.
        Skips update if Spotify returns no match.
        """
        spotify_data = await self.search_artist(artist_name)
        if not spotify_data:
            self._log.debug(
                "spotify_no_match", artist_id=str(artist_id), name=artist_name
            )
            return

        await self._update_artist_spotify(
            artist_id=artist_id,
            spotify_id=spotify_data["spotify_id"],
            image_url=spotify_data["image_url"],
        )
        self._log.debug(
            "spotify_enriched",
            artist_id=str(artist_id),
            spotify_id=spotify_data["spotify_id"],
        )

    # ── DB helpers ────────────────────────────────────────────────────────────

    async def _fetch_artists_missing_spotify(self) -> list[dict[str, Any]]:
        from sqlalchemy import text

        stmt = text(
            """
            SELECT id, name
            FROM artists
            WHERE spotify_id IS NULL
              AND name IS NOT NULL
            LIMIT 500
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return [{"id": row[0], "name": row[1]} for row in result]

    async def _update_artist_spotify(
        self,
        artist_id: uuid.UUID,
        spotify_id: str,
        image_url: str | None,
    ) -> None:
        from sqlalchemy import text

        stmt = text(
            """
            UPDATE artists SET
                spotify_id  = :spotify_id,
                image_url   = COALESCE(:image_url, image_url),
                updated_at  = now()
            WHERE id = :id
            """
        )
        async with self._session_factory() as session:
            await session.execute(
                stmt,
                {"spotify_id": spotify_id, "image_url": image_url, "id": artist_id},
            )
            await session.commit()
