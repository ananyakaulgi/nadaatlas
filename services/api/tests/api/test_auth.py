"""
Tests for /api/v1/auth/* endpoints.

Covers:
  POST /api/v1/auth/login       — success, wrong password, unknown email
  GET  /api/v1/auth/me          — authenticated, unauthenticated
  POST /api/v1/auth/refresh     — valid refresh token, invalid token
  POST /api/v1/auth/logout      — token invalidation, subsequent /me returns 401
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.models.user import User


# ---------------------------------------------------------------------------
# POST /api/v1/auth/login
# ---------------------------------------------------------------------------

class TestLogin:
    async def test_login_success_returns_tokens(
        self, client: AsyncClient, test_user: User
    ) -> None:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "TestPass123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["expires_in"], int)
        assert data["expires_in"] > 0

    async def test_login_wrong_password_returns_401(
        self, client: AsyncClient, test_user: User
    ) -> None:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "WrongPassword!"},
        )
        assert response.status_code == 401

    async def test_login_unknown_email_returns_401(
        self, client: AsyncClient
    ) -> None:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@example.com", "password": "AnyPassword!"},
        )
        assert response.status_code == 401

    async def test_login_unknown_email_does_not_reveal_existence(
        self, client: AsyncClient, test_user: User
    ) -> None:
        """Both wrong-password and unknown-email must return the same error message."""
        wrong_pw = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "BadPassword!"},
        )
        unknown = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@example.com", "password": "BadPassword!"},
        )
        assert wrong_pw.json()["detail"] == unknown.json()["detail"]

    async def test_login_missing_fields_returns_422(
        self, client: AsyncClient
    ) -> None:
        response = await client.post("/api/v1/auth/login", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/auth/me
# ---------------------------------------------------------------------------

class TestGetMe:
    async def test_me_authenticated_returns_user(
        self, client: AsyncClient, auth_headers: dict, test_user: User
    ) -> None:
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["is_active"] is True
        assert "id" in data

    async def test_me_unauthenticated_returns_401(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    async def test_me_invalid_token_returns_401(
        self, client: AsyncClient
    ) -> None:
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer this.is.not.a.valid.jwt"},
        )
        assert response.status_code == 401

    async def test_me_response_does_not_contain_password(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        data = response.json()
        assert "hashed_password" not in data
        assert "password" not in data


# ---------------------------------------------------------------------------
# POST /api/v1/auth/refresh
# ---------------------------------------------------------------------------

class TestRefresh:
    async def test_refresh_valid_token_returns_new_tokens(
        self, client: AsyncClient, test_user: User
    ) -> None:
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "TestPass123!"},
        )
        refresh_token = login.json()["refresh_token"]

        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        # New tokens must differ from the originals
        assert data["access_token"] != login.json()["access_token"]

    async def test_refresh_invalid_token_returns_401(
        self, client: AsyncClient
    ) -> None:
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.refresh.token"},
        )
        assert response.status_code == 401

    async def test_refresh_with_access_token_returns_401(
        self, client: AsyncClient, test_user: User
    ) -> None:
        """Passing an access token to /refresh must be rejected."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "TestPass123!"},
        )
        access_token = login.json()["access_token"]

        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token},
        )
        assert response.status_code == 401

    async def test_refresh_missing_body_returns_422(
        self, client: AsyncClient
    ) -> None:
        response = await client.post("/api/v1/auth/refresh", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/v1/auth/logout
# ---------------------------------------------------------------------------

class TestLogout:
    async def test_logout_returns_204(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == 204

    async def test_logout_invalidates_token(
        self, client: AsyncClient, test_user: User
    ) -> None:
        """After logout, the same access token must not authenticate /me."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "TestPass123!"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        logout = await client.post("/api/v1/auth/logout", headers=headers)
        assert logout.status_code == 204

        me = await client.get("/api/v1/auth/me", headers=headers)
        assert me.status_code == 401

    async def test_logout_unauthenticated_returns_401(
        self, client: AsyncClient
    ) -> None:
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == 401
