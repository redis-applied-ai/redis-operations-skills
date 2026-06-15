---
name: redis-software-faceted-search
description: "Design and troubleshoot faceted search in Redis Enterprise Software using Redis Search with HASH or JSON documents. Use when the user asks for TAG facet schemas, `FT.AGGREGATE GROUPBY` counts, `FT.SEARCH` facet filters, missing or inconsistent facet counts across shards, Search module validation with `MODULE LIST` or `rladmin status modules`, `FT.PROFILE`, shard imbalance, CRDB regional freshness, or large aggregate performance."
---

# Redis Software Faceted Search

Use this skill when building or debugging faceted search in Redis Enterprise Software clusters.

## Core Model

Use `TAG` fields for exact facets and `TEXT` fields for full-text content. Use `FT.AGGREGATE` with `GROUPBY` and `COUNT` for facet counts, and `FT.SEARCH` for drill-down filters.

## Schema And Query Pattern

Hash schema:

```text
FT.CREATE doc_idx PREFIX 1 doc: SCHEMA category TAG content TEXT title TEXT
```

Facet count:

```text
FT.AGGREGATE doc_idx * GROUPBY 1 @category REDUCE COUNT 0 AS num_per_ctg SORTBY 2 @num_per_ctg DESC LIMIT 0 20
```

Facet drill-down:

```text
FT.SEARCH doc_idx '@category:{kb}' RETURN 1 title LIMIT 0 10
```

Text plus facet:

```text
FT.SEARCH doc_idx 'performance @category:{kb}' RETURN 1 title LIMIT 0 10
```

## Redis Software Checks

1. Confirm Search capability/module is present:

   ```text
   MODULE LIST
   rladmin status modules extra all
   ```

2. Confirm index state:

   ```text
   FT.INFO doc_idx
   ```

3. Check `indexing`, `num_docs`, and indexing failure counters.
4. For performance, profile the query:

   ```text
   FT.PROFILE doc_idx AGGREGATE QUERY "*"
   ```

5. Check shard size and placement if aggregate performance varies:

   ```bash
   rladmin status shards
   ```

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Facet counts missing | Index incomplete or indexing failures | Check `FT.INFO`, wait for indexing to finish, fix failed documents. |
| Facet filter returns no results | Field indexed as `TEXT` or wrong TAG syntax | Recreate/update schema with TAG field and validate query escaping. |
| Unknown `FT.AGGREGATE` | Search capability/module unavailable | Check `MODULE LIST` and Redis Enterprise module status. |
| Fewer aggregate results than expected | Timeout or partial execution | Use `FT.PROFILE`; reduce candidate set or tune limits. |
| Slow aggregation | Large result set, no `LIMIT`, shard imbalance, or broad grouping | Add `LIMIT`/`SORTBY`, filter earlier, and check shard distribution. |
| Inconsistent CRDB results | Region-local replication freshness | Run per-region checks and account for Active-Active convergence. |

## Cluster Guidance

- Redis Search handles shard-level aggregation, but large global aggregates can be CPU-intensive.
- Constrain broad aggregations with filters and limits.
- Schedule heavy validation or analytics during lower traffic where possible.
- For multi-value fields, normalize at write time or use aggregation transforms such as `APPLY "split(@field)" AS field` when appropriate.

## Evidence To Collect

- Redis Enterprise Software version and database ID.
- Search module/capability status.
- Index schema from `FT.INFO`.
- Query and profile output.
- Shard layout from `rladmin status shards`.
- CRDB/region details if Active-Active is involved.
