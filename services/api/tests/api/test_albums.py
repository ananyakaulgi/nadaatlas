"""
Tests for /api/v1/albums/* endpoints.

Covers:
  GET    /api/v1/albums/       — list, pagination
  GET    /api/v1/albums/{id}   — 200 / 404
  POST   /api/v1/albums/       — auth required, creates album
  PUT    /api/v1/albums/{id}   — auth required, updates
  DELETE /api/v1/albums/{id}   — auth required, soft-deletes
"""
from __future__ import annotations

import uuid

from httpx import AsyncClient

from app.models.album import Album
from app.models.artist import Artist

# ---------------------------------------------------------------------------
# GET /api/v1/albums/
# ---------------------------------------------------------------------------

class TestListAlbums:
    async def test_list_returns_200(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        response = await client.get("/api/v1/albums/")
        assert response.status_code == 200

    async def test_list_response_shape(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        data = (await client.get("/api/v1/albums/")).json()
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data

    async def test_list_contains_seeded_album(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        data = (await client.get("/api/v1/albums/")).json()
        ids = [item["id"] for item in data["items"]]
        assert str(sample_album.id) in ids

    async def test_list_album_item_has_artist_summary(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        data = (await client.get("/api/v1/albums/")).json()
        for item in data["items"]:
            assert "artist" in item

    async def test_list_pagination_skip(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        response = await client.get("/api/v1/albums/?skip=1000&limit=10")
        assert response.status_code == 200
        assert response.json()["items"] == []

    async def test_list_pagination_limit(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        response = await client.get("/api/v1/albums/?skip=0&limit=1")
        assert response.status_code == 200
        assert len(response.json()["items"]) <= 1

    async def test_list_filter_by_artist_id(
        self, client: AsyncClient, sample_album: Album, sample_artist: Artist
    ) -> None:
        response = await client.get(
            f"/api/v1/albums/?artist_id={sample_artist.id}"
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["artist"]["id"] == str(sample_artist.id)

    async def test_list_filter_by_musical_tradition(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        tradition = sample_album.musical_tradition
        response = await client.get(
            f"/api/v1/albums/?musical_tradition={tradition}"
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["musical_tradition"] == tradition

    async def test_list_filter_by_unknown_artist_id_returns_empty(
        self, client: AsyncClient
    ) -> None:
        response = await client.get(f"/api/v1/albums/?artist_id={uuid.uuid4()}")
        assert response.status_code == 200
        assert response.json()["items"] == []


# ---------------------------------------------------------------------------
# GET /api/v1/albums/{id}
# ---------------------------------------------------------------------------

class TestGetAlbum:
    async def test_get_existing_returns_200(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        response = await client.get(f"/api/v1/albums/{sample_album.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_album.id)
        assert data["title"] == sample_album.title

    async def test_get_includes_artist_summary(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        data = (await client.get(f"/api/v1/albums/{sample_album.id}")).json()
        assert "artist" in data
        assert data["artist"] is not None

    async def test_get_unknown_uuid_returns_404(
        self, client: AsyncClient
    ) -> None:
        response = await client.get(f"/api/v1/albums/{uuid.uuid4()}")
        assert response.status_code == 404

    async def test_get_invalid_uuid_returns_422(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/api/v1/albums/not-a-uuid")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/v1/albums/
# ---------------------------------------------------------------------------

class TestCreateAlbum:
    async def test_create_requires_auth(
        self, client: AsyncClient, sample_artist: Artist
    ) -> None:
        response = await client.post(
            "/api/v1/albums/",
            json={"title": "Unauthenticated Album", "artist_id": str(sample_artist.id)},
        )
        assert response.status_code == 401

    async def test_create_authenticated_returns_201(
        self, client: AsyncClient, auth_headers: dict, sample_artist: Artist
    ) -> None:
        payload = {
            "title": "Chants of India",
            "artist_id": str(sample_artist.id),
            "album_type": "album",
            "musical_tradition": "Hindustani Classical",
            "release_date": "1997-05-06",
        }
        response = await client.post(
            "/api/v1/albums/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Chants of India"
        assert "id" in data

    async def test_create_minimal_required_fields(
        self, client: AsyncClient, auth_headers: dict, sample_artist: Artist
    ) -> None:
        """Only title and artist_id are required."""
        payload = {
            "title": "Minimal Album",
            "artist_id": str(sample_artist.id),
        }
        response = await client.post(
            "/api/v1/albums/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201

    async def test_create_missing_artist_id_returns_422(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/albums/", json={"title": "No Artist"}, headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_invalid_artist_id_returns_422(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/albums/",
            json={"title": "Bad Artist ID", "artist_id": "not-a-uuid"},
            headers=auth_headers,
        )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /api/v1/albums/{id}
# ---------------------------------------------------------------------------

class TestUpdateAlbum:
    async def test_update_requires_auth(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        response = await client.put(
            f"/api/v1/albums/{sample_album.id}",
            json={"title": "Should Fail"},
        )
        assert response.status_code == 401

    async def test_update_authenticated_returns_200(
        self, client: AsyncClient, auth_headers: dict, sample_album: Album
    ) -> None:
        response = await client.put(
            f"/api/v1/albums/{sample_album.id}",
            json={"label": "Deutsche Grammophon"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["label"] == "Deutsche Grammophon"

    async def test_update_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.put(
            f"/api/v1/albums/{uuid.uuid4()}",
            json={"title": "Ghost Album"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    async def test_update_partial_preserves_other_fields(
        self, client: AsyncClient, auth_headers: dict, sample_album: Album
    ) -> None:
        original_title = sample_album.title
        response = await client.put(
            f"/api/v1/albums/{sample_album.id}",
            json={"label": "New Label"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == original_title
        assert data["label"] == "New Label"


# ---------------------------------------------------------------------------
# DELETE /api/v1/albums/{id}
# ---------------------------------------------------------------------------

class TestDeleteAlbum:
    async def test_delete_requires_auth(
        self, client: AsyncClient, sample_album: Album
    ) -> None:
        response = await client.delete(f"/api/v1/albums/{sample_album.id}")
        assert response.status_code == 401

    async def test_delete_authenticated_returns_204(
        self, client: AsyncClient, auth_headers: dict, sample_album: Album
    ) -> None:
        response = await client.delete(
            f"/api/v1/albums/{sample_album.id}", headers=auth_headers
        )
        assert response.status_code == 204

    async def test_deleted_album_not_found_on_get(
        self, client: AsyncClient, auth_headers: dict, sample_album: Album
    ) -> None:
        await client.delete(
            f"/api/v1/albums/{sample_album.id}", headers=auth_headers
        )
        response = await client.get(f"/api/v1/albums/{sample_album.id}")
        assert response.status_code == 404

    async def test_deleted_album_excluded_from_list(
        self, client: AsyncClient, auth_headers: dict, sample_album: Album
    ) -> None:
        await client.delete(
            f"/api/v1/albums/{sample_album.id}", headers=auth_headers
        )
        data = (await client.get("/api/v1/albums/")).json()
        ids = [item["id"] for item in data["items"]]
        assert str(sample_album.id) not in ids

    async def test_delete_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.delete(
            f"/api/v1/albums/{uuid.uuid4()}", headers=auth_headers
        )
        assert response.status_code == 404
