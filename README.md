# FragBro

I built FragBro around my interest in fragrances. It keeps track of what I own, what I want to try and what I actually wear.

The app has a React frontend, a FastAPI backend and a SQLite database. It started as a command-line tool, and the CLI still works alongside the web app.

## What it does

- Browse the fragrance catalog with names, brands and scent accords.
- Keep collection ratings, wishlist notes and links between dupes and their originals in the database.
- Log wears locally through the CLI, including the date, occasion, weather and rating (0–10).
- Show wear counts, most-worn fragrances and how long owned bottles have gone untouched.

The React view shows the catalog and wear statistics. Collection details and wishlist entries are available through the API and CLI. The HTTP API is read-only; wear logging stays in the local CLI.

The database has seven tables. Fragrances link to scent families through a join table, and `dupe_of_id` links a fragrance to another entry in the catalog. The seed files contain a small catalog and records from my own collection.

Recommendations were part of the original idea. The current version focuses on collection tracking and wear statistics; it does not include a questionnaire or semantic search.

[Frontend deployment](https://fragbro.vercel.app)

## Run locally

Use Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS or Linux, or `.venv\Scripts\Activate.ps1` in Windows PowerShell. Then:

```bash
python -m pip install -e ".[dev]"
uvicorn fragbro.api:app --reload
```

Startup creates `data/fragbro.db` if needed and loads the seed records. Open `http://127.0.0.1:8000/docs` to explore the API. Follow the [frontend instructions](frontend/README.md) to start React in a second terminal.

The CLI uses the same database:

```bash
fragbro list
fragbro collection
fragbro wishlist
fragbro wear "Fattan" --occasion uni
fragbro wear-stats
```

The API and CLI use one seeded user. Account registration and authentication are not implemented. The demo has no HTTP write endpoints; CORS allows public reads and is not an authentication mechanism.

## Tests and source

Run `python -m pytest` from the root. Tests cover the database schema, repeated startup/seeding, API responses, blocked HTTP writes and CLI validation, using temporary SQLite files.

- [src/fragbro](src/fragbro) contains the database, API, CLI and seed scripts.
- [frontend](frontend) contains the React app. [web](web) keeps the earlier vanilla JavaScript version.
- [Data model](docs/data_model.md) describes the tables and relationships.
- [Glossary](GLOSSARY.md) contains my technical notes. [Build log](docs/weeklog.md) records the early work from May 2026.

## License

MIT.
