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
from app.schemas.genre import GenreCreate, GenreResponse, GenreSummary, GenreUpdate

router = APIRouter(prefix="/api/v1/genres", tags=["genres"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[GenreResponse])
async def list_genres(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    search: str | None = Query(default=None),
):
    from app.models.genre import Genre

    stmt = select(Genre).where(Genre.deleted_at.is_(None))
    if search:
        stmt = stmt.where(Genre.name.ilike(f"%{search}%"))
    stmt = stmt.order_by(Genre.name)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(items=rows, total=total, skip=pagination.skip, limit=pagination.limit)


@router.get("/summary", response_model=list[GenreSummary])
async def list_genres_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """All genres for dropdowns."""
    from app.models.genre import Genre

    rows = (
        await db.execute(select(Genre).where(Genre.deleted_at.is_(None)).order_by(Genre.name))
    ).scalars().all()
    return rows


@router.get("/{genre_id}", response_model=GenreResponse)
async def get_genre(
    genre_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.genre import Genre

    genre = (
        await db.execute(
            select(Genre).where(Genre.id == genre_id, Genre.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return genre


@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(
    payload: GenreCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.genre import Genre

    genre = Genre(**payload.model_dump())
    db.add(genre)
    await db.flush()
    await db.refresh(genre)
    logger.info("create_genre", id=str(genre.id), name=genre.name)
    return genre


@router.put("/{genre_id}", response_model=GenreResponse)
async def update_genre(
    genre_id: UUID,
    payload: GenreUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.genre import Genre

    genre = (
        await db.execute(
            select(Genre).where(Genre.id == genre_id, Genre.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(genre, field, value)

    await db.flush()
    await db.refresh(genre)
    return genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.genre import Genre

    genre = (
        await db.execute(
            select(Genre).where(Genre.id == genre_id, Genre.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")

    genre.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_genre", id=str(genre_id))
