# The Pattern Specular — Design Specification

> **Status: living product specification.** This is the product source of truth referenced by
> [CLAUDE.md](../CLAUDE.md) and [CONVENTIONS.md](CONVENTIONS.md). It is maintained as a living
> document — edit it as the product evolves, with git history as the decision trail. Where an
> [ADR](adr/) conflicts with this document, **the ADR supersedes it**: ADRs are the immutable
> record for architecture decisions and their trade-offs, while this file describes the product itself.

---

## 1. Core Alignment & Positioning

**The problem.** Bias in hiring and talent management writing is not primarily an awareness problem — it is a visibility problem. Managers with hiring and promotion authority know the theory, have completed the training, and still produce job descriptions, interview feedback notes, and promotion justifications that carry coded language, shifted evaluation criteria, and framing asymmetries. No single document looks egregious in isolation. The pattern is only visible across a manager's entire body of writing over time — a view that no current tool constructs.

**Why existing tools miss it.** Bias training addresses understanding; it does not show a manager where their own writing departs from what they understand. Organisation-wide diversity dashboards report outcomes, not the writing that produced them. Single-document grammar and readability checkers operate on one document at a time: they cannot detect tendencies that only emerge longitudinally.

**The value.** Pattern Specular gives managers a calibration mirror against their own writing history, grounded in statutory labor law and peer-reviewed research.

- **Evidence at the source.** Flags cite the legislation or academic study that justifies them — not the model's opinion. Managers with authority can dismiss a tool that says "this seems biased"; they are harder pressed to dismiss TAFEP guidelines or the Equality Act 2010.
- **Longitudinal intelligence.** A single flagged phrase is data. The same phrase recurring across 18 feedback notes over two hiring cycles is a pattern. Pattern Specular surfaces the latter, not just the former.
- **Multi-jurisdiction coverage.** The statutory engine evaluates writing against four frameworks simultaneously — India (Code on Wages, RPwD Act, Transgender Persons Act), Singapore (TAFEP), United States (EEOC Title VII, ADEA), and United Kingdom (Equality Act 2010). One platform, one analysis run, four regulatory lenses.
- **Audit defensibility.** Every flag is logged with its provenance: which statutory rule, which dictionary entry or agent run, which confidence score. If a flag is challenged months later, the full chain is reconstructable.

**Design principles.**

- *Specular, not judicial.* The platform reflects writing patterns back to the manager for self-calibration. It never penalises, never scores, never gates.
- *Private by architecture.* Individual manager writing is accessible only to that manager — enforced at the schema and API route levels, not by policy alone. HR sees aggregated trends; individual content is structurally inaccessible to them.
- *Non-blocking.* Every flag is dismissible. No submission or approval process is ever gated by the platform.
- *Evidence for every flag.* Every surfaced observation cites a statutory provision or peer-reviewed publication. No flag without a source.

**What this is not.** Not a chatbot. Not a compliance training module. Not a hiring gate. Not a scoring system. Not a substitute for legal review.

---

## 2. Product Surfaces — Four Views, One Engine (Manager Portal)

The manager portal exposes four surfaces, all backed by the same analysis engine and Neon PostgreSQL data store. They are not four separate products; they are four windows into the same longitudinal record.

#### View 1 — JD Studio

The manager's writing surface for job descriptions. As they type or paste a job description, potentially problematic phrasing is underlined in real time. The mental model is *a bias-aware editor*, not a form. Every underline cites statutory guidance or peer-reviewed research. Hovering reveals the citation and the specific concern. The manager can accept the suggested rewrite, dismiss the flag, or leave it and continue.

JD Studio runs on a **two-layer latency model**:

- **Layer 1 — Dictionary flags** · <100ms · live as the manager types. Deterministic spaCy lemma matching against the multi-jurisdiction statutory lexicon. No LLM call, no network latency beyond the HTTP round trip.
- **Layer 2 — Contextual pass** · ~5–8s · streams in via Server-Sent Events after a typing pause. Google Gemini evaluates coded language, genuine occupational requirements (GDOR), and phrases that the dictionary doesn't yet know.

