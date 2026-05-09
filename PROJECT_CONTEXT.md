# FragBro — Project Context

## What I'm building
FragBro — a fragrance recommendation PWA (Progressive Web App). Mobile-first, shareable via link. Questionnaire-based recommendations in v1, evolving to embedding-based natural language search. Feature set includes blind-buy scoring, personal collection tracking, wear logs, wishlist, and later: influencer collections and community features.

## Current phase
Phase 1: Warm-up — the project has a CLI, tested database layer, working HTTP API with interactive documentation, and a minimal browser frontend that fetches from the API and renders the catalog.

## This week's goal
Polish the frontend, decide on the framework approach for the rest of P1, and deploy something live before phase 1 wraps.

## Last session
Day 5 — Friday May 8. Shipped first browser frontend (`web/index.html`): vanilla HTML + CSS + JS, calls `GET /fragrances`, renders cards with name, brand, accords, dupe info. Closed the full browser → API → DB → JSON → DOM loop. Engineering rules updated to v2 (see Engineering Rules section below).

## Next step
Day 6 — Step 6 walkthrough (line-by-line review of the JS in `web/index.html` covering async/await, fetch, DOM, template literals, .map, ternary). Then either polish the frontend (styling, second view) or push toward deployment.

## Key decisions
- Product name: FragBro (capital F, capital B, everywhere)
- Delivery: mobile-first PWA
- Language: Python primary, JavaScript secondary
- Database: SQLite for Phase 1, PostgreSQL for Phase 2+
- Web framework: FastAPI
- Frontend approach: vanilla HTML/CSS/JS for warm-up, framework decision pending
- Repo: github.com/abdullahnyle/FragBro

---

# Engineering Rules (v2 — locked Day 5)

These rules are the contract for how engineering work is done on this project. They replace the v1 rules. They apply for the rest of Phase 1 minimum, re-evaluated at Phase 2 start.

## North Star

The goal of the technical work is to become an **excellent code reader and system thinker who can write code when needed.** Emphasis on debugging, system understanding, and architectural judgment over keystroke fluency.

## Rule 1 — Three-Bucket Model

Every line of code falls into one of three buckets. The bucket determines the workflow.

### Bucket 1 — Concept-First Learning Loop (genuinely first-time concepts only)

Triggers: a concept never used before. First HTML file, first fetch, first SQL JOIN, first React useState, first embedding call. One time per concept, ever.

Workflow:
1. Articulate the goal in plain English first
2. Identify the concepts needed and learn them with examples not from this project
3. Draft an attempt
4. Review and refine
5. Update GLOSSARY.md with new terms
6. Confirm one-line "what does this do" understanding for every line before commit

### Bucket 2 — Draft, then Review (decisions and architecture)

Triggers: anything requiring a decision. Data model design, recommender algorithm, eval harness, embedding pipeline shape, API endpoint architecture, test design.

Workflow:
1. Draft the implementation independently
2. Submit for review
3. Critique, refine, accept/reject changes with reasoning
4. Final version reflects own judgment plus refinement

This is where most engineering judgment compounds. The most important bucket.

### Bucket 3 — Generated, Read Carefully (boilerplate)

Triggers: config files, repeat CRUD, standard test scaffolding, gitignore additions, repeat patterns, documentation drafts.

Workflow: code generated, every line read and understood, commit. Significant time spent here is fine — it's where productivity gains live.

## Rule 2 — Read Every Line Before Commit

Non-negotiable. Any line that can't be explained doesn't get committed.

## Rule 3 — 10-Minute Solo Debug Floor

When code breaks: read the error, look at the line, form a hypothesis, check the code. Ten minutes solo before consulting any external help.

## Rule 4 — New Term to Glossary

Every new technical term goes to GLOSSARY.md immediately, in plain language.

## Rule 5 — Solo Build Test

Once every two weeks initially, monthly after Phase 1 ships:

A 1-2 hour throwaway project, no external help, just docs. Examples: weather-fetch script, file-rename bash one-liner, tiny Flask endpoint, SQL against a CSV, list-flatten function. Code is discarded after.

The point is the diagnostic, not the artifact.

## Rule 6 — Whiteboard Prep (Phase 3 onward)

Starting Phase 3 (Sept 2026 target), one whiteboard-style problem per week. 30-45 min each. LeetCode easy/medium or pen-and-paper algorithm sketches.

## Rule 7 — Per-Session Rhythm

1. Plan the session
2. Execute per Three-Bucket rules
3. Hit a wall → 10-min solo debug → consult
4. Before commit → read every line, glossary updates, commit
5. End-of-session → commit, weeklog entry, update build status

---

# Build Status — End of Day 5 (Friday May 8, 2026)

## Repository

- **GitHub:** `https://github.com/abdullahnyle/FragBro`
- **Local path:** `D:\GitHub\FragBro`
- **Latest commit:** `954732b` (frontend Day 5)
- **Branch:** `main`

## What's been built

### Documentation
- `README.md` — project framing, roadmap, tech stack, quickstart, API section
- `docs/data_model.md` — full Phase 1 schema spec for all 7 tables
- `docs/weeklog.md` — engineering log (Day 5 entry pending)
- `BACKLOG.md` — inbox for new ideas
- `FUTURE_FEATURES.md` — deliberately deferred features
- `GLOSSARY.md` — plain-language reference for technical terms
- `tests/README.md` — test suite usage guide

