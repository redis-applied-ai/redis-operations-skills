---
name: redis-cloud-faceted-search
description: "Design and troubleshoot faceted search in Redis Cloud with Redis Search and Query. Use when the user asks how to build product/category/brand/color filters, define TAG fields for facets, run `FT.AGGREGATE GROUPBY` counts, combine `FT.SEARCH` full-text and facet filters, use JSON documents, fix missing facet counts, schema mismatches, multi-value facets, or slow aggregation queries."
---

# Redis Cloud Faceted Search

Use this skill when building or debugging faceted search in a Redis Cloud database.

## Core Model

Facets should be indexed as `TAG` fields. Use `FT.SEARCH` to filter results and `FT.AGGREGATE` to compute facet counts with `GROUPBY` and `COUNT`.

Do not model facet filters as `TEXT` fields unless full-text matching is intentionally required; `TEXT` tokenization is not a substitute for exact facet filtering.

## Schema Pattern

JSON example:

```text
FT.CREATE product_idx ON JSON PREFIX 1 product: SCHEMA
  $.Name AS name TEXT
  $.Brand AS brand TAG SORTABLE
  $.Color AS color TAG SORTABLE
```

Facet fields such as brand, color, category, region, status, or tenant are usually `TAG`. Searchable descriptions or titles are usually `TEXT`.

## Query Patterns

Facet count:

```text
FT.AGGREGATE product_idx * GROUPBY 1 @color REDUCE COUNT 0 AS num SORTBY 2 @num DESC LIMIT 0 20
```

Facet filter:

```text
FT.SEARCH product_idx '@color:{brown}' RETURN 2 name brand
```

Text plus facet:

```text
FT.SEARCH product_idx 'leather @brand:{Santoni}' RETURN 3 name brand color
```

Use `LIMIT` on result and aggregation queries to control response size.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Facet filter returns no results | Field was indexed as `TEXT`, not `TAG`, or query syntax is wrong | Check schema with `FT.INFO`; recreate index with TAG if needed. |
| Counts missing or stale | Index still building or indexing failures | Check `FT.INFO <index>` for `indexing` and `hash_indexing_failures`. |
| Aggregation returns duplicate-like facet values | Multi-value field is not normalized/split as intended | Normalize values at write time or use aggregation transforms such as `APPLY` when appropriate. |
| `FT.AGGREGATE` unavailable | Search and Query capability unavailable or wrong database mode | Verify database capabilities and OSS Cluster API compatibility. |
| Slow aggregation | Too many candidates or broad grouping | Add selective filters, `LIMIT`, `SORTBY`, and review index schema. |

## Design Checks

1. Confirm data type: JSON or HASH.
2. Confirm prefix matches document keys.
3. Confirm facet fields are stable exact values.
4. Normalize case and separators before indexing.
5. Avoid high-cardinality fields as UI facets unless the product explicitly needs them.
6. Keep returned fields minimal.
7. Pair explain/profile tooling with slow queries.

## Validation Commands

```text
FT.INFO product_idx
FT.SEARCH product_idx '@brand:{Santoni}' LIMIT 0 5
FT.AGGREGATE product_idx * GROUPBY 1 @brand REDUCE COUNT 0 AS count LIMIT 0 10
```

## Escalation Packet

Collect:

- Redis Cloud plan/database capability details.
- Index schema from `FT.INFO`.
- Example document.
- Failing `FT.SEARCH` or `FT.AGGREGATE` query.
- Expected and actual facet counts.
- Indexing failure counters and query latency.
