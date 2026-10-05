# ADR 0014: Google Gemini over Anthropic Claude

**Date:** 2026-07-12
**Status:** Accepted

## Context

Pattern Specular inherits the engine architecture from Pattern Mirror, which was built
against Anthropic Claude (Sonnet 4.6 for analysis, drift, and recommendations; Haiku 4.5
for judging). Evaluating the model layer for this adaptation surfaced three requirements
that drove the provider decision:

1. **Latency budget.** Stage 2 (Contextual Pass) and Stage 6 (Judge) run in the
   real-time path after a manager's typing pause. The full contextual pass must
   complete and begin streaming within 4–5 seconds to preserve the UX contract.
2. **Schema enforcement.** Every LLM-stage output feeds directly into a typed Pydantic
   model inside a LangGraph state channel. Field hallucinations or type mismatches
   cannot be tolerated — they corrupt the pipeline state.
3. **Cost at scale.** The Judge runs N independent samples per flag. At any non-trivial
   usage volume, per-token cost for the Judge model determines whether multi-sample
   consensus is economically viable.

## Decision

Replace Anthropic Claude with **Google Gemini** across all agentic engine stages.

Model allocation:

| Stage | Model | Rationale |
|---|---|---|
| Contextual Pass | `gemini-2.5-flash` | Full-context evaluation; best balance of reasoning depth and latency |
| Judge | `gemini-3.5-flash-lite` | Multi-sample runs; cost efficiency for N independent calls |
| Recommendations | `gemini-2.5-flash` | Evidence-anchored rewrite quality matters more than volume |
| Debate agents (×4) | `gemini-2.5-flash` | Independent reasoning per agent; citation retrieval |
| Drift check | `gemini-2.5-flash` | Criteria coverage evaluation against reference corpus |

Integration via `instructor.from_genai(genai.Client(api_key=...))` wrapped in a
`_GeminiInstructorAdapter`. Token usage metrics are normalised at the adapter layer:
`prompt_token_count` → `input_tokens`, `candidates_token_count` → `output_tokens`,
keeping audit telemetry consistent with the existing `agent_runs` schema. Pydantic
schema deserialisation uses `strict=False` to handle seamless coercion between raw
JSON strings and Python `StrEnum` instances (`BiasCategory`, `FlagScope`, `FlagVerdict`).

## Consequences

- **Cost.** `gemini-3.5-flash-lite` at ~\$0.05/MTok input and ~\$0.20/MTok output
  makes multi-sample Judge runs economically viable at the default sample count.
- **Degraded mode.** Without `GOOGLE_API_KEY`, LLM stages become transparent
  passthroughs — dictionary flagging (Stage 1) still runs. This is deliberate: the
  deterministic path should never be blocked by a missing API credential.
- **Schema invariant.** Instructor guarantees that only validated Pydantic instances
  enter LangGraph state channels — LLM output never flows as raw text into the engine.
- **Provider lock-in is shallow.** The `StructuredCompletionClient` protocol decouples
  the engine from SDK-specific calling conventions. Model ids are config, not code;
  changing a model variant requires no engine change.
