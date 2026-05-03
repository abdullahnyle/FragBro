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