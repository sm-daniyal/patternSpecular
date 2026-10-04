"""Verify active US and UK regulatory rules and citations in the database."""

import pytest
from sqlalchemy import select

from pattern_specular.db.session import get_sessionmaker
from pattern_specular.engine.dictionary import load_active_rules


def test_us_rules_loaded() -> None:
    session_factory = get_sessionmaker()
    with session_factory() as session:
        rules = load_active_rules(session, region_code="US")
        terms = {r.term for r in rules}
        assert "digital native" in terms
        assert "cultural fit" in terms
        assert "clean-shaven" in terms
        assert len(rules) >= 3


def test_uk_rules_loaded() -> None:
    session_factory = get_sessionmaker()
    with session_factory() as session:
        rules = load_active_rules(session, region_code="GB")
        terms = {r.term for r in rules}
        assert "mature" in terms
        assert "native English speaker" in terms
        assert "recent graduate" in terms
        assert len(rules) >= 3
