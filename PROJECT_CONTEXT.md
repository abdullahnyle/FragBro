# FragBro — Project Context

## What I'm building
FragBro — a fragrance recommendation PWA (Progressive Web App). Mobile-first, shareable via link, no app store friction. Questionnaire-based recommendations in v1, evolving to embedding-based natural language search. Feature set includes blind-buy scoring, personal collection tracking, wear logs, wishlist, and later: influencer collections and community features.

## Current phase
Phase 1: Warm-up — the project now has a CLI, a tested database layer, and a working HTTP API with interactive documentation. Frontend is the current layer being added.

## This week's goal
Get a minimal browser frontend talking to the live API, then deploy something live before phase 1 wraps.

## Last session
Day 4 — Monday May 5 (in progress). Completed: VS Code venv auto-activation finally fixed (PowerShell execution policy issue), VS Code workspace shortcut pinned to taskbar, GitHub Student Pack application submitted and approved (pending 72-hour propagation — UET email + 2FA + address required). Frontend build (Block 2) not yet started this session.

## Next step
Day 4 Block 2 — first frontend touch. Single `web/index.html` file (vanilla HTML + inline CSS + inline JS, no framework) that calls `GET /fragrances` and renders the list in the browser. Closes the end-to-end loop: browser → API → database → JSON → DOM.

