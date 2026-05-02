# FragBro Data Model — Phase 1

**Status:** Draft v1
**Last updated:** May 3, 2026

## Purpose

This document defines the data model for FragBro Phase 1. It exists so that the database structure is designed deliberately before any code is written, and so future changes are tracked against a known baseline.

## Design philosophy

- Build for Phase 1 needs, but don't block Phase 2/3 enhancements
- Use free text where human nuance matters (we'll mine patterns with NLP later)
- Use structured fields where clear categories exist
- Don't pre-build what ML will figure out from behavior data

## Tables overview

Seven tables total:

1. `fragrances` — the master catalog of all fragrances
2. `users` — registered users
3. `collection` — which user owns which fragrances
4. `wear_logs` — when and how a user wore a fragrance
5. `wishlist` — fragrances a user wants to buy
6. `dna_families` — predefined scent family categories (e.g., Barber Shop / Fougère)
7. `fragrance_dna` — many-to-many link between fragrances and DNA families

## Table definitions

### 1. `fragrances`

The master catalog. Every fragrance that exists in FragBro lives here.

| Field | Type | Required | Example | Notes |
|---|---|---|---|---|
| `id` | integer | yes | 1 | Auto-incremented primary key |
| `name` | text | yes | "Khamrah" | |
| `brand` | text | yes | "Lattafa" | |
| `release_year` | integer | no | 2022 | |
| `description` | text | no | "A warm, spicy gourmand..." | For Phase 3 NLP embeddings |
| `top_notes` | text | no | "Cinnamon, nutmeg" | Comma-separated |
| `heart_notes` | text | no | "Mahanad, praline" | |
| `base_notes` | text | no | "Vanilla, tonka, benzoin" | |
| `accords` | text | no | "Sweet, spicy, warm" | |
| `dupe_of_id` | integer | no | 412 | Foreign key to another fragrance — only filled if this is a clone |

### 2. `users`

| Field | Type | Required | Example | Notes |
|---|---|---|---|---|
| `id` | integer | yes | 1 | |
| `username` | text | yes | "abdullah" | |
| `email` | text | yes | "abdullah@example.com" | |
| `created_at` | datetime | yes | 2026-05-03 19:00 | |

### 3. `collection`

A row exists for every (user, fragrance) pair where the user owns that fragrance.

| Field | Type | Required | Example | Notes |
|---|---|---|---|---|
| `id` | integer | yes | 1 | |
| `user_id` | integer | yes | 1 | Foreign key → users |
| `fragrance_id` | integer | yes | 88 | Foreign key → fragrances |
| `bottle_size_ml` | integer | no | 100 | |
| `purchase_date` | date | no | 2025-11-12 | |
| `personal_rating` | integer | no | 8 | 1-10 scale |
| `unworn_reason` | text | no | "Outshone by Qahwa — same lane, better execution." | Free text, captures human nuance |

### 4. `wear_logs`

A row per wearing event. Powers Phase 2 ML and gives users a wear history.

| Field | Type | Required | Example | Notes |
|---|---|---|---|---|
| `id` | integer | yes | 1 | |
| `user_id` | integer | yes | 1 | |
| `fragrance_id` | integer | yes | 88 | |
| `wear_date` | date | yes | 2026-05-03 | |
| `occasion` | text | no | "office" | |
| `weather` | text | no | "warm and humid" | |
| `performance_rating` | integer | no | 7 | How it performed *that day* |
| `mood` | text | no | "confident" | |

### 5. `wishlist`

| Field | Type | Required | Example | Notes |
|---|---|---|---|---|
| `id` | integer | yes | 1 | |
| `user_id` | integer | yes | 1 | |
| `fragrance_id` | integer | yes | 77 | |
| `added_date` | date | yes | 2026-05-03 | |
| `notes` | text | no | "Smelled at a friend's, want for summer" | |
| `blind_buy_safe` | boolean | no | true | Phase 2 will fill this with ML predictions |

### 6. `dna_families`

Predefined scent DNA categories. Seeded once with a fixed list (Barber Shop / Fougère, Sweet Oriental, Aquatic Fresh, etc.).

| Field | Type | Required | Example | Notes |
|---|---|---|---|---|
| `id` | integer | yes | 1 | |
| `name` | text | yes | "Barber Shop / Fougère" | |
| `description` | text | no | "Spicy lavender + fresh aromatics. Classic men's grooming DNA — Brut, Azzaro Pour Homme, Drakkar Noir." | |
| `era_peak` | text | no | "1970s–1990s" | |

### 7. `fragrance_dna`

Links fragrances to their DNA families. A fragrance can belong to multiple families.

| Field | Type | Required | Example | Notes |
|---|---|---|---|---|
| `fragrance_id` | integer | yes | 88 | |
| `dna_family_id` | integer | yes | 1 | |

## Relationships diagram

The seven tables connect through five core relationships:

- **users → collection → fragrances**: a user owns fragrances (a row in `collection` is one user owning one fragrance)
- **users → wear_logs → fragrances**: a user wears a fragrance on a given date (one row per wearing event)
- **users → wishlist → fragrances**: a user wants to buy a fragrance
- **fragrances → fragrance_dna → dna_families**: a fragrance belongs to one or more DNA families (many-to-many)
- **fragrances → fragrances**: a fragrance can be a dupe of another fragrance (self-link via `dupe_of_id`)

In one sentence: every relationship between a user and a fragrance flows through a middle table (`collection`, `wear_logs`, or `wishlist`), and fragrances themselves are categorized by DNA family and optionally linked to the original they clone.

## Decisions explicitly NOT made yet

- **Vibe tags system** — to be detailed in a separate spec when we hit it
- **Image storage for fragrance bottles** — Phase 1.5 or later
- **Authentication strategy** — Phase 2

## Storage choice

- **Phase 1:** SQLite (single file, no server, beginner-friendly)
- **Phase 2 onward:** Migrate to PostgreSQL when web app needs multi-user concurrency

## Worked example: 5 real fragrances

Stress-tested against the model:

1. **J. Janan Platinum** — daily wear, vibe tags: clean, simple, soapy
2. **Lattafa Khamrah** — owned, low wear, `unworn_reason`: "Outshone by Qahwa — less headache-inducing"
3. **Kaaf by Ahmed al Maghribi** — wishlist, `dupe_of_id` → PDM Percival
4. **Liquid Brun by French Avenue** — owned, `dupe_of_id` → PDM Althair
5. **Rasasi Fattan** — owned, `fragrance_dna` → Barber Shop / Fougère