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
from app.schemas.raga import RagaCreate, RagaResponse, RagaSummary, RagaUpdate

router = APIRouter(prefix="/api/v1/ragas", tags=["ragas"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[RagaResponse])
async def list_ragas(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    tradition: str | None = Query(default=None, description="hindustani | carnatic | both"),
    that: str | None = Query(default=None, description="Hindustani thaat name"),
    melakarta_number: int | None = Query(default=None, description="Carnatic melakarta number 1–72"),
    search: str | None = Query(default=None, description="Search by name (case-insensitive)"),
):
    from app.models.raga import Raga

    stmt = select(Raga).where(Raga.deleted_at.is_(None))
    if tradition:
        stmt = stmt.where(Raga.tradition == tradition)
    if that:
        stmt = stmt.where(Raga.that.ilike(f"%{that}%"))
    if melakarta_number is not None:
        stmt = stmt.where(Raga.melakarta_number == melakarta_number)
    if search:
        stmt = stmt.where(Raga.name.ilike(f"%{search}%"))

    stmt = stmt.order_by(Raga.name)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(items=rows, total=total, skip=pagination.skip, limit=pagination.limit)


@router.get("/summary", response_model=list[RagaSummary])
async def list_ragas_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    tradition: str | None = Query(default=None),
):
    """Lightweight list for dropdowns — no pagination, name + key fields only."""
    from app.models.raga import Raga

    stmt = select(Raga).where(Raga.deleted_at.is_(None)).order_by(Raga.name)
    if tradition:
        stmt = stmt.where(Raga.tradition == tradition)

    rows = (await db.execute(stmt)).scalars().all()
    return rows


@router.get("/{raga_id}", response_model=RagaResponse)
async def get_raga(
    raga_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.raga import Raga

    raga = (
        await db.execute(
            select(Raga).where(Raga.id == raga_id, Raga.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if raga is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raga not found")
    return raga


@router.post("/", response_model=RagaResponse, status_code=status.HTTP_201_CREATED)
async def create_raga(
    payload: RagaCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.raga import Raga

    raga = Raga(**payload.model_dump())
    db.add(raga)
    await db.flush()
    await db.refresh(raga)
    logger.info("create_raga", id=str(raga.id), name=raga.name)
    return raga


@router.put("/{raga_id}", response_model=RagaResponse)
async def update_raga(
    raga_id: UUID,
    payload: RagaUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.raga import Raga

    raga = (
        await db.execute(
            select(Raga).where(Raga.id == raga_id, Raga.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if raga is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raga not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(raga, field, value)

    await db.flush()
    await db.refresh(raga)
    return raga


@router.delete("/{raga_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_raga(
    raga_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.raga import Raga

    raga = (
        await db.execute(
            select(Raga).where(Raga.id == raga_id, Raga.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if raga is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raga not found")

    raga.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_raga", id=str(raga_id))
