# Pattern Specular — Comprehensive Context Document

> **For Claude (or any AI assistant starting a new session):**  
> This document provides the complete, authoritative context of the **Pattern Specular** repository, its current architectural state, recent progress, technical constraints, and exact instructions for the upcoming **Documentation Overhaul** phase.

---

## 1. Project Overview & Identity

* **Project Name**: `Pattern Specular`
* **Local Workspace**: `D:\pattern-specular\`
* **GitHub Repository**: `sm-daniyal/patternSpecular` (Private Repository)
* **Author / Sovereign Owner**: `sm-daniyal` (Syed Daniyal)
* **Lineage & Origin**: Sovereign architectural evolution of *Pattern Mirror* (originally developed by Bernice Koh under MIT License).
* **Core Strict Branding Rules**:
  * **Author Attribution**: `sm-daniyal` throughout repository, package metadata, commits, and UI.
  * **Zero Leaks**: Absolute zero mention of "Bernice", "UBS", or "OnePay" in UI text, code comments, or commit messages (clean, standard MIT license attribution to Bernice Koh is reserved strictly for `LICENSE` / `README.md` attribution lines).
  * **Drive Boundary**: All code and operations strictly live on `D:\pattern-specular\`. Zero operations on `C:` drive.
  * **Production Model**: Google Gemini (`gemini-2.5-flash` / `gemini-3.5-flash-lite` via `google-genai` and `instructor`), replacing legacy Anthropic Claude references in backend engine and docs.

---

## 2. Current Implementation State (90% Complete)

Every single functional and testing requirement has been built, verified, and pushed to `main`:

### A. Backend Architecture & Test Suite (100% Complete)
* **Framework**: FastAPI + SQLAlchemy 2.0 + Pydantic v2 + Alembic + LangGraph + Structlog.
* **Database**: Live cloud **Neon Serverless PostgreSQL** (`patternSpecularDB`), with connection pooling and SSL mode required.
* **Alembic Migrations**: All migrations applied to `head`, including `0020_india_region_lexicon.py`.
* **Backend Test Suite Status**: **`240 passed, 317 skipped, 0 failed`** in ~14.7s across all 76 test files (`889837b`).
  * Unit/in-memory tests: 100% pass rate.
  * DB-marked tests: Safely skipped when offline, fully pass in disposable CI containers.
* **Standard Build System**: Configured PEP 518 `[build-system]` (`setuptools.build_meta`) in `pyproject.toml` (`783ae5a`).

### B. Multi-Jurisdiction Statutory Engine
* Evaluates job descriptions, candidate feedback, and promotion writeups **simultaneously** across 4 major legal jurisdictions:
  1. **India (`IN`)**: *Code on Wages 2019*, *Rights of Persons with Disabilities (RPwD) Act 2016*, *Transgender Persons (Protection of Rights) Act 2019*.
  2. **Singapore (`SG`)**: *TAFEP (Tripartite Alliance for Fair & Progressive Employment Practices)* guidelines.
  3. **United States (`US`)**: *EEOC Title VII*, *Age Discrimination in Employment Act (ADEA)*.
  4. **United Kingdom (`UK`)**: *Equality Act 2010*.
* **2-Pass Architecture**:
  * **Pass 1 (Deterministic AST Lemmatizer)**: spaCy `en_core_web_sm` matching lemmas against the regional dictionary tables with regex boundary enforcement.
  * **Pass 2 (Contextual LLM Judge)**: Evaluates borderline context, intent, and sentiment using Gemini, adjudicating false positives and generating contextual recommendations.

### C. Frontend Architecture & Design (100% Complete)
* **Tech Stack**: React 19 + Vite + TypeScript + Tailwind CSS v4 + TanStack Router + TanStack Query + TipTap Editor.
* **Visual Theme — Rosewood (Pink Shades / Dark Peach)**:
  * Primary Accent / Buttons: `#b83a58` (Rosewood), hover `#9c2742`, soft blush tint `#fbf2f4`.
  * Canvas & Surfaces: `#f7f3f4` workspace canvas, `#ffffff` card surface, `#ebdce2` hairline borders.
  * Ink / Text: Deep plum-charcoal `#1e1317` with secondary `#6e5860`.
