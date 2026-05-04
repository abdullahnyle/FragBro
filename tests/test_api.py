"""Tests for the FastAPI HTTP layer.

Uses FastAPI's TestClient — runs requests in-process against the app
without spinning up a real server. Each test gets a clean test database
via the existing tmp_db_path fixture and monkeypatches the database
path so api.py reads from the test DB instead of the real one.
"""

import pytest
from fastapi.testclient import TestClient

from fragbro import api as api_module
from fragbro.api import app
from fragbro.seed import seed_all
from fragbro.seed_personal import seed_personal


@pytest.fixture
def client(tmp_db_path, monkeypatch):
    """A TestClient with a freshly seeded test database."""
    seed_all(db_path=tmp_db_path)
    seed_personal(db_path=tmp_db_path)

    # Force api.py's database calls to use the test DB.
    # We do this by monkeypatching the get_connection function
    # that api.py imports.
    from fragbro import database as db_module
    original_get_connection = db_module.get_connection

    def get_test_connection(db_path=None):
        return original_get_connection(db_path=tmp_db_path)

    monkeypatch.setattr(api_module, "get_connection", get_test_connection)

    return TestClient(app)


# ---------- Read endpoints ----------

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_fragrances(client):
    response = client.get("/fragrances")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 11  # 7 catalog + 4 from personal extras


def test_get_fragrance_found(client):
    response = client.get("/fragrances/Fattan")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Fattan"
    assert data["brand"] == "Rasasi"
    assert "Barber Shop / Fougère" in data["dna_families"]


def test_get_fragrance_case_insensitive(client):
    response = client.get("/fragrances/fattan")
    assert response.status_code == 200
    assert response.json()["name"] == "Fattan"


def test_get_fragrance_not_found(client):
    response = client.get("/fragrances/NotARealFragrance")
    assert response.status_code == 404


def test_collection(client):
    response = client.get("/collection")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_wishlist(client):
    response = client.get("/wishlist")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_stats(client):
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["fragrances"] == 11
    assert data["users"] == 1
    assert data["collection_entries"] == 4


def test_wear_stats_shape(client):
    response = client.get("/wear-stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_wears" in data
    assert "most_worn_all_time" in data
    assert "owned_but_unworn" in data
    assert data["total_wears"] == 4


# ---------- Write endpoint ----------

def test_post_wear_success(client):
    response = client.post(
        "/wear",
        json={"name": "Fattan", "occasion": "test", "rating": 9.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["fragrance"]["name"] == "Fattan"
    assert data["occasion"] == "test"

    # Verify it was actually persisted by checking stats
    stats = client.get("/wear-stats").json()
    assert stats["total_wears"] == 5  # was 4, now 5


def test_post_wear_unknown_fragrance(client):
    response = client.post("/wear", json={"name": "NotARealFragrance"})
    assert response.status_code == 404


def test_post_wear_missing_name(client):
    response = client.post("/wear", json={"occasion": "test"})
    # Pydantic returns 422 for validation errors, not 400
    assert response.status_code == 422