Both layers surface in the same editor surface. The manager experiences one continuous stream of flags — some arrive instantly, some a few seconds later — all dismissible with the same interaction.

On **Publish JD**, the engine extracts the role's stated assessment criteria from the JD text. The manager reviews and edits the extracted criteria before confirming; only the confirmed set is stored as the reference corpus the Feedback Checkpoint drift check measures interview feedback against. The criteria are AI-extracted, manager-confirmed — the confirm gate keeps unverified model output out of the drift reference.

**Active draft persistence.** JD Studio drafts are persisted in `localStorage` across tab switches and browser sessions, so a manager working on a complex JD across multiple sittings does not lose in-progress work.

#### View 2 — Feedback Checkpoint

The manager's pre-submission surface for interview feedback. The manager pastes a draft feedback note into Checkpoint before submitting it through their organisation's existing systems. Two checks run in parallel and stream back via SSE:

- **Bias detection** — the full seven-stage engine evaluating the language used (same pipeline as JD Studio).
- **Criteria drift check** — whether the feedback addresses the criteria the manager themselves stated in the original JD.

Example output:

**Original JD — Senior Engineer role:** 5+ years Python · Production systems experience · Strong SQL · Mentorship track record

**Interview feedback — Candidate A:** *"Candidate came across as reserved in the opening. Technically solid — handled the system design section cleanly. Not sure about the cultural fit; didn't project much energy. Possibly better suited to a more back-office environment."*

**DRIFT** — 3 of 4 stated criteria not addressed in the feedback. **BIAS** — 3 observations outside JD scope: presentation demeanour, energy level, role-routing suggestion.

The manager is not blocked. They see this analysis before deciding what, if anything, to change.

#### View 3 — Pattern Dashboard

The longitudinal differentiator. The Pattern Dashboard aggregates a manager's complete flag history and surfaces writing tendencies — not flag-by-flag, but as patterns across documents and across time. A tendency surfaces only when Fisher's Exact Test confirms it is statistically significant, not merely frequent.

**Writing patterns — two modes:**

Mode A — Per-role. Across one JD and all feedback notes for that role. "You used 'polished' to describe four candidates in this round — all four are women." p = 0.003. Asymmetry invisible in any single feedback note; obvious in aggregate.

Mode B — Across time. The manager's full writing history. "Across 29 feedback notes, 'cultural fit' appears 12 times. 11 of those 12 notes were written about candidates who were not ultimately hired."

Each surfaced pattern links through to the specific documents it came from.

**Behavioural reflection:** Patterns in the manager's decisions about flags — dismiss rates by bias category, adoption trends over time. "You dismiss disability-coded flags at 71%, gender-coded flags at 22% — across 38 flags raised this quarter." Presented without editorialising; the manager draws the conclusion.

This view is private to the manager. No HR role can access it.

#### View 4 — Promotion Writeup

The manager's pre-submission surface for promotion nominations. The manager enters their justification for promoting an employee; the engine runs two parallel checks:

- **Bias detection** in the language used (same seven-stage pipeline as JD Studio and Feedback Checkpoint).
- **Criteria drift check** — whether the writeup evidences the promotion rubric criteria for the target level.

Alongside the rubric coverage, the surface shows what the employee's historical peer feedback says for each criterion — corroborating evidence that peers have already supplied for gaps the writeup omits.

Same non-blocking model as Feedback Checkpoint. The manager sees the analysis before deciding whether to revise or submit.

---

## 3. The Analysis Engine

The engine is a bounded, named-step flow orchestrated by LangGraph as an explicit StateGraph. Every stage is logged, every transition is traceable, every flag has a verified verbatim span before it reaches the manager. A flag surfaces to the manager only by surviving every gate in sequence.

#### Seven stages

**Stage 1 — Dictionary Module.** spaCy (`en_core_web_sm`) lemma matching against the curated multi-jurisdiction statutory lexicon — deterministic, no LLM call. Every hit cites its statutory source or academic reference. This is the Layer 1 latency tier: sub-millisecond response, runs on every keystroke debounce.

