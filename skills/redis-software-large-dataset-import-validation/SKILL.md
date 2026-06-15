---
name: redis-software-large-dataset-import-validation
description: "Validate and troubleshoot large dataset imports into Redis Software using RDB restore, Replica Of, RIOT, or logical migration, including clustered shard counts, `rladmin status shards`, Active-Active CRDB sync with `crdb-cli crdb-list`, `FT.INFO` Search indexing checks, `hash_indexing_failures`, module/version parity with `MODULE LIST`, memory headroom with `INFO MEMORY`, maxmemory policy review, shard distribution, and safe decisions around reindexing or replication changes."
---

# Redis Software Large Dataset Import Validation

Use this skill after or during large Redis Software imports. The goal is to prove that the imported data is complete, indexed, evenly placed where expected, compatible with the target modules, and safe for application cutover.

## Safety Rules

- Imports, restores, replication setup, and logical loaders can overwrite or diverge target data. Confirm backups and rollback before rerunning.
- Do not disable replication, drop Search indexes, recreate indexes, or manually resync shards without an approved plan and explicit confirmation.
- `FT.DROPINDEX <index> DD` deletes indexed documents; do not use `DD` unless intentional data deletion is confirmed.
- For Active-Active CRDB, do not treat local validation as global success until every participant is active and synchronized.
- If module/version compatibility is uncertain, stop before retrying a destructive import path.

## Import Method Intake

Identify:

- import method: RDB restore, Replica Of, RIOT, app loader, or other logical migration
- source and target Redis Software versions
- database type: standalone, clustered, replicated, or Active-Active CRDB
- expected key count, document count, and dataset size
- shard count and placement policy
- persistence and backup posture
- modules/capabilities: Search, JSON, TimeSeries, probabilistic data structures, functions, or custom modules
- whether Search indexes existed before import or should be created afterward

## Cluster Validation

1. Confirm cluster health:

   ```bash
   rladmin status extra all
   rladmin status shards
   rladmin cluster running_actions
   ```

2. Verify dataset completion:

   ```text
   DBSIZE
   ```

   For clustered databases, confirm whether the command path returns aggregate count or one shard's count. When in doubt, aggregate counts per shard or use a supported tool such as Redis Insight.

3. Compare against source totals and expected filtered subset.
4. Sample representative namespaces:
   - data type
   - value shape
   - TTL
   - encoding-sensitive fields
   - large or hot keys
5. Confirm shard distribution is expected, especially after clustered imports or resharding.

## Search Index Validation

For each expected Search index:

```text
FT.INFO <index>
```

Confirm:

- `indexing` is complete, commonly `0`
- `num_docs` matches expected indexed documents
- `hash_indexing_failures` or equivalent counters are `0`
- schema matches imported HASH or JSON fields
- prefixes cover the imported keys
- vector, numeric, tag, and JSON-path fields match the source data shape

If indexing never completes, investigate resource pressure, schema/type mismatches, and module parity before considering an index rebuild.

## Module And Version Parity

Check module availability and versions on the target:

```text
MODULE LIST
```

For clustered deployments, confirm module/version parity across nodes or shards using the supported Redis Software visibility path.

Common blockers:

- target missing a module used by the source
- Search/JSON module version mismatch
- RDB created by a newer or incompatible Redis/module version
- custom module data not supported on the target
- Redis 8 capability changes affecting Search/JSON behavior

If RDB compatibility is questionable, re-export using a compatible version or choose a logical migration path.

## Active-Active / CRDB Validation

For CRDB imports or migrations:

```bash
crdb-cli crdb-list
```

Confirm:

- every participating cluster is active
- sync status is healthy
- lag is expected and trending down
- no participant reports stale or divergent state
- application writes are paused or coordinated during validation if the migration requires it

Do not declare success from one region only.

## Memory And Resource Headroom

Check:

```text
INFO MEMORY
```

Also inspect Redis Software metrics for:

- memory percentage and fragmentation
- CPU during indexing or import
- disk I/O and persistence pressure
- shard balance
- replication lag
- network throughput

Treat sustained memory near the limit as a risk. The common 80 percent threshold is a planning heuristic; use the workload's policy, fragmentation, replication, and persistence overhead when deciding whether to resize.

Review:

```text
CONFIG GET maxmemory-policy
```

Confirm the policy matches the workload. `noeviction` protects data from eviction but can produce write errors at the limit; eviction policies may remove data during pressure.

## Common Failure Modes

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| `num_docs` differs from expected corpus | Indexing incomplete or failed | Check `FT.INFO`, wait for indexing, and inspect failures. |
| `hash_indexing_failures` nonzero | Schema/type mismatch | Fix data or schema and plan reindexing safely. |
| Keys missing on one shard | Import, placement, or resharding inconsistency | Check `rladmin status shards`, per-shard counts, and import logs. |
| Import stops or restarts | Node memory, disk, or module failure | Inspect `INFO MEMORY`, disk metrics, logs, and module errors. |
| Module mismatch errors | Target module/version mismatch | Standardize target capability or use logical migration. |
| CRDB lag remains high | Sync not complete or participant issue | Check CRDB health, syncer logs, and participant connectivity. |
| High CPU or latency during import | Writes and Search indexing compete for resources | Reduce write load, delay index creation when possible, or extend maintenance window. |
| Import fails after upgrade | RDB/module compatibility changed | Verify source/target versions and re-export with a compatible path. |

## Reindex And Replication Decisions

Before reindexing:

1. Confirm indexes are not merely still building.
2. Preserve or back up data if index commands can affect documents.
3. Prefer dropping only the index metadata unless deleting source documents is intentional.
4. Recreate indexes during a controlled window.
5. Validate `FT.INFO` and sample queries after rebuild.

Before disabling or changing replication:

1. Confirm why replication overhead is the bottleneck.
2. Confirm data durability and HA impact.
3. Get change approval.
4. Re-enable replication and verify sync after import.

## Escalation Packet

Collect:

- source and target Redis Software versions
- import method and dataset size
- database ID, shard count, and CRDB GUID if applicable
- expected and observed key/document counts
- `rladmin status extra all`, `rladmin status shards`, and running-actions output
- `FT.INFO` for affected indexes
- `MODULE LIST` output or module inventory
- `INFO MEMORY` and memory-policy output
- CRDB health/sync status for every participant
- import logs, timestamps, and errors

## Response Shape

When helping a user:

1. Identify import path and deployment shape.
2. Validate cluster health, counts, Search indexes, module parity, memory, and CRDB sync.
3. Classify failures as capacity, shard placement, Search indexing, module compatibility, CRDB sync, or import method.
4. Recommend wait, resize, re-export, logical migration, controlled reindex, or Support escalation based on evidence.
