# ADR 0017: Tailwind CSS v4 Design Token Architecture

## Status

Accepted

## Context

The writing surface requires high-contrast visual cues to differentiate deterministic statutory flags (solid red) from LLM-surfaced contextual flags (dashed amber). A maintainable design system must decouple raw hex colors from UI component logic.

## Decision

We leverage Tailwind CSS v4's CSS variable engine to establish semantic tokens:
- `--color-canvas`: Background writing canvas.
- `--color-ink`: Primary typography.
- `--color-flag-dict`: Statutory dictionary underline and badge tint.
- `--color-flag-context`: Agentic contextual pass dashed underline tint.

## Consequences

- Consistent visual hierarchy across TipTap editor decorations and sidebar summary panels.
- Rapid adaptation for high-contrast accessibility themes.