**Stage 2 — Contextual Pass Agent.** One schema-enforced Gemini call (`gemini-2.5-flash` via `instructor.from_genai`). Evaluates the full document context around each dictionary hit, catches coded phrases absent from the dictionary, and tags each candidate flag as *general* (dictionary-eligible in future runs) or *role-specific* (LLM-only flag, not a dictionary candidate). Results stream back to the frontend via SSE.

**Stage 3 — Adjudicator Module.** Deterministic Python — no LLM call. Every span claimed by Stage 2 is verified by literal string match against the source document text. Any LLM-claimed quote that does not exist verbatim in the source is dropped and logged. Hallucinated flags structurally cannot reach the manager.

**Stage 4 — Verdict Module.** Statutory in-context ruling. Suppresses confirmed false positives: phrases that constitute genuine occupational requirements (GDOR) given the specific role and jurisdiction context. The distinction between a biased phrase and a legitimate requirement depends on context; this stage makes that determination against the applicable statutory framework.

**Stage 5 — Suppression Module.** Computes the lemma-bag sentence fingerprint for each surviving flag and checks it against the manager's prior dismissal record for this document. Flags the manager has already dismissed in this context are suppressed. Context changes (sentence edits that shift the lemma bag) cause a dismissed flag to re-surface. See Section 12 for the full fingerprint design.

**Stage 6 — Judge Agent.** Multi-sample consensus gate. Gemini (`gemini-3.5-flash-lite`) re-examines each surviving flag against the document using a fixed rubric, independently, across N runs. Confidence is the fraction of runs that agree the flag is biased. Flags below the confidence threshold (0.70) are terminated here and logged but not surfaced. The Judge's full reasoning and per-run scores are persisted.

**Stage 7 — Recommendations Agent.** `gemini-2.5-flash` with a separate prompt and Instructor-enforced output schema. Generates 2–3 evidence-anchored, jurisdiction-aware neutral rewrites for every flag above the confidence threshold. Only runs on flags the Judge has passed — see Section 7.

#### The drift-check stage (parallel to bias detection)

For Feedback Checkpoint and Promotion Writeup, a parallel concern runs alongside the seven-stage pipeline: a **drift check** that evaluates whether the current writing addresses a reference set of criteria.

- **Feedback Checkpoint** drift: interview feedback vs. the JD's confirmed assessment criteria.
- **Promotion Writeup** drift: promotion justification vs. the promotion rubric for the target level.

Architecturally the same agent, different reference corpus. Promotion analysis requires no new engine components — only a different reference document fed into the existing drift stage.

#### Why the structure matters

LangGraph logs every state transition. Any flag can be reconstructed exactly — which stage produced it, what the input was, what the output schema contained, why it was suppressed or terminated. This is what makes audit defensibility real rather than a claim.

---

## 4. The Multi-Jurisdiction Lexicon — Foundation, Categories, and Growth

The statutory lexicon is the engine's anchor to verifiable evidence. Without it, the platform would be an LLM bias checker — accurate-sounding but dismissible. Every flag that originates from the lexicon carries a specific statutory provision or academic citation that a manager cannot easily wave away.

#### Foundation: four jurisdictions, one runtime

The lexicon is organised by jurisdiction in the `dictionaries` table. The engine loads the applicable scope at runtime; a document can be evaluated against multiple jurisdictions simultaneously.

| Jurisdiction | Legislation / Guidance | Bias categories covered |
|---|---|---|
| **India (IN)** | Code on Wages 2019 · Rights of Persons with Disabilities (RPwD) Act 2016 · Transgender Persons (Protection of Rights) Act 2019 | Gender · Age · Disability · Gender identity · Caste-coded framing |
| **Singapore (SG)** | TAFEP Fair Employment Guidelines | Gender · Age · Race/ethnicity · Nationality · Religion · Disability · Family status |
| **United States (US)** | EEOC Title VII · Age Discrimination in Employment Act (ADEA) | Gender · Race · Age · National origin · Religion · Disability |
| **United Kingdom (UK)** | Equality Act 2010 | All nine protected characteristics |

Academic backing where applicable — e.g. Gaucher et al. (2011) on masculine-coded language in job postings, supplying empirical effect sizes to complement statutory provisions.

#### Lexicon growth — the four-agent debate loop

