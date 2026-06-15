---
name: redis-cloud-failover-test
description: "Plan, schedule, and validate Redis Cloud failover tests. Use when the user asks to run a Redis Cloud shard failover, node failure test, disaster recovery drill, go-live HA test, endpoint rebind test, RTO/RPO validation, client reconnect testing, DNS TTL troubleshooting, support-scheduled failover, or Pro-plan failover test with Redis Support and customer chat-room presence."
---

# Redis Cloud Failover Test

Use this skill when a user needs to validate application behavior during Redis Cloud failover or disaster recovery.

## Safety Rules

- Redis Cloud failover tests are coordinated with Redis Support; do not present them as arbitrary self-serve commands.
- Prefer staging or QA before production.
- Confirm HA replication before shard or node failover tests.
- Confirm persistence/backups before DR drills.
- Keep customer technical staff present during the test window.
- Use UTC for scheduling.

## Test Types

| Test | Purpose | Requirements | Expected impact |
| --- | --- | --- | --- |
| Shard failover | Validate shard migration without endpoint rebind. | Replication enabled. | Elevated latency, usually low disruption. |
| Node failure test | Validate behavior when a node fails and endpoints rebind. | Replication enabled. | Temporary disconnects and reconnects. |
| Full-cluster DR drill | Validate recovery from persistence/backup. | Persistence/backups enabled. | Longer outage; plan multi-hour window. |

Verify current plan eligibility and scheduling rules with Redis Support. Historically, these tests require Pro plans and advance scheduling.

## Pre-Test Checklist

1. Confirm database IDs, names, endpoints, regions, and environment.
2. Confirm replication/HA status.
3. Confirm persistence and backup status for DR tests.
4. Confirm test type and UTC time window.
5. Confirm applications use hostnames, not static IPs.
6. Review DNS caching behavior, especially Java/JVM DNS cache settings.
7. Confirm client retry, reconnect, timeout, and backoff behavior.
8. Ensure a representative workload runs during the test.
9. Prepare application, Redis Cloud, and infrastructure dashboards.
10. Open a Redis Support ticket with requested details.

## Support Request Details

Provide:

- Redis Cloud account and subscription IDs.
- Database IDs and endpoints.
- Environment: staging, production, or go-live validation.
- Requested test type: shard failover, node failure, or DR drill.
- Preferred UTC windows.
- Business impact and success criteria.
- Customer contacts who will join the test chat.
- Any co-resident database concerns for node tests.

## During the Test

Monitor:

- Application disconnect/reconnect logs.
- p95/p99 latency.
- Error and timeout rates.
- Recovery time against RTO.
- Data consistency and write success.
- Redis Cloud database metrics.

Keep traffic active; idle connections do not prove application resilience.

## Client Readiness

| Issue | Fix |
| --- | --- |
| App does not reconnect | Add retry and reconnect logic with exponential backoff. |
| DNS cached too long | Lower client/runtime DNS TTL; for Java, review `networkaddress.cache.ttl`. |
| Failover feels slow | Use sensible connect/socket timeouts, often low seconds. |
| Static IPs used | Switch to Redis Cloud endpoint hostnames. |
| Old client library bugs | Upgrade Lettuce, Jedis, Redisson, or other clients. |
| Retry storm | Add jitter, backoff, and circuit-breaking. |

## Post-Test Validation

Confirm:

- Redis Support reports test completion.
- Application traffic resumes normally.
- Latency and errors return to baseline.
- RTO/RPO expectations were met or gaps were documented.
- Logs and metrics are saved for the runbook.
- Follow-up client or architecture changes are tracked.

## Escalation Packet

Collect:

- Test type and scheduled UTC window.
- Database IDs, endpoints, and regions.
- HA, persistence, and backup status.
- Application client libraries and timeout/retry settings.
- Metrics before, during, and after failover.
- Application errors and reconnect evidence.
- RTO/RPO results.
- Redis Support ticket number.
