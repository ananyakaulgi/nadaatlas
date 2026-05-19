from typing import Annotated

from fastapi import Depends, Query

from app.core.auth import get_current_user  # real JWT auth dependency
from app.core.database import get_db  # re-export
from app.schemas.common import PaginationParams

__all__ = ["get_db", "get_current_user", "get_pagination"]


def get_pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)


# Annotated type aliases for use in route signatures
DBDep = Annotated[object, Depends(get_db)]
CurrentUserDep = Annotated[object, Depends(get_current_user)]
PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]
