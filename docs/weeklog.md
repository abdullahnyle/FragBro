# FragBro Engineering Log

A short, honest record of what got built each working session. Not a polished blog. The point is to capture the actual work — including dead ends, recoveries, and lessons — so future-me, recruiters, and admissions committees can see how this was actually built, not just what it ended up as.

---

## Day 1 — Saturday, May 2, 2026

**Goal:** Get the project off the ground. Validate the data model against real fragrances. Set up the repo so it doesn't look like a "first commit, README only" graveyard.

**Time spent:** ~6 hours (loose count — split across the day).

### Built
- Repo created at `github.com/abdullahnyle/fragbro` (renamed from earlier `cologne` working name)
- `README.md` — front page with project framing (positioned as semantic search and recommendation over subjective product reviews, applied to fragrances), roadmap, tech stack, quickstart
- `docs/data_model.md` — full schema spec for Phase 1 tables
- Data model validated against 5 real fragrances from my own collection: PDM Althair, PDM Percival, J. Janan Platinum, Lattafa Khamrah, Ahmed Al Maghribi Kaaf, French Avenue Liquid Brun, Rasasi Fattan
- Initial project skeleton: `src/fragbro/`, `tests/`, `data/`, `docs/`
- `.gitignore` covering Python, venv, IDE files, OS files, data files, logs, Jupyter junk
- Decisions locked: product name (FragBro), delivery shape (mobile-first PWA), Python primary, SQLite for Phase 1

### Concepts confirmed
- Why fragrance is the right domain: technically underserved despite smaller market vs fashion (fashion is saturated + carries a CV data tax)
- Why a PWA over native: shareable via link, no app store friction, mobile-first
- Why SQLite first, Postgres later: zero-setup, file-based, good enough for single-user

### State at end of day
- Repo live, README in place, data model spec written
- No code yet. That's fine — getting the data model right matters more than rushing to typing `def`

---

## Day 2 — Sunday, May 3, 2026

**Goal:** Turn the data model from a spec into a working database, plus a CLI to actually use it.

**Time spent:** ~10 hours, full bulk session.

### Built
- `BACKLOG.md` — inbox for new feature ideas (rule: nothing added to active plan until P1 ships)
- `FUTURE_FEATURES.md` — deliberately deferred features with reasons (inverse dupes for budget fragrances, influencer collections, social recommendations, paid tier)
- `GLOSSARY.md` — plain-language reference for every technical term used so far
- `tests/README.md` — test suite usage guide
- Python virtual environment at `venv/` (excluded from Git)
- `pyproject.toml` configured with project metadata, runtime deps (`typer`), dev deps (`pytest`), and a CLI entry point
- `requirements.txt` mirroring runtime deps
- `pip install -e ".[dev]"` configured for editable install
- **Database layer (`src/fragbro/database.py`):**
  - All 7 Phase 1 tables: `fragrances`, `users`, `collection`, `wear_logs`, `wishlist`, `dna_families`, `fragrance_dna`
  - Foreign key enforcement enabled (PRAGMA foreign_keys = ON)
  - `get_connection()` and `initialize_database()` accept optional `db_path` for testability
  - REAL type for ratings (decimal support, e.g. 9.5)
- **Catalog seed (`src/fragbro/seed.py`):**
  - 7 fragrances seeded
  - 1 DNA family: Barber Shop / Fougère
  - 2 dupe relationships: Kaaf → Percival, Liquid Brun → Althair
  - 1 fragrance-DNA link: Fattan → Barber Shop / Fougère
  - Idempotent (safe to re-run)
- **Personal seed (`src/fragbro/seed_personal.py`):**
  - User `abdullah` created
  - 4 collection entries with personal ratings
  - 4 wear logs from real recent wears
  - 3 wishlist entries
  - 4 extra catalog additions to support wishlist FKs
  - 2 extra dupe relationships
- **CLI (`src/fragbro/cli.py`)** — built with Typer, 9 working commands:
  - `init`, `seed`, `seed-personal`, `list`, `show`, `stats`, `wear`, `collection`, `wishlist`, `wear-stats`
- **Test suite (`tests/`)** — built with pytest, 9 passing tests covering schema, columns, insert/read, foreign key enforcement (valid + invalid), required fields, unique constraints, GROUP BY analytics
- `tests/conftest.py` — `tmp_db` fixture creating a throwaway database per test

### Engineering patterns established
- **Dependency injection** for testability — functions accept optional `db_path`
- **Idempotent seeds** — every insert checks for existence first
- **Two-pass insertion** — fragrances inserted with NULL `dupe_of_id`, then UPDATE in second pass to resolve foreign keys
- **Parameterized queries everywhere** — `?` placeholders only, never string concatenation
- **Separation of catalog vs personal data** — different seed files, scales naturally to multi-user later
- **`__main__` idiom** — every Python file works both as importable module and runnable script
- **CLI with auto-help** — Typer generates `--help` from function signatures

### SQL coverage by EOD
`SELECT`, `INSERT`, `UPDATE`, `JOIN`, `LEFT JOIN`, self-join, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `COUNT`, `MAX`, subqueries (`NOT EXISTS`), parameterized queries, foreign keys, composite primary keys, `julianday()` date math, `CAST` type conversion.

