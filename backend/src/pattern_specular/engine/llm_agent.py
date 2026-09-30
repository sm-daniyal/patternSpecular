"""Shared plumbing for the LLM Agent stages: Instructor client, pricing, cost estimate.

The Contextual Pass, Judge, and Recommendations stages each make one schema-enforced
LLM call; the client contract, pricing table, and cost estimate are identical and
live here once. Stage modules own only their prompt and schema.
Supports Google Gemini (via google-genai) and Anthropic Claude.
"""

from decimal import Decimal
from typing import Any, Protocol, cast

import instructor
from google import genai
from anthropic import Anthropic

from pattern_specular.core.config import Settings

# Static USD/MTok (input, output); an unknown model logs a null cost, never a wrong one.
_PRICES_USD_PER_MTOK: dict[str, tuple[str, str]] = {
    "gemini-3.5-flash-lite": ("0.05", "0.20"),
    "gemini-3.8-flash": ("0.075", "0.30"),
    "gemini-2.5-flash": ("0.075", "0.30"),
    "gemini-1.5-flash": ("0.075", "0.30"),
    "gemini-2.0-flash": ("0.10", "0.40"),
    "claude-sonnet-4-6": ("3", "15"),
    "claude-haiku-4-5": ("1", "5"),
}


class StructuredCompletionClient(Protocol):
    """Schema-validated Instructor output plus the raw completion, the only method used.

    A Protocol so the Agents accept a deterministic test fake without coupling to Instructor.
    """

    def create_with_completion(self, **kwargs: Any) -> tuple[Any, Any]: ...


class _GeminiInstructorAdapter:
    """Wraps instructor.from_genai client to normalize token usage attributes."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def create_with_completion(self, **kwargs: Any) -> tuple[Any, Any]:
        kwargs.setdefault("strict", False)
        parsed, completion = self._client.create_with_completion(**kwargs)
        # Normalize token usage if present
        usage = getattr(completion, "usage", None)
        if usage is not None:
            if not hasattr(usage, "input_tokens"):
                usage.input_tokens = getattr(usage, "prompt_token_count", None)
            if not hasattr(usage, "output_tokens"):
                usage.output_tokens = getattr(usage, "candidates_token_count", None)
        return parsed, completion


def estimate_cost_usd(
    model: str, prompt_tokens: int | None, completion_tokens: int | None
) -> Decimal | None:
    """Estimate the call cost from token usage, or None if pricing/usage is unavailable."""
    price = _PRICES_USD_PER_MTOK.get(model)
    if price is None or prompt_tokens is None or completion_tokens is None:
        return None
    input_price, output_price = price
    per_million = Decimal(1_000_000)
    return (
        Decimal(prompt_tokens) * Decimal(input_price)
        + Decimal(completion_tokens) * Decimal(output_price)
    ) / per_million


def build_instructor_client(settings: Settings) -> StructuredCompletionClient | None:
    """Build the Instructor-wrapped LLM client (Google Gemini or Anthropic Claude).

    Network-free: no request is made until ``create_with_completion`` is called. None lets
    the orchestrator degrade an Agent stage to a passthrough.
    """
    if settings.google_api_key:
        genai_client = genai.Client(api_key=settings.google_api_key)
        raw_client = instructor.from_genai(genai_client)
        return cast(StructuredCompletionClient, _GeminiInstructorAdapter(raw_client))

    if settings.anthropic_api_key:
        anthropic_client = instructor.from_anthropic(Anthropic(api_key=settings.anthropic_api_key))
        return cast(StructuredCompletionClient, anthropic_client)

    return None
