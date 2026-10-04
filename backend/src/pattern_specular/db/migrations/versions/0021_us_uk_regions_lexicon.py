"""add US and UK regions and statutory compliance lexicons

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-10-04
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "b2c3d4e5f6a7"
down_revision: str | None = "a1b2c3d4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Hardcoded citation UUIDs
_CIT_US_TITLE_VII = "c0de0004-1964-4000-a000-000000000004"
_CIT_US_ADEA = "c0de0005-1967-4000-a000-000000000005"
_CIT_US_ADA = "c0de0006-1990-4000-a000-000000000006"
_CIT_UK_EQUALITY = "c0de0007-2010-4000-a000-000000000007"

# Dictionary entry UUIDs
_D_US_01 = "d1c70002-0001-4000-a000-000000000001"
_D_US_02 = "d1c70002-0002-4000-a000-000000000002"
_D_US_03 = "d1c70002-0003-4000-a000-000000000003"
_D_UK_01 = "d1c70002-0004-4000-a000-000000000004"
_D_UK_02 = "d1c70002-0005-4000-a000-000000000005"
_D_UK_03 = "d1c70002-0006-4000-a000-000000000006"


def upgrade() -> None:
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

    # 1. Insert US and UK into regions
    regions = sa.table(
        "regions",
        sa.column("code", sa.String),
        sa.column("name", sa.String),
    )
    op.bulk_insert(
        regions,
        [
            {"code": "US", "name": "United States"},
            {"code": "GB", "name": "United Kingdom"},
        ],
    )

    # 2. Insert Citations
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
                "id": _CIT_US_TITLE_VII,
                "source_type": "regulatory",
                "title": "Title VII of the Civil Rights Act of 1964 (EEOC)",
                "reference": "https://www.eeoc.gov/statutes/title-vii-civil-rights-act-1964",
            },
            {
                "id": _CIT_US_ADEA,
                "source_type": "regulatory",
                "title": "Age Discrimination in Employment Act (ADEA), 1967",
                "reference": "https://www.eeoc.gov/statutes/age-discrimination-employment-act-1967",
            },
            {
                "id": _CIT_US_ADA,
                "source_type": "regulatory",
                "title": "Americans with Disabilities Act (ADA), 1990",
                "reference": "https://www.ada.gov/law-and-regs/ada/",
            },
            {
                "id": _CIT_UK_EQUALITY,
                "source_type": "regulatory",
                "title": "Equality Act 2010 (UK Statutory Guidance)",
                "reference": "https://www.legislation.gov.uk/ukpga/2010/15/contents",
            },
        ],
    )

    # 3. Insert Dictionaries
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
            # --- US Rules ---
            {
                "id": _D_US_01,
                "region_code": "US",
                "category": "age",
                "term": "digital native",
                "lemma_key": "digital native",
                "citation_id": _CIT_US_ADEA,
                "explanation": (
                    "Age-coded phrase that implies preference for younger generations who grew up with internet technology, "
                    "violating EEOC Age Discrimination in Employment Act (ADEA) protections."
                ),
                "recommended_alternatives": ["tech-savvy", "proficient with modern digital tools", "fast technology learner"],
            },
            {
                "id": _D_US_02,
                "region_code": "US",
                "category": "race",
                "term": "cultural fit",
                "lemma_key": "cultural fit",
                "citation_id": _CIT_US_TITLE_VII,
                "explanation": (
                    "Subjective evaluation criteria often functioning as a proxy for racial and demographic exclusion; "
                    "conflicts with EEOC Title VII guidelines favoring objective role-based competencies."
                ),
                "recommended_alternatives": ["values alignment", "collaborative team player", "cross-functional communicator"],
            },
            {
                "id": _D_US_03,
                "region_code": "US",
                "category": "religion",
                "term": "clean-shaven",
                "lemma_key": "clean-shaven",
                "citation_id": _CIT_US_TITLE_VII,
                "explanation": (
                    "Blanket grooming requirement that discriminates against individuals with religious observances "
                    "(e.g., Sikhism, Judaism, Islam) without genuine occupational justification under Title VII."
                ),
                "recommended_alternatives": ["professional appearance standards", "role-appropriate safety attire"],
            },
            # --- UK Rules ---
            {
                "id": _D_UK_01,
                "region_code": "GB",
                "category": "age",
                "term": "mature",
                "lemma_key": "mature",
                "citation_id": _CIT_UK_EQUALITY,
                "explanation": (
                    "Age-exclusionary adjective that unlawfully screens out early-career or younger applicants "
                    "under the UK Equality Act 2010 protected characteristic provisions."
                ),
                "recommended_alternatives": ["experienced", "seasoned professional", "demonstrated track record"],
            },
            {
                "id": _D_UK_02,
                "region_code": "GB",
                "category": "nationality",
                "term": "native English speaker",
                "lemma_key": "native English speaker",
                "citation_id": _CIT_UK_EQUALITY,
                "explanation": (
                    "Unlawful indirect race/nationality discrimination under the UK Equality Act 2010; "
                    "language requirements must specify objective proficiency level rather than country of origin."
                ),
                "recommended_alternatives": ["fluent in professional English", "strong business communication skills", "excellent written and verbal English"],
            },
            {
                "id": _D_UK_03,
                "region_code": "GB",
                "category": "age",
                "term": "recent graduate",
                "lemma_key": "recent graduate",
                "citation_id": _CIT_UK_EQUALITY,
                "explanation": (
                    "Indirect age discrimination excluding mature students and career switchers under UK Equality Act 2010."
                ),
                "recommended_alternatives": ["entry-level candidates", "early-career professionals", "graduates of any year"],
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            f"DELETE FROM dictionaries WHERE id IN ('{_D_US_01}', '{_D_US_02}', '{_D_US_03}', '{_D_UK_01}', '{_D_UK_02}', '{_D_UK_03}')"
        )
    )
    op.execute(
        sa.text(
            f"DELETE FROM citations WHERE id IN ('{_CIT_US_TITLE_VII}', '{_CIT_US_ADEA}', '{_CIT_US_ADA}', '{_CIT_UK_EQUALITY}')"
        )
    )
    op.execute(sa.text("DELETE FROM regions WHERE code IN ('US', 'GB')"))
