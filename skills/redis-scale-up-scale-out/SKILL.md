---
name: redis-scale-up-scale-out
description: "Choose how to increase Redis throughput or capacity by scaling up, scaling out, clustering, or adding read replicas. Use when the user sees CPU or memory near 80 percent, ops/sec capped below demand, latency spikes as traffic grows, hot shard or hot key imbalance, dataset growth, Redis Cloud clustering permanence, client cluster compatibility issues, or needs to decide between vertical scaling, shard count increases, horizontal scaling, and read scaling."
---

# Redis Scale Up Scale Out

Use this skill when a Redis workload is approaching throughput, memory, network, or shard limits and the user needs to choose a scaling direction.

## First Diagnose the Limit

Collect:

- p95/p99 latency.
- Ops/sec and command mix.
- Per-shard CPU.
- Memory usage and evictions.
- Network throughput.
- Hot key or hot shard evidence.
- Client connection and retry behavior.
- Dataset growth trend.

Do not choose a scaling path from average ops/sec alone.

## Symptom Map

| Symptom | Likely meaning | Direction |
| --- | --- | --- |
| CPU or memory near 80 percent on one shard | Single-shard saturation | Scale up short term; prepare scale out. |
| Ops/sec capped below demand | Throughput limit reached | Increase throughput or shard count. |
| One shard much hotter | Hot keys or uneven access | Fix key design before or alongside scaling. |
| Latency rises with traffic | Insufficient headroom | Scale before more load. |
| Errors after clustering | Client or key pattern incompatibility | Validate cluster-aware clients and multi-key design. |
| Read-heavy load | Read path is bottleneck | Consider read replicas if consistency tolerance allows. |

## Scale Up

Scale up when:

- Dataset is small or moderate.
- Traffic growth is incremental or bursty.
- Workload still fits a single shard.
- You need fast relief without changing client routing.

Scale up can increase memory, CPU, or configured throughput, but it does not fix:

- Hot keys.
- Sustained growth beyond one shard.
- Poor key distribution.
- Need for stronger fault isolation.

In Redis Cloud, crossing certain size or throughput thresholds can enable clustering permanently. Verify plan behavior before applying changes.

## Scale Out

Scale out when:

- Throughput growth is sustained.
- Dataset size exceeds practical single-shard capacity.
- More parallelism is required.
- Fault isolation and future growth matter.

Scaling out changes operational behavior:

- Data is partitioned across shards.
- Clients may need cluster-aware behavior.
- Multi-key operations require careful key design.
- Hash tags can help co-locate keys but can also create hot shards.

## Read Scaling

Use read replicas when:

- Most traffic is read-only.
- Applications can tolerate replica lag.
- The write path is not the bottleneck.
- Monitoring can detect lag and stale-read risk.

Read replicas complement sharding; they do not replace sharding for write-heavy workloads.

## Optimize Before Scaling

- Use pipelining and batching.
- Tune connection pooling.
- Avoid blocking commands in hot paths.
- Split large keys and hot keys.
- Add TTLs and appropriate eviction policies for cache workloads.
- Confirm serialization and payload sizes are efficient.

## Post-Change Validation

After any scaling change, verify:

- p95/p99 latency improved.
- Per-shard CPU is balanced and below target.
- Memory headroom remains healthy.
- Evictions are expected or gone.
- Throughput meets demand.
- Client errors did not increase.
- Hot keys did not simply move the bottleneck.

## Escalation Packet

Collect:

- Redis product, plan, database ID, and current topology.
- Current and target memory, throughput, shard count, and replica settings.
- Metrics before/after: CPU, memory, latency, ops/sec, network, evictions.
- Hot key or shard imbalance evidence.
- Client library and cluster-awareness status.
- Multi-key command patterns.
- Growth forecast and peak traffic window.
