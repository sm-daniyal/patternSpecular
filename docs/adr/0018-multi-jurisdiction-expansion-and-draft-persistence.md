# ADR 0018: Global Multi-Jurisdiction Statutory Lexicon and Session-Scoped Draft Persistence

## Status

Accepted

## Context

Pattern Specular initially evaluated documents against Singapore TAFEP regulations before expanding to Indian labor statutes (Code on Wages 2019, RPwD Act 2016). In multinational enterprises, hiring managers and HR teams author job descriptions and candidate feedback across global engineering corridors (Bangalore, London, New York, Singapore). Evaluating documents against a single siloed jurisdiction forced managers to toggle arbitrary settings and missed cross-border statutory non-compliance.

Additionally, user interaction research indicated that navigating between surfaces (e.g. from JD Studio to Pattern Dashboard or Feedback Checkpoint) unmounted the client editor, discarding active in-flight drafts if not explicitly opened via URL parameters.

## Decision

1. **Simultaneous Global Statutory Evaluation:**
   - Expanded the active dictionary rule loader to support simultaneous multi-region aggregation (`["SG", "IN", "US", "GB"]`).
   - Integrated US statutory citations: Title VII of the Civil Rights Act of 1964, Age Discrimination in Employment Act (ADEA) of 1967, and Americans with Disabilities Act (ADA) of 1990.
   - Integrated UK statutory citations: Equality Act 2010 protected characteristics.
   - Preserved individual statutory citation provenance on every surfaced flag via foreign key mappings to sovereign legal references.

2. **Session-Scoped Draft Restoration:**
   - Enhanced `JdStudio` with `sessionStorage` draft persistence (`active_jd_draft_id`).
   - Seamlessly re-hydrates un-submitted active documents upon navigation without losing typed content or real-time bias underlines.
   - Provided an explicit "New draft" action allowing managers to deliberately initialize fresh documents.

## Consequences

- **Global Compliance Coverage:** Job descriptions are automatically evaluated across 42 active statutory rules spanning India, Singapore, the United States, and the United Kingdom.
- **Improved Authoring Experience:** Zero draft loss during surface transitions.
- **Longitudinal Coherence:** The longitudinal Pattern Dashboard continues to aggregate findings into canonical protected categories (`gender`, `age`, `race`, `disability`) without jurisdictional fragmentation.
