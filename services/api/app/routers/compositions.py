from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_pagination
from app.core.logging import get_logger
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.composition import (
    CompositionCreate,
    CompositionResponse,
    CompositionSummary,
    CompositionUpdate,
)

router = APIRouter(prefix="/api/v1/compositions", tags=["compositions"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[CompositionResponse])
async def list_compositions(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    tradition_id: UUID | None = Query(default=None),
    composer_id: UUID | None = Query(default=None),
    raga_id: UUID | None = Query(default=None),
    tala_id: UUID | None = Query(default=None),
    composition_type: str | None = Query(default=None, description="e.g. kriti, dhrupad, khayal"),
    search: str | None = Query(default=None, description="Search by title"),
):
    from app.models.composition import Composition

    stmt = (
        select(Composition)
        .where(Composition.deleted_at.is_(None))
        .options(
            selectinload(Composition.composer),
            selectinload(Composition.raga),
            selectinload(Composition.tala),
            selectinload(Composition.tradition),
        )
    )

    if tradition_id:
        stmt = stmt.where(Composition.tradition_id == tradition_id)
    if composer_id:
        stmt = stmt.where(Composition.composer_id == composer_id)
    if raga_id:
        stmt = stmt.where(Composition.raga_id == raga_id)
    if tala_id:
        stmt = stmt.where(Composition.tala_id == tala_id)
    if composition_type:
        stmt = stmt.where(Composition.composition_type.ilike(f"%{composition_type}%"))
    if search:
        stmt = stmt.where(Composition.title.ilike(f"%{search}%"))

    stmt = stmt.order_by(Composition.title)

    total = (await db.execute(select(func.count()).select_from(
        select(Composition).where(Composition.deleted_at.is_(None)).subquery()
    ))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(items=rows, total=total, skip=pagination.skip, limit=pagination.limit)


@router.get("/summary", response_model=list[CompositionSummary])
async def list_compositions_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    composer_id: UUID | None = Query(default=None),
    tradition_id: UUID | None = Query(default=None),
):
    """Lightweight list for dropdowns."""
    from app.models.composition import Composition

    stmt = (
        select(Composition)
        .where(Composition.deleted_at.is_(None))
        .order_by(Composition.title)
    )
    if composer_id:
        stmt = stmt.where(Composition.composer_id == composer_id)
    if tradition_id:
        stmt = stmt.where(Composition.tradition_id == tradition_id)

    rows = (await db.execute(stmt)).scalars().all()
    return rows


@router.get("/{composition_id}", response_model=CompositionResponse)
async def get_composition(
    composition_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.composition import Composition

    composition = (
        await db.execute(
            select(Composition)
            .where(Composition.id == composition_id, Composition.deleted_at.is_(None))
            .options(
                selectinload(Composition.composer),
                selectinload(Composition.raga),
                selectinload(Composition.tala),
                selectinload(Composition.tradition),
            )
        )
    ).scalar_one_or_none()
    if composition is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Composition not found")
    return composition


@router.post("/", response_model=CompositionResponse, status_code=status.HTTP_201_CREATED)
async def create_composition(
    payload: CompositionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.composition import Composition

    composition = Composition(**payload.model_dump())
    db.add(composition)
    await db.flush()
    await db.refresh(composition)
    logger.info("create_composition", id=str(composition.id), title=composition.title)
    return composition


@router.put("/{composition_id}", response_model=CompositionResponse)
async def update_composition(
    composition_id: UUID,
    payload: CompositionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.composition import Composition

    composition = (
        await db.execute(
            select(Composition).where(
                Composition.id == composition_id, Composition.deleted_at.is_(None)
            )
        )
    ).scalar_one_or_none()
    if composition is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Composition not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(composition, field, value)

    await db.flush()
    await db.refresh(composition)
    return composition


@router.delete("/{composition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_composition(
    composition_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.composition import Composition

    composition = (
        await db.execute(
            select(Composition).where(
                Composition.id == composition_id, Composition.deleted_at.is_(None)
            )
        )
    ).scalar_one_or_none()
    if composition is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Composition not found")

    composition.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_composition", id=str(composition_id))
