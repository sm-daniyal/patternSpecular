"""Shared LLM-agent plumbing: cost estimation and Instructor client construction.

Client construction is network-free, so these run offline and never touch the live API.
"""

from decimal import Decimal

from pattern_specular.core.config import Settings
from pattern_specular.engine.llm_agent import build_instructor_client, estimate_cost_usd


def test_estimate_cost_usd_prices_a_known_model() -> None:
    # gemini-3.5-flash-lite: $0.05/MTok in, $0.20/MTok out -> (120*0.05 + 40*0.20) / 1e6.
    assert estimate_cost_usd("gemini-3.5-flash-lite", 120, 40) == Decimal("0.000014")
    # gemini-2.0-flash: $0.10/MTok in, $0.40/MTok out -> (120*0.10 + 40*0.40) / 1e6.
    assert estimate_cost_usd("gemini-2.0-flash", 120, 40) == Decimal("0.000028")


def test_estimate_cost_usd_is_none_for_unknown_model_or_missing_usage() -> None:
    assert estimate_cost_usd("mystery-model", 100, 50) is None
    assert estimate_cost_usd("gemini-3.5-flash-lite", None, 50) is None


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
