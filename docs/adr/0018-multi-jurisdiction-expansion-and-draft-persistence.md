# ADR 0018: Simultaneous Multi-Jurisdiction Evaluation and Active Draft Persistence

**Date:** 2026-10-04
**Status:** Accepted

## Context

Two independent problems surfaced after the India statutory expansion (ADR 0015) and
during UX review of the JD Studio surface:

**Problem 1 — Sequential jurisdiction evaluation.**
After adding India (`IN`) to the statutory lexicon alongside Singapore (`SG`), the
dictionary loader was queried per-jurisdiction sequentially. A manager authoring a job
description for a globally-distributed engineering team (Bangalore, London, New York,
Singapore) would receive flags from only the jurisdiction configured at request time.
Cross-border statutory compliance — a core product promise — required evaluating all
active jurisdictions simultaneously in a single engine run.

**Problem 2 — Draft loss on surface navigation.**
Navigating from JD Studio to the Pattern Dashboard or Feedback Checkpoint unmounted the
TipTap editor component, discarding any in-progress draft that had not been explicitly
saved. Managers working on long job descriptions across multiple sittings lost work on
tab or surface switch. The UX expectation is that an in-progress draft behaves like a
browser tab — it should survive navigation.

## Decision

**1. Simultaneous multi-jurisdiction aggregation.**

The active dictionary rule loader now aggregates rules across all active region codes
in a single query (`["SG", "IN", "US", "GB"]`), returning a unified rule set. The
engine evaluates all applicable rules in Stage 1 (Dictionary Module) in a single pass.
Each surfaced flag retains its `region_code` and its `citations` FK, so statutory
provenance is preserved per flag — managers see which jurisdiction's legislation applies.

Jurisdictions added in this revision:

| Jurisdiction | Legislation |
|---|---|
| United States (`US`) | Title VII of the Civil Rights Act 1964 · Age Discrimination in Employment Act (ADEA) 1967 |
| United Kingdom (`GB`) | Equality Act 2010 — all nine protected characteristics |

**2. `localStorage`-backed active draft persistence.**

JD Studio now serialises the active draft content and its `document_id` to
`localStorage` on every debounced change. On mount, if an active draft key is present
and no explicit `?doc_id` URL parameter is provided, the editor restores the draft
content and resumes real-time flagging from the persisted state. A "New draft" action
is provided to explicitly initialise a fresh document and clear the persisted draft.

Session-level persistence was chosen over server-side auto-save to avoid creating a
new database write path for every keystroke, and to keep the draft lifecycle client-owned
until the manager explicitly publishes.

## Consequences

- **42 active statutory rules** span India, Singapore, United States, and United
  Kingdom — evaluated simultaneously on every document submission.
- **Zero draft loss.** Active in-progress drafts survive surface navigation, browser
  refresh within the same session, and tab switching.
- **Longitudinal coherence.** The Pattern Dashboard aggregates findings into canonical
  protected categories (`gender`, `age`, `race`, `disability`, `gender_identity`,
  `disability`) regardless of originating jurisdiction — no dashboard fragmentation.
- **Jurisdiction extensibility confirmed.** Adding future jurisdictions (e.g. Australia's
  Fair Work Act, EU Directive 2000/78/EC) requires only a new region seed migration and
  an `adr/` record — no engine or frontend changes.