### Project infrastructure
- Python virtual environment at `venv/` (gitignored)
- `pyproject.toml` — runtime deps: typer, fastapi, uvicorn. Dev deps: pytest, httpx
- `requirements.txt` mirrors runtime deps
- `.vscode/settings.json` — venv auto-activation, pytest panel, hidden cache folders
- `.gitignore` covering Python, venv, IDE, OS, data files, logs, Jupyter, .private/
- Project structure: `src/fragbro/`, `tests/`, `data/`, `docs/`, `web/`
- PowerShell execution policy set to RemoteSigned (CurrentUser scope)
- Desktop/taskbar shortcut targeting VS Code with FragBro as workspace

### Database layer (`src/fragbro/database.py`)
- SQLite, all 7 Phase 1 tables: fragrances, users, collection, wear_logs, wishlist, dna_families, fragrance_dna
- Foreign key enforcement enabled
- get_connection() and initialize_database() accept optional db_path for testability

### Catalog seed (`src/fragbro/seed.py`)
- 7 fragrances seeded, plus 4 extras from personal seed = 11 total
- 1 DNA family: Barber Shop / Fougère
- 4 dupe relationships
- All inserts idempotent

### Personal seed (`src/fragbro/seed_personal.py`)
- User abdullah created
- 4 collection entries, 4 wear logs, 3 wishlist entries

### CLI (`src/fragbro/cli.py`)
9 working commands via Typer: init, seed, seed-personal, list, show, stats, wear, collection, wishlist, wear-stats

### HTTP API (`src/fragbro/api.py`)
8 endpoints via FastAPI: GET /, GET /fragrances, GET /fragrances/{name}, GET /collection, GET /wishlist, GET /wear-stats, GET /stats, POST /wear
- Auto-generated docs at /docs
- CORS middleware configured
- Pydantic-validated POST body
- Run with: `uvicorn fragbro.api:app --reload`

### Frontend (`web/index.html`)
- Vanilla HTML + inline CSS + inline JS (no framework)
- Calls GET /fragrances on load
- Renders 11 cards with name, brand, accords, dupe relationships
- async/await, fetch, try/catch, DOM manipulation, template literals, .map().join()
- Closes browser → API → DB → JSON → DOM loop

### Test suite (`tests/`)
29 passing tests via pytest:
- tests/conftest.py — tmp_db and tmp_db_path fixtures
- tests/test_database.py — 9 tests
- tests/test_seed.py — 8 tests
- tests/test_api.py — 12 tests

## Database stats (end of Day 5)
- Fragrances: 11
- Users: 1
- Collection entries: 4
- Wear logs: 4
- Wishlist entries: 3
- DNA families: 1
- Dupe relationships: 4

## Engineering patterns used
- Dependency injection for testability (optional db_path)
- Idempotent seeds
- Two-pass insertion (NULL dupe_of_id, then UPDATE)
- Parameterized queries (no string concatenation)
- Separation of catalog vs personal data
- __main__ idiom for runnable modules
- Pydantic-validated request bodies
- One database layer, two doorways (CLI and API)
- Browser DevTools as the source of truth for frontend bugs (not VS Code Problems tab)

## Coverage so far

**SQL:** SELECT, INSERT, UPDATE, JOIN, LEFT JOIN, self-join, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, COUNT, MAX, subqueries (NOT EXISTS), parameterized queries, foreign keys, composite primary keys, julianday(), date('now', '-30 days'), CAST

**HTTP/API:** GET, POST, path parameters, JSON request/response, status codes (200/201/404/422/400), Pydantic validation, CORS, auto-generated OpenAPI docs

**JavaScript/Frontend:** fetch, async/await, try/catch, Promises, DOM manipulation (getElementById, innerHTML), template literals, arrow functions, .map() and .join(), ternary operator, browser DevTools (Console + Network tabs), CORS in browser context, URL encoding (%7D etc), Live Server workflow

## Pace

- Day 1 (May 2): Data model, README, project skeleton, glossary infra
- Day 2 (May 3): Backlog, future features, package setup, DB layer, seeds, CLI, tests
- Day 3 (May 4): VS Code workspace, seed coverage, FastAPI HTTP layer, CORS, Pydantic, API tests
- Day 4 (May 5): Venv auto-activation, taskbar shortcut, Student Pack approved
- Day 5 (May 8): First frontend, 8+ bug debug session, engineering rules v2 locked

Currently 2+ weeks ahead of original Phase 1 schedule.

## Pending admin

- Switch git remote URL to capital FragBro: `git remote set-url origin https://github.com/abdullahnyle/FragBro.git`
- GitHub Student Pack benefits — once active, claim:
  - Free .dev domain (target: fragbro.abdullah.dev)
  - Railway / Render hosting credits
  - GitHub Copilot 2-year free
  - Notion Pro

## Next session targets

1. Fix git remote URL (30 sec)
2. Day 5 weeklog entry
3. Step 6 walkthrough — line-by-line review of web/index.html JS section
4. Decide: more vanilla frontend work, or move to Vite + React for rest of P1
5. Stretch: second view (e.g. wear stats), styling polish

## Working session rules

- Always cd D:\GitHub\FragBro and verify (venv) at terminal start
- Always commit at end of every working session
- Verify behavior before committing (run pytest, check CLI, hit /docs, check frontend)
- Commit messages in present-tense imperative ("Add X", not "Added X")
- New ideas → BACKLOG.md, not the active plan
- Coursework + gym are non-negotiable; project work is bounded
- Large file pastes: delete file first, recreate empty, then paste — avoids decorator collisions