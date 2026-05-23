from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RegionBase(BaseModel):
    name: str
    continent: str | None = None
    country_name: str | None = None
    state: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    name: str | None = None
    continent: str | None = None
    country_name: str | None = None
    state: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RegionResponse(RegionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class RegionSummary(BaseModel):
    id: UUID
    name: str
    continent: str | None = None
    country_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
