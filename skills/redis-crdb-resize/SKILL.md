---
name: redis-crdb-resize
description: Use when resizing Redis Software CRDB or Active-Active databases, including increasing memory, increasing shard count, using crdb-cli, checking CRDB GUIDs, avoiding local-only UI changes, validating all participating clusters, resolving not enough memory errors, busy CRDB tasks, stale replicas, sync lag, large keys, or shard-reduction requests.
---

# Redis CRDB Resize

Use this skill when changing memory or shard count for a Redis Software Active-Active CRDB. CRDB changes affect all participating clusters, so avoid local-only changes and validate every site.

## Guardrails

- Prefer `crdb-cli` or the supported API for CRDB configuration changes.
- Do not treat Admin UI changes on one participating cluster as a complete global CRDB resize.
- Do not reduce CRDB shard count as a normal operation. Treat shard reduction as a downtime/support-assisted migration or recovery plan.
- Do not resize while stale replicas, unhealthy nodes, active sync problems, or another CRDB task are present.
- Confirm recent backups and a low-traffic window before changing memory or shards.

## Pre-Resize Checks

Run or collect:

```text
crdb-cli crdb list
crdb-cli crdb get --crdb-guid <CRDB-GUID>
rladmin status
rladmin status extra all
```

Check:

- all participating clusters are healthy
- no stale replicas
- no unhealthy nodes
- enough provisional RAM for new shard and replica placement
- inter-cluster network is stable
- no CRDB task is already running
- large or hot keys have been identified
- backup and restore path is verified

Avoid large blocking deletes before resize; prefer `UNLINK` or incremental cleanup when deletion is confirmed safe.

## Resize Commands

List CRDBs:

```text
crdb-cli crdb list
```

Show configuration:

```text
crdb-cli crdb get --crdb-guid <CRDB-GUID>
```

Increase memory:

```text
crdb-cli crdb update --crdb-guid <CRDB-GUID> --memory-size 8GB
```

Increase shard count:

```text
crdb-cli crdb update --crdb-guid <CRDB-GUID> --default-db-config '{"shards_count":4}'
```

Track progress:

```text
crdb-cli task list
crdb-cli task status --task-id <Task-ID>
```

Validate the exact JSON fields and units against the deployed Redis Software version before automation.

## Validation

After resize:

- task completes successfully on all participating clusters
- CRDB config shows expected memory and shard count
- databases are active and syncing
- no stale replicas or sync errors
- memory usage and shard placement have expected headroom
- application read/write paths work in every region
- latency, replication, and conflict metrics are stable

## Troubleshooting

- Not enough memory: add memory, free capacity safely, or redistribute shards before retrying.
- Changes not visible in UI: compare local UI with `crdb-cli` global state.
- CRDB busy: wait for existing task completion; inspect task list before retrying.
- Orphaned or stuck task: collect task status and a diagnostic bundle before manual intervention.
- OOM, sync lag, or stale replicas after resize: check large keys, network health, replica status, and memory headroom.

## Response Pattern

Answer with:

1. Whether the request is memory increase, shard increase, or shard reduction.
2. The health and headroom checks.
3. The `crdb-cli` command pattern.
4. Task monitoring and all-site validation.
5. Support escalation criteria for shard reduction, stuck tasks, or inconsistent CRDB state.
