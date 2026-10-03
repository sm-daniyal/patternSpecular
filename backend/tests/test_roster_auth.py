"""Verify active user roster authentication and role assignments."""

import pytest
from sqlalchemy import select

from pattern_specular.db.session import get_sessionmaker
from pattern_specular.models.enums import UserRole
from pattern_specular.models.identity import User
from pattern_specular.services.auth import authenticate


def test_manager_roster_authentication() -> None:
    session_factory = get_sessionmaker()
    with session_factory() as session:
        user = authenticate(
            session, email="sm.daniyal@example.com", expected_role=UserRole.manager
        )
        assert user.legal_name == "SM Daniyal"
        assert UserRole.manager in {r.role for r in user.roles}


def test_hr_user_authentication() -> None:
    session_factory = get_sessionmaker()
    with session_factory() as session:
        user = authenticate(
            session, email="teresa.lisbon@example.com", expected_role=UserRole.hr
        )
        assert user.legal_name == "Teresa Lisbon"
        assert UserRole.hr in {r.role for r in user.roles}
