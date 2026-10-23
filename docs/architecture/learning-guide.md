# Architecture & Engineering Learning Guide

> An end-to-end technical guide to Pattern Specular's design, pipeline mechanics, and engineering invariants.

---

## 1. Core Architectural Mental Model

Pattern Specular is built around a non-negotiable premise: **Bias detection tools fail when they act like police officers rather than calibration mirrors.**

When AI systems assign punitive scores ("Your text is 40% biased") or block workflows, managers reject the software. Pattern Specular replaces punitive grading with four core architectural invariants:

1. **Specular, Not Judicial:** The platform reflects patterns back to the author for self-calibration. It never assigns grades, never blocks submission, and every flag is dismissible with one click.
2. **Evidence-Grounded Only:** No flag can exist based solely on "model intuition." Every candidate phrase must link via a non-nullable foreign key to a published statute (e.g., India's *Code on Wages 2019*, Singapore *TAFEP*, US *Title VII*, UK *Equality Act 2010*) or peer-reviewed academic literature.
3. **Zero-Hallucination Gate:** An LLM's claims are treated as untrusted until verified by deterministic code. If a quoted span is not an exact verbatim substring of the raw document, it is immediately discarded.
4. **Longitudinal Statistical Proof:** A single flagged word does not constitute a bias pattern. Patterns are only surfaced on the dashboard when Fisher's Exact Test confirms statistical significance ($p < 0.05$) across a manager's historical writing.

---

## 2. The 7-Stage LangGraph Pipeline

The engine is wired as a deterministic `StateGraph` using **LangGraph** (`backend/src/pattern_specular/engine/orchestrator.py`). It alternates between deterministic code modules and LLM agent passes:

```
[Raw Document Text]
        │
        ▼
[Stage 1: Dictionary Module] ──────► spaCy lemmatizer (<10ms, $0)
        │
        ▼
[Stage 2: Contextual Pass]   ──────► Gemini Flash Lite (Instructor + Pydantic)
        │
        ▼
[Stage 3: Adjudicator Gate]  ──────► Verbatim string check (kills hallucinations)
        │
        ▼
[Stage 4: Verdict Module]    ──────► Statutory GDOR / BFOQ in-context rulings
        │
        ▼
[Stage 5: Suppression]      ──────► SHA-256 sentence fingerprint dismissal filter
        │
        ▼
[Stage 6: LLM-as-a-Judge]   ──────► Multi-sample consensus (confidence ≥ 0.70)
        │
        ▼
[Stage 7: Recommendations]  ──────► 2–3 evidence-grounded neutral rewrite chips
        │
        ▼
[SSE Stream to React 19 Frontend]
```

### Stage Deep Dive

### Stage 1: Deterministic Dictionary Module (`engine/dictionary.py`)
- **Technology:** `spaCy` (`en_core_web_sm`) with parser and NER disabled for maximum throughput.
- **Mechanism:** Executes an in-memory **leftmost-longest non-overlapping sliding window** matcher over canonical lemma tokens.
- **Performance:** Sub-10ms latency, zero API token cost.

### Stage 2: Contextual Pass (`engine/contextual_pass.py`)
- **Technology:** Google Gemini (`gemini-3.5-flash-lite`) wrapped with `Instructor` and `Pydantic`.
- **Mechanism:** Analyzes non-literal bias, coded phrasing, and subtle exclusionary criteria that static lexicons miss.

### Stage 3: Adjudicator Gate (`engine/adjudicator.py`)
- **Technology:** Pure Python string slicing.
- **Mechanism:** Verifies that `span_text in document_text`. If an LLM paraphrases or invents a phrase, the Adjudicator intercepts and drops it before it ever reaches the user.

### Stage 4: Verdict Module (`engine/verdict.py`)
- **Mechanism:** Evaluates Bona Fide Occupational Qualifications (BFOQ / GDOR). If physical fitness or language proficiency is an essential requirement for the specific role, the flag is marked justified and suppressed.

### Stage 5: Suppression Engine (`engine/suppression.py`)
- **Technology:** SHA-256 sentence hashing.
- **Mechanism:** Computes $\text{Hash} = \text{SHA-256}(\text{normalized sentence context})$. If the author previously dismissed this exact flag in this context, it is suppressed permanently.

### Stage 6: LLM-as-a-Judge (`engine/judge.py`)
- **Technology:** Independent Gemini evaluation loop.
- **Mechanism:** Audits candidate flags against a decomposed boolean checklist rubric without viewing the generator's reasoning. A calibrated empirical confidence threshold of $\ge 0.70$ agreement across independent samples is required.

### Stage 7: Recommendations Engine (`engine/recommendations.py`)
- **Mechanism:** Produces 2–3 neutral, context-preserving alternatives (never a single "correct" answer) grounded in the statutory citation.

---

## 3. Relational Schema & Structural Privacy

The data layer runs on **Neon Serverless PostgreSQL 16** with 20 Alembic migrations:

### 1. Manager Isolation (`owner_id`)
Every `Document` and `AnalysisRun` record carries an `owner_id` foreign key referencing `users.id`. All database queries in manager endpoints explicitly filter:
```python
stmt = select(Document).where(
    Document.id == doc_id,
    Document.owner_id == current_user.id
)
```
There is no API route or query path that allows an HR user or peer manager to view an author's raw draft.

### 2. Mandatory Citation Foreign Keys
In `models/dictionary.py`, the `citation_id` column is a non-nullable foreign key to `citations.id`. An ungrounded bias term cannot be inserted into the system—doing so causes an immediate relational integrity error.

### 3. Anonymity Preservation ($k \ge 3$)
When HR queries firm-wide talent trends, database aggregation queries enforce:
```sql
SELECT category, COUNT(*) as total_flags
FROM flags
JOIN documents ON flags.document_id = documents.id
GROUP BY category
HAVING COUNT(DISTINCT documents.owner_id) >= 3;
```
Any data bucket containing fewer than 3 distinct managers is automatically suppressed to eliminate re-identification risk.

---

## 4. Mathematical Grounding: Fisher's Exact Test

To distinguish genuine behavioral habits from random statistical noise, Pattern Specular models manager tendencies using a $2 \times 2$ contingency table:

| | Target Group (e.g., Women) | Comparison Group (e.g., Men) |
|---|---|---|
| **Flag Present (e.g., "family commitment")** | $a$ | $b$ |
| **Flag Absent** | $c$ | $d$ |

The platform calculates the exact hypergeometric probability using `scipy.stats.fisher_exact`:

$$p = \frac{\binom{a+b}{a} \binom{c+d}{c}}{\binom{n}{a+c}} = \frac{(a+b)! (c+d)! (a+c)! (b+d)!}{a! b! c! d! n!}$$

Only when $p < 0.05$ does a pattern card materialize on the manager's Pattern Dashboard.

---

## 5. Autonomous Lexicon Growth (4-Agent Committee)

Candidate bias phrases undergo an autonomous multi-agent consensus workflow before reaching human curators:

1. **Proposer Agent:** Argues how and why the phrase creates systematic exclusion.
2. **Skeptic Agent:** Acts as adversarial counsel, defending legitimate operational usages.
3. **Categoriser Agent:** Scopes whether the issue is universal or role-specific.
4. **Citation Agent:** Cross-references statutory labor frameworks to link empirical citations.
5. **Human-in-the-Loop:** HR reviewers inspect the debate transcript in the **Dictionary Review** portal. Upon approval, the phrase enters the live Stage 1 lexicon for zero-cost sub-10ms matching.

---

## 6. Frontend Streaming Architecture

- **React 19 & Headless TipTap (ProseMirror):** Highlights flags using non-destructive custom decorations, preserving unmodified document text.
- **Server-Sent Events (SSE):** `use-flag-stream.ts` establishes an SSE connection to `/documents/{id}/stream`. Stage 1 dictionary matches render in under 10ms; Stages 2 through 7 stream in progressively as AI validation completes.
- **Rosewood Design System:** Custom atomic CSS tokens (`#b83a58`) configured in Tailwind CSS v4.
