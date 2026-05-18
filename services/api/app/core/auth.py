"""FastAPI authentication dependencies.

Provides:
  - get_redis     — yields a Redis client from the app-startup pool
  - get_current_user     — validates JWT + blacklist + DB lookup
  - get_current_superuser — additional superuser gate
"""
from __future__ import annotations

from typing import Annotated
from uuid import UUID

import structlog
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

logger = structlog.get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


# ---------------------------------------------------------------------------
# Redis dependency
# ---------------------------------------------------------------------------

async def get_redis(request: Request) -> Redis:
    """Yield the shared Redis client stored in ``app.state.redis``.

    The pool is initialised in ``main.py`` lifespan and torn down on shutdown.
    """
    return request.app.state.redis


# ---------------------------------------------------------------------------
# Current user
# ---------------------------------------------------------------------------

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> User:
    """Validate a Bearer JWT and return the matching active User.

    Steps:
      1. Decode and verify the RS256 JWT signature / expiry.
      2. Confirm the token type is "access".
      3. Check the token's ``jti`` is not in the Redis blacklist.
      4. Load the User row by UUID (``sub``).
      5. Confirm the account is active.

    Raises:
        HTTPException 401: on any token or account problem.
    """
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1 & 2 — decode (raises 401 internally on bad token)
    payload = decode_token(token)

    if payload.get("type") != "access":
        logger.warning("wrong_token_type", type=payload.get("type"))
        raise credentials_exc

    jti: str | None = payload.get("jti")
    sub: str | None = payload.get("sub")

    if not jti or not sub:
        raise credentials_exc

    # Step 3 — Redis blacklist check
    blacklisted = await redis_client.exists(f"blacklist:{jti}")
    if blacklisted:
        logger.warning("token_blacklisted", jti=jti)
        raise credentials_exc

    # Step 4 — DB lookup
    try:
        user_uuid = UUID(sub)
    except ValueError:
        raise credentials_exc

    result = await db.execute(select(User).where(User.id == user_uuid))
    user: User | None = result.scalar_one_or_none()

    if user is None:
        logger.warning("user_not_found", sub=sub)
        raise credentials_exc

    # Step 5 — active check
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled.",
        )

    return user


# ---------------------------------------------------------------------------
# Superuser gate
# ---------------------------------------------------------------------------

async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Raise 403 unless the authenticated user is a superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions.",
        )
    return current_user
