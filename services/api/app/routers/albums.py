from datetime import UTC
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_pagination
from app.core.logging import get_logger
from app.schemas.album import AlbumCreate, AlbumResponse, AlbumUpdate
from app.schemas.common import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/api/v1/albums", tags=["albums"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[AlbumResponse])
async def list_albums(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    artist_id: UUID | None = Query(default=None),
    musical_tradition: str | None = Query(default=None),
):
    from app.models.album import Album

    stmt = select(Album).where(Album.deleted_at.is_(None)).options(selectinload(Album.artist))
    if artist_id:
        stmt = stmt.where(Album.artist_id == artist_id)
    if musical_tradition:
        stmt = stmt.where(Album.musical_tradition == musical_tradition)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(
        items=rows, total=total, skip=pagination.skip, limit=pagination.limit
    )


@router.get("/{album_id}", response_model=AlbumResponse)
async def get_album(
    album_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.album import Album

    stmt = select(Album).where(
        Album.id == album_id,
        Album.deleted_at.is_(None),
    ).options(selectinload(Album.artist))
    album = (await db.execute(stmt)).scalar_one_or_none()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return album


@router.post("/", response_model=AlbumResponse, status_code=status.HTTP_201_CREATED)
async def create_album(
    payload: AlbumCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.album import Album

    album = Album(**payload.model_dump())
    db.add(album)
    await db.flush()
    await db.refresh(album)
    logger.info("create_album", id=str(album.id))
    return album


@router.put("/{album_id}", response_model=AlbumResponse)
async def update_album(
    album_id: UUID,
    payload: AlbumUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.album import Album

    stmt = select(Album).where(
        Album.id == album_id,
        Album.deleted_at.is_(None),
    )
    album = (await db.execute(stmt)).scalar_one_or_none()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(album, field, value)

    await db.flush()
    await db.refresh(album)
    return album


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(
    album_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from datetime import datetime

    from app.models.album import Album

    stmt = select(Album).where(
        Album.id == album_id,
        Album.deleted_at.is_(None),
    )
    album = (await db.execute(stmt)).scalar_one_or_none()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")

    album.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_album", id=str(album_id))
