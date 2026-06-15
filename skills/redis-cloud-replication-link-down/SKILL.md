---
name: redis-cloud-replication-link-down
description: Use when Redis Cloud shows Replication Link Down, replica disconnected from primary, replication lag spikes, sync repeatedly starts then fails, maintenance causes transient link down, big keys or hot keys exhaust replication buffers, memory or CPU headroom is low, or plan support for replicas must be verified.
---

# Redis Cloud Replication Link Down

Use this skill to triage Redis Cloud replication link down indicators. First determine whether the event is transient maintenance behavior or a persistent replication problem.

## First Checks

1. Confirm the Redis Cloud plan and database settings support replicas and replication is enabled. Verify current plan capabilities in the Console or official docs.
2. Check whether the alert overlaps a maintenance window, resize, failover, or platform event.
3. Inspect database health, replication lag, memory headroom, CPU, disk I/O, and network metrics.
4. Review available database logs or event messages for sync, buffer, authentication, TLS, or connectivity errors.

## Common Causes

- transient maintenance or failover event
- memory or CPU pressure during write spikes
- large keys causing expensive replication or full-sync pressure
- hot keys or bursty pipelines overrunning buffers
- insufficient shard or database size for the workload
- network jitter on the client or private-network path
- product-side configuration or sync-manager issue that requires Redis Support

## Diagnostic Workflow

1. Identify affected database, region, shard, and replica if visible.
2. Correlate link-down time with maintenance, failover, traffic, deploys, or bulk writes.
3. Check if replication lag returns to normal.
4. Inspect big keys and hot keys if sync repeatedly fails partway through.
5. Check whether memory and CPU have enough headroom.
6. If the link repeatedly drops or full sync cannot complete, collect evidence and escalate.

## Mitigation

- Reduce write burstiness or pipeline size during replication recovery.
- Break up large keys and avoid large blocking deletes.
- Increase memory, throughput, or shard count when resource pressure is sustained and the plan supports it.
- Use private networking options where available if network jitter is a factor.
- Test failover and reconnect behavior in non-production.

## Escalation Package

Collect:

- subscription and database IDs
- replication alert timestamps
- maintenance or failover window details
- replication lag graph
- memory, CPU, disk I/O, and network graphs
- shard or database logs mentioning sync or buffer failure
- big-key or hot-key evidence
- recent workload, deploy, or configuration changes

Escalate when link down persists, sync repeatedly fails, or logs suggest a product-side sync/configuration issue.

## Response Pattern

Answer with:

1. Whether the event looks transient or persistent.
2. Plan and replica support verification.
3. Metrics and logs to inspect.
4. Workload or sizing mitigation.
5. Evidence needed for Redis Support if it does not self-heal.
