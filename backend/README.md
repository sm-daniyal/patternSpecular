# pattern-specular backend

Python 3.12 / FastAPI service for the Pattern Specular analysis engine and API.

## Prerequisites

- Python 3.12
- Neon Serverless PostgreSQL 16 (or reachable PostgreSQL database via `DATABASE_URL`)
- Google Gemini API key (`GOOGLE_API_KEY`)

## Setup

All backend commands run from this `backend/` directory:

```bash
cd backend
```

1. **Create your `.env`** from the template (it lives here in `backend/` and is
   loaded relative to this directory):

   ```bash
   cp .env.example .env            # PowerShell: Copy-Item .env.example .env
   ```

   Configure your `DATABASE_URL` (Neon pooled connection string with `sslmode=require`)
   and `GOOGLE_API_KEY`.

2. **Install dependencies** in a virtual environment:

   ```bash
   python -m venv venv
   # Linux/macOS:
   source venv/bin/activate
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1

   pip install -e ".[dev]"
   python -m spacy download en_core_web_sm
   ```

3. **Apply migrations** to reach the full schema (20 revisions, head `0020_india_region_lexicon`):

   ```bash
   alembic upgrade head
   ```

## Database and migrations

- **Schema source of truth is the Alembic migration history**, not the model
  classes. Models live in `src/pattern_specular/models/`; the migrations in
  `src/pattern_specular/db/migrations/versions/`.
- Verify model and migration consistency:

  ```bash
  alembic check          # fails if models and migrations disagree
  alembic upgrade head   # applies latest migrations
  ```

- Multi-jurisdiction statutory lexicons (IN, SG, US, UK) are seeded via migrations
  (including `0020_india_region_lexicon.py`).

## Run

```bash
uvicorn pattern_specular.main:create_app --factory --reload
```

The `--factory` flag tells uvicorn to call `create_app()` to build the app, so importing the module has no side effects but missing configuration variables abort boot cleanly.

- Healthcheck: <http://localhost:8000/health>
- API docs (Swagger UI): <http://localhost:8000/docs>

## Checks

```bash
ruff check src tests       # lint
ruff format src tests      # format
mypy src                   # strict type-check
pytest                     # run backend tests (240 unit/integration tests)
```
