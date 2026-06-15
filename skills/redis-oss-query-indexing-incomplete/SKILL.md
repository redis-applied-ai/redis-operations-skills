---
name: redis-oss-query-indexing-incomplete
description: Use when Redis Open Source 8, Redis Stack 7.x, Redis Query Engine, or Redis Search documents are missing from indexes, indexing appears incomplete, `FT.INFO` shows indexing still active, `percent_indexed` below 1, `hash_indexing_failures` above 0, schema or prefix mismatches, HASH or JSON fields have wrong types, `FT.DROPINDEX DD` left unindexed keys behind, OSS Cluster API sharded search is unsupported, or high-churn workloads need Search GC and index rebuild guidance.
---

# Redis OSS Query Indexing Incomplete

Use this skill when Redis Open Source or Redis Stack search/query results miss HASH or JSON documents that should be indexed.

## Safety Rules

- Start with read-only `FT.INFO` and sample queries.
- Do not rebuild indexes until schema, prefix, and indexing-failure evidence is captured.
- Treat `FT.DROPINDEX <index> DD` as destructive because it deletes documents as well as the index.
- Require explicit confirmation before deleting keys or running cleanup pipelines.
- Avoid Search on unsupported sharded OSS Cluster API production designs; verify the deployment mode first.

## First Checks

```redis
FT.INFO <index>
FT.SEARCH <index> "*" LIMIT 0 10
```

Check in `FT.INFO`:

- `indexing` is `0`
- `percent_indexed` is `1`
- `hash_indexing_failures` is `0`
- `num_docs` matches expected indexed documents
- schema aliases and field types match stored HASH or JSON data

If background indexing is still active, wait or resolve CPU/memory/load bottlenecks before judging result completeness.

## Common Causes

| Cause | Evidence | Fix |
| --- | --- | --- |
| Background indexing still running | `indexing` nonzero or `percent_indexed` below 1 | Wait and monitor progress. |
| Schema type mismatch | `hash_indexing_failures` above 0 | Fix invalid documents and rebuild if needed. |
| Wrong prefix | Keys do not match `PREFIX` in `FT.CREATE` | Recreate index with correct prefix. |
| Wrong JSON path or alias | Fields absent from indexed schema | Correct schema paths and recreate index. |
| OSS Cluster API sharding | Indexes appear partial or node-local | Move to supported search architecture or single-shard test only. |
| `FT.DROPINDEX DD` left keys | Unindexed documents were not deleted | Use safe `SCAN`/`UNLINK` cleanup after confirmation. |
| High churn | Index bloat, slow queries, delayed consistency | Separate write-heavy data or tune Search GC with version-aware guidance. |

## Prefix And Schema Validation

Compare the index command to stored keys:

```redis
SCAN 0 MATCH <prefix>:* COUNT 1000
```

For JSON, inspect one sample document and verify the JSON paths in `FT.CREATE` actually exist. For NUMERIC fields, values must be numeric, not strings that look numeric.

## Cleanup After Partial Drop

If `FT.DROPINDEX <index> DD` did not remove all documents, it likely removed only successfully indexed documents. Confirm remaining keys before deletion:

```redis
SCAN 0 MATCH <prefix>:* COUNT 1000
```

Use bounded `UNLINK` batches only after confirming the prefix cannot match unintended keys.

## Rebuild Guidance

Rebuild only when:

- schema fields or types changed
- prefixes were wrong
- indexing failures persist after data correction
- index creation occurred while required capabilities were unavailable

Before rebuild:

1. Capture the current `FT.CREATE` equivalent and `FT.INFO`.
2. Decide whether documents must be retained.
3. Use `FT.DROPINDEX <index>` to drop only the index when retaining data.
4. Use `DD` only when deletion is explicitly intended and confirmed.
5. Recreate the index and monitor `indexing`, `percent_indexed`, and failures.

## High-Churn Environments

For frequent updates:

- monitor `FT.INFO`, query latency, and memory
- separate hot write-heavy data from read-heavy indexed data where possible
- use aliases or versioned indexes for schema changes
- tune Search garbage collection parameters only with current version guidance

## Escalation Packet

Collect:

- Redis version and whether this is Open Source 8 or Redis Stack 7.x
- deployment mode: standalone, cluster, or OSS Cluster API
- index name, `FT.CREATE` schema, and prefixes
- `FT.INFO <index>` output
- sample keys/documents expected to match
- exact `FT.SEARCH` query and result
- `hash_indexing_failures` and indexing progress
- recent index drops, rebuilds, data imports, or module/version changes
