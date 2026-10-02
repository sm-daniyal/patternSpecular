# ADR 0014: Google Gemini 3.5 Flash Lite over Anthropic Claude

## Status

Accepted

## Context

Pattern Specular adapts the core 6-stage LangGraph pipeline originally architected with Anthropic Claude (Sonnet 4.6 for analysis/drift/recommendations, Haiku 4.5 for judging). For modern cloud multi-tenancy, developer accessibility, and enterprise cost optimization, we evaluated Google's latest Gemini Flash series against Anthropic's Claude models.

Key evaluation criteria:
1. **Inference Latency & Cost:** Stage 2 (Contextual Pass) and Stage 6 (Judge) run in the real-time loop of the TipTap writing surface after a typing pause. Latency must stay under 4 seconds to preserve UX responsiveness.
2. **Structured Outputs & Schema Enforcement:** Pydantic schema validation using `instructor` without drift or field hallucinations.
3. **Free Tier & API Economics:** Free-tier throughput for portfolio and staging environments, scaling to sub-$0.10/MTok in production.

## Decision

We replace Anthropic Claude with **Google Gemini 3.5 Flash Lite** across all agentic engine stages (Contextual Pass, LLM-as-a-Judge, Recommendations, Criteria Extraction, Drift, and Dictionary Growth debate).

Implementation details:
1. Integrated via `instructor.from_genai(genai.Client(api_key=...))` wrapped in `_GeminiInstructorAdapter`.
2. Normalized token usage metrics: mapped `prompt_token_count` to `input_tokens` and `candidates_token_count` to `output_tokens` to keep audit telemetry consistent with the database schema.
3. Configured `strict=False` in Pydantic schema deserialization to ensure seamless coercion between raw JSON strings and Python `StrEnum` instances (`BiasCategory`, `FlagScope`, `FlagVerdict`).
4. Maintained a dual-provider fallback: if `GOOGLE_API_KEY` is absent but `ANTHROPIC_API_KEY` is present, the adapter automatically routes through `instructor.from_anthropic`.

## Consequences

- **Cost Efficiency:** Gemini 3.5 Flash Lite operates at \$0.05/MTok input and \$0.20/MTok output—representing an ~80% reduction compared to Claude 3.5 Haiku.
- **Provider Agnosticism:** The engine interfaces (`StructuredCompletionClient` protocol) remain decoupled from SDK-specific calling conventions.
- **Zero Schema Leakage:** Instructor-managed structured outputs guarantee that only validated Pydantic instances enter the LangGraph state channels.
