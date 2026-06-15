---
name: redis-software-distributed-system-triage
description: Use when Redis Software has broad distributed-system symptoms across nodes, shards, endpoints, clients, CRDB sync, latency, failover, shard imbalance, node failures, endpoint flapping, split-brain risk, clock drift, resource pressure, or inter-node communication, and the agent needs a structured triage workflow before routing to a specific Redis Software recovery or performance skill.
---

# Redis Software Distributed System Triage

Use this skill for broad Redis Software incidents where the failure could span cluster health, node resources, networking, shard placement, endpoints, clients, or CRDB replication.

## Triage Order

1. Capture current cluster state before changes.
2. Check node OS health and time synchronization.
3. Review logs around the symptom window.
4. Classify the issue type.
5. Route to the specific troubleshooting or recovery skill.

## Baseline Commands

```bash
rladmin status
rladmin status shards
rladmin status issues_only
rladmin status extra all
supervisorctl status
rlcheck
```

Node-level checks:

```bash
df -h
free -m
top
timedatectl
```

Confirm swap policy, disk headroom, time sync, CPU, memory, and service status before making database-level changes.

## Logs To Correlate

Review logs under `/var/opt/redislabs/log/`:

- `event_log.log`: failovers, endpoint changes, CPU, latency, cluster events
- `cluster_wd.log`: watchdog state, node failures, disconnects
- `dmcproxy.log`: proxy negotiation, certificate, connection errors
- `cnm_exec.log`: shard movement, migrations, failovers
- shard logs such as `redis-<id>.log`: command and shard-level errors

Line up log timestamps with monitoring spikes, application errors, and recent changes.

## Issue Classifier

| Symptom family | First checks | Route |
| --- | --- | --- |
| Node missing, unreachable, or not OK | `rladmin status`, OS checks, `supervisorctl`, network reachability | `redis-software-unreachable-node-recovery` |
| Inter-node communication or `verify_tcp_connectivity` | `rlcheck`, failed source/destination ports, firewall/routing | `redis-software-node-tcp-connectivity` |
| Endpoint moves, missing endpoints, DNS churn | endpoint status, DNS, client resolution | `redis-software-endpoint-flapping` |
| Latency or timeouts | slowlog, CPU/RAM, hot keys, client storms, blocking commands | hot-key, reconnect, large-key, or performance skills |
| CRDB lag or stale state | CRDB health report, syncer logs, inter-cluster TLS/DNS | `redis-crdb-unreachable-participants` or `redis-crdb-sync-failures-after-events` |
| Shard imbalance | shard size, operations/sec, hot keys, hash tags | `redis-hot-key-shard-imbalance` or `redis-software-resharding` |
| Split-brain or maintenance fallout | quorum, nodes offline, incomplete maintenance, partitions | `redis-software-node-maintenance-split-brain` |
| Storage or persistence symptoms | disk full, AOF/RDB issues, mount instability | `redis-software-supported-storage` |

## Distributed Sync Considerations

For Active-Active or Replica Of databases, verify the configured syncer mode and current Redis Software support before changing it. Some source guidance mentions distributed syncer mode as default for newer databases in certain Redis Enterprise versions; treat exact version behavior as release-specific.

Do not tune syncer mode, proxy policy, or replication settings until connectivity, TLS, and local database health are known.

## Diagnostic Bundle Guidance

When the issue is broad or unclear, collect a full cluster diagnostic bundle and node-level diagnostics if cluster collection misses affected nodes. Preserve evidence before service restarts, node replacement, forced CRDB updates, or shard movement.

## Escalation Packet

Collect:

- symptom timeline and recent changes
- baseline command outputs
- node OS health outputs
- relevant log snippets with timestamps
- monitoring graphs for latency, memory, CPU, connections, replication lag, and disk
- affected databases, shards, endpoints, and clients
- CRDB topology if Active-Active is involved
- any maintenance, failover, upgrade, network, storage, or certificate changes
