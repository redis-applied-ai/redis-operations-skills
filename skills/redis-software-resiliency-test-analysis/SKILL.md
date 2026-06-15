---
name: redis-software-resiliency-test-analysis
description: Use when analyzing Redis Software resiliency or failover tests, including node, shard, or network failure simulations, rladmin status review, shard promotion validation, replication-link events, endpoint movement, client reconnect behavior, support packages, memtier benchmarks, or post-test performance drops.
---

# Redis Software Resiliency Test Analysis

Use this skill after a Redis Software failover or resiliency test to determine whether the cluster, databases, endpoints, and clients recovered correctly.

## Evidence To Collect

Capture the test timeline and baseline:

- failure type: node, shard, process, network, zone, rack, or manual failover
- exact start and end time of the test
- database name, shard count, replication setting, and placement policy
- client endpoint used by applications
- application error, timeout, retry, and reconnect logs
- pre-test, during-test, and post-test latency and throughput

Run:

```text
rladmin status
rladmin status shards
rladmin status issues_only
rladmin status database
```

Review logs under `/var/opt/redislabs/log/` for replication changes, failover events, endpoint movement, shard transitions, and latency anomalies.

## Validation Workflow

1. Confirm cluster state returns to Optimal.
2. Confirm every expected node and shard is present and healthy.
3. Confirm replica promotion occurred when expected.
4. Confirm endpoints point to healthy serving shards and clients use endpoints rather than static shard or node IPs.
5. Confirm application clients reconnected automatically and resumed reads/writes.
6. Compare p95/p99 latency, throughput, client connections, replication lag, CPU, memory, swap, and disk I/O before, during, and after the test.
7. Run a representative smoke test or benchmark to confirm normal behavior.

## Common Findings

- Replica did not promote: inspect failure-domain placement, dense versus sparse placement, and whether replica and primary were exposed to the same failure.
- Data unavailable after test: check unresolved `rladmin status issues_only`, node state, Redis processes, endpoints, and client connection targets.
- Performance drop during recovery: inspect memory headroom, slow commands, CPU, swap, disk I/O, and replication backlog.
- Client did not reconnect: verify DNS-based endpoint usage, client library support, retry policy, timeouts, and connection pool behavior.
- Manual recovery needed: stop and use version-appropriate Redis Software recovery guidance; gather a support package before high-risk recovery actions where possible.

## Benchmarks And Metrics

Use `memtier_benchmark` or the application's normal load test to compare:

- steady-state latency before the event
- impact during failover
- recovery time
- post-test latency and throughput
- error and timeout rate

Use Redis Insight, Prometheus/Grafana, Datadog, or equivalent monitoring to correlate failover events with client-visible impact.

## Escalation Package

For deeper review, collect:

- support package from the Admin Console
- `rladmin` command outputs
- logs from the test window
- monitoring graphs for node health, replication lag, memory, CPU, network, and client connections
- application reconnect logs
- a timeline of every manual action taken

## Response Pattern

Answer with:

1. Whether failover succeeded at cluster, database, endpoint, and client layers.
2. The evidence that supports that conclusion.
3. Any placement, client, or resource issue discovered.
4. Specific remediation and a repeat-test validation plan.
