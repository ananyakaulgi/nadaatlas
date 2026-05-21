"""Tests for the /health endpoint."""
from __future__ import annotations

from httpx import AsyncClient


async def test_health_returns_ok(client: AsyncClient) -> None:
    """Health endpoint should return 200 with status=ok when DB is reachable."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


async def test_health_response_has_environment(client: AsyncClient) -> None:
    """Health response should include the environment field."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "environment" in data


async def test_health_version_is_string(client: AsyncClient) -> None:
    """Version field in health response should be a non-empty string."""
    response = await client.get("/health")
    data = response.json()
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0
