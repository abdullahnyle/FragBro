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

from datetime import date as date_type

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fragbro.database import get_connection


# Create the FastAPI application.
# `title` and `description` show up on the auto-generated /docs page.
app = FastAPI(
    title="FragBro API",
    description="Fragrance decision assistant — HTTP layer.",
    version="0.1.0",
)

# CORS — allow browser frontends running on localhost to call this API.
# Tighten this for production; permissive for dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Helpers ----------

def row_to_dict(cursor_description, row) -> dict:
    """
    Convert a sqlite3 row tuple to a dict using the cursor's column names.

    SQLite's default row format is a tuple like ('Fattan', 'Rasasi', 8.0).
    For JSON we want {'name': 'Fattan', 'brand': 'Rasasi', 'rating': 8.0}.
    cursor.description tells us the column names of the last query.

    Caller must ensure `row` is not None.
    """
    return {col[0]: value for col, value in zip(cursor_description, row)}


# ---------- Request models (validate incoming data) ----------

class WearLogRequest(BaseModel):
    """Schema for a POST /wear request body.

    Pydantic auto-validates incoming JSON against this. Required fields
    must be present; optional fields default to None.
    """
    name: str
    date: str | None = None
    occasion: str | None = None
    weather: str | None = None
    rating: float | None = None
    mood: str | None = None


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
        raise HTTPException(status_code=404, detail=f"Fragrance '{name}' not found.")

    fragrance = row_to_dict(description, row)

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


@app.get("/wishlist")
def list_wishlist():
    """List wishlist entries with dupe relationships and notes."""
    connection = get_connection()
    cursor = connection.execute(
        """
        SELECT f.brand, f.name, w.added_date, w.notes,
               original.brand AS dupe_of_brand,
               original.name  AS dupe_of_name
        FROM wishlist w
        JOIN fragrances f ON w.fragrance_id = f.id
        LEFT JOIN fragrances original ON f.dupe_of_id = original.id
        ORDER BY w.added_date DESC
        """
    )
    rows = cursor.fetchall()
    description = cursor.description
    connection.close()

    return [row_to_dict(description, row) for row in rows]


@app.get("/wear-stats")
def get_wear_stats():
    """Wearing analytics: most worn (all-time + 30d), unworn, days-since."""
    connection = get_connection()

    total = connection.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0]

    most_worn = connection.execute(
        """
        SELECT f.brand, f.name, COUNT(w.id) AS wear_count
        FROM wear_logs w
        JOIN fragrances f ON w.fragrance_id = f.id
        GROUP BY f.id
        ORDER BY wear_count DESC, f.name ASC
        LIMIT 5
        """
    ).fetchall()

    most_worn_30d = connection.execute(
        """
        SELECT f.brand, f.name, COUNT(w.id) AS wear_count
        FROM wear_logs w
        JOIN fragrances f ON w.fragrance_id = f.id
        WHERE w.wear_date >= date('now', '-30 days')
        GROUP BY f.id
        ORDER BY wear_count DESC, f.name ASC
        LIMIT 5
        """
    ).fetchall()

    unworn = connection.execute(
        """
        SELECT f.brand, f.name
        FROM collection c
        JOIN fragrances f ON c.fragrance_id = f.id
        WHERE NOT EXISTS (
            SELECT 1 FROM wear_logs w
            WHERE w.fragrance_id = c.fragrance_id
              AND w.user_id = c.user_id
        )
        ORDER BY f.brand, f.name
        """
    ).fetchall()

    days_since = connection.execute(
        """
        SELECT f.brand, f.name,
               MAX(w.wear_date) AS last_worn,
               CAST(julianday('now') - julianday(MAX(w.wear_date)) AS INTEGER) AS days_ago
        FROM collection c
        JOIN fragrances f ON c.fragrance_id = f.id
        LEFT JOIN wear_logs w ON w.fragrance_id = c.fragrance_id
                              AND w.user_id = c.user_id
        GROUP BY f.id
        HAVING last_worn IS NOT NULL
        ORDER BY days_ago DESC
        """
    ).fetchall()

    connection.close()

    return {
        "total_wears": total,
        "most_worn_all_time": [
            {"brand": b, "name": n, "wear_count": c} for b, n, c in most_worn
        ],
        "most_worn_last_30_days": [
            {"brand": b, "name": n, "wear_count": c} for b, n, c in most_worn_30d
        ],
        "owned_but_unworn": [
            {"brand": b, "name": n} for b, n in unworn
        ],
        "days_since_last_worn": [
            {"brand": b, "name": n, "last_worn": lw, "days_ago": d}
            for b, n, lw, d in days_since
        ],
    }


@app.get("/stats")
def get_stats():
    """Database summary stats — same as `fragbro stats` CLI command."""
    connection = get_connection()
    stats_data = {
        "fragrances": connection.execute("SELECT COUNT(*) FROM fragrances").fetchone()[0],
        "users": connection.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "collection_entries": connection.execute("SELECT COUNT(*) FROM collection").fetchone()[0],
        "wear_logs": connection.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0],
        "wishlist_entries": connection.execute("SELECT COUNT(*) FROM wishlist").fetchone()[0],
        "dna_families": connection.execute("SELECT COUNT(*) FROM dna_families").fetchone()[0],
        "dupe_relationships": connection.execute(
            "SELECT COUNT(*) FROM fragrances WHERE dupe_of_id IS NOT NULL"
        ).fetchone()[0],
    }
    connection.close()
    return stats_data


@app.post("/wear", status_code=201)
def log_wear(payload: WearLogRequest):
    """Log a wear of a fragrance. Returns the created wear log entry.

    Response: 201 Created with the new entry.
    Errors:   404 if the fragrance name doesn't exist.
              400 if no user has been seeded yet.
    """
    connection = get_connection()

    user_row = connection.execute("SELECT id FROM users LIMIT 1").fetchone()
    if user_row is None:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="No user seeded. Run `fragbro seed-personal` first.",
        )
    user_id = user_row[0]

    frag_row = connection.execute(
        "SELECT id, name, brand FROM fragrances WHERE LOWER(name) = LOWER(?)",
        (payload.name,),
    ).fetchone()
    if frag_row is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail=f"Fragrance '{payload.name}' not found.",
        )
    frag_id, frag_name, frag_brand = frag_row

    wear_date = payload.date if payload.date is not None else date_type.today().isoformat()

    cursor = connection.execute(
        """
        INSERT INTO wear_logs
            (user_id, fragrance_id, wear_date, occasion, weather, performance_rating, mood)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, frag_id, wear_date, payload.occasion, payload.weather,
         payload.rating, payload.mood),
    )
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return {
        "id": new_id,
        "fragrance": {"brand": frag_brand, "name": frag_name},
        "wear_date": wear_date,
        "occasion": payload.occasion,
        "weather": payload.weather,
        "rating": payload.rating,
        "mood": payload.mood,
    }