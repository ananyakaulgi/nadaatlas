from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "MusiCompass"
    APP_ENV: str = "development"  # "development" | "staging" | "production"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str  # No default — must be set in environment

    # Database
    DATABASE_URL: str  # Async postgres URL e.g. postgresql+asyncpg://...

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"

    # MinIO / S3-compatible object storage
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET: str = "nadaatlas"

    # JWT (RS256 asymmetric keys)
    # In production set JWT_PRIVATE_KEY / JWT_PUBLIC_KEY as env vars (PEM content).
    # In development the app falls back to reading from JWT_*_KEY_PATH files.
    JWT_PRIVATE_KEY: str = ""          # PEM content as env var (preferred in prod)
    JWT_PUBLIC_KEY: str = ""           # PEM content as env var (preferred in prod)
    JWT_PRIVATE_KEY_PATH: str = "secrets/jwt_private.pem"  # fallback (dev only)
    JWT_PUBLIC_KEY_PATH: str = "secrets/jwt_public.pem"    # fallback (dev only)
    JWT_ALGORITHM: str = "RS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # MusicBrainz
    MUSICBRAINZ_APP_NAME: str = "MusiCompass"
    MUSICBRAINZ_VERSION: str = "0.1.0"
    MUSICBRAINZ_CONTACT: str = ""

    # Spotify
    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""

    # YouTube
    YOUTUBE_API_KEY: str = ""

    # Wikipedia / Wikidata
    WIKIPEDIA_LANGUAGES: list[str] = [
        "en", "hi", "ja", "zh", "ko", "ar", "fa",
        "tr", "pt", "es", "fr", "de", "ru", "ta",
    ]
    WIKIDATA_SPARQL_URL: str = "https://query.wikidata.org/sparql"

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Sentry
    SENTRY_DSN: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
