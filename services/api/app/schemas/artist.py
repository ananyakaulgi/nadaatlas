from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.instrument import InstrumentSummary
from app.schemas.tradition import TraditionSummary


class ArtistBase(BaseModel):
    name: str
    name_native: str | None = None
    name_sort: str | None = None
    biography_short: str | None = None
    born: date | None = None
    died: date | None = None
    birth_place: str | None = None
    nationality: str | None = None
    musical_tradition: str | None = None
    image_url: str | None = None
    website_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("born", "died", mode="before")
    @classmethod
    def coerce_year_to_date(cls, v):
        """Accept a bare year integer (e.g. 1920) and convert to Jan 1 of that year."""
        if isinstance(v, int):
            return date(v, 1, 1)
        return v


class ArtistCreate(ArtistBase):
    tradition_id: UUID | None = None
    primary_instrument_id: UUID | None = None
    musicbrainz_id: str | None = None
    wikidata_id: str | None = None


class ArtistUpdate(BaseModel):
    name: str | None = None
    name_native: str | None = None
    name_sort: str | None = None
    biography_short: str | None = None
    born: date | None = None
    died: date | None = None
    birth_place: str | None = None
    nationality: str | None = None
    musical_tradition: str | None = None
    image_url: str | None = None
    website_url: str | None = None
    tradition_id: UUID | None = None
    primary_instrument_id: UUID | None = None
    musicbrainz_id: str | None = None
    wikidata_id: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("born", "died", mode="before")
    @classmethod
    def coerce_year_to_date(cls, v):
        if isinstance(v, int):
            return date(v, 1, 1)
        return v


class ArtistResponse(ArtistBase):
    id: UUID
    tradition: TraditionSummary | None = None
    primary_instrument: InstrumentSummary | None = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class ArtistDetail(ArtistResponse):
    biography: str | None = None
    spotify_id: str | None = None
    youtube_channel_id: str | None = None
    wikipedia_slug: str | None = None


class ArtistSummary(BaseModel):
    id: UUID
    name: str
    name_native: str | None = None
    musical_tradition: str | None = None
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