The lexicon is not static. As managers write across the system, the Contextual Pass (Stage 2) proposes flags on phrases absent from the lexicon. Most are role-specific noise. A small fraction are genuine new bias-coded language that should become lexicon entries — deterministic Stage-1 hits in future runs, with statutory citations attached.

The growth loop is where agentic AI does substantive autonomous work in the product.

**Trigger.** A phrase is flagged by the Contextual Pass across ≥ 2 distinct documents and ≥ 1 manager, and it is not yet in the lexicon or under review.

**Four independent Gemini agents**, one candidate each:

1. **Proposer** (`gemini-2.5-flash`) — argues for inclusion: names the protected characteristic, proposes bias category and jurisdiction scope, drafts neutral alternative phrasings.
2. **Skeptic** (`gemini-2.5-flash`) — argues against: is this standard business language? Is the evidence thin? Is the scope too narrow? Then gives its honest verdict.
3. **Categorizer** (`gemini-3.5-flash-lite`) — determines scope: biased across hiring generally, or only in specific role types?
4. **Citation** (`gemini-2.5-flash`) — searches for statutory or academic support. "No support found" is a valid and logged response; the agent never fabricates citations.

**Decision gate.** All three conditions must hold: a citation was found AND the scope is general AND at least Proposer or Skeptic is in favour. Failing the gate archives the candidate — the proposal row and all four agents' reasoning are persisted for auditability.

**Human-in-the-loop sign-off.** Candidates passing the gate enter a `pending_dictionary_additions` queue with phrase, jurisdiction mapping, citation, and all agent reasoning. HR reviews the queue (human sign-off, not auto-approval). Approved entries become live lexicon rows. Rejected or deferred entries are stamped with reviewer and timestamp; deferred items remain in the queue for future review.

**Full audit trail.** The chain from first contextual flag → trigger → agent debate → HR decision → live entry is fully reconstructable. If a manager challenges a flag — "where did this rule come from?" — the provenance is specific and citable.

---

## 5. Persistence Model

**Nothing is transient.** Every flag the engine generates, every manager interaction, every agent run is persisted. The Pattern Aggregator and the adoption metrics both depend on a complete longitudinal event log; anything not stored cannot be analysed later.

Persisted data is organised in three tiers:

**Tier 1 — Must persist (drives core product value):**

- Every flag raised, with full provenance: originating stage, dictionary entry or agent run ID, jurisdiction scope, structured rationale, Judge confidence score
- Manager response to every flag: accepted, dismissed, ignored, edited-around
- The manager's final submitted document text alongside the flagged draft — so behavioural change is measurable against final outcomes, not UI interactions alone
- Recommendations issued and which were adopted

**Tier 2 — Persist for audit and debuggability:**

- Each agent's structured input, output, and internal reasoning
- Judge per-run confidence scores and rubric answers
- Dictionary entries that fired vs. phrases added by the Contextual Pass
- All entries in the `pending_dictionary_additions` queue and their HR disposition

**Tier 3 — Aggregate-only / derived:**

- Pattern Aggregator outputs (computed on demand, cached for the dashboard)
- Manager-level adoption rate, bias category trends, drift over time
- Firm-level HR analytics (strictly aggregated, $k \ge 3$ anonymisation applied)

**Privacy frame.** The persistence model does not change the privacy contract. Individual manager writing, flags, and dismissals are accessible only to the authoring manager. HR access is limited to aggregated views, enforced at the API route and database query levels — not by policy.

**Storage.** All document text, flags, dismissals, agent outputs, and lexicon entries are stored relationally in **Neon Serverless PostgreSQL 16** via SQLAlchemy 2.0 with Alembic-managed migrations. The Neon connection uses SSL-required pooled connections. There is no local Docker PostgreSQL in production; the cloud database is the single production data store.

---

## 6. Manager Behaviour & Override Handling

Managers retain full authority to override any flag. **The platform is non-blocking by design.**

**Interaction model: binary accept/dismiss.** The interaction surface is minimal — accept the suggested rewrite, or dismiss the flag with a single gesture. Both outcomes are logged. A categorisation modal on every dismiss would create friction that undermines the seamlessness the platform's positioning depends on.

**Implicit behaviour is the primary signal:**

