---
name: redis-search-count-index-consistency
description: "Troubleshoot Redis Search `FT.SEARCH` count drift, partial results, `no such index`, inconsistent index state, and missing index on shards. Use when repeated count-only searches differ, `FT.INFO` works but `FT.SEARCH` fails, `FT.PROFILE` shows timeout, shard-level indexes differ, replicas show `ERRCLUSTER Uninitialized cluster state`, Search is used with OSS Cluster API, or deciding whether to rebuild with `FT.DROPINDEX`."
---

# Redis Search Count Index Consistency

Use this skill when Redis Search counts are inconsistent or an index appears to exist in some places but not others.

## Diagnostic Order

1. Capture the exact index and query.
2. Check index metadata:

   ```text
   FT.INFO <index>
   ```

3. Run a count-only query:

   ```text
   FT.SEARCH <index> "<query>" LIMIT 0 0
   ```

4. Profile the query:

   ```text
   FT.PROFILE <index> SEARCH QUERY "<query>" LIMIT 0 0
   ```

5. If using Redis Enterprise sharding, validate index existence on master shards only.
6. Rebuild only when the evidence shows index inconsistency or schema mismatch.

## Interpretation Matrix

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Count changes between runs | Query timeout or partial results | Check `FT.PROFILE` for timeout; reduce scope or increase timeout cautiously. |
| Count low after index creation | Background indexing incomplete | Wait for `indexing: 0` and `percent_indexed: 1`. |
| `FT.INFO` works but `FT.SEARCH` says `no such index` | Index missing on one or more master shards | Validate shard-level index list/info and rebuild if confirmed. |
| Replica returns cluster/init error | Replica is not valid for index validation | Ignore replica-only errors; check masters. |
| `Inconsistent index state` | Schema mismatch or index metadata divergence | Drop and recreate the index in a planned window. |
| Search on OSS Cluster API sharded database | Unsupported Search deployment mode | Move to supported proxy-based/search-compatible architecture. |

## Timeout Handling

If `FT.PROFILE` shows timeout:

```text
FT.SEARCH <index> "<query>" TIMEOUT 5000 LIMIT 0 0
```

Use timeout increases as diagnosis, not the only fix. Prefer:

- More selective filters.
- Avoiding large wildcard scans.
- Better schema and TAG/NUMERIC prefilters.
- Query limits and pagination.

## Shard-Level Validation

In Redis Enterprise Software, validate master shards, not replicas:

```text
shard-cli --master bdb:<db-id> FT._LIST
shard-cli <redis-id> FT.INFO <index>
```

If the index is missing on a master, collect evidence before rebuilding.

## Rebuild Safety

Rebuilding can be resource-intensive and may affect production. Before `FT.DROPINDEX`:

1. Capture index schema and `FT.INFO`.
2. Confirm whether documents should be retained.
3. Require explicit confirmation before any drop.

Command distinction:

```text
FT.DROPINDEX <index>
```

Drops the index and keeps documents.

```text
FT.DROPINDEX <index> DD
```

Drops the index and deletes documents. Treat `DD` as destructive and require explicit confirmation.

## Product Notes

- Redis Software: validate on master shards and check module/version history after upgrades or failovers.
- Redis Cloud: use `FT.INFO` and `FT.PROFILE`; escalate with outputs if inconsistency persists.
- Redis Enterprise for Kubernetes: include pod restart/reconciliation timeline and shard-level evidence.
- Redis Insight: useful for interactive commands, but verify with CLI for support evidence.

## Escalation Packet

Collect:

- Deployment/product type and database ID.
- Exact query and index name.
- `FT.INFO` output.
- `FT.PROFILE` output.
- RediSearch/Search capability version.
- Timeline of failover, crash, upgrade, maintenance, or pod restart.
- Shard-level validation results.
- Support package for production incidents.
