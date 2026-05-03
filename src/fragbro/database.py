"""
FragBro database setup.

This module is responsible for creating the SQLite database file
and defining all tables according to the Phase 1 data model spec
(see docs/data_model.md).

Running this file directly will create a fresh database at the
configured path with all 7 tables ready to receive data.
"""

import sqlite3
from pathlib import Path


# Where the database file lives.
# We put it inside the project's data/ folder so it's easy to find
# and so .gitignore can exclude it from the repo.
DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "fragbro.db"


# SQL commands to create each table.
# Each is a separate CREATE TABLE statement. SQLite will execute them in order.
# IF NOT EXISTS means: skip if the table already exists. Safe to run multiple times.

CREATE_FRAGRANCES = """
CREATE TABLE IF NOT EXISTS fragrances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    release_year INTEGER,
    description TEXT,
    top_notes TEXT,
    heart_notes TEXT,
    base_notes TEXT,
    accords TEXT,
    dupe_of_id INTEGER,
    FOREIGN KEY (dupe_of_id) REFERENCES fragrances(id)
);
"""

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_COLLECTION = """
CREATE TABLE IF NOT EXISTS collection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    fragrance_id INTEGER NOT NULL,
    bottle_size_ml INTEGER,
    purchase_date TEXT,
    personal_rating REAL,
    unworn_reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (fragrance_id) REFERENCES fragrances(id)
);
"""

CREATE_WEAR_LOGS = """
CREATE TABLE IF NOT EXISTS wear_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    fragrance_id INTEGER NOT NULL,
    wear_date TEXT NOT NULL,
    occasion TEXT,
    weather TEXT,
    performance_rating REAL,
    mood TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (fragrance_id) REFERENCES fragrances(id)
);
"""

CREATE_WISHLIST = """
CREATE TABLE IF NOT EXISTS wishlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    fragrance_id INTEGER NOT NULL,
    added_date TEXT NOT NULL,
    notes TEXT,
    blind_buy_safe INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (fragrance_id) REFERENCES fragrances(id)
);
"""

CREATE_DNA_FAMILIES = """
CREATE TABLE IF NOT EXISTS dna_families (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    era_peak TEXT
);
"""

CREATE_FRAGRANCE_DNA = """
CREATE TABLE IF NOT EXISTS fragrance_dna (
    fragrance_id INTEGER NOT NULL,
    dna_family_id INTEGER NOT NULL,
    PRIMARY KEY (fragrance_id, dna_family_id),
    FOREIGN KEY (fragrance_id) REFERENCES fragrances(id),
    FOREIGN KEY (dna_family_id) REFERENCES dna_families(id)
);
"""


# Group all CREATE statements so we can run them in one loop.
ALL_CREATE_STATEMENTS = [
    CREATE_FRAGRANCES,
    CREATE_USERS,
    CREATE_COLLECTION,
    CREATE_WEAR_LOGS,
    CREATE_WISHLIST,
    CREATE_DNA_FAMILIES,
    CREATE_FRAGRANCE_DNA,
]


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """
    Open a connection to the FragBro database.

    If db_path is provided, connects to that path instead of the default.
    Useful for tests, which need their own throwaway database.

    Creates parent folders if needed and enables foreign key enforcement.
    """
    target = db_path if db_path is not None else DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(target)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

def initialize_database(db_path: Path | None = None) -> None:
    """
    Create all tables defined in the Phase 1 data model.

    If db_path is provided, initializes that database instead of the default.
    Safe to run multiple times — each CREATE TABLE uses IF NOT EXISTS,
    so existing tables are left untouched.
    """
    target = db_path if db_path is not None else DB_PATH
    print(f"Initializing database at: {target}")

    connection = get_connection(db_path=target)
    cursor = connection.cursor()

    for statement in ALL_CREATE_STATEMENTS:
        cursor.execute(statement)

    connection.commit()
    connection.close()

    print(f"Database ready. {len(ALL_CREATE_STATEMENTS)} tables created or verified.")
    for statement in ALL_CREATE_STATEMENTS:
        cursor.execute(statement)

    connection.commit()
    connection.close()

    print(f"Database ready. {len(ALL_CREATE_STATEMENTS)} tables created or verified.")


if __name__ == "__main__":
    # This block runs only when the file is executed directly,
    # not when imported as a module. Standard Python pattern.
    initialize_database()