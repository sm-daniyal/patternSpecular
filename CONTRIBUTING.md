# Contributing to Pattern Specular

Thank you for your interest in Pattern Specular! We maintain strict code quality, type-safety, and test coverage standards.

## Code Quality Standards

1. **Strict Type Safety:**
   - Python: Must pass `mypy --strict` with zero type ignores on core models and engine nodes.
   - TypeScript: Must pass `tsc -b` with strict null checks enabled.

2. **Linting & Formatting:**
   - Backend: Formatted with `ruff` (line-length: 100).
   - Frontend: Formatted with `prettier` and validated via `eslint`.

3. **Statutory Gating:**
   - Any proposed dictionary rule must be backed by a published statutory or academic citation.
   - Raw quotes must be verified verbatim by the Adjudicator module before flags can surface.

## Pull Request Guidelines

1. Prefix commit messages following Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
2. Ensure automated CI checks pass (`.github/workflows/ci.yml`).
