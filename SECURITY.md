# Security Policy

## Supported Versions

Pattern Specular receives active security updates and patch releases on the `main` branch.

## Privacy & Data Protection Model

1. **Manager Isolation:** Individual writing content is architecturally isolated to the authenticated author.
2. **Aggregated Analytics:** All HR reporting endpoints enforce $k \ge 3$ cell-size suppression at the database query level to eliminate re-identification risks.
3. **No Model Retention:** External LLM calls via Google Gemini operate with zero prompt-storage or training retention agreements.

## Reporting a Vulnerability

If you discover a potential security concern or vulnerability, please open a private GitHub advisory or email the maintainer directly.
