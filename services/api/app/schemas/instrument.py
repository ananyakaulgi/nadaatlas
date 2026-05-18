from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.tradition import TraditionSummary


class InstrumentBase(BaseModel):
    name: str
    name_native: str | None = None
    hornbostel_sachs: str | None = None
    hs_category: str | None = None
    description: str | None = None
    origin_region: str | None = None
    materials: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)


class InstrumentCreate(InstrumentBase):
    tradition_id: UUID | None = None


class InstrumentUpdate(BaseModel):
    name: str | None = None
    name_native: str | None = None
    hornbostel_sachs: str | None = None
    hs_category: str | None = None
    description: str | None = None
    origin_region: str | None = None
    materials: list[str] | None = None
    tradition_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class InstrumentResponse(InstrumentBase):
    id: UUID
    tradition: TraditionSummary | None = None
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime


class InstrumentSummary(BaseModel):
    id: UUID
    name: str
    hs_category: str | None = None

    model_config = ConfigDict(from_attributes=True)
