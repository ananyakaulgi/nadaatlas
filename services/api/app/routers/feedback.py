from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.logging import get_logger
from app.core.rate_limiter import limiter
from app.schemas.feedback import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])
logger = get_logger(__name__)


@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit user feedback",
)
@limiter.limit("10/hour")          # per IP — generous enough for real use
async def submit_feedback(
    request: Request,              # required by slowapi for IP extraction
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
