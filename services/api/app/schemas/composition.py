from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.composer import ComposerSummary
from app.schemas.raga import RagaSummary
from app.schemas.tala import TalaSummary
from app.schemas.tradition import TraditionSummary


class CompositionBase(BaseModel):
    title: str
    title_native: str | None = None
    composer_id: UUID | None = None
    tradition_id: UUID | None = None
    composition_type: str | None = None  # e.g. kriti, dhrupad, khayal, ghazal, thumri
    raga_id: UUID | None = None
    tala_id: UUID | None = None
    maqam: str | None = None
    language: str | None = None
    description: str | None = None
    year_composed: int | None = None
    wikipedia_slug: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CompositionCreate(CompositionBase):
    lyrics: str | None = None


class CompositionUpdate(BaseModel):
    title: str | None = None
    title_native: str | None = None
    composer_id: UUID | None = None
    tradition_id: UUID | None = None
    composition_type: str | None = None
    raga_id: UUID | None = None
    tala_id: UUID | None = None
    maqam: str | None = None
    language: str | None = None
    lyrics: str | None = None
    description: str | None = None
    year_composed: int | None = None
    wikipedia_slug: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CompositionResponse(CompositionBase):
    id: UUID
    lyrics: str | None = None
    composer: ComposerSummary | None = None
    raga: RagaSummary | None = None
    tala: TalaSummary | None = None
    tradition: TraditionSummary | None = None
    created_at: datetime
    updated_at: datetime


class CompositionSummary(BaseModel):
    id: UUID
    title: str
    composer_id: UUID | None = None
    composition_type: str | None = None
    year_composed: int | None = None

    model_config = ConfigDict(from_attributes=True)


class CompositionPerformanceResponse(BaseModel):
    composition_id: UUID
    artist_id: UUID
    album_id: UUID
    track_id: UUID | None = None
    performance_year: int | None = None
    notes: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
