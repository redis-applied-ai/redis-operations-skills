---
name: redis-software-vector-database
description: "Design, enable, implement, tune, and troubleshoot Redis Software vector database workloads using Search and Query, JSON or HASH documents, FLAT or HNSW vector indexes, metadata filters, RedisVL, Redis Insight, Prometheus/Grafana monitoring, TLS/RBAC security, persistence, backups, Redis Flex/Auto-Tiering sizing, and common failures such as empty results, dimension mismatch, metric mismatch, high latency, OOM, or REST/API errors."
---

# Redis Software Vector Database

Use this skill for Redis Software vector search implementation and operations. For platform-neutral architecture review, use `redis-vector-search-architecture`; for Redis Cloud, use `redis-cloud-vector-database`.

## Core Rules

- Confirm the target database supports Redis Search / Query Engine vector indexing before proposing vector commands.
- Prefer RedisVL for Python application code when the task involves schema-driven vector indexes, hybrid filters, or retrieval workflows.
- Match embedding model, dimension, datatype, distance metric, and index schema exactly.
- Do not recreate indexes, delete keys, or change persistence/tiering settings in production without explicit confirmation and a rollback plan.
- Verify current Redis Software, Redis Open Source, Redis Stack, and Redis Cloud capability differences before making broad product availability claims.

## Intake

Ask or infer:

- Redis Software version and database Redis version.
- Deployment mode: single database, clustered database, Active-Active, or Redis Flex/Auto-Tiering.
- Data model: HASH or JSON.
- Embedding model, vector dimension, datatype, and distance metric.
- Expected corpus size, update rate, query QPS, latency SLO, recall target, and memory budget.
- Whether the app needs pure vector KNN, hybrid vector plus metadata filters, full-text search, or RAG retrieval.
- Security needs: TLS, scoped users, ACL categories or explicit command permissions, and network isolation.

## Enablement Checklist

1. Confirm Search and Query capability is available and enabled for the database.
2. Confirm JSON capability if the data model uses JSON documents.
3. Verify the client path supports the needed commands and protocol.
4. Confirm persistence and backup settings are appropriate for index rebuild cost and recovery objectives.
5. For production, confirm at least the required HA, replication, and monitoring posture for the workload.
6. If the dataset is too large for RAM, evaluate Redis Flex/Auto-Tiering sizing and latency impact before recommending it.

## Schema Guidance

Choose document shape first:

| Model | Use When | Notes |
| --- | --- | --- |
| HASH | Flat metadata and compact storage are enough | Straightforward indexing and lower overhead. |
| JSON | Nested documents, document APIs, or app-native JSON are needed | Use JSONPath schema fields and validate path consistency. |

Choose index algorithm:

| Algorithm | Use When | Tradeoff |
| --- | --- | --- |
| FLAT | Small datasets or exact recall requirements | Predictable recall, higher scan cost as corpus grows. |
| HNSW | Larger datasets or low-latency approximate search | Tune recall versus latency and memory. |

Use a single embedding dimension and metric per vector field. Re-embedding with a different model usually requires a new field or rebuilt index.

## Minimal Command-Level Pattern

JSON index shape:

```text
FT.CREATE idx:items ON JSON PREFIX 1 item: SCHEMA \
  $.description AS description TEXT \
  $.embedding AS embedding VECTOR HNSW 6 TYPE FLOAT32 DIM <dims> DISTANCE_METRIC COSINE
```

KNN query shape:

```text
FT.SEARCH idx:items "(*=>[KNN 3 @embedding $query_vector])" \
  PARAMS 2 query_vector <binary_vector> DIALECT 2
```

Hybrid filtering shape:

```text
FT.SEARCH idx:items "(@category:{docs}=>[KNN 10 @embedding $query_vector])" \
  PARAMS 2 query_vector <binary_vector> DIALECT 2
```

For application code, translate these patterns into RedisVL schema and query objects when possible instead of hand-building command strings.

## Operational Guidance

- Monitor vector query latency, ingestion throughput, memory usage, index size, shard balance, and result quality.
- Use Redis Insight for exploratory validation and Prometheus/Grafana for production metrics.
- Keep metadata fields indexed when they appear in filters or sorting.
- Avoid broad filters that fan out across many shards when a selective TAG or NUMERIC filter is available.
- Use TLS, scoped Redis users, and least-privilege command permissions for production access.
- Backups protect source data; index rebuild time still needs to be included in recovery planning.

## Troubleshooting

| Symptom | Check | Action |
| --- | --- | --- |
| `FT.CREATE` or `FT.SEARCH` unknown | Search capability unavailable or wrong endpoint | Verify database capability, module/status output, endpoint, and command path. |
| No results | Prefix mismatch, index not built, filters too strict, or vector bytes wrong | Check `FT.INFO`, prefix, document keys, vector encoding, and filters. |
| Dimension error or empty matches | Embedding dimension differs from schema | Recreate data/index with a consistent dimension after confirming impact. |
| Unexpected ranking | Distance metric or embedding model mismatch | Align metric with model guidance and re-embed/reindex if needed. |
| High latency | HNSW parameters, broad filters, high shard fan-out, or insufficient capacity | Profile query, reduce filter breadth, tune HNSW, or scale capacity. |
| OOM or memory pressure | Corpus, vector dimension, metadata, or index overhead too large | Estimate memory, reduce dimensions, shard/scale, or evaluate Redis Flex. |
| REST/API errors | Auth, TLS, port, endpoint, or role issue | Verify credentials, certificate trust, API port, and scoped permissions. |
| Upgrade changes behavior | Query Engine, ACL, or command syntax changed | Use Redis 8 Search and ACL migration skills and verify current release notes. |

## Response Shape

When helping a user:

1. State whether their Redis Software database appears eligible for vector search.
2. Recommend HASH or JSON and FLAT or HNSW based on scale and recall needs.
3. Specify required embedding details: model, dimension, datatype, metric.
4. Provide a minimal RedisVL or command-level schema/query example tailored to their shape.
5. Add production checks for security, persistence, monitoring, and memory.
6. If troubleshooting, walk the checks in order: capability, index, prefix, data shape, vector bytes, filters, then capacity.
