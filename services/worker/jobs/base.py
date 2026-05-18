"""
Base class for all NādaAtlas ingestion jobs.

Provides:
  - Async DB session management via factory
  - Upsert helpers for core entities (artists, traditions, instruments)
  - ISO country-code → NādaAtlas region mapping
  - Structured logging for every operation
"""
from __future__ import annotations

import abc
import uuid
from typing import Any, Callable

import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import WorkerSettings

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Region mapping
# ---------------------------------------------------------------------------

_COUNTRY_TO_REGION: dict[str, str] = {
    # South Asia
    "IN": "South Asia",
    "PK": "South Asia",
    "BD": "South Asia",
    "LK": "South Asia",
    "NP": "South Asia",
    "BT": "South Asia",
    "MV": "South Asia",
    # East Asia
    "CN": "East Asia",
    "JP": "East Asia",
    "KR": "East Asia",
    "TW": "East Asia",
    "HK": "East Asia",
    "MO": "East Asia",
    # Southeast Asia
    "ID": "Southeast Asia",
    "MY": "Southeast Asia",
    "TH": "Southeast Asia",
    "VN": "Southeast Asia",
    "PH": "Southeast Asia",
    "SG": "Southeast Asia",
    "MM": "Southeast Asia",
    "KH": "Southeast Asia",
    "LA": "Southeast Asia",
    "TL": "Southeast Asia",
    "BN": "Southeast Asia",
    # Central Asia
    "UZ": "Central Asia",
    "KZ": "Central Asia",
    "TJ": "Central Asia",
    "TM": "Central Asia",
    "KG": "Central Asia",
    "AF": "Central Asia",
    # Middle East & North Africa
    "EG": "Middle East & North Africa",
    "SA": "Middle East & North Africa",
    "IQ": "Middle East & North Africa",
    "IR": "Middle East & North Africa",
    "TR": "Middle East & North Africa",
    "SY": "Middle East & North Africa",
    "JO": "Middle East & North Africa",
    "LB": "Middle East & North Africa",
    "YE": "Middle East & North Africa",
    "OM": "Middle East & North Africa",
    "AE": "Middle East & North Africa",
    "QA": "Middle East & North Africa",
    "BH": "Middle East & North Africa",
    "KW": "Middle East & North Africa",
    "PS": "Middle East & North Africa",
    "IL": "Middle East & North Africa",
    "MA": "Middle East & North Africa",
    "DZ": "Middle East & North Africa",
    "TN": "Middle East & North Africa",
    "LY": "Middle East & North Africa",
    # Sub-Saharan Africa
    "NG": "West Africa",
    "GH": "West Africa",
    "SN": "West Africa",
    "ML": "West Africa",
    "GN": "West Africa",
    "CI": "West Africa",
    "BF": "West Africa",
    "TG": "West Africa",
    "BJ": "West Africa",
    "GM": "West Africa",
    "GW": "West Africa",
    "SL": "West Africa",
    "LR": "West Africa",
    "MR": "West Africa",
    "NE": "West Africa",
    "ET": "East Africa",
    "KE": "East Africa",
    "TZ": "East Africa",
    "UG": "East Africa",
    "RW": "East Africa",
    "BI": "East Africa",
    "SO": "East Africa",
    "DJ": "East Africa",
    "ER": "East Africa",
    "ZA": "Southern Africa",
    "ZW": "Southern Africa",
    "ZM": "Southern Africa",
    "MW": "Southern Africa",
    "MZ": "Southern Africa",
    "NA": "Southern Africa",
    "BW": "Southern Africa",
    "LS": "Southern Africa",
    "SZ": "Southern Africa",
    "AO": "Central Africa",
    "CD": "Central Africa",
    "CG": "Central Africa",
    "CM": "Central Africa",
    "GA": "Central Africa",
    "GQ": "Central Africa",
    "CF": "Central Africa",
    "TD": "Central Africa",
    # Europe
    "ES": "Western Europe",
    "PT": "Western Europe",
    "FR": "Western Europe",
    "BE": "Western Europe",
    "NL": "Western Europe",
    "DE": "Western Europe",
    "AT": "Western Europe",
    "CH": "Western Europe",
    "LU": "Western Europe",
    "GB": "Western Europe",
    "IE": "Western Europe",
    "NO": "Northern Europe",
    "SE": "Northern Europe",
    "DK": "Northern Europe",
    "FI": "Northern Europe",
    "IS": "Northern Europe",
    "EE": "Northern Europe",
    "LV": "Northern Europe",
    "LT": "Northern Europe",
    "IT": "Southern Europe",
    "GR": "Southern Europe",
    "HR": "Southern Europe",
    "RS": "Southern Europe",
    "BA": "Southern Europe",
    "ME": "Southern Europe",
    "AL": "Southern Europe",
    "MK": "Southern Europe",
    "SI": "Southern Europe",
    "BG": "Eastern Europe",
    "RO": "Eastern Europe",
    "PL": "Eastern Europe",
    "CZ": "Eastern Europe",
    "SK": "Eastern Europe",
    "HU": "Eastern Europe",
    "UA": "Eastern Europe",
    "BY": "Eastern Europe",
    "MD": "Eastern Europe",
    "RU": "Eastern Europe",
    # Americas
    "US": "North America",
    "CA": "North America",
    "MX": "North America",
    "BR": "South America",
    "AR": "South America",
    "CO": "South America",
    "CL": "South America",
    "PE": "South America",
    "VE": "South America",
    "EC": "South America",
    "BO": "South America",
    "PY": "South America",
    "UY": "South America",
    "GY": "South America",
    "SR": "South America",
    "CU": "Caribbean",
    "JM": "Caribbean",
    "HT": "Caribbean",
    "DO": "Caribbean",
    "PR": "Caribbean",
    "TT": "Caribbean",
    # Oceania
    "AU": "Oceania",
    "NZ": "Oceania",
    "PG": "Oceania",
    "FJ": "Oceania",
}

