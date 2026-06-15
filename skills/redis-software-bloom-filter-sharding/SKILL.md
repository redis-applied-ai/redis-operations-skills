---
name: redis-software-bloom-filter-sharding
description: Use when designing, scaling, or troubleshooting RedisBloom Bloom filters in Redis Software, including BF.RESERVE capacity and error rate, key-tag sharding, hash slot placement, application-level partitioning, CRC16 slot awareness, false-positive drift, BF.INFO monitoring, CROSSSLOT prevention, or Active-Active CRDB compatibility checks.
---

# Redis Software Bloom Filter Sharding

Use this skill when a RedisBloom Bloom filter must be distributed across shards in Redis Software. Redis does not automatically reshard one logical Bloom filter; sharding is a key-design and application-routing decision.

## Compatibility Check

First confirm:

- Redis Software version
- RedisBloom module availability
- database type and clustering mode
- whether the database is Active-Active CRDB

Verify current product behavior before promising Bloom support in Active-Active or other special topologies.

## Design Goals

Sharding a Bloom filter can help when:

- one filter is too large or too hot
- false positive rate is drifting upward because capacity was exceeded
- workload needs more shard-level parallelism
- memory distribution is uneven

It will not help if the application cannot route writes and reads to the same shard-specific filter consistently.

## Sharding Strategies

Key-tag sharding:

- use Redis hash tags to control slot placement
- vary tag values to distribute filters
- keep related operations on the intended shard

Example key shape:

```text
bf:{0}:malware
bf:{1}:malware
bf:{2}:malware
bf:{3}:malware
```

Application-level partitioning:

- choose a deterministic function from item to shard
- examples: hash prefix, modulo of a stable hash, tenant ID, region, or category
- ensure `BF.ADD` and `BF.EXISTS` use the same mapping

Slot-aware placement:

- use CRC16/hash-slot knowledge when filters must land on specific shards
- validate placement after creation

## Creation And Sizing

Create each shard-specific filter with capacity and false-positive target:

```text
BF.RESERVE <key> <error_rate> <capacity>
```

Use `NONSCALING` only when capacity is well understood and overfill behavior is acceptable.

Pre-size filters to avoid sub-filter expansion and rising false positives.

## Monitoring

Use:

```text
BF.INFO <key>
```

Monitor:

- item count and capacity
- expansion/sub-filter behavior
- false-positive rate indicators
- memory per shard
- CPU and command rate per shard
- hot filter keys

## Troubleshooting

- Uneven load: adjust partition mapping and filter assignment.
- High false positives: increase capacity, add more filter shards, or rebuild with better sizing.
- `CROSSSLOT`: group related keys with hash tags or avoid multi-key operations across slots.
- Resharding needed: create new filter shards and migrate/replay source data through the new mapping.
- Missing commands: verify RedisBloom module and database compatibility.

## Response Pattern

Answer with:

1. Compatibility and topology check.
2. Partitioning strategy.
3. Key naming and hash-tag plan.
4. Capacity and false-positive sizing.
5. Monitoring and migration plan for future growth.
