---
name: redis-software-oom-replication
description: "Reduce Redis Software data-loss risk from out-of-memory events by enabling replication and auto-failover. Use when the user has replication factor 0, OOM during restart or AOF replay, single-shard production databases, memory above 80 percent, no replica promotion, module memory spikes, fragmentation, bulk ingestion pressure, or asks how to verify replica placement with rladmin."
---

# Redis Software OOM Replication

Use this skill when a Redis Software database is exposed to OOM-related data loss because replication is disabled or failover is not available.

## Core Rule

Production databases should not run with replication factor `0` unless the business explicitly accepts data-loss risk. Replication reduces the impact of OOM but does not fix the memory growth that caused it.

## High-Risk Patterns

- Replication factor is `0`.
- Single-shard production database holds critical data.
- AOF is enabled without a replica.
- Redis modules are enabled and can spike memory during indexing, replay, or restore.
- Database memory is consistently above 80 percent.
- Node memory allocation leaves less than 20 to 25 percent headroom.
- Bulk ingestion, migration, or large queries can create transient allocations.
- RSS is much higher than logical dataset size because of fragmentation.

## Immediate Triage

| Situation | Action |
| --- | --- |
| Replication factor is `0` | Verify capacity, then increase to at least one replica per shard. |
| OOM happened during restart | Stabilize memory headroom before retrying restart. |
| Replica exists but failover is disabled | Enable auto-failover if appropriate. |
| Memory is above 80 percent | Scale memory, reduce workload, or configure eviction for cache workloads. |
| AOF replay repeatedly OOMs | Stop and assess memory headroom, persistence integrity, and backup options. |

## Capacity Checks

Before enabling replication, verify the cluster can place replicas on different nodes:

```bash
rladmin status nodes
rladmin status databases
rladmin status shards
```

Confirm:

- Enough free memory and CPU exist on separate nodes.
- Replica shards can be placed away from their primaries.
- Nodes are online and not under maintenance.
- Cluster can tolerate rebalancing.

## Enable Replication

Through Cluster Manager UI:

1. Open `Databases`.
2. Select the database and choose `Edit`.
3. Set replication to at least `1`.
4. Confirm replica placement on separate nodes.
5. Enable auto-failover if the workload requires automatic promotion.
6. Save and monitor rebalancing.

Through `rladmin`:

```bash
rladmin status databases
rladmin tune db db:<db-id> replication 1
rladmin status shards
```

Afterward, verify every primary shard has a healthy replica on a different node.

## Post-Change Verification

```bash
rladmin status shards
rladmin status nodes
```

Check:

- All shards report healthy.
- Replica placement is separated from primaries.
- Node memory headroom remains at least 20 to 25 percent.
- Application traffic remains stable during rebalancing.
- Failover behavior is tested during a controlled maintenance window.

## OOM Recovery Guidance

If replication was disabled:

- Recovery may depend entirely on AOF or backups.
- Restart can fail repeatedly if replay requires more memory than available.
- Data can be unrecoverable if persistence is missing or corrupted.

If replication was enabled:

- Redis Software can promote a replica for availability.
- Create or rebalance a replacement replica after memory pressure is stabilized.
- Still investigate the root cause: growth, eviction, modules, fragmentation, or ingestion.

## Escalation Packet

Collect:

- Redis Software version and database ID.
- Replication factor and auto-failover setting.
- `rladmin status nodes`, `databases`, and `shards`.
- OOM timestamps and affected node/shard IDs.
- Persistence mode and AOF replay status.
- Memory metrics: logical used memory, RSS, fragmentation, and headroom.
- Module usage and recent ingestion/migration/query workload.
- Backup availability and last successful backup time.
