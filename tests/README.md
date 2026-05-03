# FragBro Tests

Automated tests for the FragBro codebase. Built with `pytest`.

## Running

From the project root, with the dev dependencies installed:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_database.py
```

Run a single test by name pattern:

```bash
pytest -k "foreign_key"
```

Run with verbose output:

```bash
pytest -v
```

## Conventions

- Test files live in `tests/`
- Test files start with `test_`
- Test functions start with `test_`
- Reusable fixtures live in `tests/conftest.py`
- Tests use a temporary, in-memory-style SQLite database via the `tmp_db` fixture — they never touch `data/fragbro.db`