- Edited the flagged span after the flag appeared → behavioural adoption
- Dismissed but span remains in final submission → active rejection
- Dismissed and span is gone from final submission → dismissed-and-removed (adopted via own rewrite)
- Never interacted with the flag → passive; signal weight depends on whether span remains

**Pattern surfacing.** Dismissal patterns are surfaced on the Pattern Dashboard only after passing Fisher's Exact Test significance threshold — the same gate applied to writing patterns. Categories and rates are displayed without editorialising. The manager sees the evidence and draws the conclusion. The platform does not draw it for them.

---

## 7. Recommendations Agent

The Recommendations Agent sits in the orchestrator pipeline **after the Judge**, conditional on the Judge passing the flag above the confidence threshold (0.70).

**Why threshold-gated.** Recommendations on low-confidence flags generate noise and erode trust in the platform. The Recommendations Agent runs only when the Judge is confident the flag is genuine.

**Three operating principles:**

1. *Evidence-anchored alternatives, not prescriptions.* "The Equality Act 2010 (UK) and Gaucher et al. (2011) both identify 'aggressive' as a masculine-coded term that reduces applications from women by an estimated 25%. Alternative phrasings in peer-reviewed templates: 'direct', 'assertive', 'decisive'." The manager picks, or doesn't.
2. *Show, don't tell.* Surface 2–3 alternatives, never one prescribed answer. A single correct answer is the platform passing judgement.
3. *Recommendations are dismissible and logged.* Same interaction pattern as flags — dismissals and accepts are data that feeds the Pattern Dashboard and adoption metrics.

**Implementation.** `gemini-2.5-flash` via `instructor.from_genai` with a separate prompt and structured output schema enforced by Instructor. The Recommendations Agent uses the same model as the Contextual Pass but with a different prompt template and output schema — no new infrastructure.

---

## 8. Promotion Workflow

**Trigger model.** Manager-initiated. The manager opens Promotion Writeup, selects the employee, and enters their justification and supporting reasoning. The engine runs and streams results back. Employee-initiated promotion requests are out of scope.

**Two parallel analytical passes:**

1. The seven-stage bias detection engine against the full multi-jurisdiction statutory lexicon — gender-coded, age-coded, disability-coded language, all four jurisdiction scopes active.
2. A **criteria drift check** against the promotion rubric for the target level — which rubric criteria the writeup evidences, and which it omits.

**Architecturally, no new engine components.** The drift check used in Feedback Checkpoint (feedback vs. JD criteria) is reused with a different reference corpus — the promotion rubric instead of JD criteria. Same pattern, different input. Promotion analysis required extending what already existed, not building from scratch.

**Peer feedback as corroborating evidence.** The Promotion Writeup surface shows what the employee's historical peer feedback says for each rubric criterion alongside the manager's own coverage. For each criterion the writeup omits, the surface highlights whether peers have already evidenced it — giving the manager a fuller picture before they decide to revise or submit. The peer feedback corpus is seeded as synthetic demo data in the current implementation.

The Recommendations Agent runs on promotion-workflow flags at the same threshold and on the same principles as JD Studio and Feedback Checkpoint flags.

---

## 9. Talent Workflow Coverage

**External hiring (JD → Feedback).** The JD Studio and Feedback Checkpoint cover the full external hiring writing cycle. The criteria extracted and confirmed from the JD become the drift reference for all feedback notes on that role. All seven engine stages run on both document types.

**Internal moves and promotions.** The Promotion Writeup covers manager-authored justifications for internal promotions. The same bias detection pipeline runs; the drift check uses the promotion rubric as its reference rather than a JD.

**What the platform does not do.** The platform does not perform or analyse background checks. It does not access candidate-facing systems or ATS data. It does not make hiring decisions or generate hiring recommendations. It evaluates the writing the manager produces, not the candidates the writing describes.

---

## 10. Architecture & System Design

### Terminology

Consistent naming across all diagrams and documentation:

- **Agents** — all components that make LLM calls: Contextual Pass, Judge, Recommendations, Proposer, Skeptic, Categorizer, Citation.
- **Modules** — all deterministic, non-LLM components: Dictionary, Adjudicator, Verdict, Suppression, Pattern Aggregator.

