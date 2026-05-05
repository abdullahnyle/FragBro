# FragBro — Project Context

## What I'm building
FragBro — a fragrance recommendation PWA (Progressive Web App). Mobile-first, shareable via link, no app store friction. Questionnaire-based recommendations in v1, evolving to embedding-based natural language search. Feature set includes blind-buy scoring, personal collection tracking, wear logs, wishlist, and later: influencer collections and community features.

## Current phase
Phase 1: Warm-up — the project now has a CLI, a tested database layer, and a working HTTP API with interactive documentation. Frontend is the next conceptual layer.

## This week's goal
Get a minimal browser frontend talking to the live API, then deploy something live before phase 1 wraps.

## Last session
Day 3 — Sunday May 4. Added FastAPI HTTP layer with 8 endpoints (7 GET + 1 POST), CORS, Pydantic validation, 12 new API tests, updated README. Also: VS Code workspace settings, refactored seeds to accept db_path for testability, 8 new seed tests, fixed a duplicate-loop bug in `initialize_database()`. Test count went from 17 to 29.

## Next step
Day 4 — first frontend touch. Simple HTML/JS page (no React yet) that calls `/fragrances` and renders the list. Plus: GitHub Student Pack admin block.

## Key decisions
- Product name: FragBro (capital F, capital B, everywhere)
- Delivery: mobile-first PWA (not native app, not desktop website)
- Language: Python primary, JavaScript secondary
- Database: SQLite for Phase 1, PostgreSQL for Phase 2+
- Web framework: FastAPI (chosen Day 3 — also what we'll use to serve embedding models in Phase 3)
- Repo: github.com/abdullahnyle/fragbro
- Workflow: Claude for planning, Codex for coding, Gemini for research

---

# Build Status — End of Day 3 (Sunday, May 4, 2026)

This section captures the actual state of the FragBro codebase as of end of weekend 1, Day 3. Anything earlier in this file is foundational/planning context. This section is the "what's actually built" snapshot.

## Repository

- **GitHub:** `https://github.com/abdullahnyle/fragbro`
- **Local path:** `D:\GitHub\FragBro`
- **Commits:** ~25+ as of end of Day 3
- **Branch:** `main`

## What's been built

### Documentation (committed)

- `README.md` — front page with project framing, roadmap, tech stack, quickstart, **and now a Running the API section**
- `docs/data_model.md` — full Phase 1 schema spec for all 7 tables, validated against 5 real fragrances
- `docs/weeklog.md` — engineering log, day-by-day record of what got built, lessons, recoveries
- `BACKLOG.md` — inbox for new ideas (rule: nothing added to active plan until P1 ships)
- `FUTURE_FEATURES.md` — deliberately deferred features with reasons (inverse dupes, influencer collections, social recs, paid tier)
- `GLOSSARY.md` — plain-language reference for every technical term used so far
- `tests/README.md` — test suite usage guide

### Project infrastructure

- Python virtual environment at `venv/` (excluded from Git)
- `pyproject.toml` — runtime deps: `typer`, `fastapi`, `uvicorn`. Dev deps: `pytest`, `httpx`.
- `requirements.txt` mirrors the runtime deps
- `.vscode/settings.json` — auto-activates venv on terminal open, enables pytest panel, hides cache folders
- `.gitignore` covering Python, venv, IDE, OS, data files, logs, Jupyter
- Project structure: `src/fragbro/` (package), `tests/`, `data/`, `docs/`
- `pip install -e ".[dev]"` configured for editable install with dev dependencies

### Database layer (`src/fragbro/database.py`)

- SQLite database with all 7 Phase 1 tables: `fragrances`, `users`, `collection`, `wear_logs`, `wishlist`, `dna_families`, `fragrance_dna`
- Foreign key enforcement enabled (PRAGMA foreign_keys = ON)
- `get_connection()` and `initialize_database()` accept optional `db_path` parameter for testability
- Schema uses REAL type for ratings (decimal support, e.g. 9.5)
- **Bug fix Day 3:** removed duplicated loop that was running `cursor.execute()` on a closed connection (silently worked due to IF NOT EXISTS but technically broken)

### Catalog seed (`src/fragbro/seed.py`)

- 7 fragrances seeded: PDM Althair, PDM Percival, J. Janan Platinum, Lattafa Khamrah, Ahmed Al Maghribi Kaaf, French Avenue Liquid Brun, Rasasi Fattan
- 1 DNA family: Barber Shop / Fougère
- 2 dupe relationships: Kaaf → Percival, Liquid Brun → Althair
- 1 fragrance-DNA link: Fattan → Barber Shop / Fougère
- All inserts idempotent
- **Day 3 refactor:** `seed_all()` now accepts `db_path` parameter for testability

### Personal seed (`src/fragbro/seed_personal.py`)

- User `abdullah` created with iCloud email
- 4 collection entries: Liquid Brun (9.5), Platinum (8.0), Fattan (8.0), Khamrah (6.0 with "outshone by Qahwa" note)
- 4 wear logs from real recent wears
- 3 wishlist entries: Kaaf, Marwa (Arabiyat Prestige, dupe of LV Imagination), Aquatica (Rayhaan, dupe of Creed Virgin Island Water)
- 4 extra catalog additions: LV Imagination, Creed Virgin Island Water, Marwa, Aquatica
- 2 extra dupe relationships: Marwa → LV Imagination, Aquatica → Creed VIW
- **Day 3 refactor:** `seed_personal()` now accepts `db_path` parameter for testability

### CLI (`src/fragbro/cli.py`)

Built with Typer. **9 working commands** (unchanged from Day 2):

| Command | Purpose |
|---|---|
| `fragbro init` | Initialize the database (create tables) |
| `fragbro seed` | Seed catalog data |
| `fragbro seed-personal` | Seed user's personal data |
| `fragbro list` | List all fragrances |
| `fragbro show <name>` | Full detail card for a fragrance (with dupe + DNA info) |
| `fragbro stats` | Database summary stats |
| `fragbro wear <name>` | Log a wear (supports `--date`, `--occasion`, `--weather`, `--rating`, `--mood`) |
| `fragbro collection` | View owned fragrances sorted by rating |
| `fragbro wishlist` | View wishlist with dupe relationships and notes |
| `fragbro wear-stats` | Analytics: most worn (all-time + 30d), owned-but-unworn, days-since-last-worn |

### HTTP API (`src/fragbro/api.py`) — NEW Day 3

Built with FastAPI. **8 endpoints**:

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Health check / welcome |
| GET | `/fragrances` | List all fragrances with dupe info |
| GET | `/fragrances/{name}` | Full detail for one fragrance (case-insensitive) + DNA families |
| GET | `/collection` | Owned fragrances sorted by rating |
| GET | `/wishlist` | Wishlist entries with dupe relationships |
| GET | `/wear-stats` | Wearing analytics (most worn, unworn, days-since) |
| GET | `/stats` | Database summary stats |
| POST | `/wear` | Log a wear (Pydantic-validated body) |

- Auto-generated interactive docs at `/docs`
- Auto-generated OpenAPI schema at `/openapi.json`
- CORS middleware configured (permissive in dev; tighten before deploy)
- Pydantic `WearLogRequest` model validates POST body before code runs
- Returns proper HTTP status codes: 200, 201, 404, 422 (validation), 400 (no user)
- Reuses the same database layer as the CLI — no code duplication

**Run with:** `uvicorn fragbro.api:app --reload`

### Test suite (`tests/`)

Built with pytest. **29 passing tests** as of EOD 3:

- `tests/conftest.py` — `tmp_db` fixture (open connection) and `tmp_db_path` fixture (file path, for code that opens its own connection)
- `tests/test_database.py` — 9 tests: schema, columns, insert/read, foreign key enforcement, required fields, unique constraints, GROUP BY analytics
- `tests/test_seed.py` — 8 tests: catalog & personal seed correctness, idempotency, dupe relationships, DNA links, extra catalog
- `tests/test_api.py` — 12 tests: all 8 endpoints, 404 cases, case-insensitivity, Pydantic 422 validation, persistence verification (POST then GET confirms write)
- API tests use FastAPI's `TestClient` and `monkeypatch` to redirect to a test database — no real server needed

## Database stats (real, as of end of Day 3)
Fragrances.............. 11
Users................... 1
Collection entries...... 4
Wear logs............... 4 (or more if you've poked POST /wear)
Wishlist entries........ 3
DNA families............ 1
Dupe relationships...... 4

## Engineering patterns used (worth knowing)

- **Dependency injection** for testability — functions accept optional `db_path` to support test fixtures without touching real data
- **Idempotent seeds** — every insert checks for existence first
- **Two-pass insertion** — fragrances inserted with NULL `dupe_of_id`, then UPDATE in second pass to resolve foreign keys
- **Parameterized queries everywhere** — `?` placeholders only, never string concatenation
- **Separation of catalog vs personal data** — different seed files
- **`__main__` idiom** — every Python file works both as importable module and runnable script
- **CLI with auto-help** — Typer generates `--help` from function signatures
- **Auto-validated request bodies** — Pydantic models on POST endpoints. Type hint = validation. Zero hand-rolled checks.
- **Two doorways, one house** — CLI and HTTP API both call the same `database.py` functions. Adding the API didn't touch the database layer at all.
- **Helper contract design** — when a helper *could* return None but its only caller already None-checks the input, push the None check up so the helper has a clean contract

## SQL coverage so far

`SELECT`, `INSERT`, `UPDATE`, `JOIN`, `LEFT JOIN`, self-join, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `COUNT`, `MAX`, subqueries (`NOT EXISTS`), parameterized queries, foreign keys, composite primary keys, `julianday()` date math, `date('now', '-30 days')` filtering, `CAST` type conversion.

## HTTP / API coverage so far (NEW)

GET, POST, path parameters, query parameters (none yet but ready), JSON request/response, status codes (200/201/404/422/400), Pydantic validation, CORS, auto-generated OpenAPI docs.

## Pace and progress

- **Day 1 (Saturday May 2):** Data model design + validation, README, project skeleton, .gitignore, glossary infrastructure
- **Day 2 (Sunday May 3):** Backlog + future features, full Python package setup, database layer, catalog seed, personal seed, full CLI, automated tests
- **Day 3 (Sunday May 4):** VS Code workspace, seed test coverage, FastAPI HTTP layer with 8 endpoints, CORS, Pydantic, 12 API tests, README updates, weeklog created
- Currently estimated **2+ weeks ahead of original Phase 1 schedule**

## Pending admin

- **GitHub Student Pack application** — UET email password to be retrieved Monday on campus. 15-min admin task.

## Day 4 plan (next session)

1. GitHub Student Pack admin block (15 min)
2. Reserve `fragbro.abdullah.dev` (or similar) via the Student Pack's free .dev domain
3. **First frontend touch** — single HTML page (vanilla JS, no framework yet) that calls `/fragrances` and renders the list in the browser. Proves the end-to-end loop: browser → API → database → JSON → DOM.
4. Stretch: a second page that calls `/wear-stats` and renders the analytics
5. Decide on a frontend approach for the rest of P1: vanilla → Vite + React, or stay vanilla longer

## Working session rules (locked in)

- Always `cd D:\GitHub\FragBro` and verify `(venv)` shown at prompt at start of every terminal session
- Always commit at end of every working session
- Verify behavior before committing (run `pytest`, run the CLI, eyeball the output, hit `/docs` and click around)
- Commit messages in present-tense imperative ("Add X", not "Added X")
- New ideas → BACKLOG.md, not the active plan
- Coursework + gym are non-negotiable; FragBro work is bounded
- Large file pastes: delete the file and recreate empty before pasting, to avoid half-applied edits and decorator collisions