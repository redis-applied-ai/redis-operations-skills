---
name: redis-software-node-memory-increase
description: "Increase Redis Software node memory or maxmemory without downtime when host RAM headroom exists. Use when the user hits maxmemory, eviction thresholds, high fragmentation, needs a rolling memory increase, wants to preserve 20-30 percent memory headroom, must validate host-level RAM, reserved or provisional RAM, replication lag, DC/DR capacity alignment, or decide whether to scale nodes or shards instead."
---

# Redis Software Node Memory Increase

Use this skill when a Redis Software deployment needs more effective memory without downtime.

## Core Rule

Only increase effective memory dynamically when the host already has safe physical RAM headroom. If host-level RAM is exhausted, resize infrastructure or scale out instead.

## Safety Rules

- Do not update multiple nodes at once.
- Confirm cluster health before changing memory.
- Keep 20 to 30 percent free memory at steady state.
- Avoid decreasing maxmemory unless the dataset has already been reduced.
- Align primary and DR environments so failover does not land on undersized capacity.

## Preflight Checks

Confirm:

- Host physical RAM headroom exists on each node.
- Redis Software/platform supports dynamic memory change without restart for this setting.
- No ongoing failovers, migrations, or maintenance.
- Replication lag is low.
- Latency is stable.
- Fragmentation ratio and used memory are understood.
- Reserved or provisional RAM requirements are satisfied.

## Rolling Increase Workflow

1. Measure current usage:
   - `used_memory`
   - current `maxmemory`
   - fragmentation ratio
   - node CPU and latency
   - replication lag
2. Determine target memory:
   - Preserve 20 to 30 percent free headroom.
   - Add extra buffer when fragmentation ratio is high, for example above 1.5.
   - Prefer incremental increases when uncertain.
3. Choose one node during a lower-traffic window.
4. Apply the supported memory/maxmemory change through the platform tool.
5. Monitor for 5 to 15 minutes:
   - Memory usage.
   - CPU.
   - Latency.
   - Evictions.
   - Replication status.
6. Repeat node by node.
7. Apply equivalent sizing to DR clusters where applicable.

## Post-Change Validation

Confirm:

- `used_memory` remains comfortably below `maxmemory`.
- Evictions stop or return to expected levels.
- Latency and CPU remain within SLO.
- Replication lag does not increase.
- DR environment can handle failover load.

## When to Scale Instead

Choose node resize, more shards, or broader capacity work when:

- Host RAM headroom is unavailable.
- Dataset growth is sustained and predictable.
- Evictions continue after memory increase.
- A single shard remains CPU-bound.
- Fragmentation is not the primary issue.
- DR capacity cannot match production.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Memory increase not applied | Host RAM, platform limits, dynamic allocation support, and configuration errors. |
| Instability after change | Roll back recent change if needed; re-evaluate headroom and workload. |
| Evictions continue | Dataset growth exceeds new capacity or eviction policy is wrong. |
| Replication lag rises | Dataset growth increased replication pressure; check network and DR capacity. |
| Decrease causes failures | `used_memory` exceeded new limit; reduce data before lowering memory. |

## Escalation Packet

Collect:

- Redis Software version and deployment model.
- Node IDs and current/target memory values.
- Host RAM, reserved/provisional RAM, and free memory.
- `used_memory`, fragmentation ratio, evictions, CPU, latency.
- Replication lag before and after.
- DC/DR topology and capacity alignment.
- Platform tool or command used and any error output.
