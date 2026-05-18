"""
Worker service configuration.
All settings are read from environment variables; no defaults carry secrets.
"""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str = Field(..., description="Async PostgreSQL DSN (asyncpg)")

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis_url: str = Field(..., description="Redis connection URL")

    # ── MusicBrainz ───────────────────────────────────────────────────────────
    musicbrainz_app_name: str = Field(default="NadaAtlas")
    musicbrainz_app_version: str = Field(default="0.1.0")
    musicbrainz_contact: str = Field(..., description="Contact email for MB User-Agent")

    # ── Spotify ───────────────────────────────────────────────────────────────
    spotify_client_id: str = Field(..., description="Spotify OAuth client ID")
    spotify_client_secret: str = Field(..., description="Spotify OAuth client secret")

    # ── YouTube ───────────────────────────────────────────────────────────────
    youtube_api_key: str = Field(..., description="YouTube Data API v3 key")

    # ── Wikipedia / Wikidata ──────────────────────────────────────────────────
    wikipedia_languages: list[str] = Field(
        default=["en", "hi", "ja", "zh", "ko", "ar", "fa", "ta", "ru", "es", "pt", "fr", "de"],
        description="Wikipedia language codes to fetch, in priority order",
    )
    wikidata_sparql_url: str = Field(
        default="https://query.wikidata.org/sparql",
        description="Wikidata SPARQL endpoint URL",
    )

    # ── Worker internals ──────────────────────────────────────────────────────
    worker_version: str = Field(default="0.1.0")
    log_level: str = Field(default="INFO")


settings = WorkerSettings()
