"""
Pytest fixtures for FragBro tests.

The `tmp_db` fixture creates a fresh SQLite database in a temporary
directory, runs the schema setup on it, and yields an open connection
to the test. The connection is closed after the test ends.

This guarantees test isolation: each test runs against a clean
database, and tests never touch the real data/fragbro.db file.
"""

from pathlib import Path

import pytest

from fragbro.database import ALL_CREATE_STATEMENTS, get_connection


@pytest.fixture
def tmp_db(tmp_path: Path):
    """
    Create a fresh test database, set up the schema, and yield the connection.
    """
    db_file = tmp_path / "test_fragbro.db"
    connection = get_connection(db_path=db_file)

    # Run schema setup directly on this connection so it stays open for the test
    for statement in ALL_CREATE_STATEMENTS:
        connection.execute(statement)
    connection.commit()

    yield connection

    connection.close()