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
from app.schemas.region import RegionCreate, RegionResponse, RegionSummary, RegionUpdate

router = APIRouter(prefix="/api/v1/regions", tags=["regions"])
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[RegionResponse])
async def list_regions(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    continent: str | None = Query(default=None),
    country_name: str | None = Query(default=None),
):
    from app.models.region import Region

    stmt = select(Region).where(Region.deleted_at.is_(None))
    if continent:
        stmt = stmt.where(Region.continent.ilike(f"%{continent}%"))
    if country_name:
        stmt = stmt.where(Region.country_name.ilike(f"%{country_name}%"))

    stmt = stmt.order_by(Region.continent.nulls_last(), Region.name)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.offset(pagination.skip).limit(pagination.limit))).scalars().all()

    return PaginatedResponse(items=rows, total=total, skip=pagination.skip, limit=pagination.limit)


@router.get("/summary", response_model=list[RegionSummary])
async def list_regions_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Lightweight list for dropdowns."""
    from app.models.region import Region

    rows = (
        await db.execute(
            select(Region)
            .where(Region.deleted_at.is_(None))
            .order_by(Region.continent.nulls_last(), Region.name)
        )
    ).scalars().all()
    return rows


@router.get("/{region_id}", response_model=RegionResponse)
async def get_region(
    region_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.region import Region

    region = (
        await db.execute(
            select(Region).where(Region.id == region_id, Region.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
    return region


@router.post("/", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
async def create_region(
    payload: RegionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.region import Region

    region = Region(**payload.model_dump())
    db.add(region)
    await db.flush()
    await db.refresh(region)
    logger.info("create_region", id=str(region.id), name=region.name)
    return region


@router.put("/{region_id}", response_model=RegionResponse)
async def update_region(
    region_id: UUID,
    payload: RegionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.region import Region

    region = (
        await db.execute(
            select(Region).where(Region.id == region_id, Region.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(region, field, value)

    await db.flush()
    await db.refresh(region)
    return region


@router.delete("/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(
    region_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[object, Depends(get_current_user)],
):
    from app.models.region import Region

    region = (
        await db.execute(
            select(Region).where(Region.id == region_id, Region.deleted_at.is_(None))
        )
    ).scalar_one_or_none()
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")

    region.deleted_at = datetime.now(UTC)
    await db.flush()
    logger.info("delete_region", id=str(region_id))
