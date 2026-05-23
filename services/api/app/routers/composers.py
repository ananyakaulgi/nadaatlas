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
from app.schemas.composer import (
    ComposerCreate,
    ComposerResponse,
    ComposerSummary,
    ComposerUpdate,
)

router = APIRouter(prefix="/api/v1/composers", tags=["composers"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[ComposerResponse])
async def list_composers(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    tradition_id: UUID | None = Query(default=None),
    era: str | None = Query(default=None, description="e.g. medieval, colonial, contemporary"),
    nationality: str | None = Query(default=None),
    search: str | None = Query(default=None, description="Search by name"),
):
    from app.models.composer import Composer

    stmt = select(Composer).where(Composer.deleted_at.is_(None))
    if tradition_id:
        stmt = stmt.where(Composer.tradition_id == tradition_id)
    if era:
        stmt = stmt.where(Composer.era.ilike(f"%{era}%"))
    if nationality:
        stmt = stmt.where(Composer.nationality.ilike(f"%{nationality}%"))
    if search:
        stmt = stmt.where(Composer.name.ilike(f"%{search}%"))

    stmt = stmt.order_by(Composer.name_sort.nulls_last(), Composer.name)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (
        await db.execute(
            stmt.options(selectinload(Composer.tradition))
            .offset(pagination.skip)
            .limit(pagination.limit)
        )
    ).scalars().all()

    return PaginatedResponse(items=rows, total=total, skip=pagination.skip, limit=pagination.limit)


@router.get("/summary", response_model=list[ComposerSummary])
async def list_composers_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    tradition_id: UUID | None = Query(default=None),
):
    """Lightweight list for dropdowns."""
    from app.models.composer import Composer

    stmt = (
        select(Composer)
        .where(Composer.deleted_at.is_(None))
        .order_by(Composer.name_sort.nulls_last(), Composer.name)
    )
    if tradition_id:
        stmt = stmt.where(Composer.tradition_id == tradition_id)

    rows = (await db.execute(stmt)).scalars().all()
    return rows


@router.get("/{composer_id}", response_model=ComposerResponse)
async def get_composer(
    composer_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.composer import Composer

    composer = (
        await db.execute(
            select(Composer)
            .where(Composer.id == composer_id, Composer.deleted_at.is_(None))
            .options(selectinload(Composer.tradition))
        )
    ).scalar_one_or_none()
    if composer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Composer not found")
    return composer


@router.post("/", response_model=ComposerResponse, status_code=status.HTTP_201_CREATED)
async def create_composer(
    payload: ComposerCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.composer import Composer

    composer = Composer(**payload.model_dump())
    db.add(composer)
    await db.flush()
    await db.refresh(composer)
    logger.info("create_composer", id=str(composer.id), name=composer.name)
    return composer


@router.put("/{composer_id}", response_model=ComposerResponse)
async def update_composer(
    composer_id: UUID,
    payload: ComposerUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.composer import Composer

    composer = (
        await db.execute(
            select(Composer).where(
                Composer.id == composer_id, Composer.deleted_at.is_(None)
            )
        )
    ).scalar_one_or_none()
    if composer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Composer not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(composer, field, value)

    await db.flush()
    await db.refresh(composer)
    return composer


@router.delete("/{composer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_composer(
    composer_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.composer import Composer

    composer = (
        await db.execute(
            select(Composer).where(
                Composer.id == composer_id, Composer.deleted_at.is_(None)
            )
        )
    ).scalar_one_or_none()
    if composer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Composer not found")

    composer.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_composer", id=str(composer_id))
