# ADR 0017: Tailwind CSS v4 Design Token Architecture (Rosewood)

**Date:** 2026-08-03
**Status:** Accepted

## Context

Pattern Specular's writing surfaces — JD Studio, Feedback Checkpoint, Promotion Writeup
— use a TipTap (ProseMirror) rich text editor with inline flag decorations. Two visual
layers of flags need to be consistently distinguishable:

- **Statutory dictionary flags** (Stage 1) — deterministic, high-confidence, appear
  instantly. Should feel authoritative and immediate.
- **Contextual pass flags** (Stage 2) — LLM-surfaced, streamed in after a typing
  pause. Should feel considered and provisional.

The flag decoration styles (underline type, colour, badge) need to be defined in one
place and consumed consistently across the TipTap editor, the sidebar panel, and any
future surface. Hardcoding hex values across component files creates drift; a design
token system prevents it.

Additionally, the adapted product needed a distinct visual identity from Pattern Mirror.
Pattern Mirror uses a default-neutral palette; Pattern Specular introduces the Rosewood
palette — a deep pink/plum accent system — to establish a clear visual identity.

## Decision

Use **Tailwind CSS v4's CSS variable engine** to define the full design token system
in `frontend/src/styles/tokens/`.

Token categories:

| Token | Value | Usage |
|---|---|---|
| `--color-rosewood` | `#b83a58` | Primary accent: buttons, active states, links |
| `--color-rosewood-hover` | `#9c2742` | Hover/pressed state for primary interactive elements |
| `--color-canvas` | `#f7f3f4` | Workspace writing canvas background |
| `--color-surface` | `#ffffff` | Card and panel surfaces |
| `--color-border` | `#ebdce2` | Hairline borders and dividers |
| `--color-ink` | `#1e1317` | Primary typography (deep plum-charcoal) |
| `--color-ink-secondary` | `#6e5860` | Secondary / muted text |
| `--color-blush` | `#fbf2f4` | Soft tint for hover states and selected backgrounds |
| `--color-flag-dict` | Rosewood-derived | Statutory dictionary underline and badge |
| `--color-flag-context` | Amber-derived | Contextual pass dashed underline tint |

TipTap editor decorations, sidebar panels, and modal surfaces all consume these tokens
via Tailwind utility classes — no component hardcodes a hex value.

## Consequences

- **Consistent flag hierarchy.** Statutory flags (solid Rosewood underline) and
  contextual flags (dashed amber underline) are visually distinct at a glance without
  requiring proximity to a legend.
- **Maintainability.** Changing the palette is a one-file edit in
  `src/styles/tokens/` — it propagates automatically to every consumer.
- **Accessibility.** The token layer provides a single hook for a high-contrast
  accessibility theme override, without touching component code.
- **Identity.** The Rosewood palette gives Pattern Specular a distinct visual identity
  from Pattern Mirror, appropriate for a sovereign architectural extension.
