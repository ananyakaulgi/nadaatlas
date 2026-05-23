from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    name: str
    slug: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class GenreResponse(GenreBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class GenreSummary(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)
