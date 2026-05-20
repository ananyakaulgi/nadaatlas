"""
Tests for /api/v1/traditions/* endpoints.

Covers:
  GET    /api/v1/traditions/       — list, pagination, region filter
  GET    /api/v1/traditions/{id}   — 200 for existing, 404 for unknown UUID
  POST   /api/v1/traditions/       — auth required, creates tradition, 201
  PUT    /api/v1/traditions/{id}   — auth required, updates, 200
  DELETE /api/v1/traditions/{id}   — auth required, soft-deletes, subsequent GET 404
"""
from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient

from app.models.tradition import MusicalTradition


# ---------------------------------------------------------------------------
# GET /api/v1/traditions/
# ---------------------------------------------------------------------------

class TestListTraditions:
    async def test_list_returns_200(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.get("/api/v1/traditions/")
        assert response.status_code == 200

    async def test_list_returns_paginated_response(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.get("/api/v1/traditions/")
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data

    async def test_list_contains_seeded_tradition(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.get("/api/v1/traditions/")
        data = response.json()
        ids = [item["id"] for item in data["items"]]
        assert str(sample_tradition.id) in ids

    async def test_list_pagination_skip(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        """skip=1000 should return an empty items list (no 5xx)."""
        response = await client.get("/api/v1/traditions/?skip=1000&limit=10")
        assert response.status_code == 200
        assert response.json()["items"] == []

    async def test_list_pagination_limit(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.get("/api/v1/traditions/?skip=0&limit=1")
        assert response.status_code == 200
        assert len(response.json()["items"]) <= 1

    async def test_list_filter_by_region(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.get(
            f"/api/v1/traditions/?region={sample_tradition.region}"
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["region"] == sample_tradition.region

    async def test_list_filter_by_unknown_region_returns_empty(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.get("/api/v1/traditions/?region=NonExistentRegionXYZ")
        assert response.status_code == 200
        assert response.json()["items"] == []


# ---------------------------------------------------------------------------
# GET /api/v1/traditions/{id}
# ---------------------------------------------------------------------------

class TestGetTradition:
    async def test_get_existing_returns_200(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.get(f"/api/v1/traditions/{sample_tradition.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_tradition.id)
        assert data["name"] == sample_tradition.name

    async def test_get_unknown_uuid_returns_404(
        self, client: AsyncClient
    ) -> None:
        response = await client.get(f"/api/v1/traditions/{uuid.uuid4()}")
        assert response.status_code == 404

    async def test_get_invalid_uuid_returns_422(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/api/v1/traditions/not-a-uuid")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/v1/traditions/
# ---------------------------------------------------------------------------

class TestCreateTradition:
    async def test_create_requires_auth(self, client: AsyncClient) -> None:
        payload = {"name": "New Tradition", "region": "Test Region"}
        response = await client.post("/api/v1/traditions/", json=payload)
        assert response.status_code == 401

    async def test_create_authenticated_returns_201(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        payload = {"name": "Carnatic Music", "region": "South Asia"}
        response = await client.post(
            "/api/v1/traditions/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Carnatic Music"
        assert data["region"] == "South Asia"
        assert "id" in data

    async def test_create_returns_full_resource(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        payload = {
            "name": "Qawwali",
            "region": "South Asia",
            "subregion": "Pakistan",
            "description": "Sufi devotional music.",
        }
        response = await client.post(
            "/api/v1/traditions/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Sufi devotional music."
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_duplicate_name_returns_409(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        payload = {"name": sample_tradition.name, "region": "Any Region"}
        response = await client.post(
            "/api/v1/traditions/", json=payload, headers=auth_headers
        )
        assert response.status_code == 409

    async def test_create_missing_required_fields_returns_422(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/traditions/", json={}, headers=auth_headers
        )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /api/v1/traditions/{id}
# ---------------------------------------------------------------------------

class TestUpdateTradition:
    async def test_update_requires_auth(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.put(
            f"/api/v1/traditions/{sample_tradition.id}",
            json={"name": "Updated Name"},
        )
        assert response.status_code == 401

    async def test_update_authenticated_returns_200(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        response = await client.put(
            f"/api/v1/traditions/{sample_tradition.id}",
            json={"description": "Updated description."},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Updated description."

    async def test_update_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.put(
            f"/api/v1/traditions/{uuid.uuid4()}",
            json={"name": "Ghost Tradition"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    async def test_update_partial_fields_only_changes_specified(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        original_name = sample_tradition.name
        response = await client.put(
            f"/api/v1/traditions/{sample_tradition.id}",
            json={"description": "Partial update."},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == original_name
        assert data["description"] == "Partial update."


# ---------------------------------------------------------------------------
# DELETE /api/v1/traditions/{id}
# ---------------------------------------------------------------------------

class TestDeleteTradition:
    async def test_delete_requires_auth(
        self, client: AsyncClient, sample_tradition: MusicalTradition
    ) -> None:
        response = await client.delete(f"/api/v1/traditions/{sample_tradition.id}")
        assert response.status_code == 401

    async def test_delete_authenticated_returns_204(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        response = await client.delete(
            f"/api/v1/traditions/{sample_tradition.id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

    async def test_deleted_tradition_not_found_on_get(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        """Soft-deleted tradition must return 404 on subsequent GET."""
        await client.delete(
            f"/api/v1/traditions/{sample_tradition.id}",
            headers=auth_headers,
        )
        response = await client.get(f"/api/v1/traditions/{sample_tradition.id}")
        assert response.status_code == 404

    async def test_deleted_tradition_excluded_from_list(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        """Soft-deleted tradition must not appear in the list endpoint."""
        await client.delete(
            f"/api/v1/traditions/{sample_tradition.id}",
            headers=auth_headers,
        )
        response = await client.get("/api/v1/traditions/")
        ids = [item["id"] for item in response.json()["items"]]
        assert str(sample_tradition.id) not in ids

    async def test_delete_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.delete(
            f"/api/v1/traditions/{uuid.uuid4()}",
            headers=auth_headers,
        )
        assert response.status_code == 404
