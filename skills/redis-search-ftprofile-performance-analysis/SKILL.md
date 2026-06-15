---
name: redis-search-ftprofile-performance-analysis
description: "Use Redis Search `FT.PROFILE` to diagnose `FT.SEARCH` and `FT.AGGREGATE` latency, timeouts, shard imbalance, iterator counters, full scans, vector and hybrid query cost, coordinator overhead, sorter/loader cost, incomplete indexing, and aggregation or faceted-query performance. Use when the user provides profile output or asks how to profile slow Redis Query Engine queries."
---

# Redis Search FT.PROFILE Performance Analysis

Use this skill when runtime behavior matters: slow Search queries, vector/hybrid query latency, faceted aggregation cost, inconsistent counts, timeout warnings, or shard-level imbalance. Use `redis-search-ftexplain-optimization` first when the query's logical plan is unclear; use `FT.PROFILE` to measure what actually happened.

## Safety Rules

- Profile in staging or a realistic pre-production environment before changing production schemas.
- In production, profile narrowly: use representative queries, controlled limits, and avoid broad `LOAD *` or unbounded aggregations.
- Do not recommend index rebuilds, shard rebalancing, timeout increases, or schema changes until profile evidence and `FT.INFO` state are checked.
- Increasing query timeout can mask a bad plan; treat it as a temporary mitigation unless the query shape is already efficient.

## Intake

Collect:

- Redis product and version: Redis Software, Redis Cloud, or Redis Open Source/Stack.
- Index name and schema, including TAG, NUMERIC, TEXT, VECTOR, SORTABLE, and JSON/HASH model.
- Query command, dialect, params shape, and expected result count.
- `FT.EXPLAINCLI` output if query parsing is uncertain.
- `FT.PROFILE` output for the slow query.
- `FT.INFO <index>` output for indexing state and failure counters.
- Shard count, cluster topology, and whether latency is isolated to one shard.

## Running FT.PROFILE

Command shape:

```text
FT.PROFILE <index> <SEARCH|AGGREGATE> [LIMITED] QUERY <query>
```

Examples:

```text
FT.PROFILE idx:users SEARCH QUERY "@city:{London}" LIMIT 0 10
```

```text
FT.PROFILE idx:docs AGGREGATE QUERY "@tenant:{acme} *" GROUPBY 1 @category REDUCE COUNT 0 AS count
```

Use full profiling when diagnosing iterator and processor cost. Use `LIMITED` when output volume or profiling overhead is a concern and detailed iterator internals are not required.

## How To Read Output

Focus on these sections:

| Section | Meaning | Concern |
| --- | --- | --- |
| Total profile time | End-to-end time for the profiled query | High total time means query shape, data volume, or shard/coordinator cost needs attention. |
| Parsing and pipeline creation | Pre-execution overhead | High values can point to complex query construction or aggregation setup. |
| Per-shard profile | Work done on each shard | One slow shard suggests shard imbalance, hot keys, local resource pressure, or uneven index distribution. |
| Iterators profile | TEXT, TAG, NUMERIC, VECTOR, UNION, INTERSECT work | High counter or size usually means low selectivity or scan-heavy query shape. |
| Result processors | Loading, sorting, projecting, grouping | High sorter/loader cost means too many rows, broad projections, or missing SORTABLE fields. |
| Coordinator | Multi-shard aggregation and merge cost | High coordinator cost suggests large fan-in, global sort/aggregate, or shard imbalance. |
| Warnings | Timeout or partial execution | Treat as evidence the result may be partial or unstable. |

## Diagnosis Map

| Symptom | Likely Cause | Next Action |
| --- | --- | --- |
| High total time | Large candidate set, broad filters, vector scan, or slow shard | Check iterator size/counter and per-shard split. |
| High iterator counter | Nonselective filters or full index scan | Add selective TAG/NUMERIC filters, reorder query shape, or adjust schema. |
| High VECTOR iterator cost | KNN work too broad or vector settings too expensive | Add selective prefilters, tune HNSW/query params, or reduce candidate count. |
| High sorter time | Sorting many rows or sorting on non-SORTABLE field | Add `SORTABLE` where justified or reduce result set before sorting. |
| High loader time | Loading too many fields or large JSON payloads | Return only needed fields and avoid broad projections. |
| High coordinator time | Multi-shard merge/aggregate overhead | Reduce fan-in, add selective filters, inspect shard balance. |
| Timeout warning | Query exceeded configured time budget | Optimize first; only then consider timeout changes. |
| Inconsistent counts or facets | Indexing in progress, failure counters, timeout, or shard issue | Check `FT.INFO`, profile warnings, and shard state. |
| Aggregation slows over time | Dataset growth, missing filters, or grouping high-cardinality fields | Add selective predicates, paginate/cursor, or redesign aggregation. |

## Optimization Workflow

1. Confirm the index is healthy:

   ```text
   FT.INFO <index>
   ```

   Check indexing completion, document count, and failure counters.

2. Explain the query if parsing or filter order is unclear:

   ```text
   FT.EXPLAINCLI <index> "<query>" DIALECT <n>
   ```

3. Profile the exact slow query with realistic parameters.
4. Identify the first expensive stage: iterator, vector search, loader, sorter, aggregation, or coordinator.
5. Apply the narrowest change:
   - add or tighten TAG/NUMERIC filters
   - reduce returned fields
   - use `LIMIT` or cursor pagination
   - add `SORTABLE` only for fields that are actually sorted
   - tune vector/HNSW parameters with recall and latency measured together
   - rebalance only when shard evidence supports it
6. Re-run `FT.PROFILE` before and after the change and compare total time plus the target stage.

## Aggregate And Faceted Queries

For `FT.AGGREGATE`:

- Use selective predicates before `GROUPBY` when possible.
- Avoid unbounded grouping over high-cardinality fields.
- Add `LIMIT` or cursor-based pagination when returning many rows.
- Treat fewer rows than expected as possible timeout or partial execution until `FT.PROFILE` and `FT.INFO` prove otherwise.
- For faceted counts, confirm indexing is complete before debugging query semantics.

## Escalation Packet

Collect:

- Full query command with params redacted where needed.
- `FT.PROFILE` output.
- `FT.EXPLAINCLI` output if relevant.
- `FT.INFO <index>` output.
- Database topology: shard count, product, version, and endpoint mode.
- Latency target, observed latency, and whether issue is intermittent.
- Recent changes: schema, data growth, index rebuild, upgrade, shard rebalance, or traffic change.
