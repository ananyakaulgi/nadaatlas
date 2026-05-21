from datetime import UTC
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_pagination
from app.core.logging import get_logger
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.instrument import (
    InstrumentCreate,
    InstrumentResponse,
    InstrumentUpdate,
)

router = APIRouter(prefix="/api/v1/instruments", tags=["instruments"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[InstrumentResponse])
async def list_instruments(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    hs_category: str | None = Query(default=None),
    tradition_id: UUID | None = Query(default=None),
):
    from app.models.instrument import Instrument

    stmt = select(Instrument).where(Instrument.deleted_at.is_(None))
    if hs_category:
        stmt = stmt.where(Instrument.hs_category == hs_category)
    if tradition_id:
        stmt = stmt.where(Instrument.tradition_id == tradition_id)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(
        items=rows, total=total, skip=pagination.skip, limit=pagination.limit
    )


@router.get("/{instrument_id}", response_model=InstrumentResponse)
async def get_instrument(
    instrument_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.instrument import Instrument

    stmt = select(Instrument).where(
        Instrument.id == instrument_id,
        Instrument.deleted_at.is_(None),
    )
    instrument = (await db.execute(stmt)).scalar_one_or_none()
    if instrument is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")
    return instrument


@router.post("/", response_model=InstrumentResponse, status_code=status.HTTP_201_CREATED)
async def create_instrument(
    payload: InstrumentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.instrument import Instrument

    instrument = Instrument(**payload.model_dump())
    db.add(instrument)
    await db.flush()
    await db.refresh(instrument)
    logger.info("create_instrument", id=str(instrument.id))
    return instrument


@router.put("/{instrument_id}", response_model=InstrumentResponse)
async def update_instrument(
    instrument_id: UUID,
    payload: InstrumentUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.instrument import Instrument

    stmt = select(Instrument).where(
        Instrument.id == instrument_id,
        Instrument.deleted_at.is_(None),
    )
    instrument = (await db.execute(stmt)).scalar_one_or_none()
    if instrument is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(instrument, field, value)

    await db.flush()
    await db.refresh(instrument)
    return instrument


@router.delete("/{instrument_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instrument(
    instrument_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from datetime import datetime

    from app.models.instrument import Instrument

    stmt = select(Instrument).where(
        Instrument.id == instrument_id,
        Instrument.deleted_at.is_(None),
    )
    instrument = (await db.execute(stmt)).scalar_one_or_none()
    if instrument is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")

    instrument.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_instrument", id=str(instrument_id))
