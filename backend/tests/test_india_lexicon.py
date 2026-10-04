"""Verify active India regulatory rules and citations in the database."""

import pytest
from sqlalchemy import select

from pattern_specular.db.session import get_sessionmaker
from pattern_specular.engine.dictionary import load_active_rules


def test_india_rules_loaded() -> None:
    session_factory = get_sessionmaker()
    with session_factory() as session:
        rules = load_active_rules(session, region_code="IN")
        terms = {r.lemma_key for r in rules}
        assert "young" in terms
        assert "manpower" in terms
        assert "physically fit" in terms
        assert "male/female only" in terms
        assert len(rules) >= 7
