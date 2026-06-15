---
name: redis-cloud-high-network-warning
description: "Interpret and respond to Redis Cloud High Network Usage warnings. Use when the user sees bandwidth nearing subscription limit, throughput plateauing, ops/sec at ceiling, elevated latency during traffic peaks, dropped connections, Essentials monthly bandwidth caps, Pro configured throughput limits, large payloads, retry storms, connection churn, or needs to choose between optimizing traffic, increasing throughput, upgrading plan tier, or moving from Essentials to Pro."
---

# Redis Cloud High Network Warning

Use this skill when Redis Cloud warns about high network usage, bandwidth, throughput, or traffic-related saturation.

## First Distinction

Determine whether the database is:

- Bandwidth-bound: monthly or sustained data transfer is near a plan cap.
- Throughput-bound: operations per second or allocated throughput is at a ceiling.
- Both: high ops/sec and large payloads are driving saturation together.

## Essentials vs Pro

| Plan | Network behavior | Scaling path |
| --- | --- | --- |
| Essentials | Fixed monthly bandwidth, max throughput, and connection limits by tier; databases in a subscription can affect each other. | Upgrade to a higher Essentials tier or move to Pro. |
| Pro | Configurable throughput per database; traffic is usage-based and sizing depends on CPU/network allocation. | Increase configured throughput or resize architecture. |

Verify current plan behavior in the Redis Cloud Console before promising a specific limit or billing outcome.

## Metrics to Check

In Redis Cloud:

- Database overview usage metrics.
- Monthly bandwidth usage.
- Total ops/sec.
- Throughput trends.
- p95/p99 latency.
- Shard CPU.
- Connection count and connection churn.
- Dropped connections or timeout rates.

## Decision Tree

| Finding | Path |
| --- | --- |
| Large payloads or inefficient commands | Optimize traffic first. |
| Retry storms or connection churn | Fix client pooling, timeout, and backoff behavior. |
| Pro database at configured throughput | Increase throughput and monitor CPU/latency. |
| Essentials bandwidth or throughput cap | Upgrade Essentials tier or move to Pro. |
| One Essentials database affects others | Isolate workload or move to Pro for per-database control. |
| Sustained predictable growth | Plan capacity increase instead of relying on bursts. |

## Optimize Path

Look for:

- Large JSON reads or writes.
- Returning entire documents when only fields are needed.
- Chatty request patterns.
- Missing pipelining or batching.
- `KEYS` or broad scans in hot paths.
- Excessive client reconnects.
- Aggressive retry loops without backoff.

Actions:

- Use pipelining and batching.
- Read only required fields.
- Compress or reshape large payloads where appropriate.
- Replace `KEYS` with `SCAN`.
- Fix connection pooling.
- Add exponential backoff and jitter.

## Capacity Path

For Pro:

1. Open the database performance settings.
2. Increase configured throughput.
3. Monitor shard CPU, latency, and traffic after the change.

For Essentials:

1. Check whether the subscription tier is hitting fixed limits.
2. Upgrade tier or move to Pro if limits are repeatedly reached.
3. Consider isolating high-traffic databases from quieter workloads.

## Immediate Action Triggers

Act immediately if:

- Bandwidth exceeds about 90 percent of monthly cap.
- Latency spikes line up with throughput ceilings.
- Connections are dropped.
- Retry traffic is amplifying load.
- Other databases in the subscription are impacted.

## Escalation Packet

Collect:

- Redis Cloud account, subscription, plan, and database ID.
- Warning text and timestamp.
- Monthly bandwidth usage and cap if applicable.
- Observed ops/sec and configured throughput.
- p95/p99 latency and shard CPU during warning.
- Payload size or command patterns.
- Connection count, churn, timeout, and retry metrics.
- Whether other databases in the subscription are affected.
