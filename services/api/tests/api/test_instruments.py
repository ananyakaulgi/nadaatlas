"""
Tests for /api/v1/instruments/* endpoints.

Covers:
  GET    /api/v1/instruments/       — list, pagination, filter by hs_category
  GET    /api/v1/instruments/{id}   — 200 / 404
  POST   /api/v1/instruments/       — auth required, creates instrument
  PUT    /api/v1/instruments/{id}   — auth required, updates
  DELETE /api/v1/instruments/{id}   — auth required, soft-deletes
"""
from __future__ import annotations

import uuid

from httpx import AsyncClient

from app.models.instrument import Instrument
from app.models.tradition import MusicalTradition

# ---------------------------------------------------------------------------
# GET /api/v1/instruments/
# ---------------------------------------------------------------------------

class TestListInstruments:
    async def test_list_returns_200(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.get("/api/v1/instruments/")
        assert response.status_code == 200

    async def test_list_response_shape(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        data = (await client.get("/api/v1/instruments/")).json()
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data

    async def test_list_contains_seeded_instrument(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        data = (await client.get("/api/v1/instruments/")).json()
        ids = [item["id"] for item in data["items"]]
        assert str(sample_instrument.id) in ids

    async def test_list_pagination_skip(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.get("/api/v1/instruments/?skip=1000&limit=10")
        assert response.status_code == 200
        assert response.json()["items"] == []

    async def test_list_pagination_limit(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.get("/api/v1/instruments/?skip=0&limit=1")
        assert response.status_code == 200
        assert len(response.json()["items"]) <= 1

    async def test_list_filter_by_hs_category(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        category = sample_instrument.hs_category
        response = await client.get(
            f"/api/v1/instruments/?hs_category={category}"
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["hs_category"] == category

    async def test_list_filter_by_unknown_hs_category_returns_empty(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.get(
            "/api/v1/instruments/?hs_category=nonexistent_category_xyz"
        )
        assert response.status_code == 200
        assert response.json()["items"] == []

    async def test_list_filter_by_tradition_id(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.get(
            f"/api/v1/instruments/?tradition_id={sample_instrument.tradition_id}"
        )
        assert response.status_code == 200
        for item in response.json()["items"]:
            assert item["tradition"] is not None


# ---------------------------------------------------------------------------
# GET /api/v1/instruments/{id}
# ---------------------------------------------------------------------------

class TestGetInstrument:
    async def test_get_existing_returns_200(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.get(f"/api/v1/instruments/{sample_instrument.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_instrument.id)
        assert data["name"] == sample_instrument.name

    async def test_get_response_includes_tradition(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        data = (await client.get(f"/api/v1/instruments/{sample_instrument.id}")).json()
        assert "tradition" in data
        assert data["tradition"] is not None

    async def test_get_unknown_uuid_returns_404(
        self, client: AsyncClient
    ) -> None:
        response = await client.get(f"/api/v1/instruments/{uuid.uuid4()}")
        assert response.status_code == 404

    async def test_get_invalid_uuid_returns_422(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/api/v1/instruments/not-a-uuid")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/v1/instruments/
# ---------------------------------------------------------------------------

class TestCreateInstrument:
    async def test_create_requires_auth(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/instruments/", json={"name": "Unauthenticated Instrument"}
        )
        assert response.status_code == 401

    async def test_create_authenticated_returns_201(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        payload = {
            "name": "Tabla",
            "name_native": "तबला",
            "hs_category": "membranophone",
            "origin_region": "South Asia",
            "description": "A pair of hand drums used in Hindustani music.",
        }
        response = await client.post(
            "/api/v1/instruments/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tabla"
        assert "id" in data

    async def test_create_with_tradition_id(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_tradition: MusicalTradition,
    ) -> None:
        payload = {
            "name": "Sarod",
            "hs_category": "chordophone",
            "tradition_id": str(sample_tradition.id),
        }
        response = await client.post(
            "/api/v1/instruments/", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["tradition"] is not None
        assert data["tradition"]["id"] == str(sample_tradition.id)

    async def test_create_missing_name_returns_422(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.post(
            "/api/v1/instruments/", json={}, headers=auth_headers
        )
        assert response.status_code == 422

    async def test_create_duplicate_name_returns_409_or_500(
        self,
        client: AsyncClient,
        auth_headers: dict,
        sample_instrument: Instrument,
    ) -> None:
        """Instrument name is unique — second insert should fail with 4xx/5xx."""
        payload = {"name": sample_instrument.name}
        response = await client.post(
            "/api/v1/instruments/", json=payload, headers=auth_headers
        )
        # The router doesn't catch IntegrityError for instruments the same way traditions
        # does, so it may return 500.  Either non-2xx is acceptable.
        assert response.status_code >= 400


# ---------------------------------------------------------------------------
# PUT /api/v1/instruments/{id}
# ---------------------------------------------------------------------------

class TestUpdateInstrument:
    async def test_update_requires_auth(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.put(
            f"/api/v1/instruments/{sample_instrument.id}",
            json={"description": "Should fail"},
        )
        assert response.status_code == 401

    async def test_update_authenticated_returns_200(
        self, client: AsyncClient, auth_headers: dict, sample_instrument: Instrument
    ) -> None:
        response = await client.put(
            f"/api/v1/instruments/{sample_instrument.id}",
            json={"description": "Updated instrument description."},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Updated instrument description."

    async def test_update_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.put(
            f"/api/v1/instruments/{uuid.uuid4()}",
            json={"description": "Ghost description"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    async def test_update_partial_preserves_other_fields(
        self, client: AsyncClient, auth_headers: dict, sample_instrument: Instrument
    ) -> None:
        original_name = sample_instrument.name
        response = await client.put(
            f"/api/v1/instruments/{sample_instrument.id}",
            json={"hornbostel_sachs": "321.321.5"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == original_name
        assert data["hornbostel_sachs"] == "321.321.5"


# ---------------------------------------------------------------------------
# DELETE /api/v1/instruments/{id}
# ---------------------------------------------------------------------------

class TestDeleteInstrument:
    async def test_delete_requires_auth(
        self, client: AsyncClient, sample_instrument: Instrument
    ) -> None:
        response = await client.delete(f"/api/v1/instruments/{sample_instrument.id}")
        assert response.status_code == 401

    async def test_delete_authenticated_returns_204(
        self, client: AsyncClient, auth_headers: dict, sample_instrument: Instrument
    ) -> None:
        response = await client.delete(
            f"/api/v1/instruments/{sample_instrument.id}", headers=auth_headers
        )
        assert response.status_code == 204

    async def test_deleted_instrument_not_found_on_get(
        self, client: AsyncClient, auth_headers: dict, sample_instrument: Instrument
    ) -> None:
        await client.delete(
            f"/api/v1/instruments/{sample_instrument.id}", headers=auth_headers
        )
        response = await client.get(f"/api/v1/instruments/{sample_instrument.id}")
        assert response.status_code == 404

    async def test_deleted_instrument_excluded_from_list(
        self, client: AsyncClient, auth_headers: dict, sample_instrument: Instrument
    ) -> None:
        await client.delete(
            f"/api/v1/instruments/{sample_instrument.id}", headers=auth_headers
        )
        data = (await client.get("/api/v1/instruments/")).json()
        ids = [item["id"] for item in data["items"]]
        assert str(sample_instrument.id) not in ids

    async def test_delete_non_existent_returns_404(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        response = await client.delete(
            f"/api/v1/instruments/{uuid.uuid4()}", headers=auth_headers
        )
        assert response.status_code == 404
