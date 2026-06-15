---
name: redis-cloud-vector-database
description: Use when designing, implementing, tuning, or troubleshooting Redis Cloud vector search, semantic search, RAG, LangCache, hybrid metadata filtering, FLAT/HNSW index choices, vector dimensions, distance metrics, or Search and Query availability in Redis Cloud.
---

# Redis Cloud Vector Database

Use this skill to guide Redis Cloud vector database work from requirements through schema design, query construction, tuning, and troubleshooting.

## First Checks

1. Confirm the workload needs vector search, semantic similarity, RAG retrieval, recommendation, classification, LangCache, or hybrid vector plus metadata filtering.
2. Confirm the Redis Cloud database tier and configuration support Search and Query. Verify current Redis Cloud documentation or console state before making availability claims for a specific plan, region, endpoint type, or product feature.
3. Confirm the data model:
   - Use JSON when documents are nested or metadata is naturally structured.
   - Use HASH when the object model is flat and simple.
4. Confirm embedding details before indexing:
   - embedding model name and vector dimension
   - vector datatype, usually `FLOAT32`
   - distance metric: cosine, L2, or inner product
   - expected corpus size and update rate

## Implementation Workflow

1. Prefer RedisVL for application code when the task involves vector search, schema-driven index creation, hybrid filters, or AI retrieval workflows.
2. Create an index that includes every field used for filtering, full-text search, sorting, or returned search results.
3. Choose the vector algorithm:
   - `FLAT` for smaller datasets, exact KNN, or correctness-first validation.
   - `HNSW` for larger datasets where approximate nearest neighbor search is acceptable and latency matters.
4. Match query vector bytes to the indexed datatype and dimension. Dimension mismatches are a common cause of empty, partial, or failing results.
5. Keep search result payloads small. Use explicit return fields and limits instead of returning entire documents by default.
6. For production RAG, enable TLS, use scoped Redis users, restrict network access, and ensure persistence, backup, and high availability settings are appropriate for the rebuild cost of the index.

## Query And Tuning Guidance

- Use KNN or ANN for nearest-neighbor retrieval.
- Add metadata filters for tenant, document type, language, freshness, ACLs, or other retrieval constraints.
- Use full-text predicates when lexical matching should narrow the candidate set.
- For HNSW, tune index-time and query-time parameters to balance recall and latency. Increase query-time exploration when recall is too low, then measure the latency impact.
- Monitor query latency, memory usage, index size, ingestion throughput, and result quality. Treat recall and latency as a paired tuning exercise.
- Use `UNLINK` instead of `DEL` when removing large keys to avoid blocking latency spikes.

## Troubleshooting

When vector search does not behave as expected, check these before changing application logic:

1. Search and Query support is enabled for the database and endpoint being used.
2. The index exists, targets the correct prefix, and uses the expected HASH or JSON paths.
3. Stored vectors use the same dimension, datatype, and metric expected by the index.
4. Query vectors are encoded as binary bytes when the client and command require bytes.
5. Filters are not excluding otherwise valid vector matches.
6. HNSW recall is sufficient; raise query exploration settings if results are unexpectedly sparse.
7. Client credentials and Redis user permissions allow the needed Search, JSON, and key commands.
8. Cluster or endpoint mode supports the specific Search and Query command path being used. Verify current Redis Cloud restrictions before advising a topology change.

## Response Pattern

When helping a user, produce:

1. A short eligibility check for Redis Cloud vector support.
2. A recommended data model and index algorithm.
3. A minimal schema or RedisVL index example tailored to their document shape.
4. The query pattern, including filters and return fields.
5. The first metrics and failure modes to inspect if the query is slow or incomplete.
