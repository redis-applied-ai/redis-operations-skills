---
name: redis-cloud-high-network-troubleshooting
description: Use when troubleshooting Redis Cloud high network usage beyond alert interpretation, including bandwidth trends, throughput ceilings, latency correlated with traffic, shard CPU, connection counts, heavy `FT.SEARCH`, large `ZRANGE` or `LRANGE`, `KEYS`, large `JSON.GET`, Lua scripts over large keysets, large payloads, full-object reads, connection churn, retry storms, Essentials bandwidth limits, Pro throughput increases, or isolating heavy workloads.
---

# Redis Cloud High Network Troubleshooting

Use this skill when Redis Cloud traffic is high enough to affect latency, limits, or plan capacity. For alert interpretation and plan decision framing, use `redis-cloud-high-network-warning`.

## First Classification

Classify the pressure:

- Bandwidth-bound: data transfer or monthly bandwidth is near a plan limit.
- Throughput-bound: ops/sec flat-lines, latency rises, or configured throughput is saturated.
- Payload-bound: large values or full-object reads consume network despite moderate ops/sec.
- Connection-bound: reconnect storms, per-request connections, or retry amplification consume proxy/shard resources.

Correct classification determines whether to optimize traffic, change client behavior, increase throughput, or upgrade/isolate the workload.

## Evidence To Collect

From Redis Cloud metrics:

- monthly bandwidth usage if applicable
- total throughput and ops/sec trend
- p95/p99 latency
- shard or node CPU
- connection count and connection churn
- dropped connections or timeout rate

Optional CLI evidence:

```redis
SLOWLOG GET 200
```

## Heavy Command Checks

Look for commands that return or process large amounts of data:

- `FT.SEARCH` over large result sets
- large `ZRANGE` or `LRANGE`
- `KEYS`
- broad scans in hot paths
- large `JSON.GET`
- Lua scripts that iterate large keysets

If heavy commands dominate, refactor them before assuming the plan is too small.

## Payload Size Checks

High average request or response size lowers achievable ops/sec.

Common causes:

- multi-KB JSON documents
- blob-like values stored in Redis
- reading full objects when only a few fields are needed
- writing large objects repeatedly

Mitigations:

- fetch only required JSON paths or hash fields
- split large objects into smaller logical keys
- compress large values where latency and CPU tradeoffs are acceptable
- keep large analytical reads out of hot request paths

## Connection Behavior Checks

Symptoms:

- rapid connection count spikes
- frequent reconnect attempts
- elevated proxy or shard CPU
- timeouts followed by retry bursts

Fixes:

- use connection pooling
- avoid per-request connections
- add exponential backoff and jitter
- tune timeouts to avoid synchronized retries
- stagger application deployments and batch jobs

## Incident Stabilization

When performance is actively degraded:

1. Pause non-critical scans, exports, and bulk jobs.
2. Reduce traffic spikes and retry amplification.
3. Limit concurrency for maintenance or migration jobs.
4. Isolate the heaviest workload if it affects other databases in the subscription.
5. For Pro, consider increasing configured throughput after verifying traffic is legitimate.
6. For Essentials, begin tier or Pro migration planning if limits are repeatedly reached.

## Long-Term Fixes

| Finding | Durable fix |
| --- | --- |
| Large full-object reads | Return only required fields or paths. |
| Large collections in hot path | Page, trim, bucket, or redesign access pattern. |
| Chatty small commands | Use pipelining or batching. |
| Broad scans | Replace with incremental, bounded, off-peak scans. |
| Connection churn | Pool connections and stabilize retry behavior. |
| Sustained legitimate growth | Right-size throughput, memory, and plan architecture. |

## Escalation Packet

Collect:

- account, subscription, plan, and database ID
- metrics showing bandwidth/throughput/latency correlation
- configured throughput or plan limit context
- slowlog summary and heavy command examples
- payload-size examples with sensitive data redacted
- connection count and reconnect/retry behavior
- recent deploys, imports, migrations, or traffic changes
- whether other databases in the same subscription are affected
