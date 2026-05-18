from typing import Annotated

from fastapi import Depends, HTTPException, Query, status

from app.core.database import get_db  # re-export
from app.schemas.common import PaginationParams

__all__ = ["get_db", "get_current_user", "get_pagination"]


async def get_current_user():
    """Stub — replaced by the security layer once auth is wired up."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not yet configured.",
    )


def get_pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)


# Annotated type aliases for use in route signatures
DBDep = Annotated[object, Depends(get_db)]
CurrentUserDep = Annotated[object, Depends(get_current_user)]
PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]
