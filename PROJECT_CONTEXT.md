# FragBro — Project Context

## What I'm building
FragBro — a fragrance recommendation PWA (Progressive Web App). Mobile-first, shareable via link, no app store friction. Questionnaire-based recommendations in v1, evolving to embedding-based natural language search. Feature set includes blind-buy scoring, personal collection tracking, wear logs, wishlist, and later: influencer collections and community features.

## Current phase
Phase 1: Warm-up project planning — designing the data model

## This week's goal
Finalize FragBro data model. Write first Python script to create SQLite database and log first fragrance.

## Last session
Renamed repo from cologne to fragbro. Confirmed rename end-to-end. Drafted v1 data model with 5 tables: fragrances, users, collection, wear_logs, wishlist.

## Next step
Review data model against real fragrances from my collection. Refine fields. Then build first Python script.

## Key decisions
- Product name: FragBro (capital F, capital B, everywhere)
- Delivery: mobile-first PWA (not native app, not desktop website)
- Language: Python primary, JavaScript secondary
- Database: SQLite for Phase 1, PostgreSQL for Phase 2+
- Repo: github.com/abdullahnyle/fragbro
- Workflow: Claude for planning, Codex for coding, Gemini for research
---

# Build Status — End of Day 2 (Sunday, May 3, 2026)

This section captures the actual state of the FragBro codebase as of end of weekend 1. Anything earlier in this file is foundational/planning context. This section is the "what's actually built" snapshot.

## Repository

- **GitHub:** `https://github.com/abdullahnyle/fragbro`
- **Local path:** `D:\GitHub\FragBro`
- **Commits:** ~17+ as of end of Day 2
- **Branch:** `main`

## What's been built

### Documentation (committed)

- `README.md` — front page with project framing, roadmap, tech stack, quickstart
- `docs/data_model.md` — full Phase 1 schema spec for all 7 tables, validated against 5 real fragrances
- `BACKLOG.md` — inbox for new ideas (rule: nothing added to active plan until P1 ships)
- `FUTURE_FEATURES.md` — deliberately deferred features with reasons (inverse dupes, influencer collections, social recs, paid tier)
- `GLOSSARY.md` — plain-language reference for every technical term used so far
- `tests/README.md` — test suite usage guide

### Project infrastructure

- Python virtual environment set up at `venv/` (excluded from Git)
- `pyproject.toml` configured with project metadata, dependencies, and CLI entry point
- `requirements.txt` listing runtime + dev dependencies
- `.gitignore` covering Python, venv, IDE, OS, data files, logs, Jupyter
- Project structure: `src/fragbro/` (package), `tests/`, `data/`, `docs/`
- `pip install -e ".[dev]"` configured for editable install with dev dependencies

### Database layer (`src/fragbro/database.py`)

- SQLite database with all 7 Phase 1 tables: `fragrances`, `users`, `collection`, `wear_logs`, `wishlist`, `dna_families`, `fragrance_dna`
- Foreign key enforcement enabled (PRAGMA foreign_keys = ON)
- `get_connection()` and `initialize_database()` support optional `db_path` parameter for testability
- Schema uses REAL type for ratings (decimal support, e.g. 9.5)

### Catalog seed (`src/fragbro/seed.py`)

- 7 fragrances seeded: PDM Althair, PDM Percival, J. Janan Platinum, Lattafa Khamrah, Ahmed Al Maghribi Kaaf, French Avenue Liquid Brun, Rasasi Fattan
- 1 DNA family: Barber Shop / Fougère
- 2 dupe relationships: Kaaf → Percival, Liquid Brun → Althair
- 1 fragrance-DNA link: Fattan → Barber Shop / Fougère
- All inserts idempotent (safe to re-run)

### Personal seed (`src/fragbro/seed_personal.py`)

- User `abdullah` created with iCloud email
- 4 collection entries: Liquid Brun (9.5), Platinum (8.0), Fattan (8.0), Khamrah (6.0 with "outshone by Qahwa" note)
- 4 wear logs from real recent wears
- 3 wishlist entries: Kaaf, Marwa (Arabiyat Prestige, dupe of LV Imagination), Aquatica (Rayhaan, dupe of Creed Virgin Island Water)
- 4 extra catalog additions to support wishlist FKs: LV Imagination, Creed Virgin Island Water, Marwa, Aquatica
- 2 extra dupe relationships: Marwa → LV Imagination, Aquatica → Creed VIW

### CLI (`src/fragbro/cli.py`)

Built with Typer. **9 working commands**:

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

### Test suite (`tests/`)

Built with pytest. **9 passing tests** as of EOD 2:

- `tests/conftest.py` — `tmp_db` fixture creating a throwaway in-memory-style database per test
- `tests/test_database.py` — covers schema creation, columns, insert/read, foreign key enforcement (valid + invalid), required fields, unique constraints, GROUP BY analytics
- Tests run via `pytest`. Always passes from clean state.

## Database stats (real, as of end of Day 2)
Fragrances.............. 11
Users................... 1
Collection entries...... 4
Wear logs............... 6
Wishlist entries........ 3
DNA families............ 1
Dupe relationships...... 4
## Engineering patterns used (worth knowing)

- **Dependency injection** for testability — functions accept optional `db_path` to support test fixtures without touching real data
- **Idempotent seeds** — every insert checks for existence first, allowing re-runs without duplicates
- **Two-pass insertion** — fragrances inserted with NULL `dupe_of_id`, then UPDATE in second pass to resolve foreign keys
- **Parameterized queries everywhere** — `?` placeholders only, never string concatenation (SQL injection prevention)
- **Separation of catalog vs personal data** — different seed files, scales naturally to multi-user later
- **`__main__` idiom** — every Python file works both as importable module and runnable script
- **CLI with auto-help** — Typer generates `--help` from function signatures

## SQL coverage so far

Working knowledge demonstrated in code: `SELECT`, `INSERT`, `UPDATE`, `JOIN`, `LEFT JOIN`, self-join, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `COUNT`, `MAX`, subqueries (`NOT EXISTS`), parameterized queries, foreign keys, composite primary keys, `julianday()` date math, `date('now', '-30 days')` filtering, `CAST` type conversion.

## Pace and progress

- **Day 1 (Saturday May 2):** Data model design + validation, README, project skeleton, .gitignore, glossary infrastructure
- **Day 2 (Sunday May 3):** Backlog + future features files, glossary, full Python package setup, database layer, catalog seed, personal seed, full CLI, automated tests
- Currently estimated **~2 weeks ahead of original Phase 1 schedule**

## Pending admin

- **GitHub Student Pack application** — blocked on UET email password (going to grab it Monday in person on campus). 15-min admin task once email is accessible.

## Day 3 plan (next session)

1. GitHub Student Pack admin block (15 min)
2. Quality-of-life: `.vscode/settings.json` to auto-activate venv on terminal open
3. Expand test suite — add tests for `seed.py` and `seed_personal.py`
4. **First web layer** — turn FragBro from a CLI into something with a tiny webpage. Gateway to Phase 1's deployment goal (live URL by end of phase).

## Working session rules (locked in)

- Always `cd D:\GitHub\FragBro` and `.\venv\Scripts\Activate.ps1` at start of every terminal session
- Always commit at end of every working session
- Verify behavior before committing (run `pytest`, run the CLI, eyeball the output)
- Commit messages in present-tense imperative ("Add X", not "Added X")
- New ideas → BACKLOG.md, not the active plan
- Coursework + gym are non-negotiable; FragBro work is bounded