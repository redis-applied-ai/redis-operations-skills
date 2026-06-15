---
name: redis-software-flex-v2-operations
description: Use when choosing, sizing, migrating, operating, or troubleshooting Redis Flex v2 or Auto-Tiering on Redis Software, including Flash shard allocation, flash_shards_limit licensing, prepare_flash.sh, Kubernetes redisOnFlashSpec or flashShardsLimit, Speedb requirements, local NVMe Flash, RAM-to-Flash ratio, cold-read p99, Flash IOPS, shard balance, ratio-change rebalances, replica lag, evictions, backups, or Flex v1 to v2 upgrade behavior.
---

# Redis Software Flex v2 Operations

Use this skill for Redis Flex v2 on Redis Software in on-prem or cloud-VM deployments. Unlike Redis Cloud, the operator owns hardware layout, storage quality, and node-level monitoring, so validate infrastructure before recommending Flex.

## Fit Assessment

Flex is appropriate when:

- the dataset is large
- the hot set is much smaller than total data
- data locality is predictable
- hot reads need very low latency and warm reads can tolerate higher p99
- local dedicated Flash can satisfy cold-read IOPS and latency

Avoid Flex when:

- access is uniform across the full dataset
- the hot set is almost the whole dataset
- required features are not supported with Flex in the target Redis Software version
- local dedicated SSD/NVMe storage is not available
- the workload needs Active-Active if Flex remains unsupported for that target deployment

## Infrastructure Requirements

Before designing or changing a Flex database, verify:

- Redis Software version and Flex or Auto-Tiering support
- Speedb storage engine support and licensing
- locally attached, dedicated SSD or NVMe for Flash
- no shared NAS, SAN, or unsuitable network block storage for the Flash tier
- persistence and Flash on separate disks
- Flash capacity at least covers the database tiering design
- cloud VMs use instance-local NVMe for Flash and separate durable storage for persistence
- node CPU, NIC bandwidth, and I/O queues have headroom

Do not proceed with a Flex recommendation if the storage layout is unknown.

For VM or bare-metal clusters, confirm Flash storage is prepared on every eligible node before enabling Auto-Tiering. Use the supported Redis Software preparation workflow, commonly `prepare_flash.sh`, for the installed version.

For Kubernetes deployments, do not run host preparation steps directly unless current operator guidance says to. Use the Redis Enterprise Cluster fields for Redis on Flash / Auto-Tiering, such as `redisOnFlashSpec` and `flashShardsLimit`, according to the installed operator API.

## License And Flash Shard Limits

Before creating or scaling Auto-Tiering databases, check license capacity:

```http
GET /v1/license
```

Look for flash and RAM shard fields when supported by the installed version and license, such as:

- `flash_shards_limit`
- `flash_shards_in_use`
- `ram_shards_limit`
- `ram_shards_in_use`

Common licensing findings:

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| new Flash shard cannot be created | flash shard limit reached or license expired | renew, upgrade, or right-size shard usage |
| license update fails | invalid key, future start date, or FQDN mismatch | verify cluster FQDN and license validity |
| Flash usage not visible in UI | Auto-Tiering disabled or no Auto-Tiering DB exists | check database configuration and API metrics |
| only total `shards_limit` appears | legacy license model | verify enforcement behavior and request updated license if needed |

## Sizing Workflow

1. Estimate dataset size, hot-set size, key/value size distribution, growth, and p99 targets.
2. Start with enough RAM for the hot set plus headroom, then validate against current Redis Software version requirements.
3. Check per-node Flash IOPS, queue depth, and latency under expected cold-read bursts.
4. Balance shards so read and write pressure are not concentrated on a few nodes.
5. Baseline p99 latency, RAM hit ratio, percent values in RAM, evictions, replica lag, Flash IOPS, and node logs before changes.

## Monitoring

Monitor cluster, database, and node Flash health through UI, API, and Prometheus. Useful signals include:

- `cluster_shards_limit{shard_type="flash"}`
- `bdb_shards_used{shard_type="flash"}`
- Flash disk usage, IOPS, queue depth, and latency
- RAM hit ratio and percent values in RAM
- shard state and placement
- CPU and RAM headroom

As operating guidelines, alert before Flash shard usage approaches licensed capacity, before Flash disks are near full, and before sustained CPU/RAM pressure leaves no room for rebalancing.

## Migration Options

Choose based on topology and downtime tolerance:

- Snapshot cutover: export RDB, import into the Flex database, warm up, then cut over.
- Live migration: use ReplicaOf, Redis Data Integration, RIOT-style tooling, or another supported sync path, then validate and promote.
- Version upgrade: verify current Redis Software behavior before stating whether Flex v1 automatically transitions to Flex v2 during upgrade.

After migration or upgrade, validate endpoint health, reads/writes, p99 latency, RAM hit ratio, Flash IOPS, evictions, and replica lag.

## Change Management

RAM-to-Flash ratio changes are online but can trigger a rebalance that moves data between tiers.

Before ratio changes:

- schedule a maintenance window
- verify backups and restore process
- pause heavy jobs if possible
- monitor active resize or rebalance status
- re-baseline metrics after completion

## Troubleshooting

- Shard allocation failure: confirm Flash devices are mounted, formatted, prepared on every eligible node, and visible to Redis Software; then verify license headroom.
- Flash usage missing from UI: confirm Auto-Tiering is enabled and at least one Auto-Tiering database exists; check `/v1/license` and Prometheus metrics.
- License limit reached: compare flash shard usage with license limits and check license expiration/FQDN before changing database layout.
- Cold-read latency: increase RAM ratio, improve locality, use higher-IOPS NVMe, pre-warm hot keys, and inspect queue depth.
- Replica lag: check NIC bandwidth, replica CPU/I/O, region or rack placement, and read distribution.
- Evictions: scale memory, review TTL churn, inspect dataset growth, and verify eviction policy.
- Throughput drop after ratio change: confirm rebalance and defer heavy jobs until it completes.
- Unexpected RAM growth: check for very large keys or values that remain in RAM under current product behavior.

Useful checks:

```bash
rladmin status
rladmin status shards
rlcheck
grep -iE "flash|tier|speedb|license|shard" /var/opt/redislabs/log/*.log
```

For shards in `error`, `unassigned`, or `out_of_sync`, investigate node-level Flash mount, disk error, license, and placement constraints before retrying database changes.

## Response Pattern

Answer with:

1. Whether Flex fits the locality and latency requirements.
2. The infrastructure checks that must pass before implementation.
3. A sizing and monitoring plan.
4. Migration or ratio-change steps.
5. The first troubleshooting checks for the reported symptom.
