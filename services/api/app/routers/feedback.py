from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_superuser
from app.core.database import get_db
from app.core.logging import get_logger
from app.core.rate_limiter import limiter
from app.models.user import User
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackStatusUpdate

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])
logger = get_logger(__name__)

# Statuses that mark an item as resolved
_RESOLVED_STATUSES = {"fixed", "wont_fix", "duplicate"}


@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit user feedback",
)
@limiter.limit("10/hour")
async def submit_feedback(
    request: Request,
    payload: FeedbackCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> FeedbackResponse:
    from app.models.feedback import Feedback

    fb = Feedback(**payload.model_dump())
    db.add(fb)
    await db.flush()
    await db.refresh(fb)

    logger.info(
        "feedback_submitted",
        id=str(fb.id),
        category=fb.category,
        has_email=fb.email is not None,
    )
    return fb


@router.get(
    "/",
    response_model=list[FeedbackResponse],
    summary="List all feedback (admin only)",
)
async def list_feedback(
    db: Annotated[AsyncSession, Depends(get_db)],
    _admin: Annotated[User, Depends(get_current_superuser)],
    category: str | None = Query(None, description="Filter by category"),
    feedback_status: str | None = Query(None, alias="status", description="Filter by status"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> list[FeedbackResponse]:
    from app.models.feedback import Feedback

    q = select(Feedback).order_by(Feedback.created_at.desc())
    if category:
        q = q.where(Feedback.category == category)
    if feedback_status:
        q = q.where(Feedback.status == feedback_status)
    q = q.limit(limit).offset(offset)

    result = await db.execute(q)
    return result.scalars().all()


@router.patch(
    "/{feedback_id}/status",
    response_model=FeedbackResponse,
    summary="Update feedback status (admin only)",
)
async def update_feedback_status(
    feedback_id: UUID,
    payload: FeedbackStatusUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _admin: Annotated[User, Depends(get_current_superuser)],
) -> FeedbackResponse:
    from app.models.feedback import Feedback

    row = await db.get(Feedback, feedback_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Feedback not found")

    row.status = payload.status
    if payload.resolution_note is not None:
        row.resolution_note = payload.resolution_note

    # Set resolved_at when transitioning to a terminal status, clear it otherwise
    if payload.status in _RESOLVED_STATUSES and row.resolved_at is None:
        row.resolved_at = datetime.now(UTC)
    elif payload.status not in _RESOLVED_STATUSES:
        row.resolved_at = None

    await db.flush()
    await db.refresh(row)

    logger.info(
        "feedback_status_updated",
        id=str(feedback_id),
        status=payload.status,
    )
    return row
