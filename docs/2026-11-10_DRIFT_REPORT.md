# Drift Report: Design Specifications vs Codebase Reality
**Date:** 2026-11-10  
**Scope:** `docs/` and `docs/architecture/` design specifications compared against `backend/` and `frontend/` implementations.

---

## DESIGN_SPEC.md

* **LLM Model Allocation:** Section 3 (lines 108, 118), Section 4 (lines 162-164), and Section 10 (lines 280-284) specify `gemini-2.5-flash` for the Contextual Pass, Recommendations, Drift check, and Growth Debate Agents. In the implementation (`core/config.py` lines 58-68 and `.env`), all agent stages default to `gemini-3.5-flash-lite`.
* **Latency Tier Estimation:** Section 2 specifies Layer 2 Contextual Pass latency as ~5–8s; with `gemini-3.5-flash-lite` and streaming SSE, first flag emission is typically 1.5–3s.

## architecture/api-contracts.md

* **Authentication Endpoint Request Schema (`POST /auth/login`):** Contract specifies `{"email": "...", "role": "manager"}`. Code (`api/auth.py`, `LoginRequest`) requires `{"email": "...", "password": "...", "expected_role": "manager"}`.
* **Authentication Endpoint Response Schema:** Contract specifies `"roles": ["manager"]`. Code (`LoginUser`) returns `"role": "manager"` (singular `UserRole` enum) and adds an `"initials"` string.
* **Analysis Request Schema (`POST /analyze`):** Contract specifies `{"document_id": "uuid", "text": "...", "doc_type": "jd", "region_code": "SG"}`. Code (`api/analyze.py`, `AnalyzeRequest`) expects `{"document_id": "uuid", "content": "..."}`; `doc_type` and `region_code` are loaded directly from the database entity, not passed in the request body.
* **Server-Sent Event (SSE) Protocol Channels (`POST /analyze/stream`):** Contract documents event types: `run_started`, `flag`, `recommendations`, `done`. Code (`api/sse.py`, `format_sse`) emits `stage`, `flag` (with embedded recommendations), and `done`. Dedicated `run_started` and `recommendations` events do not exist in the stream framing.

## architecture/data-model.md

* **Missing Entities in Entity Map:** The document map and Mermaid ER diagram list 17 core entities but omit `PromotionRubricCriterion` (`models/promotion_rubric.py`), `CalibrationSample` (`models/calibration.py`), and `CalibrationRun` (`models/calibration.py`), which are active relational models in Alembic migrations and SQLAlchemy metadata.

## architecture/flags-and-suppression.md

* **Sentence Segmentation Implementation:** Section "Known limitation" states that sentence boundaries are derived from spaCy's sentence segmentation. In code (`engine/fingerprint.py`, `slice_sentence`), sentence boundaries are extracted using explicit character terminators (`.!?`) via `rfind` and `find`, bypassing spaCy sentence parsing.

## architecture/statistical-proofs.md

* **Sample Size Gating Condition ($n \ge 10$):** Section 3 states that a pattern is surfaced if and only if $p < 0.05$ AND $(a + b + c + d) \ge 10$. In code (`services/significance.py` line 44, `services/pattern_aggregator.py` lines 243, 345), only the p-value condition (`p_value < threshold`) is evaluated; there is no minimum marginal sample size constraint $(n \ge 10)$ enforced.

## architecture/llm-judge.md

* **Jurisdiction Hardcoding in System Prompt:** While ADR-0015 and the design specification establish multi-jurisdiction statutory evaluation, `engine/judge.py` (`_SYSTEM_PROMPT`) explicitly hardcodes: `"You are an independent reviewer of hiring and promotion bias flags under Singapore's TAFEP fair-employment rules."`
* **Docstring Stage Numbering:** `engine/judge.py` line 1 docstring still labels the Judge as `"Stage 4 of the engine"` (reflecting an earlier 5-stage iteration), whereas orchestrator code and design architecture place it at Stage 6.

## architecture/overview.md

No drift detected.

## architecture/dictionary-growth.md

No drift detected.

## architecture/pattern-significance.md

No drift detected.

## architecture/india-lexicon-mapping.md

No drift detected.

## architecture/learning-guide.md

No drift detected.

## references/compliance_frameworks.md

No drift detected.
