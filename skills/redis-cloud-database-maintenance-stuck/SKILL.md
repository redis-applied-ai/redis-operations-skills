---
name: redis-cloud-database-maintenance-stuck
description: Use when a Redis Cloud database appears stuck in Maintenance, Modifying, Pending, Updating, or another long-running managed operation state, especially after planned maintenance, version upgrade, resize, shard change, failover, import, backup, network change, or when Console and client behavior disagree about database availability.
---

# Redis Cloud Database Maintenance Stuck

Use this skill to triage Redis Cloud databases that appear stuck in a maintenance or background-operation state. Redis Cloud maintenance is managed service state, so prioritize live Console/API evidence, customer impact, and escalation quality over speculative fixes.

## Safety Rules

- Do not advise deleting, recreating, resizing, or force-changing the database unless the user accepts the data and downtime impact.
- Do not promise that maintenance can be cancelled, skipped, or manually cleared without Redis Support confirmation.
- Verify live Redis Cloud Console/API state and the Redis status page before treating the issue as a product incident.
- Preserve timestamps and screenshots before retrying user-initiated operations.

## First Questions

Collect:

- account, subscription, database name or ID, region, plan, and cloud provider
- current status text in Redis Cloud Console
- when the status first changed and how long it has remained unchanged
- whether clients can still connect and whether reads/writes succeed
- planned maintenance notice, version upgrade, resize, import, backup, clustering, failover, or networking change around the same time
- whether the same state appears in Redis Cloud API output, if the user can query it

## Classify The Situation

| Situation | Evidence | Response |
| --- | --- | --- |
| Planned maintenance still within window | notice exists; database status changed at scheduled time | monitor impact and wait for window to finish |
| Background operation in progress | recent resize, version update, backup, import, shard, or network change | avoid starting another operation; monitor progress |
| Console stale but database works | clients succeed; metrics normal; API status differs | refresh session, compare browser/API, collect evidence |
| Database unavailable | clients fail; endpoint or metrics unhealthy | treat as service-impacting; escalate with timeline |
| Status exceeded expected window | no progress after maintenance or operation should have ended | open Support case with artifacts |
| Multiple databases affected | subscription, region, or provider pattern | check Redis status page and status of peer databases |

## Checks

Use the Redis Cloud Console as the first source of truth:

- database status and Activity or Events tab
- subscription maintenance-window settings
- recent notifications or maintenance emails
- database metrics around the state transition
- backup/import/export status if relevant
- network connectivity status for private endpoints or peering if clients fail

If API access is available, compare Console status with current API output using the official Redis Cloud API for the account and resource. Do not rely on cached screenshots alone.

## Client Impact Test

From a representative application network path:

```bash
redis-cli -h <endpoint-host> -p <port> --tls PING
```

Adapt TLS, username, password, and CA flags to the database configuration without exposing credentials.

Interpretation:

- `PONG`: data path may be healthy; focus on stuck control-plane status or background operation.
- timeout or connection refused: check maintenance notice, endpoint health, private networking, and status page.
- auth or TLS error: route to the relevant Redis Cloud authentication or TLS connection skill.

## What Not To Do

- Do not retry the same resize, clustering, version update, or network operation repeatedly.
- Do not delete the database to clear a status unless the user has a verified backup/export and accepts a rebuild.
- Do not assume a stuck UI label means data is unavailable; test from the data path.
- Do not assume successful data-path PING means the control-plane operation is safe to ignore.

## Escalation Packet

For Redis Support, collect:

- account, subscription, database ID, region, and plan
- current status text and screenshot
- operation that preceded the stuck state
- exact start time, maintenance-window notice, and elapsed time
- client impact and sample error text
- Redis Cloud API status if available
- metrics screenshots for connections, throughput, latency, CPU, memory, and replication or failover signals
- whether other databases in the same subscription or region are affected

## Response Shape

When answering, provide:

1. Whether the issue looks like planned maintenance, background operation, stale Console state, or service-impacting failure.
2. The next live status check.
3. Whether the data path is healthy.
4. What operations to avoid while the state is unresolved.
5. The exact evidence to send to Redis Support if escalation is needed.