## Key decisions
- Product name: FragBro (capital F, capital B, everywhere)
- Delivery: mobile-first PWA (not native app, not desktop website)
- Language: Python primary, JavaScript secondary
- Database: SQLite for Phase 1, PostgreSQL for Phase 2+
- Web framework: FastAPI (chosen Day 3 — also what we'll use to serve embedding models in Phase 3)
- Repo: github.com/abdullahnyle/fragbro
- Workflow: see "Teaching & workflow rules" below — locked Day 4

---

# Teaching & workflow rules (LOCKED — applies every session)

These rules were debated and locked Day 4. They override any earlier guidance in chat history. They apply for the rest of Phase 1 minimum, re-evaluated at Phase 2 start.

### 1. Stage-aware writing

What "you write the code" means depends on where Abdullah is in the journey:

| Stage | What "you write" means |
|---|---|
| **Now → Month 2** (Day 4, current) | Type code from worked examples by hand. Don't paste. Run it. Break it on purpose. Goal: typing fluency + pattern recognition. |
| **Month 2 → 5** | Given structure + key pieces, fill gaps with AI as backup. Goal: composing pieces. |
| **Month 5 → 10** | Write core logic in own voice (recommender, embedding pipeline, eval harness) with AI assisting. Goal: real engineering judgment. |
| **Month 10+** | AI as power tool. Abdullah drives. |

**Claude must not push past current stage prematurely.** If a step requires Month-5 skills, scaffold it down to current-stage-appropriate. The "throw into the deep end" approach was rejected — gradual, slow, steady is the contract.

### 2. Read every line before commit (non-negotiable from Day 1)

If AI generates code and Abdullah can't explain a line, that line doesn't get committed. Ask Claude to explain it first, add new terms to `GLOSSARY.md`, then commit. This is the single highest-compounding habit.

### 3. Debug-before-prompt — 10-minute floor

When code breaks: read the error, look at the line, form a hypothesis, check the code yourself. Ten minutes solo before opening any AI chat. After 10 min, fine to bring to Claude with: *"I tried X, saw Y, think it's Z."* That's a real engineer's debug log.

### 4. Type, don't paste — first-time concepts

When the concept is new (first HTML file, first fetch call, first SQL JOIN, etc.), Abdullah types the worked example by hand. Codex inline autocomplete is allowed — full-file paste is not. Repeated patterns from past sessions: pasting is fine.

### 5. AI as multiplier, not prosthetic

The boundary, in plain language:
- **AI writes:** boilerplate, config, repetitive CRUD, scaffolding, lookup-style code.
- **Abdullah writes:** core logic — anything that requires a decision (data model, recommendation algorithm, evaluation harness, embedding pipeline) — once at appropriate stage.
- **Abdullah always:** reads every line, explains every line, debugs before prompting.

The goal isn't to avoid AI. It's to ensure that by 2028 Abdullah can pass a no-AI technical screen — because admissions interviews and serious internships will have those.

### 6. Phase 1 tooling — single-chat mode

For Phase 1, Claude (this chat) handles all of: planning, teaching, code generation, code review, architecture decisions. Codex inside VS Code is allowed for inline autocomplete only. Other tools (ChatGPT, Gemini, DeepSeek) are paused until Phase 2 — splitting tools while still learning fundamentals fragments context and slows learning. Re-evaluated at Phase 2 kickoff.

### 7. Per-session rhythm

1. **Plan with Claude** — what's getting built, why, what concepts come up.
2. **Type the code** — first-time concepts from worked example, familiar patterns from your own draft.
3. **Hit a wall** → 10-min solo debug → Claude with what was tried.
4. **Before commit** → read every line, explain everything, glossary updates, then commit.
5. **End-of-session** → commit, weeklog entry, Claude updates `PROJECT_CONTEXT.md`.

---

# Build Status — End of Day 4 (in progress, Monday May 5, 2026)

## Repository

- **GitHub:** `https://github.com/abdullahnyle/fragbro`
- **Local path:** `D:\GitHub\FragBro`
- **Commits:** ~25+ as of end of Day 3 (Day 4 commits pending end-of-session)
- **Branch:** `main`

## What's been built

### Documentation (committed)

- `README.md` — front page with project framing, roadmap, tech stack, quickstart, and Running the API section
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
- **Day 4 fix:** PowerShell execution policy set to `RemoteSigned` (CurrentUser scope) — venv now auto-activates on every new terminal in VS Code
- **Day 4 setup:** Desktop/taskbar shortcut targeting `Code.exe "D:\GitHub\FragBro"` so VS Code always opens with FragBro as the workspace (root cause of earlier "venv not auto-activating" issue was opening files individually instead of the folder)

### Database layer (`src/fragbro/database.py`)

- SQLite database with all 7 Phase 1 tables: `fragrances`, `users`, `collection`, `wear_logs`, `wishlist`, `dna_families`, `fragrance_dna`
- Foreign key enforcement enabled (PRAGMA foreign_keys = ON)
- `get_connection()` and `initialize_database()` accept optional `db_path` parameter for testability
- Schema uses REAL type for ratings (decimal support, e.g. 9.5)

### Catalog seed (`src/fragbro/seed.py`)

- 7 fragrances seeded: PDM Althair, PDM Percival, J. Janan Platinum, Lattafa Khamrah, Ahmed Al Maghribi Kaaf, French Avenue Liquid Brun, Rasasi Fattan
- 1 DNA family: Barber Shop / Fougère
- 2 dupe relationships: Kaaf → Percival, Liquid Brun → Althair
- 1 fragrance-DNA link: Fattan → Barber Shop / Fougère
- All inserts idempotent
- `seed_all()` accepts `db_path` parameter for testability

### Personal seed (`src/fragbro/seed_personal.py`)

- User `abdullah` created with iCloud email
- 4 collection entries: Liquid Brun (9.5), Platinum (8.0), Fattan (8.0), Khamrah (6.0 with "outshone by Qahwa" note)
- 4 wear logs from real recent wears
- 3 wishlist entries: Kaaf, Marwa (Arabiyat Prestige, dupe of LV Imagination), Aquatica (Rayhaan, dupe of Creed Virgin Island Water)
- 4 extra catalog additions: LV Imagination, Creed Virgin Island Water, Marwa, Aquatica
- 2 extra dupe relationships: Marwa → LV Imagination, Aquatica → Creed VIW
- `seed_personal()` accepts `db_path` parameter for testability

### CLI (`src/fragbro/cli.py`)

Built with Typer. **9 working commands:**

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

### HTTP API (`src/fragbro/api.py`)

Built with FastAPI. **8 endpoints:**

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
- Returns proper HTTP status codes: 200, 201, 404, 422, 400
- Reuses the same database layer as the CLI — no code duplication

**Run with:** `uvicorn fragbro.api:app --reload`

### Frontend (`web/`) — Day 4 in progress

- `web/` directory created
- `web/index.html` exists, currently empty (Block 2 build pending)

### Test suite (`tests/`)

Built with pytest. **29 passing tests** as of EOD 3:

- `tests/conftest.py` — `tmp_db` fixture (open connection) and `tmp_db_path` fixture (file path)
- `tests/test_database.py` — 9 tests
- `tests/test_seed.py` — 8 tests
- `tests/test_api.py` — 12 tests

API tests use FastAPI's `TestClient` and `monkeypatch` for an isolated test database.

## Database stats (real, as of end of Day 3)

Fragrances.............. 11
Users................... 1
Collection entries...... 4
Wear logs............... 4
Wishlist entries........ 3
DNA families............ 1
Dupe relationships...... 4

## Engineering patterns used (worth knowing)

- Dependency injection for testability (optional `db_path`)
- Idempotent seeds (every insert checks for existence)
- Two-pass insertion (NULL `dupe_of_id`, then UPDATE)
- Parameterized queries everywhere — `?` placeholders, never string concatenation
- Separation of catalog vs personal data
- `__main__` idiom — every Python file works both as module and runnable script
- CLI with auto-help via Typer
- Pydantic-validated request bodies on POST endpoints
- Two doorways, one house — CLI and HTTP API both call the same `database.py` functions
- Helper contract design — push None checks up to where the data first enters the system

## SQL coverage so far

`SELECT`, `INSERT`, `UPDATE`, `JOIN`, `LEFT JOIN`, self-join, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `COUNT`, `MAX`, subqueries (`NOT EXISTS`), parameterized queries, foreign keys, composite primary keys, `julianday()` date math, `date('now', '-30 days')` filtering, `CAST` type conversion.

## HTTP / API coverage so far

GET, POST, path parameters, JSON request/response, status codes (200/201/404/422/400), Pydantic validation, CORS, auto-generated OpenAPI docs.

## Pace and progress

- **Day 1 (Saturday May 2):** Data model design + validation, README, project skeleton, .gitignore, glossary infrastructure
- **Day 2 (Sunday May 3):** Backlog + future features, full Python package setup, database layer, catalog seed, personal seed, full CLI, automated tests
- **Day 3 (Sunday May 4):** VS Code workspace, seed test coverage, FastAPI HTTP layer with 8 endpoints, CORS, Pydantic, 12 API tests, README updates, weeklog created
- **Day 4 (Monday May 5, in progress):** Venv auto-activation fixed, VS Code workspace shortcut, Student Pack approved (72-hour wait), `web/` directory + empty `index.html` created. Block 2 (first frontend) pending.
- Currently estimated **2+ weeks ahead of original Phase 1 schedule**

## Pending admin

- **GitHub Student Pack** — approved, 72-hour propagation in progress. Once active, claim:
  - Free `.dev` domain (target: `fragbro.abdullah.dev` or similar)
  - Railway / Render hosting credits (Phase 1 deployment)
  - GitHub Copilot 2-year free
  - Notion Pro

## Day 4 remaining (Block 2)

1. **First frontend touch** — single `web/index.html` page (vanilla HTML + inline CSS + inline JS, no framework). Calls `GET /fragrances` and renders the list. Proves end-to-end loop: browser → API → database → JSON → DOM.
2. Stretch: a second view that calls `/wear-stats`.
3. Decide on a frontend approach for the rest of P1: vanilla longer, or graduate to Vite + React.

## Working session rules (locked in)

- Always `cd D:\GitHub\FragBro` and verify `(venv)` shown at prompt at start of every terminal session
- Always commit at end of every working session
- Verify behavior before committing (run `pytest`, run the CLI, eyeball the output, hit `/docs` and click around)
- Commit messages in present-tense imperative ("Add X", not "Added X")
- New ideas → BACKLOG.md, not the active plan
- Coursework + gym are non-negotiable; FragBro work is bounded
- Large file pastes: delete the file and recreate empty before pasting, to avoid half-applied edits and decorator collisions