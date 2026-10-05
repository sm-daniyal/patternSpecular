# Pattern Specular — Project Memory & Master Study Guide

> **Author & Maintainer:** `sm-daniyal` (Syed Daniyal)  
> **Repository:** [`sm-daniyal/patternSpecular`](https://github.com/sm-daniyal/patternSpecular)  
> **Lineage:** Sovereign architectural evolution of *Pattern Mirror* (MIT License, Bernice Koh).  
> **Core Purpose:** End-to-end technical reference, study roadmap, and interview defense guide.

---

## 1. Project Overview & Quick Reference

* **Domain:** Longitudinal bias-pattern analysis and criteria drift checking for enterprise hiring and promotion writing.
* **The Core Problem:**
  * Enterprises spend extensive budgets on diversity and unconscious bias training. Managers understand the theory.
  * However, subtle cognitive bias still creeps into job descriptions, interview feedback, and promotion writeups.
  * In isolation, an individual instance looks like a harmless slip or borderline phrasing. **The bias only reveals itself across a manager's entire corpus of 20+ documents over time.**
* **Core Architectural Philosophies:**
  1. **Mirror, not judge:** Surfaces patterns to assist self-calibration; never blocks submissions, never scores, and never penalizes. Decision autonomy remains 100% with the manager.
  2. **Evidence-backed:** Every flag cites statutory labor legislation (India Code on Wages 2019, RPwD Act 2016; Singapore TAFEP; US EEOC Title VII; UK Equality Act 2010) or peer-reviewed research (e.g., Gaucher et al., 2011).
  3. **Privacy by architecture:** HR physically cannot query or access individual manager documents. Enforced at the schema and API route boundary; only firm-level aggregates with $k \ge 3$ anonymity suppression are served.
  4. **Statistical gating:** Writing tendencies are never labeled as "patterns" based on raw frequency. Surfaced strictly when Fisher's Exact Test achieves $p < 0.05$ against baseline distributions.

---

## 2. Master Documentation Roadmap (Study in this exact order)

| Step | Document | Core Concept | Architectural Invariant | Status |
| :---: | :--- | :--- | :--- | :---: |
| **01** | [`README.md`](../README.md) | High-level problem, 2 Portals, 6-Stage Pipeline, Tech Stack | The 30,000-ft executive overview of the system | ✅ Synced |
| **02** | [`docs/DESIGN_SPEC.md`](DESIGN_SPEC.md) | Business case, 4 Manager Views, Latency tiers (<10ms vs 5s) | Explains user journeys and why linters/chatbots fail | ⏳ Next |
| **03** | [`docs/architecture/overview.md`](architecture/overview.md) | Privacy boundary, state machine, pipeline gates | Deterministic state transitions and isolation | ⏳ Upcoming |
| **04** | [`docs/architecture/data-model.md`](architecture/data-model.md) | Schema ERD, `owner_id`, `submitted_content`, flag hashes | Physical isolation of sensitive draft documents | ⏳ Upcoming |
| **05** | [`docs/architecture/flags-and-suppression.md`](architecture/flags-and-suppression.md) | Lemma normalization, sentence fingerprints, dismissals | Respects manager dismissals across draft edits | ⏳ Upcoming |
| **06** | [`docs/architecture/llm-judge.md`](architecture/llm-judge.md) | Multi-sample consensus, rubric calibration, ECE/Brier | Eliminates LLM flakiness via ensemble agreement | ⏳ Upcoming |
| **07** | [`docs/architecture/pattern-significance.md`](architecture/pattern-significance.md) | Fisher's Exact Test, $2 \times 2$ contingency tables | Mathematical distinction between habit and noise | ⏳ Upcoming |
| **08** | [`docs/architecture/dictionary-growth.md`](architecture/dictionary-growth.md) | 4-agent debate loop (Proposer, Skeptic, Categorizer, Citation) | Autonomous self-growth with human HR approval | ⏳ Upcoming |
| **09** | [`docs/adr/`](adr/) | Architectural Decision Records (ADRs 0001–0018) | Defending engineering trade-offs in interviews | ⏳ Upcoming |
| **10** | [`docs/CONVENTIONS.md`](CONVENTIONS.md) & [`CODE_STYLE.md`](CODE_STYLE.md) | mypy --strict, PEP 518, Tailwind v4, pytest/vitest gates | Enterprise-grade production quality standards | ⏳ Upcoming |

---

## 3. Deep-Dive Log: Step 01 (`README.md`)

* **What it is:** The entry-point document that communicates product value and technical rigor in under 3 minutes.
* **The Architecture of Two Portals:**
  1. **Manager Portal (4 Dedicated Views):**
     * `JD Studio`: Instant deterministic AST lemma matching (<10ms) + background streaming Gemini contextual pass.
     * `Feedback Checkpoint`: Pre-submission check on interview feedback + **Drift Check** against the role's stated JD criteria.
     * `Promotion Writeup`: Check against target level promotion rubrics + historical peer feedback corroboration.
     * `Pattern Dashboard`: Longitudinal writing habits surfaced strictly when statistically significant ($p < 0.05$).
  2. **HR Portal (Aggregates Only, Zero Individual Writing):**
     * `Trends Dashboard`: Firm-wide demographic and category aggregates. Any cohort covering $< 3$ managers is suppressed ($k \ge 3$ differential privacy).
     * `Dictionary Review Queue`: Human-in-the-loop review queue for candidate terms surfaced autonomously by the 4-agent consensus loop.
* **The 4 Non-Negotiable Invariants:**
  * *Mirror, not judge:* Never blocks, never penalizes, manager retains full decision autonomy.
  * *Private by architecture:* Individual writing is strictly invisible to HR at the schema and route levels.
  * *Non-blocking:* Every flag is dismissible; "Publish" and "Submit" are always active.
  * *Evidence for every flag:* Every observation cites statutory acts or peer-reviewed academic literature.
* **The Core Tech Stack Decisions:**
  * *Frontend:* React 19, TipTap (ProseMirror mark extensions), Tailwind CSS v4 (Rosewood theme), TanStack Query & Router.
  * *Backend:* Python 3.12, FastAPI, Server-Sent Events (SSE) streaming.
  * *AI Orchestration:* LangGraph state graph, Google Gemini (`gemini-2.5-flash` / `gemini-3.5-flash-lite`) via `instructor`.
  * *Persistence:* Neon Serverless PostgreSQL 16 (cloud pooled), SQLAlchemy 2.0, Alembic migrations.
  * *Statistics:* `scipy.stats.fisher_exact` ($2 \times 2$ contingency tables).

---

## 4. Daily Start & Operations Reference

### To Start Pattern Specular:

**Terminal 1 — Backend (FastAPI API Server):**
```powershell
cd D:\pattern-specular\backend
.\venv\Scripts\Activate.ps1
uvicorn pattern_specular.main:create_app --factory --reload --port 8000
```

**Terminal 2 — Frontend (Vite Dev Server):**
```powershell
cd D:\pattern-specular\frontend
npm run dev
```
*Access in browser:* `http://localhost:5173`

### To Stop:
* Press `Ctrl + C` in both terminals.
* Database automatically pauses compute on Neon Serverless ($0 idle cost).

### Seed Accounts (Live Database Roster):
* **HR Portal:** `teresa.lisbon@example.com` / Password: any non-empty text (e.g., `password`)
* **Manager Portal:**
  * `sm.daniyal@example.com` (Engineering)
  * `areesha.naaz@example.com` (Engineering)
  * `patrick.jane@example.com` (Investigations)
  * `wayne.rigsby@example.com` (Operations)
  * `kimbal.cho@example.com` (Compliance)
  * `grace.vanpelt@example.com` (Data Analytics)

---

## 5. Interview Talking Points (Executive & Recruiter Ready)

1. **Pipeline Architecture:**
   > *"I engineered Pattern Specular around a bounded, 6-stage hybrid pipeline. Rather than dumping raw text into a costly LLM prompt, we execute deterministic spaCy lemmatization in under 10ms to catch catalogued statutory violations, and only route contextual ambiguity to a structured Google Gemini agent."*

2. **Hallucination Prevention:**
   > *"LLMs frequently misquote or extrapolate source text when flagging bias. We implemented an AST-level span adjudicator that verifies candidate phrases verbatim against source character offsets. Any hallucinated span is dropped before reaching the user."*

3. **Statistical Rigor vs. Subjectivity:**
   > *"Most bias linters flag isolated words, generating alert fatigue. Pattern Specular gates longitudinal pattern surfacing using Fisher's Exact Test ($p < 0.05$). We construct $2 \times 2$ contingency tables comparing a manager's demographic terminology against firm benchmarks, ensuring we only alert on mathematically significant disparities."*

4. **Privacy by Architecture:**
   > *"Privacy cannot be an afterthought enforced by UI permissions. We designed strict schema and route-level isolation: HR endpoints physically cannot query individual manager drafts or document IDs. Furthermore, all organization-wide trends enforce $k \ge 3$ anonymity suppression."*

5. **Multi-Jurisdiction Statutory Grounding:**
   > *"Unlike generic grammar tools, our rules map directly to enforceable statutory frameworks: India's Code on Wages 2019 and RPwD Act 2016, Singapore's TAFEP, US EEOC Title VII, and the UK Equality Act 2010. Every surfaced flag provides the exact legal citation and evidence-backed neutral alternatives."*
