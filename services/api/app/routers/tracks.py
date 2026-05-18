from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_pagination
from app.core.logging import get_logger
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.track import TrackCreate, TrackResponse, TrackUpdate

router = APIRouter(prefix="/api/v1/tracks", tags=["tracks"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[TrackResponse])
async def list_tracks(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    artist_id: UUID | None = Query(default=None),
    album_id: UUID | None = Query(default=None),
    musical_tradition: str | None = Query(default=None),
    raga: str | None = Query(default=None),
):
    from app.models.track import Track

    stmt = select(Track).where(Track.deleted_at.is_(None))
    if artist_id:
        stmt = stmt.where(Track.artist_id == artist_id)
    if album_id:
        stmt = stmt.where(Track.album_id == album_id)
    if musical_tradition:
        stmt = stmt.where(Track.musical_tradition == musical_tradition)
    if raga:
        stmt = stmt.where(Track.raga == raga)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(
        items=rows, total=total, skip=pagination.skip, limit=pagination.limit
    )


@router.get("/{track_id}", response_model=TrackResponse)
async def get_track(
    track_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.track import Track

    stmt = select(Track).where(
        Track.id == track_id,
        Track.deleted_at.is_(None),
    )
    track = (await db.execute(stmt)).scalar_one_or_none()
    if track is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track


@router.post("/", response_model=TrackResponse, status_code=status.HTTP_201_CREATED)
async def create_track(
    payload: TrackCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.track import Track

    track = Track(**payload.model_dump())
    db.add(track)
    await db.flush()
    await db.refresh(track)
    logger.info("create_track", id=str(track.id))
    return track


@router.put("/{track_id}", response_model=TrackResponse)
async def update_track(
    track_id: UUID,
    payload: TrackUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.track import Track

    stmt = select(Track).where(
        Track.id == track_id,
        Track.deleted_at.is_(None),
    )
    track = (await db.execute(stmt)).scalar_one_or_none()
    if track is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(track, field, value)

    await db.flush()
    await db.refresh(track)
    return track


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_track(
    track_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.track import Track
    from datetime import datetime, timezone

    stmt = select(Track).where(
        Track.id == track_id,
        Track.deleted_at.is_(None),
    )
    track = (await db.execute(stmt)).scalar_one_or_none()
    if track is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    track.deleted_at = datetime.now(timezone.utc)
    await db.flush()
    logger.info("delete_track", id=str(track_id))