### Model allocation

| Component | Model | Rationale |
|---|---|---|
| Contextual Pass | `gemini-2.5-flash` | Full-context evaluation, coded-language detection, GDOR assessment |
| Judge | `gemini-3.5-flash-lite` | Multi-sample rubric scoring; cost efficiency for N independent runs |
| Recommendations | `gemini-2.5-flash` | Evidence-anchored rewrite generation; quality over volume |
| Debate agents (×4) | `gemini-2.5-flash` | Independent reasoning per agent; citation retrieval |
| Drift check | `gemini-2.5-flash` | Criteria coverage evaluation against reference corpus |

Multi-model gateway and provider abstraction are post-MVP. The current implementation uses `google-genai` directly with `instructor.from_genai` for schema enforcement.

### Streaming protocol

Layer 2 analysis results stream back to the frontend via **Server-Sent Events (SSE)**. The frontend opens a persistent SSE connection after the typing-pause debounce fires; the backend streams partial results as each engine stage completes. The manager sees flags appearing progressively rather than waiting for a full pipeline completion.

---

## 11. HR Portal Scope

**Read-only, aggregated only.** HR sees the Trends Dashboard and the Dictionary Review queue. HR does not see any individual manager content — not documents, not flags, not dismissal decisions.

**Trends Dashboard.** SQL-aggregated analytics served via the FastAPI layer:

- **Effectiveness** — flag adoption rate over time, by bias category, by document type. Whether the platform is producing measurable writing changes.
- **Calibration** — dismiss-and-kept rate by category. Whether the platform's flags are trusted or resisted, and where.
- **Dictionary health** — proposal volume, agent agreement rate, citation coverage, HR approval throughput.

**Anonymisation.** Any aggregate covering fewer than three managers ($k \ge 3$ suppression) is withheld from the HR Trends Dashboard. No figure displayed can identify an individual manager's writing behaviour.

**Dictionary Review queue.** HR reviews candidate lexicon entries that have passed the four-agent debate gate. HR can approve (entry goes live), reject (entry is archived with reason), or defer (entry remains in queue for future review). HR does not see the trigger documents or manager writing — only the proposed phrase, the agents' reasoning, and the citation found.

---

## 12. Semantic Flag Tracking: Lemma Fingerprints and Re-Check

Flag state is **backend-resident**, not frontend-transient. The LangGraph pipeline must know what has been dismissed before it executes Stage 5 (Suppression); frontend state is unreliable across refresh, multi-tab, and session resumption; and dismissal data is the primary input to the Pattern Aggregator — storing it in two places creates desync risk.

### The duplicate-flag problem

The dictionary scan runs near-real-time on keystroke debounce. The contextual agent pass runs after a 5-second idle. Without de-duplication, the same phrase can be flagged by Stage 1, then again by Stage 2 after the manager has already dismissed it. Stage 5 prevents this — but it requires a robust identity model for what counts as "the same flag."

### Flag signature

A flag's identity is `(document_id, rule_id, normalised_span_text, sentence_fingerprint)`.

- **Document-scoped, not manager-scoped.** Dismissed within a document, stays dismissed for that document. A fresh document is a fresh check — preserving the longitudinal story. If the manager uses "aggressive" across 15 JDs over two years, the Pattern Dashboard sees all 15 occurrences; each individual JD only nags them once.
- **Span normalisation.** Lowercase, strip punctuation, lemmatise. `"Aggressive"`, `"aggressive!"`, `"aggressive"` all normalise to the same span identity.

### Sentence fingerprint (lemma bag hash)

For the sentence containing the flagged span, extract the lemma bag via spaCy and hash it. The hash is the dismissal's context anchor.

- `"aggressive leader"` → `{aggressive, leader}` → hash A
- `"aggressive leader."` (added period) → `{aggressive, leader}` → hash A — no re-trigger ✓
- `"Aggressive Leader"` (capitalisation) → `{aggressive, leader}` → hash A — no re-trigger ✓
- `"aggressive go-getter"` → `{aggressive, go-getter}` → hash B — re-trigger ✓
- `"aggressive, dynamic leader"` → `{aggressive, dynamic, leader}` → hash C — re-trigger ✓

