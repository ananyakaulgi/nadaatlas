"""
Unit tests for app/core/security.py

Tests the pure cryptographic primitives without database or network access:
  - hash_password / verify_password
  - create_access_token / create_refresh_token
  - decode_token (valid, expired, wrong type)
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from jose import jwt

# Ensure the API root is importable regardless of working directory
import sys
_API_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _API_ROOT not in sys.path:
    sys.path.insert(0, _API_ROOT)

# Set required env vars before importing settings-dependent modules
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/test")
os.environ.setdefault("SECRET_KEY", "unit-test-secret-key-not-for-production")

from app.core.security import (  # noqa: E402
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.core.config import get_settings  # noqa: E402


settings = get_settings()

# ---------------------------------------------------------------------------
# password hashing
# ---------------------------------------------------------------------------

class TestHashPassword:
    def test_hash_returns_string(self) -> None:
        result = hash_password("MySecretPassword!")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_hash_is_bcrypt(self) -> None:
        result = hash_password("MySecretPassword!")
        # bcrypt hashes begin with $2b$ or $2a$
        assert result.startswith("$2")

    def test_same_password_produces_different_hashes(self) -> None:
        """bcrypt uses random salts — two hashes of the same password must differ."""
        h1 = hash_password("SamePassword123!")
        h2 = hash_password("SamePassword123!")
        assert h1 != h2


class TestVerifyPassword:
    def test_correct_password_returns_true(self) -> None:
        hashed = hash_password("CorrectHorse99!")
        assert verify_password("CorrectHorse99!", hashed) is True

    def test_wrong_password_returns_false(self) -> None:
        hashed = hash_password("CorrectHorse99!")
        assert verify_password("WrongPassword99!", hashed) is False

    def test_empty_string_returns_false(self) -> None:
        hashed = hash_password("NotEmpty99!")
        assert verify_password("", hashed) is False

    def test_case_sensitive(self) -> None:
        hashed = hash_password("CaseSensitive99!")
        assert verify_password("casesensitive99!", hashed) is False


# ---------------------------------------------------------------------------
# JWT creation
# ---------------------------------------------------------------------------

class TestCreateAccessToken:
    def test_returns_string(self) -> None:
        token = create_access_token("user-uuid-123")
        assert isinstance(token, str)
        assert len(token.split(".")) == 3  # header.payload.signature

    def test_payload_contains_sub(self) -> None:
        subject = "user-uuid-abc"
        token = create_access_token(subject)
        payload = decode_token(token)
        assert payload["sub"] == subject

    def test_payload_type_is_access(self) -> None:
        token = create_access_token("user-uuid-xyz")
        payload = decode_token(token)
        assert payload["type"] == "access"

    def test_payload_has_jti(self) -> None:
        token = create_access_token("user-uuid-xyz")
        payload = decode_token(token)
        assert "jti" in payload
        assert len(payload["jti"]) > 0

    def test_payload_has_exp(self) -> None:
        token = create_access_token("user-uuid-xyz")
        payload = decode_token(token)
        assert "exp" in payload
        # exp must be in the future
        assert payload["exp"] > datetime.now(tz=timezone.utc).timestamp()

    def test_additional_claims_are_included(self) -> None:
        token = create_access_token("user-uuid-xyz", additional_claims={"role": "editor"})
        payload = decode_token(token)
        assert payload["role"] == "editor"


class TestCreateRefreshToken:
    def test_returns_string(self) -> None:
        token = create_refresh_token("user-uuid-123")
        assert isinstance(token, str)

    def test_payload_type_is_refresh(self) -> None:
        token = create_refresh_token("user-uuid-123")
        public_key = __import__("pathlib").Path(settings.JWT_PUBLIC_KEY_PATH).read_bytes()
        payload = jwt.decode(token, public_key, algorithms=[settings.JWT_ALGORITHM])
        assert payload["type"] == "refresh"

    def test_payload_contains_correct_sub(self) -> None:
        subject = "user-uuid-refresh"
        token = create_refresh_token(subject)
        public_key = __import__("pathlib").Path(settings.JWT_PUBLIC_KEY_PATH).read_bytes()
        payload = jwt.decode(token, public_key, algorithms=[settings.JWT_ALGORITHM])
        assert payload["sub"] == subject

    def test_refresh_token_has_longer_expiry_than_access_token(self) -> None:
        access_token = create_access_token("user-uuid-123")
        refresh_token = create_refresh_token("user-uuid-123")
        public_key = __import__("pathlib").Path(settings.JWT_PUBLIC_KEY_PATH).read_bytes()
        access_payload = jwt.decode(access_token, public_key, algorithms=[settings.JWT_ALGORITHM])
        refresh_payload = jwt.decode(refresh_token, public_key, algorithms=[settings.JWT_ALGORITHM])
        assert refresh_payload["exp"] > access_payload["exp"]


# ---------------------------------------------------------------------------
# Token decoding
# ---------------------------------------------------------------------------

class TestDecodeToken:
    def test_valid_token_returns_payload(self) -> None:
        token = create_access_token("user-uuid-decode-test")
        payload = decode_token(token)
        assert isinstance(payload, dict)
        assert payload["sub"] == "user-uuid-decode-test"

    def test_expired_token_raises_http_401(self) -> None:
        """Forge a token that already expired and confirm decode raises 401."""
        from pathlib import Path

        now = datetime.now(tz=timezone.utc)
        expired_payload = {
            "sub": "user-uuid-expired",
            "iat": now - timedelta(hours=2),
            "exp": now - timedelta(hours=1),  # expired 1 hour ago
            "jti": "some-jti-value",
            "type": "access",
        }
        private_key = Path(settings.JWT_PRIVATE_KEY_PATH).read_bytes()
        expired_token = jwt.encode(
            expired_payload, private_key, algorithm=settings.JWT_ALGORITHM
        )

        with pytest.raises(HTTPException) as exc_info:
            decode_token(expired_token)
        assert exc_info.value.status_code == 401

    def test_tampered_token_raises_http_401(self) -> None:
        token = create_access_token("user-uuid-tamper-test")
        # Replace the signature part (third segment) with garbage to invalidate it
        parts = token.split(".")
        assert len(parts) == 3, "JWT must have 3 parts"
        tampered = parts[0] + "." + parts[1] + ".invalidsignatureXXXXXXXXXXXXX"
        with pytest.raises(HTTPException) as exc_info:
            decode_token(tampered)
        assert exc_info.value.status_code == 401

    def test_garbage_string_raises_http_401(self) -> None:
        with pytest.raises(HTTPException) as exc_info:
            decode_token("this.is.not.a.jwt")
        assert exc_info.value.status_code == 401

    def test_wrong_algorithm_token_raises_http_401(self) -> None:
        """A token signed with HS256 (wrong algorithm) must be rejected."""
        payload = {
            "sub": "user-uuid-hs256",
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        }
        hs256_token = jwt.encode(payload, "some-secret", algorithm="HS256")
        with pytest.raises(HTTPException) as exc_info:
            decode_token(hs256_token)
        assert exc_info.value.status_code == 401
