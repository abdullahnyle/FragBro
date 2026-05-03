"""
FragBro seed data.

Populates the database with the 5 real fragrances we used to validate
the Phase 1 data model, plus their dependencies (originals being cloned,
DNA families, etc.).

Running this file directly will insert the seed data into an
already-initialized database. Safe to run multiple times — uses
INSERT OR IGNORE so duplicates won't be inserted.
"""

from fragbro.database import get_connection


# DNA families to seed.
# Each row: (name, description, era_peak)
DNA_FAMILIES = [
    (
        "Barber Shop / Fougère",
        "Spicy lavender + fresh aromatics. Classic men's grooming DNA — Brut, Azzaro Pour Homme, Drakkar Noir.",
        "1970s–1990s",
    ),
]


# Fragrances to seed. Order matters here:
# we insert "originals" (PDM Althair, PDM Percival) BEFORE the dupes
# that reference them, because the dupe_of_id is a foreign key.
#
# Each row is a dict — easier to read than a tuple when there are many fields.
FRAGRANCES = [
    {
        "name": "Althair",
        "brand": "Parfums de Marly",
        "release_year": 2020,
        "description": None,
        "top_notes": "Bergamot, almond",
        "heart_notes": "Tonka bean, vanilla",
        "base_notes": "Sandalwood, amber",
        "accords": "Sweet, gourmand, woody",
        "dupe_of_id": None,
    },
    {
        "name": "Percival",
        "brand": "Parfums de Marly",
        "release_year": 2018,
        "description": None,
        "top_notes": "Bergamot, juniper, cardamom",
        "heart_notes": "Lavender, geranium",
        "base_notes": "Musk, ambergris",
        "accords": "Fresh, clean, aromatic",
        "dupe_of_id": None,
    },
    {
        "name": "Platinum",
        "brand": "J. Janan",
        "release_year": None,
        "description": "Clean, simple, soapy daily wear.",
        "top_notes": None,
        "heart_notes": None,
        "base_notes": None,
        "accords": "Clean, soapy, fresh",
        "dupe_of_id": None,
    },
    {
        "name": "Khamrah",
        "brand": "Lattafa",
        "release_year": 2022,
        "description": "Warm, spicy gourmand.",
        "top_notes": "Cinnamon, nutmeg",
        "heart_notes": "Mahanad, praline",
        "base_notes": "Vanilla, tonka, benzoin",
        "accords": "Sweet, spicy, warm",
        "dupe_of_id": None,
    },
    {
        "name": "Kaaf",
        "brand": "Ahmed Al Maghribi",
        "release_year": None,
        "description": "Clean DNA — clone of PDM Percival.",
        "top_notes": None,
        "heart_notes": None,
        "base_notes": None,
        "accords": "Fresh, clean, aromatic",
        "dupe_of_id": None,  # set after insert — see resolve_dupe_links()
    },
    {
        "name": "Liquid Brun",
        "brand": "French Avenue",
        "release_year": None,
        "description": "Near-perfect dupe of PDM Althair.",
        "top_notes": None,
        "heart_notes": None,
        "base_notes": None,
        "accords": "Sweet, gourmand, woody",
        "dupe_of_id": None,  # set after insert — see resolve_dupe_links()
    },
    {
        "name": "Fattan",
        "brand": "Rasasi",
        "release_year": None,
        "description": "Classic Brut DNA — spicy, lavender, fresh. Once-famous barber-shop scent.",
        "top_notes": "Lavender, bergamot",
        "heart_notes": "Spices, geranium",
        "base_notes": "Musk, woods",
        "accords": "Spicy, fresh, aromatic",
        "dupe_of_id": None,
    },
]


# Maps fragrance NAME -> NAME of the fragrance it dupes.
# Resolved at insert time once both rows exist.
DUPE_RELATIONSHIPS = {
    "Kaaf": "Percival",
    "Liquid Brun": "Althair",
}


# Maps fragrance NAME -> list of DNA family NAMES it belongs to.
DNA_LINKS = {
    "Fattan": ["Barber Shop / Fougère"],
}


def insert_dna_families(connection) -> None:
    """Insert all DNA families. Skips duplicates."""
    for name, description, era_peak in DNA_FAMILIES:
        connection.execute(
            "INSERT OR IGNORE INTO dna_families (name, description, era_peak) VALUES (?, ?, ?)",
            (name, description, era_peak),
        )
    print(f"Seeded {len(DNA_FAMILIES)} DNA family/families.")


def insert_fragrances(connection) -> None:
    """Insert all fragrances. Skips duplicates by (name, brand)."""
    inserted_count = 0
    for frag in FRAGRANCES:
        # Check if this fragrance already exists by (name, brand)
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
                frag["name"],
                frag["brand"],
                frag["release_year"],
                frag["description"],
                frag["top_notes"],
                frag["heart_notes"],
                frag["base_notes"],
                frag["accords"],
                frag["dupe_of_id"],
            ),
        )
        inserted_count += 1
    print(f"Inserted {inserted_count} new fragrance(s).")


def resolve_dupe_links(connection) -> None:
    """
    Set dupe_of_id for each dupe fragrance to the id of its original.
    Done in a second pass so foreign keys can be resolved by name.
    """
    for dupe_name, original_name in DUPE_RELATIONSHIPS.items():
        original = connection.execute(
            "SELECT id FROM fragrances WHERE name = ?", (original_name,)
        ).fetchone()
        if original is None:
            print(f"  WARNING: original '{original_name}' not found, skipping.")
            continue

        original_id = original[0]

        connection.execute(
            "UPDATE fragrances SET dupe_of_id = ? WHERE name = ? AND dupe_of_id IS NULL",
            (original_id, dupe_name),
        )
    print(f"Linked {len(DUPE_RELATIONSHIPS)} dupe relationship(s).")


def link_fragrance_dna(connection) -> None:
    """Link fragrances to their DNA families via the fragrance_dna table."""
    link_count = 0
    for frag_name, family_names in DNA_LINKS.items():
        frag = connection.execute(
            "SELECT id FROM fragrances WHERE name = ?", (frag_name,)
        ).fetchone()
        if frag is None:
            continue
        frag_id = frag[0]

        for family_name in family_names:
            family = connection.execute(
                "SELECT id FROM dna_families WHERE name = ?", (family_name,)
            ).fetchone()
            if family is None:
                continue
            family_id = family[0]

            connection.execute(
                "INSERT OR IGNORE INTO fragrance_dna (fragrance_id, dna_family_id) VALUES (?, ?)",
                (frag_id, family_id),
            )
            link_count += 1
    print(f"Linked {link_count} fragrance/DNA pair(s).")


def seed_all() -> None:
    """Run all seed steps in order."""
    connection = get_connection()

    insert_dna_families(connection)
    insert_fragrances(connection)
    resolve_dupe_links(connection)
    link_fragrance_dna(connection)

    connection.commit()
    connection.close()
    print("Seed complete.")


if __name__ == "__main__":
    seed_all()