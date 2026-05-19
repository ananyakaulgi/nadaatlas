from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_pagination
from app.core.logging import get_logger
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.tradition import (
    TraditionCreate,
    TraditionResponse,
    TraditionUpdate,
)

router = APIRouter(prefix="/api/v1/traditions", tags=["traditions"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[TraditionResponse])
async def list_traditions(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    region: str | None = Query(default=None),
):
    from app.models.tradition import MusicalTradition as Tradition  # local import avoids circular deps

    stmt = select(Tradition).where(Tradition.deleted_at.is_(None))
    if region:
        stmt = stmt.where(Tradition.region == region)

    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(total_stmt)).scalar_one()

    stmt = stmt.offset(pagination.skip).limit(pagination.limit)
    rows = (await db.execute(stmt)).scalars().all()

    logger.info("list_traditions", count=len(rows), region=region)
    return PaginatedResponse(
        items=rows, total=total, skip=pagination.skip, limit=pagination.limit
    )


@router.get("/{tradition_id}", response_model=TraditionResponse)
async def get_tradition(
    tradition_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.tradition import MusicalTradition as Tradition

    stmt = select(Tradition).where(
        Tradition.id == tradition_id,
        Tradition.deleted_at.is_(None),
    )
    tradition = (await db.execute(stmt)).scalar_one_or_none()
    if tradition is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tradition not found")
    return tradition


@router.post("/", response_model=TraditionResponse, status_code=status.HTTP_201_CREATED)
async def create_tradition(
    payload: TraditionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.tradition import MusicalTradition as Tradition

    tradition = Tradition(**payload.model_dump())
    db.add(tradition)
    await db.flush()
    await db.refresh(tradition)
    logger.info("create_tradition", id=str(tradition.id))
    return tradition


@router.put("/{tradition_id}", response_model=TraditionResponse)
async def update_tradition(
    tradition_id: UUID,
    payload: TraditionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.tradition import MusicalTradition as Tradition

    stmt = select(Tradition).where(
        Tradition.id == tradition_id,
        Tradition.deleted_at.is_(None),
    )
    tradition = (await db.execute(stmt)).scalar_one_or_none()
    if tradition is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tradition not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(tradition, field, value)

    await db.flush()
    await db.refresh(tradition)
    logger.info("update_tradition", id=str(tradition_id))
    return tradition


@router.delete("/{tradition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tradition(
    tradition_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.tradition import MusicalTradition as Tradition
    from datetime import datetime, timezone

    stmt = select(Tradition).where(
        Tradition.id == tradition_id,
        Tradition.deleted_at.is_(None),
    )
    tradition = (await db.execute(stmt)).scalar_one_or_none()
    if tradition is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tradition not found")

    tradition.deleted_at = datetime.now(timezone.utc)
    await db.flush()
    logger.info("delete_tradition", id=str(tradition_id))
