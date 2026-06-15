---
name: redis-data-integration-intake
description: Use when a user asks about Redis Data Integration, connecting external data sources to Redis, data-ingestion architecture, change-data-capture into Redis, synchronization requirements, or choosing a supported Redis integration path but has not provided enough product, source-system, or topology detail.
---

# Redis Data Integration Intake

Use this skill as an intake and routing workflow for Redis Data Integration questions. The source material for this topic contains no procedure, so do not infer product behavior from the title alone. Verify current Redis documentation, product availability, and connector support before giving implementation instructions.

## Intake Questions

Collect:

- Redis target: Redis Cloud, Redis Software, Redis for Kubernetes, or self-managed Redis
- source system: database, stream, application events, files, or another cache
- integration pattern: batch load, CDC, event streaming, cache-aside, write-through, or search/vector indexing
- latency target and freshness requirement
- data volume, update rate, and expected key count
- transformation and schema requirements
- network path, security controls, TLS, ACLs, and private connectivity needs
- failure handling, replay, idempotency, and backfill expectations

## Decision Workflow

1. Clarify whether the user needs a managed Redis product feature, a Redis connector, an application-level ingestion pattern, or a migration workflow.
2. Verify current supported integrations for the user's Redis product and region before naming a specific connector or service.
3. If the goal is vector, search, or RAG ingestion, route to RedisVL or Search-specific design guidance.
4. If the goal is database migration, route to migration tooling and cutover planning.
5. If the goal is continuous sync, design for idempotent writes, retry, dead-letter handling, and observability.

## Design Checks

- Choose key names and data structures before implementing ingestion.
- Ensure writes are safe to replay.
- Use pipelining or batching for high-volume ingestion.
- Keep payloads small enough to meet latency and throughput targets.
- Monitor ingest lag, command errors, memory growth, evictions, and slow commands.
- Plan backfill separately from steady-state sync.

## Response Pattern

When answering:

1. State that the exact supported integration path must be verified for the user's Redis product and source system.
2. Summarize the likely integration pattern.
3. List the minimum design decisions needed before implementation.
4. Provide next-step options rather than product-specific steps unless they are verified.
