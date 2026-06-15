---
name: redis-crdb-shard-scaling
description: "Scale shards in a Redis Software Active-Active CRDB with minimal service impact. Use when the user asks to increase CRDB shard count, scale Active-Active throughput, use `crdb-cli crdb update` with `shards_count`, avoid local-only participant changes, monitor CRDB tasks, handle resharding latency, capacity or provisional RAM errors, hot or large keys before resizing, emergency local-cluster-first scaling, or reduce shard count safely."
---

# Redis CRDB Shard Scaling

Use this skill when changing shard count for a Redis Software Active-Active database. Treat shard scaling as a CRDB-level topology change.

## Safety Rules

- Prefer CRDB-level updates with `crdb-cli`; local UI-only changes can leave participants misaligned.
- Do not resize while shards, replicas, CRDB links, or participating clusters are unhealthy.
- Do not start imports, exports, backups, bulk deletes, or other topology changes during resharding.
- Do not attempt unsupported online shard reduction. Plan downtime with Redis Support or migrate to a new database.
- Confirm recent backups and rollback/contingency plan before topology changes.

## When to Scale Shards

| Goal | Action |
| --- | --- |
| More throughput/parallelism | Increase `shards_count`. |
| More memory capacity | Increase `memory_size`; shard count alone does not increase total memory. |
| More throughput and memory | Update both `shards_count` and `memory_size`. |
| Reduce shard count after peak | Do not attempt online shrink; plan supported downtime or migration. |

## Preflight Checklist

1. Confirm admin access to every participating Redis Software cluster.
2. Confirm access to `crdb-cli`.
3. Confirm CRDB health and no stale/down/recovering shards.
4. Check running actions:

   ```bash
   rladmin cluster running_actions
   crdb-cli task list
   ```

5. Confirm CPU, RAM, provisional RAM, and network headroom in every participating cluster:

   ```bash
   rladmin status extra all
   ```

6. Check for large or hot keys before the resize:

   ```bash
   redis-cli --bigkeys
   redis-cli --hotkeys
   ```

7. Schedule the resize during lower traffic.
8. Confirm backups are recent and restorable.

## CRDB-Level Scaling Workflow

List CRDBs and record the GUID:

```bash
crdb-cli crdb list
```

Review current configuration:

```bash
crdb-cli crdb get --crdb-guid <crdb-guid>
```

Increase shard count:

```bash
crdb-cli crdb update --crdb-guid <crdb-guid> \
  --default-db-config '{"shards_count":20}'
```

Increase shard count and memory together:

```bash
crdb-cli crdb update --crdb-guid <crdb-guid> \
  --default-db-config '{"memory_size":8589934592,"shards_count":20}'
```

Memory-only change, when appropriate:

```bash
crdb-cli crdb update --crdb-guid <crdb-guid> --memory-size 8GB
```

## Monitor Until Complete

```bash
crdb-cli task list
crdb-cli task status --task-id <task-id>
```

Do not begin other maintenance until the CRDB task completes across participants.

## Post-Change Validation

```bash
rladmin status extra all
crdb-cli crdb health-report --crdb-guid <crdb-guid>
```

Confirm:

- Every participant reports healthy shards.
- CRDB links are connected.
- Sync lag returns to normal.
- Latency stabilizes.
- Clients continue using the same endpoint.
- Shard count is consistent across participating clusters.

## Emergency-Only Local Path

Use only when traffic is already spiking and waiting for planned CRDB-level scaling is riskier:

1. Increase shards in the local production cluster through supported UI/API.
2. Wait for local resharding to finish.
3. Repeat on each participating cluster.
4. After stabilization, run the CRDB-level `crdb-cli crdb update` so global metadata matches.

Do not add CRDB instances or make topology changes before global alignment is complete.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| One participant changed, another did not | Local-only change | Run CRDB-level update and monitor task. |
| Resharding slow | Large/hot keys, high load, or concurrent jobs | Stop heavy jobs and monitor; schedule earlier/lower traffic next time. |
| Not enough memory | Insufficient provisional RAM or node headroom | Add capacity, rebalance, or include memory increase. |
| CRDB busy | Another task is running | Wait or escalate if task is stalled. |
| Sync does not recover | Connectivity, TLS, version, module, or backlog issue | Validate links, versions, and logs. |
| Delete latency increased | Bulk deletes during resharding | Stop bulk deletes; use incremental cleanup later. |

## Escalation Packet

Collect:

- CRDB name and GUID.
- Participating clusters and Redis Software versions.
- Current and target `shards_count` and `memory_size`.
- `crdb-cli crdb get` output.
- `rladmin status extra all` from each cluster.
- Running actions and CRDB task output.
- Large/hot key findings.
- Metrics during resize: CPU, memory, network, latency, sync lag.
- Errors from `crdb-cli`, UI, or logs.
