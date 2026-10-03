# ADR 0016: Cloud-Native Serverless PostgreSQL (Neon) over Local Docker

## Status

Accepted

## Context

Pattern Specular requires a reliable, ACID-compliant relational store for documents, 17 relational entity models, and longitudinal pattern analysis. While local Docker containerization was used for isolated local development in earlier revisions, cloud deployment and continuous accessibility require a resilient cloud-native database.

Key constraints:
1. **Zero-Configuration Developer Onboarding:** Eliminates virtualization and hardware-assisted virtualization (Intel VT-x) BIOS dependencies.
2. **Connection Pooling for Asynchronous & Serverless Workloads:** High-concurrency SSE streaming sessions (`POST /analyze/stream`) require efficient connection reuse.
3. **Branching & Migration Verification:** Instant database branching for migration dry-runs (`alembic upgrade head`).

## Decision

We adopt **Neon Serverless PostgreSQL** as the core database provider, configured via pooled connection strings (`aws.neon.tech`) and `psycopg` v3 binary drivers.

Implementation details:
1. Configured SSL-enforced connection parameters (`sslmode=require`).
2. Maintained Alembic migration compatibility across all 20 schema revisions.
3. Decoupled test database provisioning from container daemons.

## Consequences

- **Accessibility:** Enables immediate local and cloud execution without local Postgres daemon management.
- **Scalability:** Serverless compute scaling automatically handles burst traffic during multi-sample LLM judge runs.
