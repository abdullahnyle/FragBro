# FragBro

> Semantic search and recommendation over subjective product reviews — applied to fragrances.

FragBro is a decision assistant for fragrance enthusiasts. It helps you answer two practical questions: **what should I wear today?** and **should I blind-buy this bottle?** — using your own collection, your wear history, and a growing knowledge base of community reviews.

This project is built in public, in phases, as part of a long-term portfolio focused on applied machine learning and natural language processing.

---

## Status

**Currently in:** Phase 1 — Foundations
**Started:** April 2026
**Phase 1 target ship date:** Mid-2026

The project is in active early development. The data model is locked, a working CLI and HTTP API are in place, and a live demo is planned at the end of Phase 1.

---

## Why this exists

Most fragrance databases are built for one purpose: cataloging. They tell you what notes a fragrance contains, who composed it, and when it was released. They are encyclopedias.

What's missing is a tool that helps you make actual decisions:

- *I own 30 bottles. What should I wear to a humid summer evening dinner?*
- *Three reviewers say this fragrance is "barber shop classic." Is that the DNA I'm looking for, or the opposite of it?*
- *I love this $300 niche release. Is there a $30 clone that gets me 90% of the way?*

FragBro is built around those questions — not the catalog ones.

---

## Roadmap

The project follows a five-phase arc designed to grow one coherent system, rather than build disconnected demos.

| Phase | Focus | Status |
|---|---|---|
| **1. Foundations** | SQLite tracker, data model, HTTP API, deployed live | In progress |
| **2. Classical ML** | Recommender with questionnaire and blind-buy scoring | Planned |
| **3. NLP / Embeddings** | Semantic search over fragrance reviews + technical blog post | Planned |
| **4. Breadth** | Self-published benchmark evaluating embedding models | Planned |
| **5. Capstone** | Full integration and final polish | Planned |

The data model and core schema are designed to survive across phases — Phase 1 code is not throwaway.

---

## Tech stack

| Layer | Choice | Reasoning |
|---|---|---|
| Language | Python | Primary language for ML and backend |
| Database (Phase 1) | SQLite | Single file, no server, fast iteration |
| Database (Phase 2+) | PostgreSQL | Multi-user concurrency for live deployment |
| CLI | Typer | Auto-generated `--help`, type-driven commands |
| HTTP API | FastAPI + Uvicorn | Modern, type-driven, auto-generated interactive docs; same stack used for ML model serving in Phase 3 |
| Validation | Pydantic | Request body validation built into FastAPI |
| Testing | pytest | Standard, low-friction Python testing |
| Frontend | TBD (Phase 1 → 2) | Likely vanilla first, then Next.js |
| ML hosting (Phase 3+) | Hugging Face Spaces | Standard for ML model demos |
| Deployment | Railway / Render + Vercel | Free-tier friendly for student projects |

The stack is intentionally chosen to be production-realistic but achievable for a solo builder.

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/abdullahnyle/fragbro.git
cd fragbro

# Set up virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Mac/Linux

# Install dependencies (use the second form if you want to run tests)
pip install -e .
# pip install -e ".[dev]"

# Initialize and seed the database
fragbro init
fragbro seed
fragbro seed-personal

# Try the CLI
fragbro list
fragbro show Khamrah
fragbro stats
fragbro wear-stats
```

## Running the API

FragBro also exposes an HTTP API for programmatic access (and for the upcoming web frontend).

```bash
uvicorn fragbro.api:app --reload
```

Then open:
- `http://localhost:8000/docs` — interactive API documentation (try every endpoint in your browser)
- `http://localhost:8000/fragrances` — list all fragrances as JSON
- `http://localhost:8000/wear-stats` — wearing analytics

The API and CLI share the same database — you can log a wear via the CLI and see it instantly via `/wear-stats`, and vice versa.

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Health check |
| GET | `/fragrances` | List all fragrances |
| GET | `/fragrances/{name}` | Full details for one fragrance (case-insensitive) |
| GET | `/collection` | Owned fragrances sorted by rating |
| GET | `/wishlist` | Wishlist with dupe relationships |
| GET | `/wear-stats` | Wearing analytics |
| GET | `/stats` | Database summary stats |
| POST | `/wear` | Log a wear (JSON body, Pydantic-validated) |

## Tests

```bash
pip install -e ".[dev]"
pytest
```

---

## Documentation

Project documentation lives in the [`/docs`](./docs) folder.

- [Data Model — Phase 1](./docs/data_model.md) — full table-by-table schema design
- [Engineering Log](./docs/weeklog.md) — day-by-day record of what got built, lessons learned, and recoveries

Reference files in the repo root:
- [Glossary](./GLOSSARY.md) — plain-language definitions for every technical term used in the project
- [Backlog](./BACKLOG.md) — inbox for new ideas (added during a phase, evaluated at phase-shift)
- [Future Features](./FUTURE_FEATURES.md) — deferred features with reasoning

---

## About this project

FragBro is the spine project of a long-term portfolio targeting graduate study in applied machine learning. It is built deliberately — designed before coded, shipped before perfect, and documented as it grows.

Built by [@abdullahnyle](https://github.com/abdullahnyle).