---
name: redis-cloud-throughput-sizing-decision
description: Use when Redis Cloud latency, throttling, ops/sec utilization, throughput warnings, SLOWLOG output, request-size issues, Free or Essentials plan caps, Pro throughput sizing, Redis Billing Unit impact, or upgrade decisions require choosing between optimizing workload, increasing throughput, or changing subscription type.
---

# Redis Cloud Throughput Sizing Decision

Use this skill to decide whether a Redis Cloud performance problem should be handled by optimizing commands, increasing configured throughput, or moving to a plan with more control. Verify current Redis Cloud plan limits and pricing before quoting specific caps or costs.

## Evidence To Gather

Ask for or inspect:

- current plan type and database tier
- current throughput utilization and configured ops/sec
- p50, p95, and p99 latency during normal and peak load
- average and peak request payload size
- command mix and slow commands
- client connection count and connection churn
- TLS, replication, persistence, and clustering settings
- CPU, memory, network usage, and throttling or timeout signals

Use `SLOWLOG` and Redis Insight when available:

```text
SLOWLOG GET 128
```

For key-shape and access-skew checks, use production-safe sampling windows and avoid running expensive scans during peak load:

```text
redis-cli --bigkeys
redis-cli --hotkeys
CLIENT LIST
```

## Decision Flow

1. Identify the bottleneck before changing capacity.
2. Optimize first when heavy commands, large payloads, avoidable round trips, or connection churn are visible.
3. Increase throughput when the workload is efficient but sustained demand exceeds the current paid-plan throughput setting.
4. Change subscription type when the current plan cannot provide the required throughput, networking, observability, or scaling controls.
5. Validate each change under realistic load before making further changes.

## Undersized Database Signals

Treat the database as likely undersized when several of these line up during normal peak traffic:

- ops/sec is sustained near the configured throughput ceiling
- p95 or p99 latency rises as ops/sec approaches the limit
- timeouts, throttling, or retry storms appear during expected traffic
- average payload size is large enough that nominal ops/sec no longer reflects real work
- slowlog shows repeated complex commands such as broad range reads, multi-key fan-out, Lua, or module queries
- hot keys or large keys concentrate work on a small part of the database
- connection count is too low for concurrency or too high because clients churn connections

Do not call the database undersized based on a single short spike if latency, errors, CPU, and retry behavior remain healthy.

## Optimize First

Recommend optimization when:

- slow commands dominate latency
- payloads are large
- clients issue many single round trips that could be pipelined
- connection churn is high
- the application scans, deletes, or fetches more data than needed

Actions:

- simplify expensive commands and reduce returned fields
- use pipelining or batching where safe
- reduce payload size and large value churn
- split or redesign hot keys and large composite values
- use `UNLINK` for large deletes
- tune client pooling and retry behavior
- remove accidental hot-key or fan-out patterns

## Increase Throughput

Recommend increasing throughput when:

- the command mix is already reasonable
- latency rises as utilization approaches the configured throughput
- the plan supports throughput changes
- the user can validate cost and performance impact

For Pro-style configurable databases, increase throughput incrementally and watch latency, CPU, and network metrics. For tiered plans, verify the current tier's limits and available upgrade path in the Redis Cloud Console.

Apply moderate increases, validate with the same workload, and stop if latency no longer improves; the remaining bottleneck may be command shape, hot keys, memory pressure, client pooling, or network distance.

## Change Plan Or Subscription Type

Recommend a plan change when:

- the current plan has a fixed throughput ceiling that sustained workload demand exceeds
- private networking, per-database observability, multiple databases, or advanced scaling controls are required
- warnings are structural rather than occasional traffic bursts

Make endpoint, migration, and billing impact explicit. Essentials-to-Pro moves should be treated as a database migration and cutover, not an in-place performance toggle.

For Essentials-style fixed tiers, the usual path is workload optimization or tier/plan upgrade. For Pro-style configurable databases, the usual path is incremental throughput increase after optimization checks.

## Validation

After optimization or capacity changes:

- rerun the same benchmark workload
- compare latency percentiles, throughput, CPU, memory, and network usage
- check slow commands again
- confirm application timeout and error rates improved
- set alerts for renewed utilization pressure or regressions
- confirm connection count and retry rate did not increase after the change

## Response Pattern

Answer with:

1. The likely bottleneck and the evidence behind it.
2. The chosen path: optimize, increase throughput, or change plan.
3. The first concrete action.
4. What to measure after the change.
5. Cost, migration, or endpoint caveats if the path changes plan type.
