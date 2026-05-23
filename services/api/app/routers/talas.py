from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_pagination
from app.core.logging import get_logger
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.tala import TalaCreate, TalaResponse, TalaSummary, TalaUpdate

router = APIRouter(prefix="/api/v1/talas", tags=["talas"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[TalaResponse])
async def list_talas(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    tradition: str | None = Query(default=None, description="hindustani | carnatic | both"),
    beats: int | None = Query(default=None, description="Filter by beat count"),
):
    from app.models.tala import Tala

    stmt = select(Tala).where(Tala.deleted_at.is_(None))
    if tradition:
        stmt = stmt.where(Tala.tradition == tradition)
    if beats is not None:
        stmt = stmt.where(Tala.beats == beats)

    stmt = stmt.order_by(Tala.tradition, Tala.name)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(items=rows, total=total, skip=pagination.skip, limit=pagination.limit)


@router.get("/summary", response_model=list[TalaSummary])
async def list_talas_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    tradition: str | None = Query(default=None),
):
    """Lightweight list for dropdowns."""
    from app.models.tala import Tala

    stmt = select(Tala).where(Tala.deleted_at.is_(None)).order_by(Tala.tradition, Tala.name)
    if tradition:
        stmt = stmt.where(Tala.tradition == tradition)

    rows = (await db.execute(stmt)).scalars().all()
    return rows


@router.get("/{tala_id}", response_model=TalaResponse)
async def get_tala(
    tala_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.tala import Tala

    tala = (
        await db.execute(
            select(Tala).where(Tala.id == tala_id, Tala.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if tala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tala not found")
    return tala


@router.post("/", response_model=TalaResponse, status_code=status.HTTP_201_CREATED)
async def create_tala(
    payload: TalaCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.tala import Tala

    tala = Tala(**payload.model_dump())
    db.add(tala)
    await db.flush()
    await db.refresh(tala)
    logger.info("create_tala", id=str(tala.id), name=tala.name)
    return tala


@router.put("/{tala_id}", response_model=TalaResponse)
async def update_tala(
    tala_id: UUID,
    payload: TalaUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.tala import Tala

    tala = (
        await db.execute(
            select(Tala).where(Tala.id == tala_id, Tala.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if tala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tala not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(tala, field, value)

    await db.flush()
    await db.refresh(tala)
    return tala


@router.delete("/{tala_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tala(
    tala_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.tala import Tala

    tala = (
        await db.execute(
            select(Tala).where(Tala.id == tala_id, Tala.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if tala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tala not found")

    tala.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_tala", id=str(tala_id))
