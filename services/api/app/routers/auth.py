"""Authentication router — /api/v1/auth

Endpoints:
  POST /token           OAuth2 password flow (email + password + optional TOTP)
  POST /refresh         Exchange a refresh token for a new access token
  POST /logout          Blacklist the current access token
  GET  /me              Return authenticated user info
  POST /totp/setup      Generate TOTP secret + QR URI + backup codes
  POST /totp/verify     Verify TOTP code and enable TOTP on the account
  POST /totp/disable    Disable TOTP (requires current password)
  POST /change-password Change password (requires current password)
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_redis
from app.core.database import get_db
from app.core.rate_limiter import limiter
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_backup_codes,
    generate_totp_secret,
    get_totp_uri,
    hash_backup_code,
    hash_password,
    verify_backup_code,
    verify_password,
    verify_totp,
)
from app.models.user import User, UserBackupCode
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshRequest,
    TOTPSetupResponse,
    TOTPVerifyRequest,
    TokenResponse,
    UserResponse,
)
from app.core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# ---------------------------------------------------------------------------
# Constants (fall back to settings for configurability)
# ---------------------------------------------------------------------------
_MAX_FAILED_ATTEMPTS = 5
_LOCKOUT_MINUTES = 15


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


def _check_account_locked(user: User) -> None:
    """Raise 401 if the account is currently locked out."""
    if user.locked_until and user.locked_until > datetime.now(tz=timezone.utc):
        unlock_in = int((user.locked_until - datetime.now(tz=timezone.utc)).total_seconds())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Account temporarily locked. Try again in {unlock_in} seconds.",
        )


async def _record_failed_attempt(db: AsyncSession, user: User) -> None:
    user.failed_login_attempts += 1
    if user.failed_login_attempts >= _MAX_FAILED_ATTEMPTS:
        user.locked_until = datetime.now(tz=timezone.utc) + timedelta(minutes=_LOCKOUT_MINUTES)
        logger.warning(
            "account_locked",
            user_id=str(user.id),
            locked_until=user.locked_until.isoformat(),
        )
    await db.commit()


async def _reset_login_state(db: AsyncSession, user: User) -> None:
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.now(tz=timezone.utc)
    await db.commit()


# ---------------------------------------------------------------------------
# POST /token  (OAuth2 password flow — also accepts JSON LoginRequest body)
# ---------------------------------------------------------------------------

@router.post("/token", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    """Standard OAuth2 password flow.  Accepts form-encoded body.

    Intentionally returns the same error message whether the email is unknown
    or the password is wrong — prevents user enumeration.
    """
    _generic_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await _get_user_by_email(db, form_data.username)  # username == email in OAuth2 form
    if user is None:
        # Perform a dummy hash comparison to prevent timing attacks
        hash_password("dummy_timing_equaliser_NādaAtlas")
        raise _generic_401

    _check_account_locked(user)

    if not verify_password(form_data.password, user.hashed_password):
        await _record_failed_attempt(db, user)
        raise _generic_401

    # TOTP gate
    if user.totp_enabled:
        # totp_code passed as the `client_secret` field of the OAuth2 form,
        # or as a separate query param — extract from scopes or use LoginRequest endpoint
        totp_code = next(
            (s for s in (form_data.scopes or []) if s.isdigit() and len(s) == 6),
            None,
        )
        if not totp_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOTP code required.",
            )
        if not verify_totp(user.totp_secret or "", totp_code):
            await _record_failed_attempt(db, user)
            raise _generic_401

    await _reset_login_state(db, user)
    logger.info("user_login_success", user_id=str(user.id))

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login_json(
    request: Request,
    body: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    """JSON login endpoint — same logic as /token but accepts JSON body with optional totp_code."""
    _generic_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await _get_user_by_email(db, str(body.email))
    if user is None:
        hash_password("dummy_timing_equaliser_NādaAtlas")
        raise _generic_401

    _check_account_locked(user)

    if not verify_password(body.password, user.hashed_password):
        await _record_failed_attempt(db, user)
        raise _generic_401

    if user.totp_enabled:
        if not body.totp_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOTP code required.",
            )
        if not verify_totp(user.totp_secret or "", body.totp_code):
            await _record_failed_attempt(db, user)
            raise _generic_401

    await _reset_login_state(db, user)
    logger.info("user_login_success", user_id=str(user.id))

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ---------------------------------------------------------------------------
# POST /refresh
# ---------------------------------------------------------------------------

@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("20/minute")
async def refresh_token(
    request: Request,
    body: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> TokenResponse:
    """Exchange a valid refresh token for a new access token."""
    payload = decode_token(body.refresh_token)  # raises 401 on bad token

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    jti: str = payload.get("jti", "")
    sub: str = payload.get("sub", "")

    if not jti or not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    blacklisted = await redis_client.exists(f"blacklist:{jti}")
    if blacklisted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked.")

    result = await db.execute(select(User).where(User.id == UUID(sub)))
    user: User | None = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

    # Rotate: blacklist old refresh jti, issue new pair
    _exp = payload.get("exp", 0)
    _now = datetime.now(tz=timezone.utc).timestamp()
    ttl = max(int(_exp - _now), 1)
    await redis_client.setex(f"blacklist:{jti}", ttl, "1")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ---------------------------------------------------------------------------
# POST /logout
# ---------------------------------------------------------------------------

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> None:
    """Blacklist the current access token's JTI in Redis for its remaining lifetime."""
    # Re-extract raw token from the Authorization header (already verified by dependency)
    auth_header = request.headers.get("Authorization", "")
    raw_token = auth_header.removeprefix("Bearer ").strip()

    payload = decode_token(raw_token)
    jti: str = payload.get("jti", "")
    exp: int = payload.get("exp", 0)
    ttl = max(int(exp - datetime.now(tz=timezone.utc).timestamp()), 1)

    await redis_client.setex(f"blacklist:{jti}", ttl, "1")
    logger.info("user_logout", user_id=str(current_user.id), jti=jti)


