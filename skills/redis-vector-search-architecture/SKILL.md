---
name: redis-vector-search-architecture
description: Use when designing Redis vector search architecture, semantic search, RAG retrieval, recommendation systems, hybrid vector and metadata filtering, FLAT versus HNSW index selection, vector dimensions and distance metrics, JSON versus HASH modeling, shard fan-out, coordinator merge costs, recall tuning, schema drift, or vector-search latency and memory tradeoffs.
---

# Redis Vector Search Architecture

Use this skill for conceptual design and review of Redis vector search workloads. For product-specific setup, route to Redis Cloud or Redis Software vector implementation guidance after the architecture is clear.

## Architecture Model

Redis vector search has a coordinated execution path:

1. The coordinator parses the query and metadata predicates.
2. Work is distributed to shards.
3. Each shard evaluates candidates with its local vector index.
4. Results are merged, sorted, ranked, and returned.

Design consequence: metadata filters, shard count, result size, and coordinator merge work all affect latency.

## Index Choice

Choose `FLAT` when:

- the dataset is small
- exact KNN is required
- the workload is a correctness baseline or test
- predictable recall matters more than latency

Choose `HNSW` when:

- the dataset is large
- low-latency approximate nearest neighbor search is acceptable
- recall can be tuned and measured
- production scale requires avoiding full scans

Tune HNSW as a recall-latency tradeoff, not as a one-time setting.

## Data Modeling

Use JSON when:

- metadata is nested or evolving
- hybrid filtering is central to the workload
- GenAI/RAG documents carry rich attributes

Use HASH when:

- schema is fixed
- metadata is flat
- memory efficiency matters more than schema flexibility

Always enforce:

- one embedding model and dimension per index
- consistent datatype, typically `FLOAT32`
- distance metric aligned with the embedding model
- indexed metadata fields for frequent filters

Prefer RedisVL for Python application code when building schema-driven vector indexes, hybrid filters, and retrieval workflows.

## Query Design

- Apply selective metadata filters early to reduce candidate work.
- Bound result counts and returned fields.
- Avoid broad filters that force fan-out across many shards.
- Keep tenant, ACL, document-type, language, or freshness filters indexed when they are common.
- Use `FT.EXPLAIN` for query shape and `FT.PROFILE` for runtime behavior when available.

## Failure Patterns

- Schema drift: stored documents no longer match index definitions.
- Recall surprises: HNSW settings are too aggressive, or filters remove relevant candidates.
- Latency cliffs: unbounded result sets, high shard fan-out, large vectors, or coordinator merge pressure.
- Memory pressure: high vector count, high dimensions, inefficient metadata model, or poor shard balance.
- Delete spikes: large indexed keys deleted synchronously; prefer `UNLINK` when safe.

## Response Pattern

When advising:

1. Identify the retrieval use case and scale.
2. Recommend data model and index algorithm.
3. Define metadata filters and sharding implications.
4. Specify recall, latency, and memory measurements.
5. Call out the first design risks to validate before production.
