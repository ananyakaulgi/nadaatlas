from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import get_settings
from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])

settings = get_settings()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
async def health_check(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HealthResponse:
    """Returns service status. Checks DB connectivity; returns 503 if degraded."""
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(
            status="degraded",
            version="0.1.0",
            environment=settings.APP_ENV,
        )

    return HealthResponse(
        status="ok",
        version="0.1.0",
        environment=settings.APP_ENV,
    )
