---
name: redis-cloud-flex-v2-operations
description: Use when choosing, sizing, migrating, operating, or troubleshooting Redis Flex v2 in Redis Cloud, including RAM-to-Flash ratio, memory tiering, cold-read latency, RAM hit ratio, Flash IOPS, Flex v1 to v2 upgrade behavior, Active-Active limitations, resize impact, evictions, replica lag, or cost-capacity tradeoffs.
---

# Redis Cloud Flex v2 Operations

Use this skill to decide whether Redis Flex is appropriate and to guide sizing, monitoring, and troubleshooting for Redis Cloud memory tiering. Verify current Redis Cloud plan, region, version, and feature availability in the Console or official docs before promising support for a specific environment.

## Fit Assessment

Flex is a strong candidate when:

- the dataset is large
- a smaller hot set receives most traffic
- cold reads can tolerate higher latency than hot reads
- cost and capacity efficiency matter
- access patterns have predictable locality

Avoid or reconsider Flex when:

- access is uniform across most of the dataset
- the hot set is nearly the full dataset
- the workload requires features not currently supported with Flex, such as Active-Active if still unsupported for the target plan
- p99 latency targets cannot tolerate cold-read behavior

## Sizing Workflow

1. Estimate total dataset size, hot-set size, growth rate, and p99 latency target.
2. Choose an initial RAM percentage based on the hot set plus headroom, then verify current minimums and plan constraints.
3. Confirm Flash IOPS and throughput headroom for cold-read bursts.
4. Validate shard count, replication, persistence, backup, and network requirements.
5. Baseline latency, RAM hit ratio, percent values in RAM, evictions, Flash IOPS, and replica lag before changing configuration.

## Change Management

Changing the RAM-to-Flash ratio is online, but it triggers an active resize that moves data between tiers.

Before changing ratio or database size:

- schedule the change during a maintenance or low-traffic window
- verify recent backups and restore process
- pause heavy batch jobs when possible
- notify application owners about possible temporary performance effects
- re-baseline metrics after the resize completes

## Migration And Upgrade Notes

When discussing Flex architecture upgrades:

- Check the database Redis version and current Redis Cloud release behavior.
- Verify whether the database is still on Flex v1 or already on Flex v2.
- For source guidance that says Flex v1 transitions during Redis 8.2+ upgrade, present that only after checking current product documentation or console state.
- After any upgrade, validate latency, RAM hit ratio, Flash IOPS, and replica lag.

## Troubleshooting

- Cold-read latency spikes: increase RAM percentage, pre-warm hot keys, improve locality, and check Flash IOPS.
- Throughput dip during ratio changes: confirm active resize and defer heavy workloads until it completes.
- Evictions: increase RAM percentage or total database size, review TTL churn, and inspect eviction policy.
- Replica lag: check region distance, replica resources, bandwidth, and I/O capacity.
- Unexpected RAM growth: look for very large keys or values that cannot be moved out of RAM under current product behavior.
- Cost spike: review recent size, ratio, shard, replica, and throughput changes against current billing details.

## Response Pattern

Answer with:

1. Whether Flex fits the workload's locality and latency profile.
2. The initial RAM/Flash sizing approach and metrics to validate.
3. Change-window and backup guidance for ratio edits.
4. Troubleshooting steps tied to the observed symptom.
5. Current-state verification points for plan, version, feature support, and billing.
