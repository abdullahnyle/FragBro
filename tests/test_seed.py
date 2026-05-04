"""Tests for catalog and personal data seeding.

These tests verify that running the seed functions actually populates
the database with the expected entities, that re-running them is safe
(idempotent), and that key relationships (dupes, DNA links, FKs) are
intact afterward.
"""

import sqlite3

from fragbro.seed import seed_all
from fragbro.seed_personal import seed_personal


# ---------- Catalog seed (seed_all) ----------

def test_seed_all_creates_fragrances(tmp_db_path):
    seed_all(db_path=tmp_db_path)

    conn = sqlite3.connect(tmp_db_path)
    count = conn.execute("SELECT COUNT(*) FROM fragrances").fetchone()[0]
    conn.close()

    assert count == 7, f"Expected 7 catalog fragrances, got {count}"


def test_seed_all_creates_dupe_relationships(tmp_db_path):
    seed_all(db_path=tmp_db_path)

    conn = sqlite3.connect(tmp_db_path)
    dupes = conn.execute(
        "SELECT COUNT(*) FROM fragrances WHERE dupe_of_id IS NOT NULL"
    ).fetchone()[0]
    conn.close()

    assert dupes == 2, f"Expected 2 dupe links (Kaaf, Liquid Brun), got {dupes}"


def test_seed_all_links_dna_family(tmp_db_path):
    seed_all(db_path=tmp_db_path)

    conn = sqlite3.connect(tmp_db_path)
    family_links = conn.execute("SELECT COUNT(*) FROM fragrance_dna").fetchone()[0]
    families = conn.execute("SELECT COUNT(*) FROM dna_families").fetchone()[0]
    conn.close()

    assert families == 1, "Expected 1 DNA family seeded (Barber Shop / Fougère)"
    assert family_links == 1, "Expected Fattan to be linked to its DNA family"


def test_seed_all_is_idempotent(tmp_db_path):
    seed_all(db_path=tmp_db_path)
    seed_all(db_path=tmp_db_path)  # second run should not duplicate

    conn = sqlite3.connect(tmp_db_path)
    fragrances = conn.execute("SELECT COUNT(*) FROM fragrances").fetchone()[0]
    families = conn.execute("SELECT COUNT(*) FROM dna_families").fetchone()[0]
    links = conn.execute("SELECT COUNT(*) FROM fragrance_dna").fetchone()[0]
    conn.close()

    assert fragrances == 7, f"Re-running seed_all inflated fragrance count to {fragrances}"
    assert families == 1, f"Re-running seed_all inflated families to {families}"
    assert links == 1, f"Re-running seed_all inflated DNA links to {links}"


# ---------- Personal seed (seed_personal) ----------

def test_seed_personal_creates_user(tmp_db_path):
    seed_all(db_path=tmp_db_path)
    seed_personal(db_path=tmp_db_path)

    conn = sqlite3.connect(tmp_db_path)
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    username = conn.execute("SELECT username FROM users LIMIT 1").fetchone()[0]
    conn.close()

    assert user_count == 1
    assert username == "abdullah"


def test_seed_personal_populates_collection_and_wishlist(tmp_db_path):
    seed_all(db_path=tmp_db_path)
    seed_personal(db_path=tmp_db_path)

    conn = sqlite3.connect(tmp_db_path)
    collection = conn.execute("SELECT COUNT(*) FROM collection").fetchone()[0]
    wishlist = conn.execute("SELECT COUNT(*) FROM wishlist").fetchone()[0]
    wears = conn.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0]
    conn.close()

    assert collection == 4, f"Expected 4 collection entries, got {collection}"
    assert wishlist == 3, f"Expected 3 wishlist entries, got {wishlist}"
    assert wears == 4, f"Expected 4 wear logs, got {wears}"


def test_seed_personal_adds_extra_catalog(tmp_db_path):
    """Personal seed should add 4 extra fragrances (originals + dupes for wishlist)."""
    seed_all(db_path=tmp_db_path)
    seed_personal(db_path=tmp_db_path)

    conn = sqlite3.connect(tmp_db_path)
    total_fragrances = conn.execute("SELECT COUNT(*) FROM fragrances").fetchone()[0]
    conn.close()

    # 7 from seed_all + 4 from seed_personal extras = 11
    assert total_fragrances == 11


def test_seed_personal_is_idempotent(tmp_db_path):
    seed_all(db_path=tmp_db_path)
    seed_personal(db_path=tmp_db_path)
    seed_personal(db_path=tmp_db_path)  # second run

    conn = sqlite3.connect(tmp_db_path)
    users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    collection = conn.execute("SELECT COUNT(*) FROM collection").fetchone()[0]
    wishlist = conn.execute("SELECT COUNT(*) FROM wishlist").fetchone()[0]
    wears = conn.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0]
    conn.close()

    assert users == 1, "Second personal seed run created duplicate user"
    assert collection == 4, "Second personal seed inflated collection"
    assert wishlist == 3, "Second personal seed inflated wishlist"
    assert wears == 4, "Second personal seed inflated wear logs"