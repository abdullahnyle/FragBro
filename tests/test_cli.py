from datetime import date, timedelta

import pytest
from typer.testing import CliRunner

from fragbro import database
from fragbro.cli import app
from fragbro.seed import seed_all
from fragbro.seed_personal import WISHLIST, seed_personal


@pytest.fixture
def seeded_db(tmp_db_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_db_path)
    seed_all()
    seed_personal()
    connection = database.get_connection()
    yield connection
    connection.close()


@pytest.mark.parametrize("options", [
    ["--date", "2026-02-30"],
    ["--date", "20260102"],
    ["--date", (date.today() + timedelta(days=1)).isoformat()],
    ["--rating", "-1"],
    ["--rating", "11"],
    ["--rating", "nan"],
    ["--rating", "inf"],
])
def test_invalid_wear_does_not_write(seeded_db, options):
    before = seeded_db.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0]
    result = CliRunner().invoke(app, ["wear", "Fattan", *options])
    assert result.exit_code == 2, result.output
    assert seeded_db.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0] == before


@pytest.mark.parametrize("rating", ["0", "10"])
def test_wear_stores_valid_rating_boundaries(seeded_db, rating):
    result = CliRunner().invoke(app, [
        "wear", "fattan", "--date", "2026-01-02", "--rating", rating,
        "--occasion", "test",
    ])
    assert result.exit_code == 0, result.output
    row = seeded_db.execute("""
        SELECT f.name, w.wear_date, w.performance_rating, w.occasion
        FROM wear_logs w JOIN fragrances f ON f.id = w.fragrance_id
        ORDER BY w.id DESC LIMIT 1
    """).fetchone()
    assert row == ("Fattan", "2026-01-02", float(rating), "test")


def test_unknown_fragrance_does_not_write(seeded_db):
    before = seeded_db.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0]
    result = CliRunner().invoke(app, ["wear", "not in the catalog"])
    assert result.exit_code == 1
    assert seeded_db.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0] == before


def test_wishlist_prints_each_note(seeded_db):
    result = CliRunner().invoke(app, ["wishlist"])
    assert result.exit_code == 0, result.output
    for name, _, note in WISHLIST:
        assert name in result.output
        assert note in result.output
