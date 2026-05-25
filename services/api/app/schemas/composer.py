from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.tradition import TraditionSummary


class ComposerBase(BaseModel):
    name: str
    name_native: str | None = None
    name_sort: str | None = None
    tradition_id: UUID | None = None
    era: str | None = None
    born: date | None = None
    died: date | None = None
    birth_place: str | None = None
    nationality: str | None = None
    biography_short: str | None = None
    musicbrainz_id: str | None = None
    wikidata_id: str | None = None
    openopus_id: str | None = None
    wikipedia_slug: str | None = None
    image_url: str | None = None
    website_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ComposerCreate(ComposerBase):
    biography: str | None = None


class ComposerUpdate(BaseModel):
    name: str | None = None
    name_native: str | None = None
    name_sort: str | None = None
    tradition_id: UUID | None = None
    era: str | None = None
    born: date | None = None
    died: date | None = None
    birth_place: str | None = None
    nationality: str | None = None
    biography: str | None = None
    biography_short: str | None = None
    musicbrainz_id: str | None = None
    wikidata_id: str | None = None
    openopus_id: str | None = None
    wikipedia_slug: str | None = None
    image_url: str | None = None
    website_url: str | None = None
    is_verified: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class ComposerResponse(ComposerBase):
    id: UUID
    biography: str | None = None
    is_verified: bool
    tradition: TraditionSummary | None = None
    created_at: datetime
    updated_at: datetime


class ComposerSummary(BaseModel):
    id: UUID
    name: str
    name_sort: str | None = None
    era: str | None = None
    nationality: str | None = None

    model_config = ConfigDict(from_attributes=True)