_DEFAULT_REGION = "Global"


class BaseIngestionJob(abc.ABC):
    """
    Abstract base for all ingestion jobs.

    Subclasses must implement `run()`.
    """

    def __init__(
        self,
        db_session_factory: async_sessionmaker[AsyncSession],
        settings: WorkerSettings,
    ) -> None:
        self._session_factory = db_session_factory
        self._settings = settings
        self._log = logger.bind(job=self.__class__.__name__)

    # ── Abstract interface ────────────────────────────────────────────────────

    @abc.abstractmethod
    async def run(self) -> None:
        """Entry point called by the scheduler."""

    # ── Entity upsert helpers ─────────────────────────────────────────────────

    async def upsert_artist(self, data: dict[str, Any]) -> uuid.UUID:
        """
        Upsert an artist record.

        `data` must contain `musicbrainz_id` for conflict resolution.
        Returns the artist UUID (existing or newly created).
        """
        stmt = text(
            """
            INSERT INTO artists (
                id,
                name,
                name_sort,
                name_native,
                musicbrainz_id,
                wikidata_id,
                spotify_id,
                born,
                died,
                birth_place,
                nationality,
                musical_tradition,
                image_url,
                biography_short,
                biography,
                source_tier,
                updated_at
            ) VALUES (
                gen_random_uuid(),
                :name,
                :name_sort,
                :name_native,
                :musicbrainz_id,
                :wikidata_id,
                :spotify_id,
                :born,
                :died,
                :birth_place,
                :nationality,
                :musical_tradition,
                :image_url,
                :biography_short,
                :biography,
                :source_tier,
                now()
            )
            ON CONFLICT (musicbrainz_id) DO UPDATE SET
                name            = EXCLUDED.name,
                name_sort       = EXCLUDED.name_sort,
                name_native     = COALESCE(EXCLUDED.name_native, artists.name_native),
                wikidata_id     = COALESCE(EXCLUDED.wikidata_id, artists.wikidata_id),
                spotify_id      = COALESCE(EXCLUDED.spotify_id, artists.spotify_id),
                born            = COALESCE(EXCLUDED.born, artists.born),
                died            = COALESCE(EXCLUDED.died, artists.died),
                birth_place     = COALESCE(EXCLUDED.birth_place, artists.birth_place),
                nationality     = COALESCE(EXCLUDED.nationality, artists.nationality),
                musical_tradition = COALESCE(EXCLUDED.musical_tradition, artists.musical_tradition),
                image_url       = COALESCE(EXCLUDED.image_url, artists.image_url),
                biography_short = COALESCE(EXCLUDED.biography_short, artists.biography_short),
                biography       = COALESCE(EXCLUDED.biography, artists.biography),
                source_tier     = LEAST(EXCLUDED.source_tier, artists.source_tier),
                updated_at      = now()
            RETURNING id
            """
        )
        row_data = {
            "name": data.get("name"),
            "name_sort": data.get("name_sort"),
            "name_native": data.get("name_native"),
            "musicbrainz_id": data.get("musicbrainz_id"),
            "wikidata_id": data.get("wikidata_id"),
            "spotify_id": data.get("spotify_id"),
            "born": data.get("born"),
            "died": data.get("died"),
            "birth_place": data.get("birth_place"),
            "nationality": data.get("nationality"),
            "musical_tradition": data.get("musical_tradition"),
            "image_url": data.get("image_url"),
            "biography_short": data.get("biography_short"),
            "biography": data.get("biography"),
            "source_tier": data.get("source_tier", 1),
        }
        async with self._session_factory() as session:
            result = await session.execute(stmt, row_data)
            await session.commit()
            row = result.fetchone()
        artist_id: uuid.UUID = row[0]
        self._log.debug("upsert_artist", artist_id=str(artist_id), name=data.get("name"))
        return artist_id

    async def upsert_tradition(
        self,
        name: str,
        region: str,
        **kwargs: Any,
    ) -> uuid.UUID:
        """
        Upsert a musical_traditions record.
        Conflict key: name (unique).
        """
        stmt = text(
            """
            INSERT INTO musical_traditions (
                id, name, region, description, updated_at
            ) VALUES (
                gen_random_uuid(), :name, :region, :description, now()
            )
            ON CONFLICT (name) DO UPDATE SET
                region      = EXCLUDED.region,
                description = COALESCE(EXCLUDED.description, musical_traditions.description),
                updated_at  = now()
            RETURNING id
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(
                stmt,
                {
                    "name": name,
                    "region": region,
                    "description": kwargs.get("description"),
                },
            )
            await session.commit()
            row = result.fetchone()
        tradition_id: uuid.UUID = row[0]
        self._log.debug("upsert_tradition", tradition_id=str(tradition_id), name=name)
        return tradition_id

    async def upsert_instrument(self, name: str, **kwargs: Any) -> uuid.UUID:
        """
        Upsert an instruments record.
        Conflict key: name (unique).
        """
        stmt = text(
            """
            INSERT INTO instruments (
                id, name, name_native, family, region, description, updated_at
            ) VALUES (
                gen_random_uuid(), :name, :name_native, :family, :region, :description, now()
            )
            ON CONFLICT (name) DO UPDATE SET
                name_native = COALESCE(EXCLUDED.name_native, instruments.name_native),
                family      = COALESCE(EXCLUDED.family, instruments.family),
                region      = COALESCE(EXCLUDED.region, instruments.region),
                description = COALESCE(EXCLUDED.description, instruments.description),
                updated_at  = now()
            RETURNING id
            """
        )
        async with self._session_factory() as session:
            result = await session.execute(
                stmt,
                {
                    "name": name,
                    "name_native": kwargs.get("name_native"),
                    "family": kwargs.get("family"),
                    "region": kwargs.get("region"),
                    "description": kwargs.get("description"),
                },
            )
            await session.commit()
            row = result.fetchone()
        instrument_id: uuid.UUID = row[0]
        self._log.debug(
            "upsert_instrument", instrument_id=str(instrument_id), name=name
        )
        return instrument_id

    # ── Utility ───────────────────────────────────────────────────────────────

    @staticmethod
    def _map_region(country_code: str) -> str:
        """Map ISO 3166-1 alpha-2 country code to a NādaAtlas region string."""
        return _COUNTRY_TO_REGION.get(country_code.upper(), _DEFAULT_REGION)
