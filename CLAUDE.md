# Working with Claude on Pattern Specular

This file tells Claude how to collaborate on this repo. It is loaded automatically every session and supersedes any general defaults.

## Project context

Pattern Specular is a longitudinal bias-pattern analysis platform for hiring and promotion writing. It is a **sovereign architectural extension** of Pattern Mirror (originally built by Bernice Koh under MIT), restructured and extended by **sm-daniyal** with a different model provider (Google Gemini), cloud-native database (Neon Serverless PostgreSQL), multi-jurisdiction statutory engine (India, Singapore, US, UK), and a new frontend design system (Rosewood / Tailwind CSS v4).

The codebase is complete and in production state: 240 backend tests pass, 251 frontend tests pass, CI is green. We are in the **Documentation Overhaul phase**. The primary goal of any session is accurate, authoritative documentation — not feature work.

Read `README.md` for product and architecture scope. Read `docs/CONVENTIONS.md` for workflow rules. Read `docs/CODE_STYLE.md` for language-level style. Read `docs/DESIGN_SPEC.md` for the product source of truth. If something we are about to do conflicts with any of those, **stop and flag it** rather than silently deviating.

## Branding and attribution — non-negotiable

- Author attribution: **sm-daniyal** throughout repository metadata, commits, and documentation.
- Zero mention of "Bernice", "UBS", or "OnePay" anywhere in UI text, code comments, commit messages, or documentation body copy. The MIT attribution to Bernice Koh is reserved strictly for `LICENSE` and the provenance section of `README.md`.
- Model references: **Google Gemini** (`gemini-2.5-flash` / `gemini-3.5-flash-lite`). Never reference Anthropic Claude in technical docs, comments, or architecture diagrams.
- Database references: **Neon Serverless PostgreSQL** (cloud, SSL, pooled). Never reference Docker-local PostgreSQL as the production setup.
- Drive boundary: all operations strictly on `D:\pattern-specular\`. Zero writes to `C:`.

## Default mode — explain as you go

For every non-trivial decision — design choice, library selection, algorithm, naming — explain:

1. **What it is** in one or two sentences.
2. **Why this way** — the constraint or principle driving the choice.
3. **The alternatives** and how they differ, briefly.
4. **What can go wrong** — the failure modes the pattern exists to prevent.
5. **Is this industry-standard?** Be honest. Distinguish widely-used practice from project-specific preference.

Compress the teaching for: trivial mechanical edits, repeated patterns (explain once, apply silently), or explicit "just ship it" signals.

## Code conventions — non-negotiable

- Follow `docs/CONVENTIONS.md` and `docs/CODE_STYLE.md` strictly. If silent on a question, ask before deciding.
- One concern per commit. Conventional Commits format.
- Never `git add .` or `git add -A`. Stage explicit paths.
- Never commit `.env` or anything resembling a secret. `GOOGLE_API_KEY` and `DATABASE_URL` never appear in code, tests, fixtures, or logs.
- Never push directly to `main`. Branch and open a PR.
- Don't skip hooks (`--no-verify`) unless explicitly asked.
- Synthetic data only — no real names or real organisational content in fixtures or issues (the seeded demo names are fictional).

## Folder rules

- `backend/` — Python/FastAPI. `src/pattern_specular/` subfolders: `api/`, `engine/`, `services/`, `models/`, `jobs/`, `db/`, `core/`.
- `frontend/` — React/TS/Vite. Components in `src/components/`; pages in `src/pages/`; design tokens in `src/styles/tokens/`.
- `docs/` — all engineering documentation; new design notes and ADRs go here.
- No `deploy/` directory — the project uses Neon cloud directly; no local Docker Compose for the database.

## Decisions made and locked

These are settled. If asked about them again, recall the decision and reason rather than relitigating.

- **Python 3.12**, **FastAPI**, **Structlog**, **Pytest**.
- **SQLAlchemy 2.0 typed API** + **Alembic**; **Neon Serverless PostgreSQL 16** (cloud, SSL, pooled).
- **LangGraph** orchestrates the seven-stage engine; **Instructor** (`instructor.from_genai`) enforces LLM output schemas.
- **Google Gemini**: `gemini-2.5-flash` for Contextual Pass, Recommendations, Drift, and Debate agents; `gemini-3.5-flash-lite` for the Judge. Multi-provider abstraction is post-MVP.
- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS v4 + TipTap, managed with `npm`. Rosewood design token system in `src/styles/tokens/`.
- **GitHub Actions CI** — Ubuntu runner, Python 3.12 + PostgreSQL 16 container for backend; Node.js 20 for frontend.
- **Engine semantics from `docs/DESIGN_SPEC.md` are binding**: the Adjudicator's verbatim span check, Fisher's-exact gating on pattern surfacing, sentence-level dismissal fingerprints, log-everything/suppress-in-UI, non-blocking flags, $k \ge 3$ HR aggregation anonymity.

## When to ask vs when to act

- **Ask first**: folder restructuring, swapping a dependency, schema changes, anything touching engine stage contracts or the privacy model (manager-only visibility, HR aggregates-only access).
- **Just do it**: bounded, reversible tasks — a described function, a clearly-identified bug, a test, a documentation section.
- **Always ask before**: destructive git operations, Alembic migrations against the live Neon DB, new top-level dependencies.

## Documentation phase rules

- Match Pattern Mirror's documentation structure and editorial style — same heading hierarchy, same table layout, same diagram patterns — but use Pattern Specular's own original voice and technical specifics throughout. Zero verbatim copying of Pattern Mirror prose.
- Every architecture doc must describe current built state. Use the ADRs to record decisions, not to describe what might be built.
- Rendered Mermaid diagrams belong in `docs/architecture/`; keep `README.md` diagrams inside `<details>` collapsible blocks.
