from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TalaBase(BaseModel):
    name: str
    name_native: str | None = None
    tradition: str  # hindustani | carnatic | both
    beats: int | None = None
    vibhag: int | None = None
    sam_beats: str | None = None
    jati: str | None = None
    anga_structure: str | None = None
    common_tempos: list[str] | None = None
    description: str | None = None
    wikipedia_slug: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TalaCreate(TalaBase):
    pass


class TalaUpdate(BaseModel):
    name: str | None = None
    name_native: str | None = None
    tradition: str | None = None
    beats: int | None = None
    vibhag: int | None = None
    sam_beats: str | None = None
    jati: str | None = None
    anga_structure: str | None = None
    common_tempos: list[str] | None = None
    description: str | None = None
    wikipedia_slug: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TalaResponse(TalaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class TalaSummary(BaseModel):
    id: UUID
    name: str
    tradition: str
    beats: int | None = None
    anga_structure: str | None = None

    model_config = ConfigDict(from_attributes=True)
