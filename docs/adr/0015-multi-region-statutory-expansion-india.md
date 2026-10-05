# ADR 0015: Multi-Region Statutory Expansion — India Jurisdiction

**Date:** 2026-07-12
**Status:** Accepted

## Context

The inherited engine was scoped to Singapore's TAFEP guidelines as its single active
jurisdiction. Bias-language coding is region-specific — phrases that constitute indirect
discrimination under India's Code on Wages 2019 do not map to TAFEP categories, and
vice versa. Evaluating a document authored in a global engineering context against a
single jurisdiction's lexicon produces false negatives for managers operating in or
hiring for other markets.

Demonstrating jurisdiction-agnostic scalability required adding at least one additional
statutory framework with materially different protected characteristics and legislative
language. India was selected because:

1. It has three distinct, well-documented statutory instruments covering different
   protected characteristics (wages/gender, disability, gender identity).
2. The legislation is recent (2016–2019), actively enforced, and publicly available
   in official gazette form for citation.
3. Its protected-characteristic categories (disability-coded language, gender-identity
   framing) extend coverage beyond TAFEP's scope without duplicating it.

## Decision

Expand the statutory lexicon to the `IN` jurisdiction.

Implementation:

1. Seeded the `regions` table with the `IN` jurisdiction code.
2. Created Alembic migration `0020_india_region_lexicon.py` to seed regulatory
   citations and curated dictionary entries for the three Indian statutes.
3. Statutory coverage added:

| Statute | Protected characteristic | Example term |
|---|---|---|
| Code on Wages 2019 | Age · Gender | `young`, `fresh`, `energetic`, `manpower` |
| RPwD Act 2016 | Disability | `physically fit`, `able-bodied`, `normal` |
| Transgender Persons Act 2019 | Gender identity | `male/female only`, binary-exclusive framing |

4. Each seeded entry carries a `citations` FK to the specific legislative provision —
   Section 3(1) Code on Wages, Section 20 RPwD Act, Section 11 Transgender Act — so
   the provenance is reconstructable to the official gazette.

## Consequences

- **Multi-jurisdiction by partition.** The dictionary loader selects entries by
  `region_code`; no engine change was required to add `IN`. The same pattern applies to
  future jurisdictions — US (Title VII, ADEA), UK (Equality Act 2010), and others.
- **Verifiable provenance.** Every flagged term in the Indian jurisdiction links
  directly to official Ministry of Law and Justice gazette references.
- **Test coverage.** The 76-file backend test suite covers the India lexicon entries
  as unit tests against the Dictionary Module and as integration tests through the full
  seven-stage pipeline.