### State at end of day
- Working CLI for everything you'd actually want to do with a fragrance database
- 9 passing tests, ~17 commits
- ~2 weeks ahead of original Phase 1 schedule

---

## Day 3 — Monday, May 4, 2026

**Goal:** Turn FragBro from a CLI-only project into a real web service. Add an HTTP layer, get auto-generated interactive docs working, prepare the foundation for a frontend in the next session.

**Time spent:** ~6 hours, full bulk session.

### Built

**Block 1 — admin & polish (~45 min)**
- `.vscode/settings.json` — auto-activates the venv on terminal open, enables pytest test panel, hides cache folders
- New `tmp_db_path` fixture in `tests/conftest.py` — yields a path instead of a connection, for tests that need to call functions which open their own connection
- `tests/test_seed.py` — 8 new tests covering catalog seed, personal seed, idempotency, dupe relationships, DNA links, and extra catalog additions
- Refactored `seed.py` and `seed_personal.py` to accept an optional `db_path` parameter (matching the existing pattern in `database.py` and `get_connection`) so seeds can be tested against throwaway databases without touching `data/fragbro.db`
- Fixed a real bug in `database.py`: `initialize_database()` had a duplicated loop running `cursor.execute()` on a closed connection. Surfaced cleanly during testing.

**Block 2 — first web layer (~2 hours)**
- Installed FastAPI + Uvicorn
- New file: `src/fragbro/api.py` — first HTTP layer
- Added 4 read endpoints: `GET /`, `GET /fragrances`, `GET /fragrances/{name}`, `GET /collection`
- Verified the auto-generated `/docs` interactive documentation works end-to-end in the browser
- Confirmed the architecture hypothesis from Day 2: because the database layer was already cleanly separated, the web layer dropped in beside the CLI without touching `database.py` at all. Two doorways into the same house.

**Block 3 — round out the API + frontend prep (~2 hours)**
- 3 more read endpoints: `GET /wishlist`, `GET /wear-stats`, `GET /stats` — full parity with the CLI
- First **write endpoint**: `POST /wear` — accepts a JSON body, validates it via Pydantic, inserts a wear log, returns 201 Created with the new entry
- Pydantic request model `WearLogRequest` for input validation — required vs optional fields enforced before any code runs
- CORS middleware configured for permissive local-dev access (will tighten before deploy)
- 12 new API tests in `tests/test_api.py` using FastAPI's `TestClient` — covers all 8 endpoints, including the 422 validation error case for missing required fields
- README updated with a "Running the API" section
- New runtime deps in `pyproject.toml`: `fastapi`, `uvicorn`. New dev dep: `httpx` (required by `TestClient`).
- This file (`docs/weeklog.md`) created

### Test count: 17 → 29

### Concepts learned today
- **HTTP basics** — GET vs POST, status codes (200, 201, 404, 422, 500), localhost vs 127.0.0.1, ports
- **FastAPI fundamentals** — `@app.get` and `@app.post` decorators, path parameters (`/fragrances/{name}`), JSON serialization, auto-generated `/docs`
- **Pydantic models** — `BaseModel` for request validation, `field: Type | None = None` syntax for optional fields
- **CORS** — what it is, why a browser frontend needs it, how to configure it in FastAPI
- **TestClient** — pytest pattern for testing endpoints in-process, no real server needed
- **monkeypatch** — pytest tool for hot-swapping functions during tests; used to redirect API endpoints to a test database
- **Pylance type narrowing** — when a helper returns `T | None`, push the None check up to the caller so the helper has a cleaner contract; avoids defensive code being duplicated

### Recoveries (the ugly part — kept honest)
- Created `api.py` in the wrong directory (project root instead of `src/fragbro/`). Caught it via `Get-ChildItem` recursive search, fixed with `Move-Item`. Lesson: VS Code creates new files in whichever folder you have selected — single-click the target folder before pressing "New File."
- Two failed pastes of the same file caused decorator collisions (`)@app.get(...)` jammed onto the closing paren of a SQL string). Solution: delete the file and recreate empty before pasting large content. Stopped half-applied edits cold.
- Misnamed test functions on first try (assumed `seed_catalog` and `seed_personal_data` but the real names were `seed_all` and `seed_personal`). Lesson: read the actual file before writing tests against it.
- Duplicate loop bug in `initialize_database()` — quietly worked due to `IF NOT EXISTS` on the schema, but failed loudly when `cursor.execute()` was called after `connection.close()`. Surfacing latent bugs is one of the side benefits of writing tests.

### State at end of day
- 8 working endpoints, all visible in `/docs`
- 29 tests passing, 0 failing
- ~25 commits on the day
- API and CLI both reading from the same SQLite database
- Architecture remains clean: `database.py` was not modified at all in Blocks 2 or 3 — the web layer slotted in beside the CLI

### Tomorrow / Day 4 plan
- Claim GitHub Student Pack (UET email password Monday, 15-min admin task)
- Reserve a `.dev` domain via the Student Pack
- First frontend touch: simple HTML/JS page that calls `/fragrances` and renders the list. Not styled, just functional. Proves end-to-end the browser → API → database loop works.