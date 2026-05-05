# Glossary

A plain-language reference for technical terms used in this project. Terms are added as they appear in the build — this glossary grows with FragBro.

---

## Git and GitHub

**Repository (repo)**
A project's folder, tracked by Git, usually hosted on GitHub. The whole FragBro project lives in one repo.

**Commit**
A saved snapshot of the project at a point in time, with a message describing what changed. Every commit is a permanent waypoint in the project's history.

**Push**
Sending your local commits up to GitHub so they're visible online and backed up.

**Stage (git add)**
Telling Git which changes to include in the next commit. Changes can be made without committing — staging is the "ready to be committed" state.

**Untracked file**
A file Git has noticed but is not actively tracking yet. Becomes tracked once it's staged and committed.

**Branch**
A parallel line of development. The default branch is usually called `main`. Feature work happens on separate branches and gets merged back into `main`.

**`.gitignore`**
A file that tells Git which files to ignore. Used to exclude data files, secrets, system junk, and IDE config from the repo.

**`.gitkeep`**
An empty placeholder file. Used to force Git to track an otherwise-empty folder, since Git doesn't track empty folders by default.

**Personal Access Token**
A password substitute used to authenticate Git operations against GitHub. More secure than a password, can be revoked individually.

---

## Files and formats

**Markdown (`.md`)**
A plain-text format using simple symbols (`#`, `|`, `-`) to represent headers, tables, and lists. GitHub renders Markdown into formatted documents automatically.

**README**
The front-page document of a project. GitHub displays it below the file list when someone visits the repo URL. Must live at the root of the repo.

**`requirements.txt`**
A standard Python file listing every external package the project depends on, with versions. Other developers (and deployment systems) read this file to install the right dependencies.

**`pyproject.toml`**
The modern standard configuration file for a Python project. Declares the project's name, version, dependencies, scripts, and which folders contain code. FragBro uses this to register the `fragbro` CLI command and to declare runtime vs dev dependencies.

**JSON**
A simple text format for representing structured data — basically a dictionary written out as text. Used everywhere on the web for sending data between programs. The HTTP API returns JSON; the browser displays it.

---

## Databases

**Database**
An organized place to store data. Different kinds exist for different needs.

**SQLite**
A database that lives inside a single file. No server needed, no installation — just a `.db` file on disk. Used in FragBro Phase 1 for simplicity.

**PostgreSQL**
A more powerful database that runs as a server and handles many users at once. FragBro will migrate to PostgreSQL in Phase 2 when the app goes live.

**Table**
A structured collection of rows and columns inside a database — like a spreadsheet, but with strict types. FragBro has 7 tables (fragrances, users, collection, etc.).

**Field (or column)**
A single piece of information in a table — for example, the `name` field of the `fragrances` table.

**Row (or record)**
A single entry in a table — for example, one specific fragrance like "J. Janan Platinum."

**Primary key**
A unique number that identifies each row. In FragBro, every table uses an `id` field as its primary key.

**Foreign key**
A field in one table that points to a row in another table. For example, `dupe_of_id` in the `fragrances` table is a foreign key pointing to the original fragrance.

**One-to-many relationship**
One row in table A can be linked to many rows in table B, but each row in B links back to only one row in A. Example: one user has many wear logs.

**Many-to-many relationship**
Rows in table A and rows in table B can both link to multiple rows in the other. Requires a third "linking" table to express. Example: a fragrance belongs to multiple DNA families, and each DNA family contains multiple fragrances — connected through the `fragrance_dna` table.

**Schema**
The overall design of a database — which tables exist, what fields each has, and how they relate to each other.

---

## Web and APIs

**HTTP**
The protocol the web speaks. When a browser requests a page, it sends an "HTTP request" and the server sends back an "HTTP response." FragBro's API uses HTTP.

**Localhost**
Your own computer, when programs on it talk to each other over the network. Same thing as the address `127.0.0.1`. When you run the FragBro server, it listens at `http://localhost:8000` — only programs on your machine can reach it.

**Port**
A number that distinguishes different programs running on the same machine — like an apartment number. FragBro's dev server uses port `8000`, which is the FastAPI/Uvicorn convention.

