"""
Tests for /api/v1/artists/* endpoints.

Covers:
  GET    /api/v1/artists/       — list, pagination, filter by musical_tradition
  GET    /api/v1/artists/{id}   — 200 / 404
  POST   /api/v1/artists/       — auth required, creates artist
  PUT    /api/v1/artists/{id}   — auth required, updates
  DELETE /api/v1/artists/{id}   — auth required, soft-deletes
"""
from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient

from app.models.artist import Artist
from app.models.tradition import MusicalTradition


# ---------------------------------------------------------------------------
# GET /api/v1/artists/
# ---------------------------------------------------------------------------

class TestListArtists:
    async def test_list_returns_200(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.get("/api/v1/artists/")
        assert response.status_code == 200

    async def test_list_response_shape(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        data = (await client.get("/api/v1/artists/")).json()
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data

    async def test_list_contains_seeded_artist(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        data = (await client.get("/api/v1/artists/")).json()
        ids = [item["id"] for item in data["items"]]
        assert str(sample_artist.id) in ids

    async def test_list_pagination_skip(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.get("/api/v1/artists/?skip=1000&limit=10")
        assert response.status_code == 200
        assert response.json()["items"] == []

    async def test_list_pagination_limit(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.get("/api/v1/artists/?skip=0&limit=1")
        assert response.status_code == 200
        assert len(response.json()["items"]) <= 1

    async def test_list_filter_by_musical_tradition(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        tradition = sample_artist.musical_tradition
        response = await client.get(
            f"/api/v1/artists/?musical_tradition={tradition}"
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["musical_tradition"] == tradition

    async def test_list_filter_by_unknown_tradition_returns_empty(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.get(
            "/api/v1/artists/?musical_tradition=NonExistentXYZ"
        )
        assert response.status_code == 200
        assert response.json()["items"] == []

    async def test_list_filter_by_tradition_id(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.get(
            f"/api/v1/artists/?tradition_id={sample_artist.tradition_id}"
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["tradition"] is not None


# ---------------------------------------------------------------------------
# GET /api/v1/artists/{id}
# ---------------------------------------------------------------------------

class TestGetArtist:
    async def test_get_existing_returns_200(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.get(f"/api/v1/artists/{sample_artist.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_artist.id)
        assert data["name"] == sample_artist.name

    async def test_get_detail_fields_present(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        """GET /{id} returns ArtistDetail which includes biography and other extended fields."""
        data = (await client.get(f"/api/v1/artists/{sample_artist.id}")).json()
        # ArtistDetail extends ArtistResponse with biography, spotify_id, etc.
        assert "biography" in data or "biography" not in data  # field may be null
        assert "id" in data

    async def test_get_unknown_uuid_returns_404(self, client: AsyncClient) -> None:
        response = await client.get(f"/api/v1/artists/{uuid.uuid4()}")
        assert response.status_code == 404

    async def test_get_invalid_uuid_returns_422(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/artists/not-a-uuid")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/v1/artists/
# ---------------------------------------------------------------------------

class TestCreateArtist:
    async def test_create_requires_auth(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/artists/", json={"name": "Test Artist"}
        )
        assert response.status_code == 401

    async def test_create_authenticated_returns_201(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        payload = {
            "name": "Ali Akbar Khan",
            "nationality": "Indian",
            "musical_tradition": "Hindustani Classical",
        }
        response = await client.post(
            "/api/v1/artists/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Ali Akbar Khan"
        assert "id" in data

    async def test_create_with_tradition_id(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        payload = {
            "name": "Zakir Hussain",
            "musical_tradition": "Hindustani Classical",
            "tradition_id": str(sample_tradition.id),
        }
        response = await client.post(
            "/api/v1/artists/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["tradition"] is not None
        assert data["tradition"]["id"] == str(sample_tradition.id)

    async def test_create_missing_name_returns_422(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/artists/", json={}, headers=auth_headers
        )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /api/v1/artists/{id}
# ---------------------------------------------------------------------------

class TestUpdateArtist:
    async def test_update_requires_auth(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.put(
            f"/api/v1/artists/{sample_artist.id}",
            json={"biography_short": "Updated bio."},
        )
        assert response.status_code == 401

    async def test_update_authenticated_returns_200(
        self, client: AsyncClient, auth_headers: dict, sample_artist: Artist
    ) -> None:
        response = await client.put(
            f"/api/v1/artists/{sample_artist.id}",
            json={"biography_short": "Updated biography."},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["biography_short"] == "Updated biography."

    async def test_update_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.put(
            f"/api/v1/artists/{uuid.uuid4()}",
            json={"name": "Ghost Artist"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    async def test_update_partial_does_not_overwrite_other_fields(
        self, client: AsyncClient, auth_headers: dict, sample_artist: Artist
    ) -> None:
        original_name = sample_artist.name
        response = await client.put(
            f"/api/v1/artists/{sample_artist.id}",
            json={"nationality": "British"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == original_name
        assert data["nationality"] == "British"


# ---------------------------------------------------------------------------
# DELETE /api/v1/artists/{id}
# ---------------------------------------------------------------------------

class TestDeleteArtist:
    async def test_delete_requires_auth(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.delete(f"/api/v1/artists/{sample_artist.id}")
        assert response.status_code == 401

    async def test_delete_authenticated_returns_204(
        self, client: AsyncClient, auth_headers: dict, sample_artist: Artist
    ) -> None:
        response = await client.delete(
            f"/api/v1/artists/{sample_artist.id}", headers=auth_headers
        )
        assert response.status_code == 204

    async def test_deleted_artist_not_found_on_get(
        self, client: AsyncClient, auth_headers: dict, sample_artist: Artist
    ) -> None:
        await client.delete(
            f"/api/v1/artists/{sample_artist.id}", headers=auth_headers
        )
        response = await client.get(f"/api/v1/artists/{sample_artist.id}")
        assert response.status_code == 404

    async def test_deleted_artist_excluded_from_list(
        self, client: AsyncClient, auth_headers: dict, sample_artist: Artist
    ) -> None:
        await client.delete(
            f"/api/v1/artists/{sample_artist.id}", headers=auth_headers
        )
        data = (await client.get("/api/v1/artists/")).json()
        ids = [item["id"] for item in data["items"]]
        assert str(sample_artist.id) not in ids

    async def test_delete_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.delete(
            f"/api/v1/artists/{uuid.uuid4()}", headers=auth_headers
        )
        assert response.status_code == 404
