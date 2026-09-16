from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from fragbro import database
from fragbro.api import app as api
from fragbro.cli import app as cli
from fragbro.seed import seed_all
from fragbro.seed_personal import seed_personal


@pytest.fixture
def wear_history(tmp_db_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_db_path)
    database.initialize_database()
    seed_all()
    seed_personal()
    # Seed before clearing: startup should not reintroduce demo records here.
    with TestClient(api) as client:
        connection = database.get_connection()
        connection.execute("DELETE FROM wear_logs")
        user = connection.execute("SELECT id FROM users").fetchone()[0]
        fragrances = dict(connection.execute("SELECT name, id FROM fragrances"))
        today = date.fromisoformat(connection.execute("SELECT date('now')").fetchone()[0])
        for name, age in [("Fattan", 0), ("Fattan", 29), ("Platinum", 30), ("Khamrah", -1)]:
            connection.execute(
                "INSERT INTO wear_logs (user_id, fragrance_id, wear_date) VALUES (?, ?, ?)",
                (user, fragrances[name], (today - timedelta(days=age)).isoformat()),
            )
        connection.commit()
        yield client, connection, today
        connection.close()


def test_recent_window_excludes_day_31_and_future_dates(wear_history):
    client, _, _ = wear_history
    stats = client.get("/wear-stats").json()
    assert stats["total_wears"] == 4
    assert stats["most_worn_last_30_days"] == [
        {"brand": "Rasasi", "name": "Fattan", "wear_count": 2},
    ]
    result = CliRunner().invoke(cli, ["wear-stats"])
    assert result.exit_code == 0, result.output
    recent = result.output.split("--- Most worn (last 30 days) ---")[1].split("---")[0]
    assert "2x" in recent and "Fattan" in recent
    assert "Platinum" not in recent and "Khamrah" not in recent


def test_unworn_and_elapsed_days_follow_logs_not_ratings(wear_history):
    client, _, today = wear_history
    stats = client.get("/wear-stats").json()
    assert stats["owned_but_unworn"] == [{"brand": "French Avenue", "name": "Liquid Brun"}]
    assert stats["most_worn_all_time"][0]["name"] == "Fattan"
    days = {row["name"]: row for row in stats["days_since_last_worn"]}
    assert days["Fattan"]["days_ago"] == 0
    assert days["Fattan"]["last_worn"] == today.isoformat()
    assert days["Platinum"]["days_ago"] == 30
    assert "Liquid Brun" not in days


def test_empty_history_keeps_owned_bottles_visible(wear_history):
    client, connection, _ = wear_history
    connection.execute("DELETE FROM wear_logs")
    connection.commit()
    stats = client.get("/wear-stats").json()
    assert stats["total_wears"] == 0
    assert stats["most_worn_all_time"] == []
    assert stats["most_worn_last_30_days"] == []
    assert stats["days_since_last_worn"] == []
    assert len(stats["owned_but_unworn"]) == 4
    result = CliRunner().invoke(cli, ["wear-stats"])
    assert result.exit_code == 0, result.output
    for bottle in stats["owned_but_unworn"]:
        assert bottle["name"] in result.output
