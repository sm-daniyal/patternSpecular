# ADR 0016: Cloud-Native Serverless PostgreSQL (Neon) over Local Docker

**Date:** 2026-08-03
**Status:** Accepted

## Context

Pattern Mirror used a local Docker Compose PostgreSQL container as its development and
test database. Pattern Specular needed to reconsider this approach for three reasons:

1. **Developer environment portability.** Local Docker requires hardware-assisted
   virtualisation (Intel VT-x or AMD-V enabled in BIOS). On some development machines
   this is disabled or unavailable, blocking the entire local dev path.
2. **Connection pooling requirements.** The SSE streaming path (`POST /analyze/stream`)
   opens a persistent server-side connection per active editor session. Multiple
   concurrent streaming sessions against a local Docker Postgres will exhaust the
   default connection limit quickly, even in development.
3. **Migration verification.** Alembic `upgrade head` runs against the actual
   production-shaped database needed to be reliable without spinning up a local daemon.

Alternatives considered:

- **Keep local Docker Compose** — not viable given the hardware virtualisation
  dependency and connection limit problems.
- **SQLite for dev, Postgres for CI** — rejected. SQLite differences (e.g. no array
  types, different constraint handling) mean tests pass locally and fail in CI, which
  is exactly the failure mode the CI pipeline exists to catch.
- **Neon Serverless PostgreSQL** — PostgreSQL 16, fully managed, SSL-required pooled
  connections via `psycopg` v3 binary driver, free tier sufficient for development and
  staging, instant branching for migration dry-runs.

## Decision

Adopt **Neon Serverless PostgreSQL** as the sole database provider for development,
staging, and production.

Configuration:

- `DATABASE_URL` contains the Neon pooled connection string (`*.aws.neon.tech`).
- `sslmode=require` enforced on every connection.
- `psycopg` v3 binary driver for async compatibility with FastAPI and SQLAlchemy 2.0.
- `@pytest.mark.db` tests run against a PostgreSQL 16 service container in CI (GitHub
  Actions); they are safely skipped in environments without a database URL.

## Consequences

- **No local daemon.** A developer with `DATABASE_URL` in `.env` is immediately
  operational — no Docker, no BIOS configuration.
- **Connection pooling.** Neon's pooler handles concurrent SSE sessions without
  exhausting Postgres connection limits.
- **Test isolation.** CI spins up a fresh PostgreSQL 16 container per workflow run,
  migrates to `head`, seeds, runs, tears down — identical behaviour to a full Neon
  environment without hitting the live cloud database in CI.
- **Schema source of truth.** The Alembic migration history (20 revisions, current
  head: `0020_india_region_lexicon`) remains the schema source of truth. Model classes
  are derived, not authoritative.
