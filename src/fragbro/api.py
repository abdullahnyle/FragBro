"""
FragBro HTTP API.

Exposes FragBro's data over HTTP as a JSON API. Built on FastAPI.
This is the second doorway into FragBro — the CLI is the first; both
talk to the same database layer underneath.

Run the server with:
    uvicorn fragbro.api:app --reload

Then open:
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException

from fragbro.database import get_connection


# Create the FastAPI application.
# `title` and `description` show up on the auto-generated /docs page.
app = FastAPI(
    title="FragBro API",
    description="Fragrance decision assistant — HTTP layer.",
    version="0.1.0",
)


# ---------- Helpers ----------

def row_to_dict(cursor_description, row):
    """
    Convert a sqlite3 row tuple to a dict using the cursor's column names.

    SQLite's default row format is a tuple like ('Fattan', 'Rasasi', 8.0).
    For JSON we want {'name': 'Fattan', 'brand': 'Rasasi', 'rating': 8.0}.
    cursor.description tells us the column names of the last query.
    """
    if row is None:
        return None
    return {col[0]: value for col, value in zip(cursor_description, row)}


# ---------- Endpoints ----------

@app.get("/")
def read_root():
    """Health check / welcome endpoint."""
    return {
        "service": "FragBro API",
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/fragrances")
def list_fragrances():
    """List all fragrances in the catalog, with dupe info if applicable."""
    connection = get_connection()
    cursor = connection.execute(
        """
        SELECT f.id, f.name, f.brand, f.release_year, f.accords,
               original.name AS dupe_of_name,
               original.brand AS dupe_of_brand
        FROM fragrances f
        LEFT JOIN fragrances original ON f.dupe_of_id = original.id
        ORDER BY f.brand, f.name
        """
    )
    rows = cursor.fetchall()
    description = cursor.description
    connection.close()

    return [row_to_dict(description, row) for row in rows]


@app.get("/fragrances/{name}")
def get_fragrance(name: str):
    """Get full details for a single fragrance by name (case-insensitive)."""
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT f.id, f.name, f.brand, f.release_year, f.description,
               f.top_notes, f.heart_notes, f.base_notes, f.accords,
               original.name AS dupe_of_name,
               original.brand AS dupe_of_brand
        FROM fragrances f
        LEFT JOIN fragrances original ON f.dupe_of_id = original.id
        WHERE LOWER(f.name) = LOWER(?)
        """,
        (name,),
    )
    row = cursor.fetchone()
    description = cursor.description

    if row is None:
        connection.close()
        # 404 is HTTP-speak for "not found"
        raise HTTPException(status_code=404, detail=f"Fragrance '{name}' not found.")

    fragrance = row_to_dict(description, row)

    # Also fetch DNA families for this fragrance
    dna_rows = connection.execute(
        """
        SELECT d.name FROM dna_families d
        JOIN fragrance_dna fd ON fd.dna_family_id = d.id
        WHERE fd.fragrance_id = ?
        """,
        (fragrance["id"],),
    ).fetchall()
    connection.close()

    fragrance["dna_families"] = [r[0] for r in dna_rows]
    return fragrance


@app.get("/collection")
def list_collection():
    """List all owned fragrances with personal ratings, sorted by rating."""
    connection = get_connection()
    cursor = connection.execute(
        """
        SELECT f.brand, f.name, c.bottle_size_ml, c.purchase_date,
               c.personal_rating, c.unworn_reason
        FROM collection c
        JOIN fragrances f ON c.fragrance_id = f.id
        ORDER BY c.personal_rating DESC NULLS LAST, f.brand, f.name
        """
    )
    rows = cursor.fetchall()
    description = cursor.description
    connection.close()

    return [row_to_dict(description, row) for row in rows]