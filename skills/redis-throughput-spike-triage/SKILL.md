---
name: redis-throughput-spike-triage
description: "Triage Redis Cloud or Redis Software traffic spikes above configured Ops/Sec. Use when observed throughput exceeds configured ops/sec, latency or p95/p99 rises during bursts, shard CPU saturates, clients time out or retry storm, evictions or memory pressure appear, load tests overwhelm dev environments, or the user needs guidance on pipelining, batching, shard scaling, memory headroom, eviction policy, and capacity alignment."
---

# Redis Throughput Spike Triage

Use this skill when Redis traffic exceeds planned or configured throughput and the user needs to stabilize, diagnose, or resize.

## Core Rule

Configured Ops/Sec is usually a capacity-planning signal, not the only indicator of overload. Latency, error rate, shard CPU, memory pressure, network saturation, and retry behavior determine whether the system is healthy.

## Immediate Stabilization

1. Reduce or pause non-critical workloads:
   - Analytics jobs.
   - Scans.
   - Maintenance jobs.
   - Load tests.
   - Bulk imports or migrations.
2. Check for blocking or expensive commands:
   - `KEYS`
   - Large `SCAN` jobs.
   - Heavy Lua or `EVAL`.
   - Large collection deletes or range operations.
3. Confirm clients use sane timeouts and exponential backoff to avoid retry storms.
4. Watch p95/p99 latency and error rate while load is reduced.

## Assessment Checklist

Collect peak-window metrics, not only averages:

- Observed ops/sec versus configured ops/sec.
- p95 and p99 latency.
- Per-shard CPU, especially sustained values above roughly 70 percent.
- Memory usage and free-memory headroom.
- Evictions and rejected writes.
- Network throughput and packet drops.
- Client timeout and retry rates.
- Hot shard or hot key indicators.

## Mitigation Matrix

| Symptom | Action |
| --- | --- |
| Observed ops/sec far above configuration but latency is stable | Update sizing assumptions and alert thresholds; keep monitoring headroom. |
| p95/p99 latency rises during bursts | Add pipelining, batching, and reduce chatty request patterns. |
| One shard CPU is saturated | Add shards, rebalance, or fix hot-key/hash-slot distribution. |
| All shards CPU-saturated | Increase capacity or reduce workload. |
| Evictions or memory pressure | Increase memory, adjust eviction policy, and confirm TTL strategy. |
| Retry storms | Add exponential backoff, jitter, circuit breaking, and sane timeout limits. |
| Dev/test spike overload | Isolate load tests or resize non-production environments for expected tests. |

## Scaling Guidance

- Scale to peak p95/p99 demand, not average load.
- Keep per-shard CPU below about 70 percent during peak when possible.
- Maintain 20 to 30 percent memory headroom.
- Add shards for horizontal throughput when key distribution supports it.
- Increase memory if evictions or allocator pressure occur.
- Update configured Ops/Sec to match real observed peaks after the workload pattern is understood.

## Client Optimization

- Use pipelining for many independent commands.
- Use command batching such as `MGET` or `MSET` when data access patterns allow.
- Avoid one network round trip per tiny operation.
- Use backoff and jitter on retries.
- Put load shedding or queue limits around background jobs.

## Success Criteria

The spike is handled when:

- p95 and p99 latency stay within SLO.
- Error rate and timeouts return to normal.
- No sustained evictions occur unless expected for cache workload.
- Per-shard CPU and network utilization remain within headroom.
- Client retry volume does not amplify load.

## Escalation Packet

Collect:

- Redis product, plan, database ID, and configured Ops/Sec.
- Peak observed ops/sec and time window.
- p95/p99 latency, error rate, and timeout metrics.
- Per-shard CPU, memory, and network metrics.
- Eviction and memory-pressure metrics.
- Recent workload changes, deploys, load tests, or jobs.
- Client timeout, retry, pipeline, and batching settings.
- Blocking command or slowlog evidence.
