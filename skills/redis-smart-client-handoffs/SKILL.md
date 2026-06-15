---
name: redis-smart-client-handoffs
description: Use when Redis Cloud or Redis Software applications see disconnects, timeouts, reconnect loops, or latency spikes during maintenance, rolling upgrades, in-place upgrades, database version upgrades, shard migration, failover, or endpoint movement, and the answer should assess Smart Client Handoffs, RESP3 readiness, client library support, timeout relaxation, and upgrade-method tradeoffs.
---

# Redis Smart Client Handoffs

Use this skill to reduce application disruption during Redis maintenance by checking whether Smart Client Handoffs (SCH), RESP3, and client retry behavior are ready.

## When SCH Helps

SCH is most useful when planned maintenance changes node availability or shard routing:

- Redis Cloud maintenance and database version upgrades
- Redis Software rolling cluster upgrades
- Redis Software maintenance mode for node patching or hardware work
- Redis Software database version upgrades
- shard migration, endpoint movement, or failover tests

SCH reduces reconnect flaps and timeout errors by letting capable clients prepare for maintenance and use relaxed timeouts during the transition. It does not eliminate every disconnect, especially when an in-place upgrade restarts the server process under active connections.

## Readiness Checklist

1. Identify product and operation: Redis Cloud or Redis Software; rolling upgrade, in-place upgrade, maintenance mode, database upgrade, shard migration, or failover.
2. Confirm the application uses DNS/database endpoints rather than static node or shard addresses.
3. Confirm RESP3 is enabled or available in the client.
4. Confirm the client library version supports SCH. Verify current minimum versions against official client documentation before giving a final version recommendation.
5. Confirm client retry, reconnect, timeout, and backoff settings are not overly aggressive.
6. Identify blocking or long-held connections such as Pub/Sub; expect them to reconnect normally rather than pre-handoff.
7. Capture baseline connection success rate, reconnect count, timeout rate, and p95/p99 latency.

## Product-Specific Checks

For Redis Cloud:

- SCH is generally managed by Redis for capable databases and clients.
- Verify the database and client can use RESP3.
- If unexpected disconnects continue, focus on client library support, RESP3 settings, DNS behavior, socket timeouts, and reconnect policy.

For Redis Software:

- Confirm the cluster version and database engine version support the planned SCH behavior.
- Confirm SCH is enabled server-side through the supported REST API or admin workflow.
- Prefer rolling upgrades or maintenance mode for lower-impact production maintenance.
- Treat in-place upgrades as partially mitigated: timeout behavior may improve, but active connections can still drop during process replacement.

## Client Guidance

| Client family | What to verify |
| --- | --- |
| go-redis | SCH-capable release, RESP3 mode, reconnect backoff, and socket timeouts. |
| redis-py | SCH-capable release, RESP3 protocol selection, retry settings, and connection pool behavior. |
| node-redis | SCH-capable release, RESP3 mode, reconnect strategy, and command timeout settings. |
| Lettuce | SCH-capable release, RESP3 support, topology refresh, reconnect, and timeout settings. |

Use the latest stable client release when practical, then verify compatibility in staging with an active workload.

## Troubleshooting Matrix

| Symptom | Likely cause | Action |
| --- | --- | --- |
| SCH does not trigger | Client lacks SCH/RESP3 support, server-side SCH is disabled, or database version is not eligible. | Verify client, RESP3, Redis Software SCH config, and database capability. |
| Timeouts still happen | Socket or command timeout is too strict for maintenance latency. | Relax maintenance-window timeouts and use bounded retry with backoff. |
| Disconnects during in-place upgrade | Process replacement breaks active connections. | Prefer rolling upgrade where possible and rely on reconnect for remaining drops. |
| Pub/Sub or blocking commands drop | Blocking connections are not covered by SCH behavior. | Design handlers to resubscribe and resume after reconnect. |
| Reconnect surge after maintenance | Clients restart or reconnect in sync. | Use `redis-reconnect-storms` to tune jitter, pool sizing, and rollout pacing. |

## Validation Pattern

During a staging test or maintenance window, report:

- client library and version, RESP mode, and SCH support status
- operation type and expected maintenance behavior
- whether timeouts were relaxed during the event
- reconnect count, timeout count, latency change, and recovery time
- any remaining gaps: static addresses, old clients, unsupported blocking workflows, or over-tight timeouts
