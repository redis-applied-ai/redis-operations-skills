---
name: redis-software-replication-link-down
description: Use when Redis Software or Redis Enterprise Software reports Replication Link Down, replica shard cannot sync from primary, replication lag grows, replica sync repeatedly fails, failover is stuck, shard placement looks wrong after reboot, output buffers overflow, TLS or node network issues affect shard replication, or you must distinguish database HA replication from Active-Active CRDB sync failures.
---

# Redis Software Replication Link Down

Use this skill to triage Redis Software replication link failures safely. First determine whether the problem is database HA shard replication inside one cluster or an Active-Active CRDB sync problem, then collect evidence and fix infrastructure or workload causes before attempting recovery.

## Safety Rules

- Capture cluster state and logs before restarting shards, moving nodes, or changing database settings.
- Do not prescribe low-level CCS/state-machine edits, `rlutil` resets, or undocumented shard control commands as customer-facing steps.
- Avoid rebooting paired nodes or multiple replica-bearing nodes together.
- Do not remove persistence files, shard configs, or orphaned processes until placement and data-safety impact are understood.
- Escalate to Redis Support when state-machine cleanup, ghost shard correction, or missing persistence files appear involved.

## Classify The Replication Type

Ask or inspect:

- database name and ID
- affected shard IDs and node IDs
- whether this is local database HA replication or Active-Active CRDB replication
- whether the alert started after node maintenance, reboot, upgrade, network change, TLS change, or load spike
- whether replicas were enabled and healthy before the incident

If the issue is Active-Active CRDB-wide sync between clusters, use a CRDB sync skill after collecting initial evidence. If it is a replica shard inside one Redis Software cluster, continue here.

## First Evidence

```bash
rladmin status issues_only
rladmin status extra all
rladmin status databases
rladmin status shards
```

Collect time-aligned logs from affected nodes:

```bash
ls -ltr /var/opt/redislabs/log/
grep -iE "replication|sync|link|buffer|tls|certificate|failover|state" /var/opt/redislabs/log/*.log
```

Preserve:

- affected database, shard, primary, replica, and node IDs
- timestamps of first link-down alert and recent maintenance
- replication lag and whether it is increasing or decreasing
- node CPU, memory, disk, swap, and network saturation
- persistence mode and recent backup/AOF/RDB availability

## Root Cause Tracks

### Network, DNS, Firewall, Or TLS

Suspect this when multiple replica links fail across nodes or logs show connection, handshake, certificate, or timeout errors.

Check:

- node-to-node reachability and required Redis Software ports
- DNS and hostname resolution between nodes
- firewall or security group changes
- certificate expiration, trust chain, and internode TLS configuration
- clock skew and time synchronization

Fix the underlying node communication issue, then watch whether replication catches up without disruptive shard action.

### Resource Pressure

Suspect this when the replica OOMs, disk fills, full sync cannot complete, or replication repeatedly drops during high write load.

Check:

- shard and node memory headroom
- disk free space on persistence paths
- swap usage and disk I/O wait
- CPU saturation and network throughput
- eviction and fragmentation indicators

Stabilize resources before retrying recovery. Add capacity, rebalance shards, reduce ingestion bursts, or move workloads away from saturated nodes.

### Replication Buffer Exhaustion

Suspect this when replication works at low load but drops during write bursts, big-key updates, or hot-key traffic.

Actions:

- identify large keys and hot keys
- reduce burst writes and oversized pipeline batches
- consider increasing the database replica buffer only after confirming the database has memory headroom

Example:

```bash
rladmin tune db <db-name-or-id> slave_buffer <megabytes>
```

Validate the setting in a maintenance-aware change plan; an oversized buffer can increase memory pressure.

### Maintenance Or Reboot Sequencing

Suspect this when the alert follows simultaneous reboots, forced node termination, or node patching.

Check:

- whether primary and replica shards for the same database were affected together
- whether maintenance mode was used
- whether shard placement now differs from expected layout
- whether any shards appear duplicated, missing, or bound to unexpected nodes

If ghost processes, duplicated shards, or misplaced configs are suspected, stop and escalate with the collected state. Do not manually clean files or processes without a support-approved plan.

### State Machine Or Failover Stuck

Suspect this when `rladmin status` shows persistent active-change, failover, or replication actions that do not progress after infrastructure is stable.

Collect:

```bash
rladmin cluster running_actions
rladmin status issues_only
rladmin status extra all
```

Escalate rather than running undocumented reset or retry commands. Include the action name, affected database ID, and logs around the first failure.

## Recovery Decision

Before suggesting any restart or failover action, confirm:

- current primary and replica placement
- persistence files or backups exist when needed
- no node-level resource shortage remains
- internode network and TLS are healthy
- the database is not in the middle of another cluster action

Prefer non-disruptive fixes first: restore connectivity, add capacity, reduce write bursts, and let replication catch up.

## Validation

```bash
rladmin status issues_only
rladmin status extra all
rladmin status shards
```

Confirm:

- replication-link-down issue clears
- replica sync progresses and lag decreases
- failover or active-change actions complete
- no new OOM, disk, TLS, or network errors appear in logs
- application latency and error rates return to baseline

## Escalate When

- replication remains down after network, TLS, and resources are fixed
- persistence files are missing, corrupt, or inconsistent
- shards appear duplicated, misplaced, or orphaned after reboot
- state-machine actions are stuck
- Active-Active CRDB participants are stale or divergent
- data loss or manual shard recovery is possible

Attach a support package or equivalent diagnostics, plus the affected database/shard/node IDs and incident timeline.
