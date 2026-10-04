"""Shared LLM-agent plumbing: cost estimation and Instructor client construction.

Client construction is network-free, so these run offline and never touch the live API.
"""

from decimal import Decimal

from pattern_specular.core.config import Settings
from pattern_specular.engine.llm_agent import build_instructor_client, estimate_cost_usd


def test_estimate_cost_usd_prices_a_known_model() -> None:
    # claude-sonnet-4-6: $3/MTok in, $15/MTok out -> (120*3 + 40*15) / 1e6.
    assert estimate_cost_usd("claude-sonnet-4-6", 120, 40) == Decimal("0.00096")
    # claude-haiku-4-5: $1/MTok in, $5/MTok out -> (120*1 + 40*5) / 1e6.
    assert estimate_cost_usd("claude-haiku-4-5", 120, 40) == Decimal("0.00032")


def test_estimate_cost_usd_is_none_for_unknown_model_or_missing_usage() -> None:
    assert estimate_cost_usd("mystery-model", 100, 50) is None
    assert estimate_cost_usd("claude-sonnet-4-6", None, 50) is None


def _settings(*, GOOGLE_API_KEY: str | None) -> Settings:
    return Settings(
        app_env="test",
        database_url="postgresql+psycopg://x:y@localhost/db",
        GOOGLE_API_KEY=GOOGLE_API_KEY,
    )


def test_build_instructor_client_is_none_without_a_key() -> None:
    assert build_instructor_client(_settings(GOOGLE_API_KEY=None)) is None


def test_build_instructor_client_builds_a_client_with_a_key() -> None:
    # Construction is network-free; no request is made here.
    assert build_instructor_client(_settings(GOOGLE_API_KEY="sk-ant-test")) is not None
