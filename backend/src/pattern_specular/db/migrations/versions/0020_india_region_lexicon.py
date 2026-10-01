"""add india region and lexicon

Revision ID: a1b2c3d4e5f6
Revises: 0019_dictionary_recs
Create Date: 2026-10-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "a1b2c3d4e5f6"
down_revision: str | None = "0019_dictionary_recs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Hardcoded citation UUIDs so the downgrade can reference them.
_CIT_WAGES = "c0de0001-2019-4000-a000-000000000001"
_CIT_RPWD = "c0de0002-2016-4000-a000-000000000002"
_CIT_TRANS = "c0de0003-2019-4000-a000-000000000003"

# Dictionary entry UUIDs.
_D01 = "d1c70001-0001-4000-a000-000000000001"
_D02 = "d1c70001-0002-4000-a000-000000000002"
_D03 = "d1c70001-0003-4000-a000-000000000003"
_D04 = "d1c70001-0004-4000-a000-000000000004"
_D05 = "d1c70001-0005-4000-a000-000000000005"
_D06 = "d1c70001-0006-4000-a000-000000000006"
_D07 = "d1c70001-0007-4000-a000-000000000007"


def upgrade() -> None:
    # --- Region ---
    regions = sa.table("regions", sa.column("code", sa.String), sa.column("name", sa.String))
    op.bulk_insert(regions, [{"code": "IN", "name": "India"}])

    citation_source_type = postgresql.ENUM(
        "tafep", "academic", "regulatory", "other", name="citation_source_type", create_type=False
    )
    bias_category = postgresql.ENUM(
        "gender",
        "age",
        "race",
        "nationality",
        "religion",
        "disability",
        "family_status",
        name="bias_category",
        create_type=False,
    )

    # --- Citations ---
    citations = sa.table(
        "citations",
        sa.column("id", sa.Uuid),
        sa.column("source_type", citation_source_type),
        sa.column("title", sa.String),
        sa.column("reference", sa.String),
    )
    op.bulk_insert(
        citations,
        [
            {
                "id": _CIT_WAGES,
                "source_type": "regulatory",
                "title": "Code on Wages, 2019",
                "reference": "https://labour.gov.in/code-on-wages",
            },
            {
                "id": _CIT_RPWD,
                "source_type": "regulatory",
                "title": "Rights of Persons with Disabilities Act, 2016",
                "reference": "https://disabilityaffairs.gov.in/content/page/rpwd-act-2016.php",
            },
            {
                "id": _CIT_TRANS,
                "source_type": "regulatory",
                "title": "Transgender Persons (Protection of Rights) Act, 2019",
                "reference": "https://legislative.gov.in/sites/default/files/A2019-40_0.pdf",
            },
        ],
    )

    # --- Dictionary entries (India lexicon) ---
    dictionaries = sa.table(
        "dictionaries",
        sa.column("id", sa.Uuid),
        sa.column("region_code", sa.String),
        sa.column("category", bias_category),
        sa.column("term", sa.String),
        sa.column("lemma_key", sa.String),
        sa.column("citation_id", sa.Uuid),
        sa.column("explanation", sa.Text),
        sa.column("recommended_alternatives", postgresql.JSONB),
    )
    op.bulk_insert(
        dictionaries,
        [
            # --- Code on Wages, 2019 ---
            {
                "id": _D01,
                "region_code": "IN",
                "category": "age",
                "term": "young",
                "lemma_key": "young",
                "citation_id": _CIT_WAGES,
                "explanation": (
                    "Age-coded language excludes candidates over an unspecified threshold, "
                    "violating equal remuneration principles under the Code on Wages, 2019."
                ),
                "recommended_alternatives": ["motivated", "enthusiastic", "driven"],
            },
            {
                "id": _D02,
                "region_code": "IN",
                "category": "age",
                "term": "fresh",
                "lemma_key": "fresh",
                "citation_id": _CIT_WAGES,
                "explanation": (
                    "Proxy for early-career or young candidates; discriminates by age "
                    "under the Code on Wages, 2019."
                ),
                "recommended_alternatives": ["recent graduate", "early-career"],
            },
            {
                "id": _D03,
                "region_code": "IN",
                "category": "age",
                "term": "energetic",
                "lemma_key": "energetic",
                "citation_id": _CIT_WAGES,
                "explanation": (
                    "Often used as proxy for youth; discriminatory under the "
                    "Code on Wages, 2019."
                ),
                "recommended_alternatives": ["proactive", "self-driven"],
            },
            {
                "id": _D04,
                "region_code": "IN",
                "category": "gender",
                "term": "manpower",
                "lemma_key": "manpower",
                "citation_id": _CIT_WAGES,
                "explanation": (
                    "Gender-coded term implying male workforce; conflicts with equal pay "
                    "for equal work provisions under the Code on Wages, 2019."
                ),
                "recommended_alternatives": ["workforce", "personnel", "team members"],
            },
            # --- RPwD Act, 2016 ---
            {
                "id": _D05,
                "region_code": "IN",
                "category": "disability",
                "term": "physically fit",
                "lemma_key": "physically fit",
                "citation_id": _CIT_RPWD,
                "explanation": (
                    "Blanket fitness requirement excludes persons with disabilities unless "
                    "stated as a genuine occupational requirement under the RPwD Act, 2016."
                ),
                "recommended_alternatives": [
                    "able to perform essential job functions",
                    "meets role-specific physical requirements",
                ],
            },
            {
                "id": _D06,
                "region_code": "IN",
                "category": "disability",
                "term": "normal",
                "lemma_key": "normal",
                "citation_id": _CIT_RPWD,
                "explanation": (
                    "Ableist language that others persons with disabilities; conflicts "
                    "with RPwD Act, 2016 anti-discrimination provisions."
                ),
                "recommended_alternatives": ["typical", "standard", "expected"],
            },
            # --- Transgender Persons Act, 2019 ---
            {
                "id": _D07,
                "region_code": "IN",
                "category": "gender",
                "term": "male/female only",
                "lemma_key": "male/female only",
                "citation_id": _CIT_TRANS,
                "explanation": (
                    "Binary gender restriction excludes transgender persons, violating "
                    "the Transgender Persons (Protection of Rights) Act, 2019."
                ),
                "recommended_alternatives": [
                    "all genders welcome",
                    "open to all candidates",
                ],
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM dictionaries WHERE region_code = 'IN'")
    )
    op.execute(
        sa.text(
            "DELETE FROM citations WHERE id IN (:c1, :c2, :c3)"
        ).bindparams(c1=_CIT_WAGES, c2=_CIT_RPWD, c3=_CIT_TRANS)
    )
    op.execute(sa.text("DELETE FROM regions WHERE code = 'IN'"))
