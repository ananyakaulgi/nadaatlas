from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl

from app.schemas.tradition import TraditionSummary
from app.schemas.instrument import InstrumentSummary


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
