---
name: redis-reconnect-storms
description: "Triage and mitigate Redis connection surges, reconnect storms, max-client errors, proxy pressure, and deployment-related thundering-herd reconnects. Use when many clients reconnect after deploys, failovers, maintenance, network events, proxy flips, or restarts, or when the user needs client pool sizing, backoff, jitter, and connection-health monitoring guidance."
---

# Redis Reconnect Storms

Use this skill when Redis errors or latency correlate with many clients connecting or reconnecting at once.

## Incident Workflow

1. Identify the trigger:
   - Application deploy or autoscaling event.
   - Redis maintenance, failover, proxy flip, or endpoint change.
   - Network interruption, DNS change, TLS/certificate change, or firewall update.
2. Capture symptoms:
   - `ERR max number of clients reached`.
   - Connection reset/refused/timeouts.
   - High connection creation rate.
   - Latency spikes with normal shard CPU.
   - Proxy or file-descriptor pressure.
3. Apply immediate mitigations:
   - Pause or slow rollout.
   - Stagger service restarts.
   - Add reconnect backoff with jitter.
   - Cap pool growth and startup concurrency.
   - Close idle or leaked connections.
4. Check Redis and infrastructure metrics:
   - Connected clients and rejected connections.
   - New connections per second.
   - Proxy CPU and logs.
   - Shard CPU and latency.
   - File descriptor usage and limits.
   - Client pod/process restart counts.

## Client Behavior Rules

| Client pattern | Guidance |
| --- | --- |
| Unbounded reconnect loop | Add capped exponential backoff and jitter. |
| Large pool per process | Size pools to real concurrency, not peak replicas times guessed threads. |
| Mass startup pool warm-up | Delay and randomize warm-up; deploy in waves. |
| Per-request connection creation | Reuse clients or pools. |
| Idle connection leak | Enable lifecycle management and close unused connections. |

## Ecosystem Notes

| Ecosystem | Preferred pattern |
| --- | --- |
| Python / redis-py | Use a bounded pool such as `BlockingConnectionPool`; pair with application-level retry backoff. |
| Node.js / node-redis or ioredis | Prefer connection reuse/multiplexing; cap reconnect delay and retry attempts where appropriate. |
| Java / Jedis or Lettuce | Align pool size to thread/concurrency model; enable reconnect backoff; avoid synchronized startup. |
| .NET / StackExchange.Redis | Reuse a small number of `ConnectionMultiplexer` instances per process; avoid creating one per request. |

## Scenario Matrix

| Scenario | What to check | Fix |
| --- | --- | --- |
| Deploy causes immediate errors | Release batch size, new connection rate, pool warm-up behavior | Roll out in waves and jitter client startup. |
| Redis failover triggers reconnect loop | Client retry policy and DNS/endpoint refresh behavior | Add backoff/jitter and accept brief reconnect window. |
| Intermittent max-client errors | Pool sizing, idle leaks, connection count over time | Bound pools, close idle connections, tune limits if justified. |
| Latency spikes with low shard CPU | Proxy pressure or file descriptor exhaustion | Reduce connection churn, inspect proxy logs, verify OS limits. |
| Persistent churn after incident | Client retry bug, health-check loop, network instability | Trace client logs by source IP/service and fix retry loop. |

## Verification

The storm is under control when:

- New connection rate returns to baseline.
- Connected clients stabilize below limits.
- Rejected connections stop or return to expected background levels.
- Redis latency and proxy CPU recover.
- Application error rate recovers without synchronized retries.

## Escalation Packet

Collect:

- Time window and trigger event.
- Redis product and deployment type.
- Affected database endpoint.
- Connected clients, rejected clients, connection rate, CPU, and latency graphs.
- Proxy and Redis logs for the window.
- Client library, version, pool settings, retry settings, and deployment batch size.
- Infrastructure limits such as file descriptors, pod/process counts, and autoscaling events.
