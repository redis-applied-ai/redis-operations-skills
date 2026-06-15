---
name: redis-hot-key-shard-imbalance
description: "Diagnose and remediate Redis hot keys overloading one shard. Use when shard CPU, memory, or latency is imbalanced, one Redis shard is overloaded, hot keys dominate traffic, `redis-cli --hotkeys`, `OBJECT FREQ`, SLOWLOG, INFO, CLIENT LIST, FT.INFO, or FT.PROFILE are needed, hash tags are concentrating traffic, shard count increases or key redesign are being considered, or Redis Search query/index patterns overload a shard."
---

# Redis Hot Key Shard Imbalance

Use this skill when one or a few Redis keys concentrate traffic on a shard and create uneven CPU, memory, or latency.

## Core Principle

Adding shards or rebalancing can reduce general load, but it does not eliminate a truly hot key. The durable fix is usually changing key design, access pattern, caching strategy, or query/index behavior.

## Detection Workflow

1. Compare shard-level metrics in Redis Cloud, Redis Software, Prometheus, or Grafana:
   - CPU above roughly 80 percent on one shard.
   - Latency elevated on one shard.
   - Memory much higher on one shard.
   - Network or command rate skewed to one shard.
2. Identify frequent keys where tooling supports it:

   ```bash
   redis-cli --hotkeys
   OBJECT FREQ <key>
   ```

   `OBJECT FREQ` and `--hotkeys` depend on LFU frequency tracking; if unavailable, use application logs, slowlog, command profiling, or sampled tracing.

3. Inspect slow or frequent operations:

   ```redis
   SLOWLOG GET
   INFO
   CLIENT LIST
   ```

4. Map suspicious keys to slots/shards using cluster-aware tooling or a key slot calculator.
5. For Search workloads, inspect query/index behavior:

   ```redis
   FT.INFO <index>
   FT.PROFILE <index> SEARCH QUERY "<query>"
   ```

## Common Causes

| Pattern | Why it overloads a shard |
| --- | --- |
| One popular key | All reads/writes route to one shard. |
| Large hash, list, set, sorted set, or JSON document | Operations target one key and one shard. |
| Overused hash tags | Many related keys are forced onto one shard. |
| Search query/index skew | Queries or indexes concentrate work on one shard. |
| Background ingestion or maintenance | Batch jobs repeatedly hit one shard or key prefix. |

## Remediation Options

| Cause | Remediation |
| --- | --- |
| Single hot object | Split into smaller keys by tenant, bucket, time window, or sub-resource. |
| Large collection | Partition collection across multiple keys and aggregate in application logic. |
| Overused hash tags | Remove or narrow hash tags unless key co-location is required. |
| Read hotspot | Add application-side caching, request coalescing, or replicated/read-optimized pattern where supported. |
| Write hotspot | Shard counters or queues, then aggregate asynchronously. |
| Search hotspot | Refactor index/query design and reduce broad queries hitting the same data. |
| General capacity pressure | Increase shard count or capacity after confirming key design is not the sole issue. |

## Hash Tag Guidance

Hash tags force keys to the same slot. Use them only when operations require key co-location. Overusing a tag such as `{tenant123}` can create a hot shard if that tenant is busy.

Do not use hash tags as a manual balancing tool unless the access pattern has been tested.

## Scaling Guidance

- In Redis Cloud or Redis Software, use supported UI/API paths to increase shard count where applicable.
- Do not assume `rladmin` can manually increase shard count or assign slots for the user.
- After scaling, monitor shard CPU, memory, latency, and key distribution to verify improvement.
- If the same key remains hot, scaling alone will not solve the problem.

## Escalation Packet

Collect:

- Product, database ID, shard count, and clustering mode.
- Shard-level CPU, latency, memory, and ops/sec during the incident.
- Suspected hot keys and access frequency evidence.
- Slowlog samples and client/application evidence.
- Key slot/shard mapping for suspected keys.
- Hash tag usage examples.
- Search index/query profile data if relevant.
- Recent ingestion, deploy, campaign, or traffic spike timeline.
