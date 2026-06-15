---
name: redis-sidekiq-cloud-pro-crossslot-migration
description: "Plan and troubleshoot Sidekiq migration from Heroku Redis to Redis Cloud Pro without CROSSSLOT, MOVED, ASK, or worker-stall failures. Use when Sidekiq workers stop after migration, Redis Cloud Pro introduces sharded behavior, multi-key queue operations fail, app components use different Redis endpoints, or the user needs staging, cutover, rollback, and validation guidance for Ruby background jobs."
---

# Redis Sidekiq Cloud Pro CROSSSLOT Migration

Use this skill when migrating a Sidekiq workload from Heroku Redis or another single-node-like Redis service to Redis Cloud Pro.

## Core Risk

Many Sidekiq deployments assume single-node Redis behavior. If the target Redis Cloud Pro database exposes sharded or cluster-style multi-key behavior, commands touching keys in different hash slots can fail with `CROSSSLOT Keys in request don't hash to the same slot`.

Do not treat `CROSSSLOT`, `MOVED`, or `ASK` as generic connection noise. They indicate a target behavior or client compatibility mismatch.

## Preflight Review

1. Inventory Redis usage:
   - Sidekiq queues and whether workers listen to multiple queues.
   - Scheduled jobs and retries.
   - Sidekiq plugins.
   - Application Redis use beyond Sidekiq, such as cache, locks, counters, or custom sets.
   - Direct use of multi-key commands such as `MGET`, `MSET`, `SUNION`, `SDIFF`, or Lua scripts touching multiple keys.
2. Confirm current Heroku Redis behavior and connection settings.
3. Confirm target Redis Cloud Pro database behavior:
   - Whether it behaves like the current single endpoint for multi-key operations.
   - Whether cluster-aware client behavior or hash-slot restrictions are expected.
   - TLS, authentication, CIDR/private connectivity, and endpoint details.
4. Define rollback: previous Redis URL, restart procedure, and expected job consistency risk.

## Migration Approach

| Workload state | Safer approach |
| --- | --- |
| Sidekiq/app assumes single-node Redis | Choose a target configuration that preserves compatible behavior before changing application code. |
| App is known cluster-compatible | Validate hash-slot-safe key patterns and cluster-aware client behavior in staging. |
| Workers listen to many queues or use plugins | Simplify temporarily during migration; test plugins under the target behavior. |
| Production-only traffic patterns are suspected | Load test or replay representative workload before cutover. |

## Staging Validation

Before production:

1. Point staging web, workers, schedulers, and job producers at the target database.
2. Restart every component so no process keeps the old endpoint.
3. Exercise:
   - Job enqueue.
   - Job fetch and processing.
   - Retries.
   - Scheduled jobs.
   - Multiple queue configurations.
   - Custom Redis code paths.
4. Search logs for `CROSSSLOT`, `MOVED`, `ASK`, authentication, TLS, and reconnect errors.
5. Do not proceed if workers connect but do not process jobs.

## Cutover Workflow

1. Pick a maintenance window or lower-traffic period.
2. Pause or reduce new job creation when feasible.
3. Allow in-flight jobs to drain where appropriate.
4. Update Redis connection environment variables such as `REDIS_URL`.
5. Restart all components:
   - Web processes.
   - Sidekiq workers.
   - Schedulers.
   - One-off/background job runners.
6. Confirm all components log the new endpoint or environment version.
7. Enqueue and process test jobs.
8. Monitor queue latency, processed count, retries, worker concurrency, connection errors, and application error rate.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `CROSSSLOT Keys in request don't hash to the same slot` | Multi-key operation against sharded behavior | Use compatible target behavior, redesign key patterns, or ensure related keys share slots where supported. |
| Workers connect but stop processing | Queue operations fail after connection | Inspect Sidekiq logs for CROSSSLOT/redirection errors and simplify queue/plugin use. |
| Some processes work and others fail | Mixed endpoints or stale env vars | Restart all dynos/processes and verify runtime config. |
| `MOVED` or `ASK` errors | Client/target cluster behavior mismatch | Confirm client supports the target mode or use a compatible database configuration. |
| TLS/auth errors | Connection string mismatch | Verify `rediss://`, host, port, password, user, and certificate trust. |
| Only production fails | Higher-concurrency Redis path not covered in staging | Capture commands/logs under load and retest with representative traffic. |

## Escalation Packet

Collect:

- Heroku app name and current Redis add-on/source details.
- Redis Cloud Pro database ID and target behavior/configuration.
- Sidekiq version, Redis client gem version, and relevant plugins.
- `REDIS_URL` shape without secrets.
- Worker queue configuration and concurrency.
- Exact errors and timestamps.
- Whether all web, worker, and scheduler processes were restarted.
- Staging validation results and rollback status.
