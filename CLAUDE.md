# Pattern Specular — Development Guide

## Philosophy & Core Directives

1. **Mirror, Not Judge:** Pattern Specular surfaces longitudinal patterns in hiring and promotion writing with cited statutory and academic evidence. It never penalises, computes punitive bias scores, or acts as a hiring gate.
2. **Private by Architecture:** A manager's individual writing is visible only to that manager. The HR portal provides firm-wide aggregates only with strict $k \ge 3$ k-anonymity suppression enforced at the database query layer.
3. **Deterministic First, Agentic Second:** Fast statutory flags execute deterministically in milliseconds with zero LLM cost (Stage 1 Dictionary). The LLM contextual pass (Stage 2) and multi-sample Judge (Stage 6) run asynchronously after a typing pause.
4. **Verbatim Provenance:** Hallucinations cannot reach the manager. The Adjudicator module drops any LLM-claimed span that does not exist verbatim in the source document. Every surviving flag must carry a verified citation.

---

## Tech Stack

- **Backend:** Python 3.12, FastAPI, LangGraph, SQLAlchemy 2.0, Alembic, Pydantic v2 Settings, Structlog.
- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS v4, TipTap (ProseMirror), TanStack Router & TanStack Query.
- **AI / LLM:** Google Gemini 3.5 Flash Lite via `instructor.from_genai` with `strict=False` StrEnum coercion.
- **Database:** Neon Serverless PostgreSQL 16 (`patternSpecularDB`).
- **NLP / Stats:** spaCy (`en_core_web_sm`), scipy (`scipy.stats.fisher_exact`).

---

## Common Commands

### Backend (from `backend/`)
```powershell
.\venv\Scripts\Activate.ps1
# Run API server
uvicorn pattern_specular.main:create_app --factory --reload

# Migrations
alembic upgrade head

# Re-seed demo data
python -m pattern_specular.jobs.seed_demo

# Run tests
pytest
```

### Frontend (from `frontend/`)
```powershell
npm install
npm run dev      # http://localhost:5173
npm run build    # Typecheck (tsc -b) + Vite production build
npm test         # Vitest unit tests
```

---

## Active Test Logins

| Name | Email | Role | Portal |
|---|---|---|---|
| SM Daniyal | `sm.daniyal@example.com` | Manager | `/jd-studio`, `/feedback-checkpoint`, `/pattern-dashboard`, `/promotion-writeup` |
| Areesha Naaz | `areesha.naaz@example.com` | Manager | Manager Portal |
| Patrick Jane | `patrick.jane@example.com` | Manager | Manager Portal |
| Wayne Rigsby | `wayne.rigsby@example.com` | Manager | Manager Portal |
| Kimbal Cho | `kimbal.cho@example.com` | Manager | Manager Portal |
| Grace Van Pelt | `grace.vanpelt@example.com` | Manager | Manager Portal |
| Teresa Lisbon | `teresa.lisbon@example.com` | **HR** | `/hr`, `/hr/dictionary-review` |

*Password for all accounts:* `password`
