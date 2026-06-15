---
name: redis-crdb-delete-latency
description: "Diagnose and reduce latency from DEL and UNLINK in Redis Software Active-Active CRDB. Use when delete operations cause latency spikes, blocked shards, timeouts, replication lag, CRDB convergence delays, or no improvement after switching from DEL to UNLINK, and when the user needs SLOWLOG, big key analysis, key redesign, TTL cleanup, batched deletion, or cross-region delete workload shaping."
---

# Redis CRDB Delete Latency

Use this skill when `DEL` or `UNLINK` causes latency, blocked shards, or replication delays in Active-Active CRDB.

## Core Rule

In Active-Active CRDB, `UNLINK` does not provide the same latency relief users may expect from non-CRDB Redis. Deletes must be replicated and coordinated across regions, so large key deletion can still block and create latency.

## Detection Workflow

1. Correlate application timeouts or latency spikes with delete jobs, expiration waves, or cleanup tasks.
2. Check slowlog:

   ```bash
   crdb-cli -d <db-name> slowlog get
   ```

3. Compare timestamps with CPU, memory, replication lag, and regional convergence metrics.
4. Inspect Redis Enterprise logs for blocked operations or sync issues:
   - `cluster_wd.log`
   - `shard-*.log`
5. Identify whether the workload uses `DEL`, `UNLINK`, bulk deletes, or application cleanup loops.

## Key Size Analysis

Find large keys and large collections:

```bash
redis-cli -c -h <shard-host> --bigkeys
```

Prioritize keys with:

- Lists, sets, or sorted sets with very high element counts.
- Hashes with many fields or large values.
- Any key around 10 MB or larger.
- Collections above roughly 100,000 elements.

## Mitigation Patterns

| Problem | Better pattern |
| --- | --- |
| Massive single key deletion | Split data into smaller keys by tenant, time bucket, or logical partition. |
| Cleanup job deletes many large keys at once | Batch and throttle deletes during low-traffic windows. |
| Key grows without bound | Add TTLs or size limits before data becomes huge. |
| Periodic bulk purge | Use rolling expiration or incremental cleanup. |
| Switching `DEL` to `UNLINK` did not help | Redesign key shape and delete cadence; do not rely on command substitution. |

## Operational Guidance

- Schedule cleanup outside peak traffic.
- Limit batch size and add sleeps between batches.
- Prefer gradual TTL-based lifecycle management where data model allows it.
- Monitor every participating region during deletion.
- Watch replication lag and convergence time, not only local command latency.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| High latency during deletes | Large key size, element count, synchronous CRDB propagation. |
| Replication lag after cleanup | Delete volume and replication queue pressure. |
| Shards appear unavailable | Blocking delete work or CPU saturation. |
| `UNLINK` still slow | Expected CRDB behavior; redesign cleanup. |
| Latency only in one region | Regional shard load, network path, and local large-key distribution. |

## Escalation Packet

Collect:

- CRDB topology and Redis Software version.
- Delete command type and cleanup job schedule.
- Slowlog entries for delete operations.
- Big key analysis output.
- Key type, size, and element-count examples.
- CPU, memory, and replication lag during the incident.
- Relevant `cluster_wd.log` and `shard-*.log` snippets.
- Regions affected and convergence delay observed.
