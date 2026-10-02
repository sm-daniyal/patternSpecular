# ADR 0015: Multi-Region Statutory Expansion (India Jurisdiction)

## Status

Accepted

## Context

The initial MVP of the architecture was scoped strictly to Singapore's TAFEP (Tripartite Alliance for Fair and Progressive Employment Practices) guidelines. To demonstrate jurisdiction-agnostic scalability, the system was expanded to support multi-national regulatory compliance frameworks, specifically adding India's statutory employment laws.

Key Indian labor regulations addressed:
1. **Code on Wages, 2019:** Mandates gender-neutral remuneration and prohibits discrimination on grounds of sex or age for the same work or work of similar nature.
2. **Rights of Persons with Disabilities (RPwD) Act, 2016:** Prohibits discrimination against persons with disabilities and mandates reasonable accommodations in recruitment.
3. **Transgender Persons (Protection of Rights) Act, 2019:** Forbids unfair discrimination in employment, recruitment, and career advancement against transgender individuals.

## Decision

1. Expanded the `regions` table to seed the `IN` jurisdiction code alongside `SG`.
2. Created Alembic migration `0020_india_region_lexicon.py` to seed regulatory citations and curated dictionary rules for India.
3. Added statutory lexicon rules for:
   - `young`, `fresh`, `energetic` (Age discrimination under Code on Wages, 2019)
   - `manpower` (Gender exclusion under Code on Wages, 2019)
   - `physically fit`, `normal` (Disability-coded language under RPwD Act, 2016)
   - `male/female only` (Binary exclusion under Transgender Persons Act, 2019)
4. Configured curated, research-backed neutral alternatives for all seeded Indian statutory terms.

## Consequences

- **Multi-Region Architecture:** Proves that the deterministic Stage 1 dictionary and the LLM-gated Stage 2 contextual pass scale seamlessly to distinct international legal standards simply by partitioning on `region_code`.
- **Verifiable Provenance:** Every flagged term in the Indian jurisdiction links directly to official Ministry gazettes and legislative acts (`citations` table).
