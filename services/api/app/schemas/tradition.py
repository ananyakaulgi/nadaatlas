from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TraditionBase(BaseModel):
    name: str
    name_native: str | None = None
    region: str
    subregion: str | None = None
    description: str | None = None
    origin_period: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TraditionCreate(TraditionBase):
    pass


class TraditionUpdate(BaseModel):
    name: str | None = None
    name_native: str | None = None
    region: str | None = None
    subregion: str | None = None
    description: str | None = None
    origin_period: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TraditionResponse(TraditionBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TraditionSummary(BaseModel):
    id: UUID
    name: str
    region: str

    model_config = ConfigDict(from_attributes=True)
