"""record_agent_run persists one agent_runs row, flushed but not committed."""

from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from pattern_specular.models.audit import AgentRun
from pattern_specular.models.documents import Document
from pattern_specular.models.enums import AgentName, DocType
from pattern_specular.models.identity import User
from pattern_specular.services.agent_runs import record_agent_run

pytestmark = pytest.mark.db


def _document(db_session: Session) -> Document:
    owner = User(
        external_user_id="test-manager",
        legal_name="Test Manager",
        email="test.manager@example.com",
    )
    db_session.add(owner)
    db_session.flush()
    document = Document(owner_id=owner.id, doc_type=DocType.jd, content="We want a digital native.")
    db_session.add(document)
    db_session.flush()
    return document


def test_persists_a_full_row(db_session: Session) -> None:
    document = _document(db_session)

    run = record_agent_run(
        db_session,
        agent_name=AgentName.judge,
        model="gemini-3.5-flash-lite",
        input={"span": "digital native"},
        output={"confidence": 0.91},
        document_id=document.id,
        prompt_tokens=120,
        completion_tokens=8,
        cost_usd=Decimal("0.000412"),
        latency_ms=640,
    )

    assert run.id is not None
    assert run.created_at is not None

    stored = db_session.get(AgentRun, run.id)
    assert stored is not None
    assert stored.agent_name is AgentName.judge
    assert stored.model == "gemini-3.5-flash-lite"
    assert stored.document_id == document.id
    assert stored.prompt_tokens == 120
    assert stored.completion_tokens == 8
    assert stored.cost_usd == Decimal("0.000412")
    assert stored.latency_ms == 640


def test_optional_fields_default_to_null(db_session: Session) -> None:
    run = record_agent_run(
        db_session,
        agent_name=AgentName.contextual_pass,
        model="gemini-3.5-flash-lite",
        input={"document_text": "We want a digital native."},
        output={"flags": []},
    )

    stored = db_session.get(AgentRun, run.id)
    assert stored is not None
    assert stored.document_id is None
    assert stored.flag_id is None
    assert stored.analysis_run_id is None
    assert stored.prompt_tokens is None
    assert stored.completion_tokens is None
    assert stored.cost_usd is None
    assert stored.latency_ms is None


def test_jsonb_io_round_trips(db_session: Session) -> None:
    nested_input = {"context": {"role": "engineer", "tags": ["general", "role-specific"]}}
    nested_output = {"flags": [{"span": "sharp", "confidence": 0.8}], "count": 1}

    run = record_agent_run(
        db_session,
        agent_name=AgentName.recommendations,
        model="gemini-3.5-flash-lite",
        input=nested_input,
        output=nested_output,
    )

    db_session.expire(run)
    assert run.input == nested_input
    assert run.output == nested_output
