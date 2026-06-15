---
name: redis-software-cluster-failure-diagnostics
description: Use when identifying Redis Software cluster failures before recovery, including node or shard errors, cluster warnings, Redis Admin UI yellow or red states, Prometheus or Grafana anomalies, Redis Insight performance bottlenecks, `rladmin status extra all`, `rlcheck`, `supervisorctl`, Redis logs, OS resource checks, DNS checks, support diagnostic bundles, or deciding which deeper recovery skill to use.
---

# Redis Software Cluster Failure Diagnostics

Use this skill to gather evidence for Redis Software cluster failures before recommending recovery actions.

## Diagnostic Order

1. Establish scope: cluster, node, shard, endpoint, database, client, or infrastructure.
2. Capture current cluster state with read-only commands.
3. Correlate monitoring, logs, and OS resource symptoms.
4. Decide whether to route to node recovery, database recovery, networking, storage, client, or performance skills.
5. Preserve evidence before disruptive recovery actions.

## Cluster And Database State

Run:

```bash
rladmin status extra all
rladmin status extra all errors_only
rladmin status shards
rladmin status database
rlcheck
```

Record:

- nodes not `OK`, missing, unreachable, or in maintenance
- shards in error, stale, syncing, or missing state
- endpoint placement and database status
- active alerts or warning/error indicators in Cluster Manager
- recent event-log entries

## Process And Service Checks

On affected nodes:

```bash
supervisorctl status
```

Check whether Redis Enterprise management services, proxies, shards, or watchdog processes are stopped or restarting.

## OS And Infrastructure Checks

Use node-level tools:

```bash
df -h
free -m
top
dig <cluster-fqdn>
```

Check:

- disk full or near-full
- memory pressure and swap
- CPU saturation or high load
- DNS resolution problems
- recent firewall, route, storage, or OS changes

## Monitoring Sources

Use Prometheus/Grafana, Redis Insight, and the Admin UI together:

- Prometheus/Grafana: latency, throughput, memory, CPU, disk, network, errors, replication lag.
- Redis Insight: command patterns, slow operations, memory analysis, client behavior.
- Admin UI: node/database status, warnings, errors, and log/event views.

Do not rely on a single tool if symptoms cross node, database, and client layers.

## Log Files

Review logs under `/var/opt/redislabs/log/`, especially:

- `event_log.log`
- `cluster_wd.log`
- `supervisord.log`
- `dmcproxy.log`
- `resource_mgr.log`
- shard logs such as `redis-<id>.log`

Correlate log timestamps with monitoring spikes and user-visible errors.

## Routing

| Evidence | Next skill |
| --- | --- |
| Node unreachable or not `OK` | `redis-software-unreachable-node-recovery` |
| Cluster or database recovery needed | `redis-software-recovery` |
| Storage errors, mount problems, AOF/RDB issues | `redis-software-supported-storage` |
| Endpoint flapping | `redis-software-endpoint-flapping` |
| Split-brain after maintenance | `redis-software-node-maintenance-split-brain` |
| Resiliency test aftermath | `redis-software-resiliency-test-analysis` |
| Client reconnect surge | `redis-reconnect-storms` |

## Escalation Packet

Collect:

- failure timeline and first symptom
- `rladmin status extra all` and `errors_only`
- `rlcheck` output
- `supervisorctl status` from affected nodes
- relevant log snippets with timestamps
- Prometheus/Grafana or Redis Insight graphs around the incident
- OS resource output for affected nodes
- recent changes: upgrades, patching, network, firewall, storage, DNS, certificates, or client deploys
- diagnostic bundle if the issue remains unclear or support escalation is likely
