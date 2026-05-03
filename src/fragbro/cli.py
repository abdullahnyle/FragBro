"""
FragBro CLI.

Command-line interface for interacting with the FragBro database.
Provides commands to list, search, and inspect fragrances.

Usage:
    fragbro list
    fragbro show <name>
    fragbro stats
"""

import typer
from datetime import date as date_type
from fragbro.database import get_connection, initialize_database
from fragbro.seed import seed_all
from fragbro.seed_personal import seed_personal


app = typer.Typer(
    name="fragbro",
    help="FragBro — fragrance decision assistant CLI.",
    no_args_is_help=True,
)


@app.command()
def init() -> None:
    """Initialize the database (create all tables)."""
    initialize_database()


@app.command()
def seed() -> None:
    """Seed the database with the initial set of fragrances."""
    seed_all()
    
@app.command(name="seed-personal")
def seed_personal_cmd() -> None:
    """Seed the database with the project owner's personal data."""
    seed_personal()


@app.command(name="list")
def list_fragrances() -> None:
    """List all fragrances in the database."""
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT f.id, f.name, f.brand,
               original.name AS dupe_of_name,
               original.brand AS dupe_of_brand
        FROM fragrances f
        LEFT JOIN fragrances original ON f.dupe_of_id = original.id
        ORDER BY f.brand, f.name
        """
    ).fetchall()
    connection.close()

    if not rows:
        typer.echo("No fragrances in the database. Run `fragbro seed` first.")
        return

    typer.echo(f"\n{len(rows)} fragrance(s) in the database:\n")
    for row in rows:
        frag_id, name, brand, dupe_name, dupe_brand = row
        line = f"  [{frag_id}]  {brand} — {name}"
        if dupe_name:
            line += f"   (dupe of {dupe_brand} {dupe_name})"
        typer.echo(line)
    typer.echo("")


@app.command()
def show(name: str = typer.Argument(..., help="Fragrance name to look up.")) -> None:
    """Show full details for a fragrance by name (case-insensitive)."""
    connection = get_connection()

    row = connection.execute(
        """
        SELECT f.id, f.name, f.brand, f.release_year, f.description,
               f.top_notes, f.heart_notes, f.base_notes, f.accords,
               original.name AS dupe_of_name, original.brand AS dupe_of_brand
        FROM fragrances f
        LEFT JOIN fragrances original ON f.dupe_of_id = original.id
        WHERE LOWER(f.name) = LOWER(?)
        """,
        (name,),
    ).fetchone()

    if row is None:
        typer.echo(f"No fragrance found matching '{name}'.")
        connection.close()
        raise typer.Exit(code=1)

    (
        frag_id,
        frag_name,
        brand,
        release_year,
        description,
        top_notes,
        heart_notes,
        base_notes,
        accords,
        dupe_name,
        dupe_brand,
    ) = row

    # Get DNA families for this fragrance
    dna_rows = connection.execute(
        """
        SELECT d.name FROM dna_families d
        JOIN fragrance_dna fd ON fd.dna_family_id = d.id
        WHERE fd.fragrance_id = ?
        """,
        (frag_id,),
    ).fetchall()
    connection.close()

    typer.echo(f"\n{brand} — {frag_name}")
    typer.echo("=" * (len(brand) + len(frag_name) + 3))
    if release_year:
        typer.echo(f"Released: {release_year}")
    if description:
        typer.echo(f"Description: {description}")
    if accords:
        typer.echo(f"Accords: {accords}")
    if top_notes:
        typer.echo(f"Top notes: {top_notes}")
    if heart_notes:
        typer.echo(f"Heart notes: {heart_notes}")
    if base_notes:
        typer.echo(f"Base notes: {base_notes}")
    if dupe_name:
        typer.echo(f"Dupe of: {dupe_brand} {dupe_name}")
    if dna_rows:
        families = ", ".join(r[0] for r in dna_rows)
        typer.echo(f"DNA families: {families}")
    typer.echo("")


@app.command()
def stats() -> None:
    """Show summary statistics about the database."""
    connection = get_connection()

    stats_data = {
        "Fragrances": connection.execute("SELECT COUNT(*) FROM fragrances").fetchone()[0],
        "Users": connection.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "Collection entries": connection.execute("SELECT COUNT(*) FROM collection").fetchone()[0],
        "Wear logs": connection.execute("SELECT COUNT(*) FROM wear_logs").fetchone()[0],
        "Wishlist entries": connection.execute("SELECT COUNT(*) FROM wishlist").fetchone()[0],
        "DNA families": connection.execute("SELECT COUNT(*) FROM dna_families").fetchone()[0],
        "Dupe relationships": connection.execute(
            "SELECT COUNT(*) FROM fragrances WHERE dupe_of_id IS NOT NULL"
        ).fetchone()[0],
    }
    connection.close()

    typer.echo("\nFragBro database stats:")
    typer.echo("-" * 30)
    for key, value in stats_data.items():
        typer.echo(f"  {key:.<24} {value}")
    typer.echo("")

@app.command()
def wear(
    name: str = typer.Argument(..., help="Fragrance name to log a wear for."),
    date: str = typer.Option(
        None,
        "--date",
        "-d",
        help="Wear date in YYYY-MM-DD format. Defaults to today.",
    ),
    occasion: str = typer.Option(
        None, "--occasion", "-o", help="Occasion (e.g. 'uni', 'date night')."
    ),
    weather: str = typer.Option(
        None, "--weather", "-w", help="Weather (e.g. 'warm and humid')."
    ),
    rating: float = typer.Option(
        None, "--rating", "-r", help="Performance rating 0-10 for the day."
    ),
    mood: str = typer.Option(
        None, "--mood", "-m", help="Mood when wearing it."
    ),
) -> None:
    """Log a wear of a fragrance."""
    connection = get_connection()

    # Resolve the user (just one user for now — yourself)
    user_row = connection.execute("SELECT id FROM users LIMIT 1").fetchone()
    if user_row is None:
        typer.echo("No user found. Run `fragbro seed-personal` first.")
        connection.close()
        raise typer.Exit(code=1)
    user_id = user_row[0]

    # Resolve the fragrance by name (case-insensitive)
    frag_row = connection.execute(
        "SELECT id, name, brand FROM fragrances WHERE LOWER(name) = LOWER(?)",
        (name,),
    ).fetchone()
    if frag_row is None:
        typer.echo(f"No fragrance found matching '{name}'.")
        connection.close()
        raise typer.Exit(code=1)
    frag_id, frag_name, frag_brand = frag_row

    # Default to today if no date passed
    wear_date = date if date is not None else date_type.today().isoformat()

    connection.execute(
        """
        INSERT INTO wear_logs
            (user_id, fragrance_id, wear_date, occasion, weather, performance_rating, mood)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, frag_id, wear_date, occasion, weather, rating, mood),
    )
    connection.commit()
    connection.close()

    typer.echo(f"Logged: {frag_brand} — {frag_name} on {wear_date}")


