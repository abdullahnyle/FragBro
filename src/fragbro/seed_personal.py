"""
FragBro personal seed.

Seeds the database with the project owner's personal data:
- The owner as the first user
- Their real fragrance collection
- Recent wear logs
- Their wishlist
- Catalog additions needed to support the wishlist

Separate from seed.py because catalog data is shared (everyone using
FragBro sees the same fragrances) while personal data is per-user.
This pattern scales naturally to multi-user when we get there.
"""

from fragbro.database import get_connection


# === User ===

USER = {
    "username": "abdullah",
    "email": "abdullahnyle@icloud.com",
}


# === Catalog additions ===
# These fragrances need to exist before we can wishlist their dupes.
# Originals first, then their dupes.

EXTRA_CATALOG = [
    {
        "name": "Imagination",
        "brand": "Louis Vuitton",
        "release_year": 2021,
        "description": None,
        "top_notes": "Mandarin, lemon, ginger",
        "heart_notes": "Black tea, saffron",
        "base_notes": "Cedar, ambrox, woody amber",
        "accords": "Citrus, woody, aromatic",
        "dupe_of_id": None,
    },
    {
        "name": "Virgin Island Water",
        "brand": "Creed",
        "release_year": 2007,
        "description": None,
        "top_notes": "Lime, coconut, mandarin",
        "heart_notes": "White rum, hibiscus",
        "base_notes": "Sugar cane, musk, white musk",
        "accords": "Tropical, citrus, fresh",
        "dupe_of_id": None,
    },
    {
        "name": "Marwa",
        "brand": "Arabiyat Prestige",
        "release_year": None,
        "description": "Dupe of LV Imagination — closer to the original than J. Janan Platinum.",
        "top_notes": None,
        "heart_notes": None,
        "base_notes": None,
        "accords": "Citrus, woody, aromatic",
        "dupe_of_id": None,  # set below
    },
    {
        "name": "Aquatica",
        "brand": "Rayhaan",
        "release_year": None,
        "description": "Near-perfect dupe of the old-formula Creed Virgin Island Water (blue bottle).",
        "top_notes": None,
        "heart_notes": None,
        "base_notes": None,
        "accords": "Tropical, citrus, fresh",
        "dupe_of_id": None,  # set below
    },
]

EXTRA_DUPE_LINKS = {
    "Marwa": "Imagination",
    "Aquatica": "Virgin Island Water",
}


# === Collection ===
# The user's owned fragrances.
# (fragrance_name, bottle_size_ml, purchase_date, personal_rating, unworn_reason)

COLLECTION = [
    ("Platinum", 100, "2026-03-01", 8.0, None),
    ("Khamrah", 100, "2025-11-01", 6.0, "Outshone by Qahwa — same lane, less headache-inducing."),
    ("Liquid Brun", 100, "2025-12-01", 9.5, None),
    ("Fattan", 50, "2025-04-01", 8.0, None),
]


# === Wear logs ===
# Recent wears.
# (fragrance_name, wear_date, occasion, weather, performance_rating, mood)

WEAR_LOGS = [
    ("Platinum", "2026-04-27", "uni", None, None, None),
    ("Khamrah", "2025-12-30", "evening out", "cool", None, None),
    ("Liquid Brun", "2025-03-10", "casual", None, None, None),
    ("Fattan", "2026-04-02", "casual", None, None, None),
]


# === Wishlist ===
# (fragrance_name, added_date, notes)

WISHLIST = [
    ("Kaaf", "2026-05-03", "Want as a clone of PDM Percival — clean DNA staple."),
    ("Marwa", "2026-05-03", "Closer dupe of LV Imagination than Platinum."),
    ("Aquatica", "2026-05-03", "Gets me 90% of Creed Virgin Island Water at a fraction."),
]


# === Helper functions ===

def get_or_insert_user(connection) -> int:
    """Return the user's id, inserting them if they don't exist."""
    existing = connection.execute(
        "SELECT id FROM users WHERE username = ?", (USER["username"],)
    ).fetchone()
    if existing:
        return existing[0]

    cursor = connection.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (USER["username"], USER["email"]),
    )
    print(f"Created user: {USER['username']}")
    return cursor.lastrowid


def get_fragrance_id(connection, name: str) -> int | None:
    """Return the id of a fragrance by name, or None if not found."""
    row = connection.execute(
        "SELECT id FROM fragrances WHERE name = ?", (name,)
    ).fetchone()
    return row[0] if row else None


