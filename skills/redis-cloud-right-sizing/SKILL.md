---
name: redis-cloud-right-sizing
description: "Right-size oversized Redis Cloud databases safely by reducing throughput, memory, replication, or Active-Active only after metric validation. Use when the user asks whether a Redis Cloud database is over-provisioned, how to lower ops/sec, reduce memory allocation, downgrade Essentials, reduce Pro RBUs, remove unnecessary HA, or validate cost-saving changes without causing latency or OOM regressions."
---

# Redis Cloud Right-Sizing

Use this skill when a Redis Cloud database appears over-provisioned for its actual workload.

## Evidence First

Do not recommend downsizing from allocation alone. Confirm sustained underuse with metrics across representative traffic periods:

- Actual ops/sec versus configured throughput.
- Latency under normal and peak load.
- Used memory, dataset growth, and headroom.
- Request size and payload patterns.
- Evictions, rejected operations, or throttling.
- Business requirements for replication, persistence, and Active-Active.

## Oversized Signals

| Signal | Interpretation |
| --- | --- |
| Actual ops/sec far below configured limit | Throughput may be oversized. |
| Memory usage consistently far below allocation | Memory allocation may be oversized. |
| Stable low latency under realistic peak load | There may be headroom to reduce capacity. |
| Replication or Active-Active enabled without SLA need | HA/durability cost may exceed business requirement. |
| Small request payloads with low throughput | Plan may be larger than workload needs. |

## Right-Sizing Workflow

1. Establish a baseline: metrics, current configuration, and cost driver.
2. Choose one change dimension at a time:
   - Throughput / ops/sec.
   - Memory allocation.
   - Essentials tier.
   - Replication or Active-Active.
3. Model the target state:
   - Dataset fits with overhead and growth.
   - Throughput covers peak and burst behavior.
   - Business SLA still matches HA/durability choices.
4. Apply the smallest practical reduction.
5. Run realistic load or observe a representative traffic window.
6. Set alerts for latency, throughput saturation, memory pressure, evictions, and connection errors.
7. Revert or adjust incrementally if performance regresses.

## Plan Differences

| Plan | Right-sizing approach |
| --- | --- |
| Essentials | Downgrade only if dataset, throughput, and connection usage fit the lower tier. Verify current plan limits in the console/docs before acting. |
| Pro | Tune database throughput and memory incrementally; validate impact after each change. |

## Memory Reduction Checks

Before lowering memory:

- Account for replicas/HA.
- Account for persistence and capability/module overhead.
- Leave growth and fragmentation headroom.
- Check eviction policy.
- Confirm no recent import, migration, or traffic pattern makes current usage unrepresentative.

## HA/Durability Safety

Disabling replication or Active-Active can materially change availability and recovery behavior. Before recommending it:

1. Confirm the business no longer requires the current SLA.
2. Explain the availability and failure-domain tradeoff.
3. Confirm backups and recovery expectations.
4. Ask for explicit confirmation before making the change.

## Validation

After each change:

- Compare before/after latency, ops/sec, CPU, memory, evictions, and errors.
- Verify the intended configuration in Redis Cloud Console.
- Confirm application-level SLOs remain healthy.
- Keep a rollback path for the previous configuration.

## Escalation Packet

Collect:

- Subscription/database ID and plan type.
- Current throughput, memory, replication, persistence, and Active-Active settings.
- Metrics baseline and peak traffic window.
- Proposed target configuration.
- Load-test or post-change validation results.
- Business SLA assumptions for HA/durability.