# ---------------------------------------------------------------------------
# GET /me
# ---------------------------------------------------------------------------

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


# ---------------------------------------------------------------------------
# POST /totp/setup
# ---------------------------------------------------------------------------

@router.post("/totp/setup", response_model=TOTPSetupResponse)
async def totp_setup(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TOTPSetupResponse:
    """Generate a new TOTP secret + QR URI + backup codes.

    Does NOT enable TOTP yet — the caller must verify a code via /totp/verify.
    The raw secret is returned only once; thereafter only the hash is stored.
    """
    secret = generate_totp_secret()
    qr_uri = get_totp_uri(secret, current_user.email)
    raw_codes = generate_backup_codes(8)

    # Persist pending secret (not yet enabled); delete existing unused backup codes
    result = await db.execute(
        select(UserBackupCode).where(UserBackupCode.user_id == current_user.id)
    )
    for old_code in result.scalars().all():
        await db.delete(old_code)

    for code in raw_codes:
        db.add(UserBackupCode(user_id=current_user.id, code_hash=hash_backup_code(code)))

    current_user.totp_secret = secret  # encrypted at rest via column transformer (future)
    current_user.totp_enabled = False  # enabled only after verification
    await db.commit()

    logger.info("totp_setup_initiated", user_id=str(current_user.id))
    return TOTPSetupResponse(secret=secret, qr_uri=qr_uri, backup_codes=raw_codes)


# ---------------------------------------------------------------------------
# POST /totp/verify
# ---------------------------------------------------------------------------

@router.post("/totp/verify", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def totp_verify(
    request: Request,
    body: TOTPVerifyRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Verify a TOTP code and activate TOTP on the account."""
    if not current_user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TOTP setup not initiated. Call /totp/setup first.",
        )

    if not verify_totp(current_user.totp_secret, body.totp_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid TOTP code.",
        )

    current_user.totp_enabled = True
    await db.commit()
    logger.info("totp_enabled", user_id=str(current_user.id))
    return {"detail": "TOTP enabled successfully."}


# ---------------------------------------------------------------------------
# POST /totp/disable
# ---------------------------------------------------------------------------

@router.post("/totp/disable", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def totp_disable(
    request: Request,
    body: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Disable TOTP. Requires the current password as confirmation."""
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
        )

    current_user.totp_enabled = False
    current_user.totp_secret = None

    # Remove all backup codes
    result = await db.execute(
        select(UserBackupCode).where(UserBackupCode.user_id == current_user.id)
    )
    for code in result.scalars().all():
        await db.delete(code)

    await db.commit()
    logger.info("totp_disabled", user_id=str(current_user.id))
    return {"detail": "TOTP disabled successfully."}


# ---------------------------------------------------------------------------
# POST /change-password
# ---------------------------------------------------------------------------

@router.post("/change-password", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def change_password(
    request: Request,
    body: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> dict:
    """Change the authenticated user's password.

    Invalidates all existing tokens by convention — the caller should
    re-authenticate after a password change.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password.",
        )

    current_user.hashed_password = hash_password(body.new_password)
    await db.commit()
    logger.info("password_changed", user_id=str(current_user.id))
    return {"detail": "Password changed successfully. Please log in again."}
