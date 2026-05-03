"""
Tests for fragbro.database — schema and basic operations.
"""


# === Schema tests ===
import pytest
def test_all_tables_are_created(tmp_db):
    """The 7 Phase 1 tables should exist after initialization."""
    expected_tables = {
        "fragrances",
        "users",
        "collection",
        "wear_logs",
        "wishlist",
        "dna_families",
        "fragrance_dna",
    }

    rows = tmp_db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    actual_tables = {row[0] for row in rows}

    # The schema may add internal tables (like sqlite_sequence).
    # We only care that all our expected tables are present.
    assert expected_tables.issubset(actual_tables), (
        f"Missing tables: {expected_tables - actual_tables}"
    )


def test_fragrances_columns(tmp_db):
    """The fragrances table should have all expected columns."""
    rows = tmp_db.execute("PRAGMA table_info(fragrances)").fetchall()
    column_names = {row[1] for row in rows}

    expected = {
        "id", "name", "brand", "release_year", "description",
        "top_notes", "heart_notes", "base_notes", "accords", "dupe_of_id",
    }
    assert expected.issubset(column_names), (
        f"Missing columns: {expected - column_names}"
    )


# === Insert / read tests ===

def test_insert_and_read_fragrance(tmp_db):
    """We can insert a fragrance and read it back."""
    tmp_db.execute(
        "INSERT INTO fragrances (name, brand) VALUES (?, ?)",
        ("Test Fragrance", "Test Brand"),
    )
    tmp_db.commit()

    row = tmp_db.execute(
        "SELECT name, brand FROM fragrances WHERE name = ?",
        ("Test Fragrance",),
    ).fetchone()

    assert row == ("Test Fragrance", "Test Brand")


def test_inserted_fragrance_gets_an_id(tmp_db):
    """A newly inserted fragrance should have an auto-assigned id."""
    cursor = tmp_db.execute(
        "INSERT INTO fragrances (name, brand) VALUES (?, ?)",
        ("Auto ID Test", "Test Brand"),
    )
    tmp_db.commit()

    assert cursor.lastrowid is not None
    assert cursor.lastrowid > 0


# === Foreign key tests ===

def test_foreign_key_violation_on_invalid_dupe(tmp_db):
    """Inserting a dupe_of_id pointing to a nonexistent fragrance should fail."""
    import sqlite3

    with pytest.raises(sqlite3.IntegrityError):
        tmp_db.execute(
            "INSERT INTO fragrances (name, brand, dupe_of_id) VALUES (?, ?, ?)",
            ("Bad Dupe", "Test Brand", 999999),  # 999999 doesn't exist
        )
        tmp_db.commit()


def test_foreign_key_works_for_valid_dupe(tmp_db):
    """A valid dupe_of_id should insert successfully."""
    cursor = tmp_db.execute(
        "INSERT INTO fragrances (name, brand) VALUES (?, ?)",
        ("Original", "Brand A"),
    )
    original_id = cursor.lastrowid

    tmp_db.execute(
        "INSERT INTO fragrances (name, brand, dupe_of_id) VALUES (?, ?, ?)",
        ("Dupe", "Brand B", original_id),
    )
    tmp_db.commit()

    row = tmp_db.execute(
        "SELECT name, dupe_of_id FROM fragrances WHERE name = ?",
        ("Dupe",),
    ).fetchone()

    assert row == ("Dupe", original_id)


# === Required-field tests ===

def test_fragrance_name_is_required(tmp_db):
    """Fragrances must have a name."""
    import sqlite3

    with pytest.raises(sqlite3.IntegrityError):
        tmp_db.execute(
            "INSERT INTO fragrances (brand) VALUES (?)",
            ("Brand only — no name",),
        )
        tmp_db.commit()


def test_user_email_must_be_unique(tmp_db):
    """Two users cannot share an email."""
    import sqlite3

    tmp_db.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("user1", "shared@example.com"),
    )
    tmp_db.commit()

    with pytest.raises(sqlite3.IntegrityError):
        tmp_db.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            ("user2", "shared@example.com"),
        )
        tmp_db.commit()


def test_count_wears_per_fragrance(tmp_db):
    """We can count wears grouped by fragrance — basic analytics test."""
    # Insert two fragrances
    cursor1 = tmp_db.execute(
        "INSERT INTO fragrances (name, brand) VALUES (?, ?)", ("A", "Brand X")
    )
    frag_a = cursor1.lastrowid
    cursor2 = tmp_db.execute(
        "INSERT INTO fragrances (name, brand) VALUES (?, ?)", ("B", "Brand Y")
    )
    frag_b = cursor2.lastrowid

    # Insert a user
    cursor3 = tmp_db.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("testuser", "test@example.com"),
    )
    user_id = cursor3.lastrowid

    # Insert 3 wears for A, 1 wear for B
    for _ in range(3):
        tmp_db.execute(
            "INSERT INTO wear_logs (user_id, fragrance_id, wear_date) VALUES (?, ?, ?)",
            (user_id, frag_a, "2026-05-01"),
        )
    tmp_db.execute(
        "INSERT INTO wear_logs (user_id, fragrance_id, wear_date) VALUES (?, ?, ?)",
        (user_id, frag_b, "2026-05-01"),
    )
    tmp_db.commit()

    # Group and count
    rows = tmp_db.execute(
        """
        SELECT f.name, COUNT(w.id) AS wear_count
        FROM wear_logs w
        JOIN fragrances f ON w.fragrance_id = f.id
        GROUP BY f.id
        ORDER BY wear_count DESC
        """
    ).fetchall()

    assert rows == [("A", 3), ("B", 1)]