# FragBro

I built FragBro around my interest in fragrances. It keeps track of what I own, what I want to try and what I actually wear.

The app has a React frontend, a FastAPI backend and a SQLite database. It started as a command-line tool, and the CLI still works alongside the web app.

## What it does

- Browse the fragrance catalog with names, brands and scent accords.
- Keep collection ratings, wishlist notes and links between dupes and their originals in the database.
- Log wears locally through the CLI, including the date, occasion, weather and rating (0–10).
- Show wear counts, most-worn fragrances and how long owned bottles have gone untouched.

The React view shows the catalog and wear statistics. Collection details and wishlist entries are available through the API and CLI. The HTTP API is read-only; wear logging stays in the local CLI.

The database has seven tables. Fragrances link to scent families through a join table, and `dupe_of_id` links a fragrance to another entry in the catalog. The seed files contain a small catalog and a collection snapshot.

This is a fixed demo dataset, not a live diary: 11 fragrances, 4 owned entries, 3 wishlist entries and 12 wear records after both seeds run. Dates and fragrance descriptions have not been independently verified. Ratings and dupe notes are subjective inputs, not measured similarity or recommendations.

Wear statistics count log entries. "Last 30 days" covers today and the previous 29 dates in UTC and excludes future-dated rows. Days since last wear uses the latest recorded date; a bottle with no wear history appears separately. High ratings do not imply frequent use, and missing logs do not prove a bottle was never worn.

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

The CLI uses the same database. If you have not started the API, initialize and seed it first:

```bash
fragbro init
fragbro seed
fragbro seed-personal
```

Then:

```bash
fragbro list
fragbro collection
fragbro wishlist
fragbro wear "Fattan" --occasion uni
fragbro wear-stats
```

The API and CLI use one seeded user. Account registration and authentication are not implemented. The demo has no HTTP write endpoints; CORS allows public reads and is not an authentication mechanism.

## Database and deployment

Set `FRAGBRO_DB_PATH` to an absolute SQLite file path before starting the API or CLI to keep data outside the checkout. For example, `export FRAGBRO_DB_PATH=/path/to/fragbro.db` in Bash, or `$env:FRAGBRO_DB_PATH = 'D:\Data\fragbro.db'` in PowerShell. Use the same value for both processes.

The default is `data/fragbro.db`. Startup loads missing seed records without duplicating existing ones. It does not migrate schemas or validate an existing database. Keep a backup before changing personal data directly.

On an ephemeral host, local changes disappear when its disk is replaced and startup restores the bundled seeds. Personal records need a persistent disk and the database path pointed at it. The public demo should expose only data you intend to share.

Backend start command: `uvicorn fragbro.api:app --host 0.0.0.0 --port "$PORT"` on a host that supplies `PORT`. The frontend is built separately with `VITE_API_URL` pointing at that backend. After deployment, `/openapi.json` should list only GET operations, with no `/wear` route.

## Tests and source

Run `python -m pytest` from the root. Tests cover the database schema, repeated startup/seeding, API responses, blocked HTTP writes and CLI validation, using temporary SQLite files.

They also exercise recent-window boundaries, empty history, unworn bottles and elapsed days. The GitHub workflow runs Python checks on Linux and Windows and builds/lints the React frontend. Build success alone does not verify a deployed service.

- [src/fragbro](src/fragbro) contains the database, API, CLI and seed scripts.
- [frontend](frontend) contains the React app. [web](web) keeps the earlier vanilla JavaScript version.
- [Data model](docs/data_model.md) describes the tables and relationships.
- [Glossary](GLOSSARY.md) contains my technical notes. [Build log](docs/weeklog.md) records the early work from May 2026.

## License

MIT.