* **Branding & Logo**: Geometric prism/diamond SVG logo (`psLogo`) displayed adjacent to the bold **Pattern Specular** wordmark in Outfit font.
* **Card & Typography Sizing**: Standard generous dimensions matching Pattern Mirror (`px-11 py-10`, `max-w-[480px]` login card, body typography `--text-body: 16px`, title `24px`).
* **Active Draft Persistence**: JD Studio drafts persist across tab switches in localStorage without accidental clearing.
* **Vitest Suite**: **251 passed, 0 failed** in ~21s. Production build compiles in ~473ms.

### D. GitHub Actions CI Pipeline
* **Status**: **100% Green** across all runs (`36 workflow runs`, latest `783ae5a` passed).
* `backend (lint, types, tests)`: Ubuntu runner with PostgreSQL 16 container, Python 3.12, ruff, mypy, pytest.
* `frontend (lint, test, build)`: Node.js 20, npm install, eslint, vitest, production build (`npm run build`).

---

## 3. Active User Roster in Database

### HR Administrator (1):
* **Teresa Lisbon** (`teresa.lisbon@example.com`) — *Department: Human Resources*

### Managers (6):
1. **SM Daniyal** (`sm.daniyal@example.com`) — *Department: Engineering*
2. **Areesha Naaz** (`areesha.naaz@example.com`) — *Department: Engineering*
3. **Patrick Jane** (`patrick.jane@example.com`) — *Department: Investigations*
4. **Wayne Rigsby** (`wayne.rigsby@example.com`) — *Department: Operations*
5. **Kimball Cho** (`kimbal.cho@example.com`) — *Department: Compliance*
6. **Grace Van Pelt** (`grace.vanpelt@example.com`) — *Department: Data Analytics*

*(Password for mock auth: any non-empty string, e.g. `password` or `123456`)*.

---

## 4. Immediate Objective: Phase 6 Documentation Overhaul

The code, styling, tests, and CI are finished. The final phase is the **Documentation Overhaul & Walkthrough**:

### What Needs to be Done:
1. **Document Refactoring**:
   * `docs/DESIGN_SPEC.md`
   * `docs/CONVENTIONS.md`
   * `README.md`
   * Architecture documents (`docs/architecture/*.md`)
   * Architectural Decision Records (`docs/adr/`)
2. **User's Input & Analogy**:
   * The user (`sm-daniyal`) will provide a specific **analogy** and compliance guidelines for how the system should be explained in the docs.
   * The user will share reference files one-by-one.
3. **Interactive Learning & Walkthrough**:
   * Along with updating each document, explain the underlying architecture, design rationale, and interview talking points to prepare the user to explain and defend every layer of the system.

---

## 5. Directory Reference Map

```text
D:\pattern-specular\
├── .github\workflows\ci.yml        # GitHub Actions CI workflow
├── backend\
│   ├── pyproject.toml              # Python project & dev dependencies
│   ├── .env                        # Neon DB & Google API keys
│   ├── src\pattern_specular\
│   │   ├── api\                    # FastAPI endpoints (analyze, documents, hr, patterns, etc.)
│   │   ├── core\                   # Settings, exceptions, logging
│   │   ├── db\                     # SQLAlchemy Base, session, Alembic migrations
│   │   ├── engine\                 # AST dictionary, contextual pass, LLM judge, recommendations
│   │   ├── models\                 # 17 SQLAlchemy models
│   │   └── services\               # Business logic, drift detection, pattern aggregator
│   └── tests\                      # 76 backend test files (240 passed)
├── frontend\
│   ├── package.json
│   ├── src\
│   │   ├── components\             # UI components, TopBar, AppShell, Editor
│   │   ├── pages\                  # JD Studio, Feedback, Promotion, Dashboard, HR Portal
│   │   ├── styles\tokens\          # CSS theme variables (Rosewood palette)
│   │   └── lib\                    # Auth, API client, hooks
└── docs\                           # Documentation directory to be overhauled
```
