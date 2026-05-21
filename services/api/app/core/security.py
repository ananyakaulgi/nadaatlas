"""Core security primitives: password hashing, JWT RS256, TOTP, backup codes.

Never log passwords, raw tokens, or TOTP secrets — they are masked at this layer.
"""
from __future__ import annotations

import random
import string
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pyotp
import structlog
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

# ---------------------------------------------------------------------------
# Password hashing (bcrypt, cost factor 12)
# ---------------------------------------------------------------------------

_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*.  Never log the input."""
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time comparison via passlib.  Returns True on match."""
    return _pwd_context.verify(plain, hashed)


# ---------------------------------------------------------------------------
# JWT RS256
# ---------------------------------------------------------------------------

def load_private_key(path: str) -> bytes:
    """Return PEM private key bytes.

    Prefers the JWT_PRIVATE_KEY env var (production / Railway).
    Falls back to reading from *path* (development with local key files).
    """
    if settings.JWT_PRIVATE_KEY:
        return settings.JWT_PRIVATE_KEY.encode()
    return Path(path).read_bytes()


def load_public_key(path: str) -> bytes:
    """Return PEM public key bytes.

    Prefers the JWT_PUBLIC_KEY env var (production / Railway).
    Falls back to reading from *path* (development with local key files).
    """
    if settings.JWT_PUBLIC_KEY:
        return settings.JWT_PUBLIC_KEY.encode()
    return Path(path).read_bytes()


def create_access_token(
    subject: str,
    additional_claims: dict | None = None,
) -> str:
    """Create a signed RS256 access JWT.

    Args:
        subject: User UUID as string (stored in ``sub``).
        additional_claims: Extra claims merged into the payload.

    Returns:
        Compact serialised JWT string.
    """
    now = datetime.now(tz=timezone.utc)
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: dict = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "type": "access",
    }
    if additional_claims:
        payload.update(additional_claims)

    private_key = load_private_key(settings.JWT_PRIVATE_KEY_PATH)
    token = jwt.encode(payload, private_key, algorithm=settings.JWT_ALGORITHM)
    logger.debug("access_token_created", sub=subject, jti=payload["jti"])
    return token


def create_refresh_token(subject: str) -> str:
    """Create a signed RS256 refresh JWT.

    Args:
        subject: User UUID as string.

    Returns:
        Compact serialised JWT string.
    """
    now = datetime.now(tz=timezone.utc)
    expire = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    payload: dict = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "type": "refresh",
    }
    private_key = load_private_key(settings.JWT_PRIVATE_KEY_PATH)
    token = jwt.encode(payload, private_key, algorithm=settings.JWT_ALGORITHM)
    logger.debug("refresh_token_created", sub=subject, jti=payload["jti"])
    return token


def decode_token(token: str) -> dict:
    """Verify and decode a JWT using the RS256 public key.

    Raises:
        HTTPException 401: if the token is invalid, expired, or malformed.

    Returns:
        Decoded payload dict.
    """
    try:
        public_key = load_public_key(settings.JWT_PUBLIC_KEY_PATH)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as exc:
        logger.warning("token_decode_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


# ---------------------------------------------------------------------------
# TOTP
# ---------------------------------------------------------------------------

def generate_totp_secret() -> str:
    """Return a random Base32 TOTP seed via pyotp."""
    return pyotp.random_base32()


def get_totp_uri(secret: str, email: str) -> str:
    """Return an otpauth:// provisioning URI suitable for QR code generation."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.APP_NAME)


def verify_totp(secret: str, code: str) -> bool:
    """Verify *code* against *secret*.

    Accepts a ±1 step window to accommodate minor clock drift.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)


# ---------------------------------------------------------------------------
# Backup codes
# ---------------------------------------------------------------------------

_BACKUP_CODE_ALPHABET = string.ascii_uppercase + string.digits
_BACKUP_CODE_LENGTH = 8


def generate_backup_codes(n: int = 8) -> list[str]:
    """Generate *n* random 8-character uppercase alphanumeric backup codes.

    Returns plaintext codes — the caller is responsible for displaying them
    once and storing only the hashed form via :func:`hash_backup_code`.
    """
    return [
        "".join(random.SystemRandom().choices(_BACKUP_CODE_ALPHABET, k=_BACKUP_CODE_LENGTH))
        for _ in range(n)
    ]


def hash_backup_code(code: str) -> str:
    """Return a bcrypt hash of a backup code for safe storage."""
    return _pwd_context.hash(code)


def verify_backup_code(plain: str, hashed: str) -> bool:
    """Constant-time comparison for a backup code.  Returns True on match."""
    return _pwd_context.verify(plain, hashed)
