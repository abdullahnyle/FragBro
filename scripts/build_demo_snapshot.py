"""Export the seeded public catalog and wear summary for the static demo."""

import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fragbro.database import initialize_database  # noqa: E402
from fragbro.seed import seed_all  # noqa: E402
from fragbro.seed_personal import seed_personal  # noqa: E402


def rows(connection, query):
    return [dict(row) for row in connection.execute(query)]


def main():
    with TemporaryDirectory() as directory:
        db_path = Path(directory) / "fragbro.db"
        initialize_database(db_path)
        seed_all(db_path)
        seed_personal(db_path)

        with closing(sqlite3.connect(db_path)) as connection:
            connection.row_factory = sqlite3.Row
            snapshot = {
                "fragrances": rows(connection, """
                    SELECT f.id, f.name, f.brand, f.release_year, f.accords,
                           original.name AS dupe_of_name,
                           original.brand AS dupe_of_brand
                    FROM fragrances f
                    LEFT JOIN fragrances original ON f.dupe_of_id = original.id
                    ORDER BY f.brand, f.name
                """),
                "stats": {
                    "total_wears": connection.execute(
                        "SELECT COUNT(*) FROM wear_logs"
                    ).fetchone()[0],
                    "most_worn_all_time": rows(connection, """
                        SELECT f.brand, f.name, COUNT(w.id) AS wear_count
                        FROM wear_logs w
                        JOIN fragrances f ON w.fragrance_id = f.id
                        GROUP BY f.id
                        ORDER BY wear_count DESC, f.name ASC
                        LIMIT 5
                    """),
                    "owned_but_unworn": rows(connection, """
                        SELECT f.brand, f.name
                        FROM collection c
                        JOIN fragrances f ON c.fragrance_id = f.id
                        WHERE NOT EXISTS (
                            SELECT 1 FROM wear_logs w
                            WHERE w.fragrance_id = c.fragrance_id
                              AND w.user_id = c.user_id
                        )
                        ORDER BY f.brand, f.name
                    """),
                    "days_since_last_worn": rows(connection, """
                        SELECT f.brand, f.name, MAX(w.wear_date) AS last_worn
                        FROM collection c
                        JOIN fragrances f ON c.fragrance_id = f.id
                        LEFT JOIN wear_logs w ON w.fragrance_id = c.fragrance_id
                                              AND w.user_id = c.user_id
                        GROUP BY f.id
                        HAVING last_worn IS NOT NULL
                        ORDER BY last_worn ASC
                    """),
                },
            }

    output = ROOT / "frontend" / "src" / "demo.json"
    output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(snapshot['fragrances'])} fragrances to {output}")


if __name__ == "__main__":
    main()
