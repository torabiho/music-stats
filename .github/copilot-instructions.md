# Copilot Instructions for music-stats

## Project Overview
- **music-stats** is a monorepo with two main components:
  - `api/`: Python FastAPI backend with SQLAlchemy models and Alembic migrations.
  - `web/`: Next.js frontend (TypeScript) bootstrapped with `create-next-app`.

## Architecture & Data Flow
- **Backend (`api/`)**
  - Entrypoint: `api/app/main.py` (FastAPI app)
  - Database: PostgreSQL (see `docker-compose.yml` in `infra/`)
  - ORM: SQLAlchemy models in `api/app/models.py`
  - Migrations: Alembic (`api/migrations/`)
  - Config: `api/app/config.py`
- **Frontend (`web/`)**
  - Entrypoint: `web/src/app/page.tsx`
  - Uses Next.js App Router and TypeScript
  - Static assets in `web/public/`

## Developer Workflows
- **Backend**
  - Run locally: (from `api/`)
    ```bash
    uvicorn app.main:app --reload
    ```
  - Run DB migrations:
    ```bash
    alembic upgrade head
    ```
  - Connect to DB (Docker):
    ```bash
    docker exec -it music_postgres psql -U music_user -d music_db
    ```
- **Frontend**
  - Run locally: (from `web/`)
    ```bash
    npm run dev
    ```

## Conventions & Patterns
- **Backend**
  - All DB access via SQLAlchemy models in `models.py`
  - App config via `config.py` (env vars, settings)
  - Migrations tracked in `migrations/versions/`
- **Frontend**
  - Use Next.js conventions for routing and components
  - Global styles in `web/src/app/globals.css`

## Integration Points
- API endpoints exposed by FastAPI (`main.py`) are consumed by the Next.js frontend
- Database is managed via Docker Compose (`infra/docker-compose.yml`)

## Examples
- To add a new DB table: update `models.py`, create Alembic migration, run `alembic upgrade head`
- To add a new page: create a file in `web/src/app/`

---

**For AI agents:**
- Prefer explicit imports and clear separation between backend and frontend code.
- Reference this file and the respective `README.md` files for more details on each component.
