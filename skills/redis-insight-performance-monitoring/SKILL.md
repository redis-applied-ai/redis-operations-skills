---
name: redis-insight-performance-monitoring
description: "Use Redis Insight to monitor and diagnose Redis performance across Redis Cloud, Redis Enterprise Software, and OSS. Use when the user asks about Redis Insight Profiler, slowlog review, database analysis, hot keys, large keys, memory distribution, latency, connection spikes, evictions, streams, Query Engine performance, or when to move from Redis Insight to Prometheus/Grafana."
---

# Redis Insight Performance Monitoring

Use this skill to guide performance diagnosis with Redis Insight and decide when deeper production observability is needed.

## Setup Checks

1. Confirm Redis Insight can reach the database endpoint.
2. Verify host, port, username/password, TLS settings, and CA trust.
3. For Redis Cloud, confirm the source IP is allow-listed or private networking is configured.
4. Use read-only or least-privilege credentials when possible for inspection workflows.

## Diagnostic Workflow

1. Start with the symptom:
   - High latency.
   - Memory pressure or evictions.
   - Connection errors.
   - Slow commands.
   - Hot key or shard imbalance.
   - Stream backlog.
   - Search/Query Engine slowdown.
2. Open Redis Insight and select the database.
3. Use Profiler for real-time command behavior:
   - Command frequency.
   - Expensive operations.
   - Client source patterns.
4. Use Database Analysis for:
   - Data type breakdown.
   - Large keys.
   - Namespace distribution.
   - Expiration coverage.
   - Memory hotspots.
5. Use Slow Log for blocking or long-running commands.
6. Use Browser/Bulk Actions only after confirming the target keyset; destructive actions require explicit confirmation.
7. For production trends or alerting, switch to Prometheus/Grafana or the platform monitoring stack.

## Metric Interpretation

Treat thresholds as starting points, not universal SLOs.

| Signal | Investigate when |
| --- | --- |
| Latency | Average or p99 rises above workload expectations. |
| CPU | Sustained high CPU on a shard/core correlates with latency. |
| Memory | Usage approaches plan/node limits, swap appears, fragmentation is high, or evictions occur unexpectedly. |
| Connections | Sudden growth, churn, or rejected clients appears. |
| Evictions | Any unexpected spike occurs for a workload that should retain data. |
| Slow log | Blocking or unbounded commands appear. |
| Hot keys | One key or small namespace dominates operations. |
| Query Engine | Index scans, broad wildcard queries, or large result sets dominate query time. |

## Common Findings

| Finding | Action |
| --- | --- |
| `KEYS` or unbounded scans/ranges | Replace with incremental `SCAN`, bounded ranges, or application-side pagination. |
| Large synchronous deletes | Use `UNLINK` or Redis Insight Bulk Actions with confirmation and monitoring. |
| Large keys | Redesign data model, split keys, or cap collection sizes. |
| Hot key | Shard/distribute access, cache locally, or redesign key layout. |
| Connection churn | Add pooling, reuse clients, and inspect reconnect behavior. |
| Memory growth | Check TTL coverage, eviction policy, top namespaces, and data type distribution. |
| Slow Search queries | Review schema, TAG/NUMERIC filters, result limits, and use `FT.PROFILE` for deeper detail. |

## Production Observability

Redis Insight is useful for interactive diagnosis. For production monitoring:

- Use Redis Cloud or Redis Enterprise metrics.
- Use Prometheus/Grafana for dashboards, history, and alerting where supported.
- For Redis Enterprise Software, validate the current Prometheus endpoint and dashboard package against the deployed version.
- In Kubernetes, verify exporter/service-monitor configuration, network policies, and secured metric access.

## Escalation Packet

Collect:

- Database type and deployment.
- Redis Insight version.
- Symptom and time window.
- Profiler evidence.
- Slowlog entries.
- Database Analysis screenshots or exported findings.
- Memory, CPU, latency, connection, eviction, and key distribution metrics.
- Query examples and index schema for Search/Query issues.
