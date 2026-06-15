---
name: redis-cloud-essentials-network-limits
description: "Triage Redis Cloud Essentials bandwidth, ops/sec, connection, throttling, and subscription-limit issues. Use when the user sees high network usage, dropped connections, slow performance near plan limits, noisy databases sharing an Essentials subscription, missing per-database bandwidth visibility, or asks whether to isolate workloads, upgrade an Essentials plan, or move to Redis Cloud Pro."
---

# Redis Cloud Essentials Network Limits

Use this skill to diagnose Redis Cloud Essentials usage limits and guide workload isolation, plan changes, or Pro migration decisions.

## Limit Model

Redis Cloud Essentials enforces plan limits at the subscription level for bandwidth and throughput. Those shared limits apply across databases in the subscription. Connection limits are database-specific and normally cannot be raised inside the existing Essentials database.

Do not quote exact current quota, price, or plan-size values from memory. Verify them in the Redis Cloud Console or current Redis Cloud pricing/docs before giving a definitive number.

## Triage Workflow

1. Confirm the plan type is Redis Cloud Essentials.
2. Identify all databases in the affected subscription and which applications use them.
3. Check subscription usage in the Redis Cloud Console:
   - `Subscriptions -> Overview` for current-month bandwidth and aggregate throughput.
   - `Configuration` or alert settings for near-limit notifications.
4. Ask for symptoms:
   - Throttled or degraded performance.
   - Dropped operations.
   - Rejected clients or connection-limit errors.
   - Alert emails around usage thresholds.
5. Look for a noisy database:
   - Large value reads.
   - High-volume cache traffic.
   - Bulk scans or exports.
   - Repeated large JSON/document reads.
6. Decide whether to tune the application, split databases into separate subscriptions, resize/upgrade the Essentials plan, or migrate to Pro.

## Known Visibility Limits

Essentials console visibility is useful for subscription-level state but limited for deep diagnosis:

- No real-time per-database bandwidth breakdown.
- No egress versus ingress split.
- Limited historical trend detail.
- Limited external observability integration compared with Pro.

When exact per-database attribution is required, recommend application-side metrics, client telemetry, temporary workload isolation, or Pro-level observability.

## Remediation Matrix

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Bandwidth cap or throttling alerts | Shared subscription usage near limit | Reduce payloads, isolate the heavy database, resize/upgrade, or move workload to Pro. |
| Other databases slow down | One database consumes shared quota | Move noisy workload to its own subscription or Pro database. |
| Connection limit reached | Too many concurrent clients for one database | Add pooling, close idle clients, reduce connection fanout, or choose a plan/database shape with a higher supported limit. |
| Cannot identify the heavy database | Essentials visibility is subscription-level | Add client/app metrics or isolate suspected workloads to separate subscriptions. |
| Private networking is required | Essentials does not provide private VPC networking | Evaluate Redis Cloud Pro. |

## Application Tuning

Use these before or alongside plan changes:

- Batch operations and use pipelining for high-volume clients.
- Avoid `KEYS *` and unbounded range operations.
- Prefer incremental scans for discovery workflows.
- Reduce large value and large JSON payload sizes where possible.
- Avoid repeated full-object reads when field-level reads or caching are sufficient.
- Use `UNLINK` instead of `DEL` for large asynchronous deletions when appropriate.

## Migration Pattern

When a workload needs isolation or a different plan:

1. Create a new subscription sized for the workload.
2. Create a new database in that subscription.
3. Migrate data using supported Redis Cloud migration tooling, replication, or an application-specific migration plan.
4. Update application configuration to use the new endpoint.
5. Watch both old and new subscription usage during cutover.

## Pro Upgrade Signals

Recommend evaluating Redis Cloud Pro when the user needs:

- Private networking or VPC peering.
- Better observability and custom alerting.
- Isolation from other database workloads.
- Higher or more predictable throughput.
- Active-Active or other advanced deployment capabilities.
- Billing model where network egress is treated separately from Essentials quota behavior.