**Endpoint**
A single URL the API responds to. Each endpoint = one Python function. `/fragrances` is one endpoint, `/wear-stats` is another. Together they make up the API.

**GET**
The HTTP verb for "give me data" — read-only, no changes. Most FragBro endpoints are GET.

**POST**
The HTTP verb for "create something new." `POST /wear` creates a new wear log entry.

**Status code**
A 3-digit number an HTTP response includes to indicate what happened. `200 OK` = success. `201 Created` = something new was created. `404 Not Found` = the thing you asked for doesn't exist. `422 Unprocessable Entity` = your request body failed validation. `500 Internal Server Error` = the server crashed.

**JSON body**
The data sent along with a POST/PUT/PATCH request, formatted as JSON. The body of `POST /wear` looks like `{"name": "Fattan", "occasion": "uni"}`.

**Path parameter**
A piece of data captured directly from inside the URL. In `/fragrances/{name}`, whatever appears in place of `{name}` gets passed to the function as the `name` argument.

**FastAPI**
The Python web framework FragBro uses to build its HTTP API. Modern, type-driven, and famous for auto-generating interactive documentation at `/docs`. Same framework used to serve ML models in production.

**Uvicorn**
The actual server program that runs FastAPI applications. FastAPI is the recipe; Uvicorn is the kitchen that cooks the orders. Run with `uvicorn fragbro.api:app --reload`.

**Pydantic**
A library FastAPI uses to validate incoming data. You write a Python class describing the expected shape of a request body; Pydantic checks that incoming requests match it before your code runs. Missing required field → automatic 422 response, no hand-rolled validation.

**CORS (Cross-Origin Resource Sharing)**
A browser security rule that, by default, prevents a webpage on one origin (e.g. `localhost:5173`) from calling an API on another origin (e.g. `localhost:8000`). Servers explicitly opt-in via CORS headers to allow it. FragBro's API enables CORS in dev so the upcoming frontend can call it.

**Decorator**
The `@something` syntax in Python that goes on the line above a function. It wraps the function with extra behavior. `@app.get("/fragrances")` tells FastAPI to register the function below it as the handler for GET requests at that URL.

**Auto-generated docs**
The interactive web page FastAPI creates at `/docs` showing every endpoint, what arguments they take, and a "Try it out" button to send live requests. Generated automatically from the type hints on the endpoint functions — no manual documentation needed.

---

## Testing

**pytest**
The standard Python testing framework. Auto-discovers any function starting with `test_` in any file starting with `test_` and runs them. FragBro uses pytest for all its tests.

**Fixture**
A reusable setup function for tests. Defined with `@pytest.fixture`. FragBro's `tmp_db` fixture creates a fresh throwaway database for each test that uses it, so tests never touch the real `data/fragbro.db` file.

**TestClient**
A FastAPI tool that pretends to be a browser and calls your endpoints directly in-process. Lets you test the API without spinning up a real server, and without using a real port.

**monkeypatch**
A pytest tool that temporarily replaces a function with a test version, then restores it after the test ends. FragBro uses it to redirect API endpoints to a test database during testing.

**Idempotent**
A property of an operation: running it twice produces the same result as running it once. FragBro's seed scripts are idempotent — re-running them won't create duplicate fragrances.

---

## Project terms

**FragBro**
A fragrance decision assistant — semantic search and recommendation over subjective product reviews, applied to fragrances. The spine project of an 18-month portfolio.

**Phase**
A defined stage of the FragBro roadmap with specific goals and a defined ship target. The project has 5 phases over ~18 months.

**DNA family**
A scent identity category (e.g., "Barber Shop / Fougère") that captures the overall character of a fragrance, distinct from its individual notes. A fragrance can belong to multiple DNA families.

**Vibe tag**
A human-language descriptor of how a fragrance feels in use ("clean," "soapy," "headache-inducing"). Captures user-experienced reality, distinct from a perfumer's note pyramid.

**Backlog**
The inbox file (`BACKLOG.md`) where new ideas are captured during a phase. Items are evaluated only at phase-shift checkpoints, never mid-phase.