def insert_extra_catalog(connection) -> None:
    """Insert the extra catalog fragrances (originals + dupes for the wishlist)."""
    inserted = 0
    for frag in EXTRA_CATALOG:
        existing = connection.execute(
            "SELECT id FROM fragrances WHERE name = ? AND brand = ?",
            (frag["name"], frag["brand"]),
        ).fetchone()
        if existing:
            continue

        connection.execute(
            """
            INSERT INTO fragrances
                (name, brand, release_year, description,
                 top_notes, heart_notes, base_notes, accords, dupe_of_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                frag["name"], frag["brand"], frag["release_year"],
                frag["description"], frag["top_notes"], frag["heart_notes"],
                frag["base_notes"], frag["accords"], frag["dupe_of_id"],
            ),
        )
        inserted += 1
    print(f"Inserted {inserted} extra catalog fragrance(s).")


def resolve_extra_dupe_links(connection) -> None:
    """Link Marwa → Imagination and Aquatica → Virgin Island Water."""
    for dupe_name, original_name in EXTRA_DUPE_LINKS.items():
        original_id = get_fragrance_id(connection, original_name)
        if original_id is None:
            print(f"  WARNING: original '{original_name}' not found.")
            continue
        connection.execute(
            "UPDATE fragrances SET dupe_of_id = ? WHERE name = ? AND dupe_of_id IS NULL",
            (original_id, dupe_name),
        )
    print(f"Linked {len(EXTRA_DUPE_LINKS)} extra dupe relationship(s).")


def insert_collection(connection, user_id: int) -> None:
    """Insert the user's owned fragrances."""
    inserted = 0
    for name, size, purchase_date, rating, unworn_reason in COLLECTION:
        frag_id = get_fragrance_id(connection, name)
        if frag_id is None:
            print(f"  WARNING: fragrance '{name}' not found, skipping.")
            continue

        existing = connection.execute(
            "SELECT id FROM collection WHERE user_id = ? AND fragrance_id = ?",
            (user_id, frag_id),
        ).fetchone()
        if existing:
            continue

        connection.execute(
            """
            INSERT INTO collection
                (user_id, fragrance_id, bottle_size_ml, purchase_date,
                 personal_rating, unworn_reason)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, frag_id, size, purchase_date, rating, unworn_reason),
        )
        inserted += 1
    print(f"Added {inserted} fragrance(s) to collection.")


def insert_wear_logs(connection, user_id: int) -> None:
    """Insert recent wear logs."""
    inserted = 0
    for name, wear_date, occasion, weather, performance, mood in WEAR_LOGS:
        frag_id = get_fragrance_id(connection, name)
        if frag_id is None:
            continue

        # Skip exact duplicates (same user, fragrance, date)
        existing = connection.execute(
            """
            SELECT id FROM wear_logs
            WHERE user_id = ? AND fragrance_id = ? AND wear_date = ?
            """,
            (user_id, frag_id, wear_date),
        ).fetchone()
        if existing:
            continue

        connection.execute(
            """
            INSERT INTO wear_logs
                (user_id, fragrance_id, wear_date, occasion,
                 weather, performance_rating, mood)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, frag_id, wear_date, occasion, weather, performance, mood),
        )
        inserted += 1
    print(f"Added {inserted} wear log(s).")


def insert_wishlist(connection, user_id: int) -> None:
    """Insert wishlist entries."""
    inserted = 0
    for name, added_date, notes in WISHLIST:
        frag_id = get_fragrance_id(connection, name)
        if frag_id is None:
            print(f"  WARNING: wishlist fragrance '{name}' not found, skipping.")
            continue

        existing = connection.execute(
            "SELECT id FROM wishlist WHERE user_id = ? AND fragrance_id = ?",
            (user_id, frag_id),
        ).fetchone()
        if existing:
            continue

        connection.execute(
            "INSERT INTO wishlist (user_id, fragrance_id, added_date, notes) VALUES (?, ?, ?, ?)",
            (user_id, frag_id, added_date, notes),
        )
        inserted += 1
    print(f"Added {inserted} wishlist entry/entries.")


def seed_personal() -> None:
    """Run all personal seed steps."""
    connection = get_connection()

    # Catalog must exist before we can reference fragrances by id
    insert_extra_catalog(connection)
    resolve_extra_dupe_links(connection)

    user_id = get_or_insert_user(connection)
    insert_collection(connection, user_id)
    insert_wear_logs(connection, user_id)
    insert_wishlist(connection, user_id)

    connection.commit()
    connection.close()
    print("Personal seed complete.")


if __name__ == "__main__":
    seed_personal()