from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_pagination
from app.core.logging import get_logger
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.artist import (
    ArtistCreate,
    ArtistDetail,
    ArtistResponse,
    ArtistUpdate,
)

router = APIRouter(prefix="/api/v1/artists", tags=["artists"])
logger = get_logger(__name__)


@router.get("/search", response_model=PaginatedResponse[ArtistResponse])
async def search_artists(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    q: str = Query(..., min_length=1),
):
    """Full-text search by name (ilike). Phase 4 will upgrade to vector search."""
    from app.models.artist import Artist

    pattern = f"%{q}%"
    stmt = select(Artist).where(
        Artist.deleted_at.is_(None),
        or_(
            Artist.name.ilike(pattern),
            Artist.name_native.ilike(pattern),
        ),
    )
    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(
        items=rows, total=total, skip=pagination.skip, limit=pagination.limit
    )


@router.get("/", response_model=PaginatedResponse[ArtistResponse])
async def list_artists(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    musical_tradition: str | None = Query(default=None),
    nationality: str | None = Query(default=None),
    tradition_id: UUID | None = Query(default=None),
):
    from app.models.artist import Artist

    stmt = select(Artist).where(Artist.deleted_at.is_(None))
    if musical_tradition:
        stmt = stmt.where(Artist.musical_tradition == musical_tradition)
    if nationality:
        stmt = stmt.where(Artist.nationality == nationality)
    if tradition_id:
        stmt = stmt.where(Artist.tradition_id == tradition_id)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(
        items=rows, total=total, skip=pagination.skip, limit=pagination.limit
    )


@router.get("/{artist_id}", response_model=ArtistDetail)
async def get_artist(
    artist_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.artist import Artist

    stmt = select(Artist).where(
        Artist.id == artist_id,
        Artist.deleted_at.is_(None),
    )
    artist = (await db.execute(stmt)).scalar_one_or_none()
    if artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return artist


@router.post("/", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
async def create_artist(
    payload: ArtistCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.artist import Artist

    artist = Artist(**payload.model_dump())
    db.add(artist)
    await db.flush()
    await db.refresh(artist)
    logger.info("create_artist", id=str(artist.id))
    return artist


@router.put("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: UUID,
    payload: ArtistUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.artist import Artist

    stmt = select(Artist).where(
        Artist.id == artist_id,
        Artist.deleted_at.is_(None),
    )
    artist = (await db.execute(stmt)).scalar_one_or_none()
    if artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(artist, field, value)

    await db.flush()
    await db.refresh(artist)
    return artist


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(
    artist_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.artist import Artist
    from datetime import datetime, timezone

    stmt = select(Artist).where(
        Artist.id == artist_id,
        Artist.deleted_at.is_(None),
    )
    artist = (await db.execute(stmt)).scalar_one_or_none()
    if artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")

    artist.deleted_at = datetime.now(timezone.utc)
    await db.flush()
    logger.info("delete_artist", id=str(artist_id))