A dismissal means "I have considered this concern in this context." Unchanged context → previous judgement still applies. Changed context → the manager re-judges.

### Suppression logic

When the engine produces a candidate flag, it computes the signature and looks up dismissals matching `(doc_id, rule_id, normalised_span)`:

- No match → new flag, surface.
- Match with same `sentence_fingerprint` → same flag in same context, suppress.
- Match with different `sentence_fingerprint` → context shifted, surface as a new flag.

**Log everything, suppress only in the UI.** Every engine-generated flag is persisted with a `suppressed` boolean and a reference to the dismissal that caused the suppression. The frontend renders only un-suppressed flags. The Pattern Aggregator still observes every engine hit — suppression is a UI concern, not a data loss.

### Edge case: sentence boundary instability

spaCy sentence segmentation can shift on punctuation edits, changing the fingerprint for a trivially different reason. If this surfaces in practice, the fallback is a fixed N-token window around the flagged span (8 tokens each side) in place of the full containing sentence — less semantically clean, more stable under editing. The decision is empirical once real edit traces are available.

### Edge case: deleted span

Manager dismisses, then deletes the span in a rewrite. The dismissal row remains in the database and matches nothing in the new text. This is correct and expected. The Pattern Aggregator distinguishes "dismissed-and-kept" from "dismissed-and-removed" by joining dismissals against the final submitted text at submission time.

### Manual re-check

For major rewrites where the manager wants a clean pass against the current document state:

```
POST /documents/{doc_id}/recheck
  → Mark all flag_dismissals.active = false for this document
  → Trigger fresh engine run on current document text
  → Stream all flags (including previously suppressed) via SSE
```

---

## 13. Adoption Metrics

Adoption is measured at the **outcome level** — what ends up in the final submitted document — not at the interaction level. A manager who rewrites the flagged phrase in their own words has arguably adopted the feedback more deeply than one who clicked accept and used the platform's suggested phrasing. Both count as adoption.

### Five behavioural states per flag

**Adoption (platform worked):**

1. **Explicit accept** — clicked accept, final submission contains the suggested text.
2. **Edited around it** — did not accept, did not dismiss, but the flagged span is absent or changed in the final submission, and the edit occurred after the flag appeared.
3. **Dismissed and removed** — dismissed the flag, but the span is gone from the final submission.

**Non-adoption (platform did not change behaviour):**

4. **Dismissed and kept** — dismissed the flag, span remains in the final submission.
5. **Ignored and kept** — never interacted with the flag, span remains.

### Primary metric

**Adoption Rate = (States 1 + 2 + 3) / total flags raised.**

Framed for stakeholders: *"In X% of cases where the platform flagged bias-coded language, the language was removed or revised in the final submission."* This avoids causal over-claiming while reporting the business-relevant outcome.

### Effectiveness and calibration are separate metrics

A high dismissal rate could mean *managers resist the platform* or it could mean *the platform's flags are noisy*. The Pattern Aggregator does not conflate them. Three independent metrics:

- **Dismiss-and-kept rate** → manager-side rejection signal
- **Adoption rate** (states 1+2+3) → writing behaviour change signal
- **Agreement with held-out gold set** → platform calibration signal

No composite score. All three are reported independently.

### State 2 as the product-improvement signal

If managers consistently do not click accept but do edit the flagged text away, the detection pipeline is working but the recommendation phrasing is not landing. That is a Recommendations Agent problem, not a flag problem. Tracking State 2 separately allows iteration on the Recommendations Agent without questioning the underlying detection pipeline.

### Aggregation levels

- **By bias category** — which categories (gender-coded, age-coded, disability-coded, etc.) land vs. are resisted.
- **By manager** — feeds the individual Pattern Dashboard, framed as the manager's own longitudinal improvement trend, never visible to HR.
- **By document type** — JD vs. interview feedback vs. promotion writeup — surfaces where the platform is most and least useful.
- **Over time** — week-over-week, quarter-over-quarter longitudinal story.

The aggregate-across-managers figure is what HR and leadership see. The per-manager figure is visible only to the individual manager.
