# FragBro

A fragrance decision assistant, semantic search and recommendation over subjective product reviews, applied to fragrances. This was meant to be the spine of an 18-month portfolio, with a 5-phase roadmap: SQLite and a FastAPI backend first, then a real frontend, then a move to PostgreSQL and a live launch.

**I'm not actively building this anymore.** My focus shifted toward health data, which is where `label-vs-reality` came from, and FragBro didn't fit alongside it. This wasn't a project that stalled or broke. It was working, and I chose to put my time into something else instead.

## What actually got built

7 SQLite tables covering fragrances, users, collections, and wear logs, with a many-to-many relationship for scent-family tagging and a self-reference for tracking cheaper dupes of a given fragrance. A FastAPI backend with a real HTTP API, auto-generated docs, and CORS set up for local frontend work. A pytest suite that never touched the real database, using fixtures and a throwaway test DB. A frontend that started in vanilla HTML and JS and got migrated to Vite and React partway through, once the next feature I wanted to build (a matching questionnaire) needed real form state that vanilla JS wasn't going to handle well. And a working analytics view, wear counts, most-worn fragrances, longest-untouched items, all pulled from real logged data.

## What didn't happen

Everything past Phase 1. No move to PostgreSQL, no semantic search over reviews (the actual "recommendation" half of the idea), no questionnaire. It stopped mid-way through the frontend migration.

## The site's still up

[fragbro.vercel.app](https://fragbro.vercel.app) is still live and shows real data I logged. It's slow and I'm not maintaining it, so if you land there after finding this repo, that's expected.

## If you're looking at the code

`src/fragbro/` is the backend, `frontend/` is the React rewrite in progress, `web/` is the older vanilla JS version it was replacing, `tests/` is the test suite, `data/` is the database. `docs/` has notes from each build session, and `GLOSSARY.md` is a running list of things I looked up and explained to myself as I went, mostly useful if you're learning this stack for the first time.

## License

MIT.
