from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RagaBase(BaseModel):
    name: str
    name_native: str | None = None
    tradition: str  # hindustani | carnatic | both
    hindustani_name: str | None = None
    carnatic_name: str | None = None
    that: str | None = None
    melakarta_number: int | None = None
    arohana: str | None = None
    avarohana: str | None = None
    vadi: str | None = None
    samvadi: str | None = None
    pakad: str | None = None
    time_of_day: str | None = None
    season: str | None = None
    rasa: str | None = None
    description: str | None = None
    wikipedia_slug: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RagaCreate(RagaBase):
    pass


class RagaUpdate(BaseModel):
    name: str | None = None
    name_native: str | None = None
    tradition: str | None = None
    hindustani_name: str | None = None
    carnatic_name: str | None = None
    that: str | None = None
    melakarta_number: int | None = None
    arohana: str | None = None
    avarohana: str | None = None
    vadi: str | None = None
    samvadi: str | None = None
    pakad: str | None = None
    time_of_day: str | None = None
    season: str | None = None
    rasa: str | None = None
    description: str | None = None
    wikipedia_slug: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RagaResponse(RagaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class RagaSummary(BaseModel):
    id: UUID
    name: str
    tradition: str
    that: str | None = None
    melakarta_number: int | None = None
    arohana: str | None = None

    model_config = ConfigDict(from_attributes=True)
