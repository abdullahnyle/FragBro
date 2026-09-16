"""Tests for the FastAPI HTTP layer.

Uses FastAPI's TestClient — runs requests in-process against the app
without spinning up a real server. Each test gets a clean test database
via the existing tmp_db_path fixture and monkeypatches the database
path so api.py reads from the test DB instead of the real one.
"""

import pytest
from fastapi.testclient import TestClient

from fragbro.api import app


@pytest.fixture
def client(tmp_db_path, monkeypatch):
    from fragbro import database
    monkeypatch.setattr(database, "DB_PATH", tmp_db_path)
    with TestClient(app) as test_client:
        yield test_client


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
    assert data["total_wears"] == 12


def test_http_cannot_log_wears(client):
    before = client.get("/wear-stats").json()["total_wears"]
    response = client.post("/wear", json={"name": "Fattan", "rating": 9})
    assert response.status_code == 404
    assert client.get("/wear-stats").json()["total_wears"] == before
    paths = client.get("/openapi.json").json()["paths"]
    assert all(set(operations) == {"get"} for operations in paths.values())


def test_startup_is_repeatable(tmp_path, monkeypatch):
    from fragbro import database
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "fresh.db")
    for _ in range(2):
        with TestClient(app) as client:
            counts = client.get("/stats").json()
            assert counts["fragrances"] == 11
            assert counts["wear_logs"] == 12
            assert counts["collection_entries"] == 4
