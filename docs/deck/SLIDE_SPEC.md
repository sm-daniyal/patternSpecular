# Pattern Specular — 17-Slide Presentation Specification

> **Deck Title:** Pattern Specular — A Longitudinal Bias-Pattern Analysis Tool for Managers  
> **Author:** `sm-daniyal` (Syed Daniyal)  
> **Repository:** [`sm-daniyal/patternSpecular`](https://github.com/sm-daniyal/patternSpecular)  
> **Design Format:** 16:9 Landscape Widescreen (1920 × 1080)

---

### Slide 01: Title Slide
* **Header / Logo:** Geometric Diamond Prism Logo + `Pattern Specular` wordmark in Outfit typography.
* **Title:** The Pattern Specular
* **Subtitle:** A longitudinal bias-pattern analysis platform for hiring and talent management writing.
* **Callout Box:** *"Surfaces bias patterns in a manager's own writing, with statutory and academic evidence, so they can decide what to change."*
* **Footer:** Applied-AI & Full-Stack Portfolio Project · Designed & Built by sm-daniyal · Slide 01 / 17

---

### Slide 02: About the Author
* **Title:** About the Author
* **Profile:** sm-daniyal (Syed Daniyal)
* **Role / Focus:** Full-Stack & Applied-AI Software Engineer.
* **Domain:** Enterprise Systems, NLP Pipelines, Statistical Data Modeling, and Modern React/FastAPI Architectures.
* **Project Mission:** Engineering an autonomous, privacy-preserving compliance system that solves the longitudinal bias visibility gap in corporate talent writing.
* **Footer:** Slide 02 / 17

---

### Slide 03: Contents (Agenda)
* **Columns:**
  1. **The Product:**
     * 04 Why it exists (The Motivation)
     * 05 What it does (Evidence in, decision theirs)
     * 06 Writing tools for managers (JD Studio, Feedback Checkpoint, Promotion Writeup)
     * 07 Seeing your own patterns (Longitudinal Fisher's exact gating)
     * 08 The HR view (Firm aggregates & $k \ge 3$ privacy)
  2. **The Engineering:**
     * 09 Inside the bias-detection engine (7-stage hybrid state graph)
     * 10 LLM as a Judge (Multi-sample consensus confidence gating)
     * 11 Research behind the Judge (Published ML research foundations)
     * 12 How the dictionary grows itself (4-agent autonomous debate loop)
     * 13 Architecture & tech stack (FastAPI + React 19 + Neon PostgreSQL)
     * 14 The data model (Relational privacy and audit trails)
  3. **Wrap-up:**
     * 15 Version 2 roadmap (Architectural seams)
     * 16 Engineering learnings & production practices
     * 17 Repository & contact
* **Footer:** Slide 03 / 17

---

### Slide 04: Motivation — Where Bias Training Stops, This Begins
* **Headline:** "Where bias training stops, this begins."
* **Point 01 (The Gap):** Managers complete fair-hiring and unconscious bias training, but nothing verifies whether it alters the job descriptions, interview feedback, and promotion justifications they produce. Training is theoretical; writing is where decisions are codified.
* **Point 02 (The Insight):** Bias in writing is a longitudinal pattern. Any single document appears unremarkable or borderline; the tendency only emerges across 20+ documents over time.
* **Point 03 (The Response):** Pattern Specular flags statutory and coded bias in real-time, checks writeups against reference criteria (JD skills / promotion rubrics), and surfaces longitudinal tendencies mathematically.
* **Footer:** Slide 04 / 17

---

### Slide 05: What It Does — Evidence In, Decision Theirs
* **Concept:** A flag marks a specific span with plain-English reasoning and citations. The manager retains 100% decision autonomy.
* **What it does:**
  * *Every flag is cited:* Cites statutory acts (India Code on Wages 2019, RPwD Act 2016; Singapore TAFEP; US EEOC; UK Equality Act 2010) or peer-reviewed research. Unbacked flags are dropped.
  * *Patterns are statistically significant:* Tendencies are only surfaced when passing Fisher's Exact Test ($p < 0.05$).
  * *HR sees aggregates only:* Firm-level trends with zero access to individual manager text.
* **Design Invariants:**
  * *Mirror, not judge:* Never scores, never penalizes.
  * *Private by architecture:* Structural schema isolation; no query path from HR to drafts.
  * *Non-blocking:* Every flag is dismissible.
  * *Not a chatbot · Not a training module · Not a hiring gate.*
* **Footer:** Slide 05 / 17

---

### Slide 06: Product / Manager — Three Writing Tools, One Engine Underneath
* **Hero UI Image:** [`06-jd-studio-hero.png`](assets/06-jd-studio-hero.png) showing TipTap editor, flagged spans, and expanded Rosewood citation card.
* **Feature Highlights:**
  1. *Instant flags on known phrasing:* Sub-millisecond deterministic spaCy lemmatizer matching against statutory lexicons.
  2. *A deeper check on typing pause:* Streaming Google Gemini contextual pass evaluating coded language and bona-fide occupational justifications (GDOR).
  3. *Evidence and fix in every flag:* Direct legal citation link, explanation, and one-click alternative rewrite chips.
* **Inset Panels:** Previews of Feedback Checkpoint (JD criteria drift) and Promotion Writeup (peer feedback corroboration).
* **Footer:** Slide 06 / 17

---

### Slide 07: Product / Manager — A Pattern is a Statistical Finding, Not an Impression
* **Hero UI Image:** [`07-pattern-dashboard.png`](assets/07-pattern-dashboard.png) showing monthly trend charts and recurring cards.
* **Key Mechanisms:**
  1. *Longitudinal View:* Flag volume over time, categorized across protected characteristics (age, gender, disability, family status).
  2. *Only Significant Patterns Appear:* Gated via Fisher's Exact Test ($p < 0.05$). A habit is only surfaced if mathematically improbable by chance.
  3. *Evidence Drill-Down:* Slide-over drawer detailing historical document titles, dates, and verbatim contexts behind each finding.
* **Footer:** Slide 07 / 17

---

### Slide 08: Product / HR — Firm-Level Trends and Structural Anonymity
* **UI Image Left:** [`08-hr-trends-dashboard.png`](assets/08-hr-trends-dashboard.png) (HR Trends Portal).
  * KPI tiles, adoption rates, category distributions.
  * Small-cell suppression: Any cohort covering $< 3$ managers is suppressed ($k \ge 3$ privacy invariant).
* **UI Image Right:** [`08-hr-dictionary-review.png`](assets/08-hr-dictionary-review.png) (Dictionary Review Queue).
  * Candidate term cloud / list generated autonomously by the 4-agent debate loop.
  * Human-in-the-loop review card displaying Proposer arguments, Skeptic counter-arguments, and citation evidence.
* **Footer:** Slide 08 / 17

---

### Slide 09: Engineering — Inside the Bias-Detection Engine
* **Diagram:** 7-stage state graph sequence diagram.
* **Flow:**
  1. Document text $\rightarrow$ Stage 1: Dictionary Module (spaCy lemma matching, <10ms).
  2. Stage 2: Contextual Pass Agent (Google Gemini via Instructor).
  3. Stage 3: Adjudicator (Deterministic Python span verification — hallucinated quotes dropped).
  4. Stage 4: Verdict Module (In-context statutory rulings & GDOR exceptions applied).
  5. Stage 5: Suppression Module (Checks sentence-level fingerprint hashes against manager dismissals).
  6. Stage 6: Judge Agent (Independent second opinion via multi-sample consensus).
  7. Stage 7: Recommendations Agent (2–3 evidence-anchored neutral rewrites).
* **Footer:** Slide 09 / 17

---

### Slide 10: Engineering — LLM as a Judge (Consensus Confidence Gating)
* **Core Concept:** An independent model evaluates each surviving flag without seeing the generator's explanation.
* **Architectural Elements:**
  * *A different model judges:* Prevents LLM self-preference bias.
  * *A rubric, not a score:* Boolean rubric checklist decomposition (`references_characteristic`, `gdor_plausible`, `stated_objectively`) evaluated in code.
  * *Confidence is a frequency:* Evaluates $N$ independent samples; confidence equals agreement percentage.
  * *Flag order shuffled:* Eliminates list-position bias.
* **Footer:** Slide 10 / 17

---

### Slide 11: Engineering — Published Research Foundations
* **Research Citations Table:**
  * *Different model judges:* Panickssery, Bowman & Feng (2024, arXiv:2404.13076) on causal self-preference bias.
  * *Rubric decomposition:* CheckEval — Lee et al. (EMNLP 2025, arXiv:2403.18771); Gu et al. (2024, arXiv:2411.15594).
  * *Self-consistency confidence:* Wang et al. (ICLR 2023, arXiv:2203.11171); Xiong et al. (ICLR 2024, arXiv:2306.13063).
  * *Position shuffling:* Wang et al. (2023, arXiv:2305.17926); Zheng et al. (NeurIPS 2023, arXiv:2306.05685).
  * *Calibration measurement:* Tian et al. (EMNLP 2023, arXiv:2305.14975); Feuer et al. (2026, arXiv:2603.05485).
* **Footer:** Slide 11 / 17

---

### Slide 12: Engineering — Autonomous Dictionary Growth Loop
* **Diagram:** 4-agent consensus debate architecture.
* **Pipeline:**
  * Recurring contextual flags ($\ge 2$ documents, $\ge 1$ manager) trigger candidates.
  * *Proposer Agent:* Argues for inclusion and proposes category.
  * *Skeptic Agent:* Tests validity against standard business language.
  * *Categorizer Agent:* Determines general vs role-specific scope.
  * *Citation Agent:* Verifies statutory labor law or academic backing.
  * *Gate:* Citation Found + General Scope + Proposer/Skeptic support.
  * *HR Human-in-the-Loop:* Final sign-off converts phrase into zero-latency Stage 1 dictionary hit.
* **Footer:** Slide 12 / 17

---

### Slide 13: Engineering — Architecture & Tech Stack
* **System Topology:** One unified FastAPI service, one React 19 single-page app, one Neon Serverless PostgreSQL database.
* **Tech Stack Matrix:**
  * *Frontend:* React 19, TypeScript, Vite, Tailwind CSS v4 (Rosewood tokens), TipTap editor, TanStack Router/Query.
  * *Backend:* Python 3.12, FastAPI, Server-Sent Events (SSE), LangGraph state machine, Structlog.
  * *AI Layer:* Google Gemini (`gemini-2.5-flash` / `gemini-3.5-flash-lite`) via `instructor`.
  * *Database:* Neon Serverless PostgreSQL 16 (cloud pooled), SQLAlchemy 2.0, Alembic migrations.
  * *Statistics:* scipy (`scipy.stats.fisher_exact`).
* **Footer:** Slide 13 / 17

---

### Slide 14: Engineering — Data Model, Privacy & Audit Trail
* **Entity Relationship Overview:** 17 core SQLAlchemy entities.
* **Structural Guarantees:**
  * `User` $\rightarrow$ `Document` (`owner_id`): Every manager query filters strictly on `owner_id`. HR endpoints physically lack fields for individual document content.
  * `Dictionary` $\rightarrow$ `Citation` (Mandatory FK): Non-nullable foreign key ensures no un-evidenced bias rule can exist.
  * `AnalysisRun` $\rightarrow$ `AgentRun`: Every LLM call, token usage, latency, and prompt output is recorded as an immutable audit fact.
* **Footer:** Slide 14 / 17

---

### Slide 15: Wrap-up — Version 2 Architectural Seams
* **Clean Extension Seams:**
  1. *Multi-Model Gateway:* Runtime routing across Google Gemini, Claude, and DeepSeek via existing `StructuredCompletionClient`.
  2. *Video Drift Reference:* Native multimodal interview video processing via Gemini.
  3. *Historical RAG:* Owner-scoped semantic search over past manager writing via `pgvector`.
  4. *Global Statutory Expansion:* Pluggable regional dictionary tables (EU, Japan, Australia) with zero engine changes.
* **Footer:** Slide 15 / 17

---

### Slide 16: Wrap-up — Engineering Learnings & Production Standards
* **Key Takeaways:**
  * *Rigorous Testing:* 240 backend unit/integration tests (Pytest) + 251 frontend component tests (Vitest).
  * *Schema-First Contracts:* Pydantic v2 and Instructor eliminate JSON formatting failures across LLM boundaries.
  * *Regulated Domain Invariants:* Privacy enforced by schema design rather than application authorization checks.
  * *Mathematical Gating:* Mitigating alert fatigue by requiring statistical proof ($p < 0.05$) before surfacing writing habits.
* **Footer:** Slide 16 / 17

---

### Slide 17: Project Repository & Contact
* **Repository Link:** `https://github.com/sm-daniyal/patternSpecular`
* **Maintainer:** sm-daniyal (Syed Daniyal)
* **Architecture Docs:** Comprehensive documentation suite in `docs/` (`DESIGN_SPEC.md`, `STUDY_GUIDE.md`, ADRs 0001–0018).
* **Footer:** Pattern Specular · Slide 17 / 17