@app.command()
def collection() -> None:
    """Show your fragrance collection with ratings."""
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT f.brand, f.name, c.bottle_size_ml, c.purchase_date,
               c.personal_rating, c.unworn_reason
        FROM collection c
        JOIN fragrances f ON c.fragrance_id = f.id
        ORDER BY c.personal_rating DESC NULLS LAST, f.brand, f.name
        """
    ).fetchall()
    connection.close()

    if not rows:
        typer.echo("Your collection is empty. Run `fragbro seed-personal` to populate it.")
        return

    typer.echo(f"\nYour collection — {len(rows)} fragrance(s):\n")
    for row in rows:
        brand, name, size, purchase, rating, unworn_reason = row
        size_str = f"{size}ml" if size else "?ml"
        rating_str = f"{rating}/10" if rating is not None else "unrated"
        line = f"  {rating_str:>10}   {brand} — {name}  ({size_str})"
        typer.echo(line)
        if unworn_reason:
            typer.echo(f"               note: {unworn_reason}")
    typer.echo("")


@app.command()
def wishlist() -> None:
    """Show your wishlist with notes."""
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT f.brand, f.name, w.added_date, w.notes,
               original.brand AS dupe_of_brand, original.name AS dupe_of_name
        FROM wishlist w
        JOIN fragrances f ON w.fragrance_id = f.id
        LEFT JOIN fragrances original ON f.dupe_of_id = original.id
        ORDER BY w.added_date DESC
        """
    ).fetchall()
    connection.close()

    if not rows:
        typer.echo("Your wishlist is empty.")
        return

    typer.echo(f"\nYour wishlist — {len(rows)} fragrance(s):\n")
    for row in rows:
        brand, name, added, notes, dupe_brand, dupe_name = row
        typer.echo(f"  {brand} — {name}   (added {added})")
        if dupe_name:
            typer.echo(f"      dupe of: {dupe_brand} {dupe_name}")
        if notes:
            typer.echo(f"      note: {notes}")
    typer.echo("")
if __name__ == "__main__":
    app()