---
name: redis-crdb-flush
description: "Safely flush a Redis Software Active-Active CRDB database. Use when the user asks to empty or reset a CRDB, learns FLUSHDB or FLUSHALL are not supported, needs `crdb-cli crdb flush`, REST API `/v1/crdbs/{guid}/flush`, Cluster Manager UI flush, CRDB GUID lookup, pre-flush health checks, backup confirmation, propagation verification, or troubleshooting stalled or partial CRDB flushes."
---

# Redis CRDB Flush

Use this skill when a user needs to remove all data from a Redis Software Active-Active CRDB.

## Safety Rules

- Flushing is irreversible. Require explicit user confirmation of the exact CRDB before giving final flush commands.
- Confirm backup/snapshot status if recovery may be needed.
- Do not use `FLUSHDB` or `FLUSHALL` against a CRDB; they are not the supported CRDB flush path.
- Confirm all participating clusters and shards are healthy before flushing.
- Verify current Redis Software/module support before using async flush options.

## Preflight Checklist

Confirm:

- CRDB GUID.
- CRDB name and participating clusters/regions.
- Administrative access.
- Cluster health is green in all participating clusters.
- No stale replicas or disconnected regions.
- Backup decision is complete.
- Flush window is acceptable for the workload.
- Users understand every region will be emptied.

## Preferred Method: crdb-cli

After confirmation:

```bash
crdb-cli crdb flush --crdb-guid <crdb-guid>
```

Use the environment/profile flags required by the installation. Review output for per-region success or failure.

## REST API Method

After confirmation:

```bash
curl -u <username>:<password> \
  -X PUT https://<hostname>:9443/v1/crdbs/<crdb-guid>/flush
```

If considering async flush, first verify it is supported by the Redis Software version, CRDB configuration, and enabled modules:

```json
{"async_flush": true}
```

Do not use async flush when module compatibility is uncertain.

## Cluster Manager UI Method

1. Open Cluster Manager.
2. Navigate to `Databases` then `Active-Active`.
3. Select the CRDB.
4. Choose `Flush database`.
5. Type the required database name or confirmation text.
6. Confirm only after backup and target checks are complete.

## Verification

Check keyspace from the CRDB endpoint:

```bash
redis-cli -h <endpoint> -p <port> DBSIZE
redis-cli -h <endpoint> -p <port> SCAN 0 COUNT 10
```

Check CRDB propagation:

```bash
crdb-cli crdb status --crdb-guid <crdb-guid>
```

Verify every participating region reports completion and the keyspace is empty.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `ERR command not allowed` | User attempted `FLUSHDB` or `FLUSHALL`; use CRDB CLI/API/UI path. |
| Flush stalls | Shard health, stale replicas, sync lag, memory pressure, and `cluster_wd.log`. |
| Some regions still contain data | Region disconnected, replica unhealthy, or propagation incomplete. |
| UI button disabled | User lacks role/ACL permission or database state blocks operation. |
| High latency during flush | Large keyspace or replication pressure; retry during low-traffic window after health review. |

## Escalation Packet

Collect:

- Redis Software version.
- CRDB name and GUID.
- Participating clusters/regions.
- Backup status.
- Pre-flush health and stale replica status.
- Flush method used and timestamp.
- `crdb-cli crdb status` output.
- `DBSIZE` or `SCAN` verification from each region if needed.
- Relevant `cluster_wd.log` and shard logs for stalled flushes.
