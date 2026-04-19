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