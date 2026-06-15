---
name: redis-software-active-change-pending-ccs
description: "Recover Redis Enterprise Software databases stuck in `active-change-pending` with CCS errors, stuck state machines, shard migration/failover failures, stale shard info, duplicate shard ownership, or Kubernetes operator reconciliation conflicts. Use when `rladmin status extra all` shows `CCS ERROR: DOWN`, `CCS ERROR: TIMEOUT`, `EXEC_STATE_MACHINE`, `SMStandaloneRedisMigrate`, `SMRedisFailover`, `SMUpdateBDB`, `REPLICATION LINK DOWN`, or when deciding between `rlutil retry_bdb` and `rlutil reset_bdb_sm`."
---

# Redis Software Active Change Pending CCS

Use this skill when a Redis Enterprise Software database remains in `active-change-pending`, especially with CCS, node, shard, or state-machine errors.

## Safety Rule

Do not start with `rlutil` recovery commands. First determine whether the blocker is node health, CCS, network connectivity, storage, shard startup, Kubernetes reconciliation, or only a stuck control-plane state machine.

If production traffic is impacted, multiple nodes show CCS errors, shard files are missing, or persistence corruption is suspected, collect evidence and open Support early.

## Initial Diagnosis

Run:

```bash
rladmin status extra all
rladmin cluster running_actions
rladmin cluster status
```

Look for:

- `active-change-pending`.
- `CCS ERROR: DOWN` or `CCS ERROR: TIMEOUT`.
- `EXEC_STATE`, `EXEC_STATE_MACHINE`, `RETRYABLE ERROR`, or `FINAL ERROR`.
- State machines such as `SMStandaloneRedisMigrate`, `SMRedisFailover`, `SMUpdateBDB`, `SMRedisACL`, or `SMBindEndpoint`.
- Shard errors: stale info, missing info, duplicate placement, `REPLICATION LINK DOWN`, `LOADING`, or shard process not running.

## Root-Cause Branches

| Finding | First action |
| --- | --- |
| CCS error on a node | Verify host/pod reachability, Redis services, local CCS socket, storage, and recent patching/reboot. |
| CCS timeout | Check node-to-node communication, DNS, routing, firewalls, network policies, and cluster master load. |
| Shard missing/unavailable/duplicated | Investigate shard process, ownership, port use, persistence files, and replica/master relationship before state-machine reset. |
| Database pending but nodes/shards healthy | Treat as possible stuck state machine and consider retry/reset. |
| Kubernetes deployment | Verify REC/REDB desired state and operator logs before manual recovery. |
| Issue followed maintenance | Check storage remount, services, permissions, pre-stop hooks, and blocked ports. |

## Kubernetes / OpenShift Checks

If operator-managed:

- Confirm REDB/REC resources match intended state.
- Check operator logs and pod events.
- Confirm pods are not stuck `Terminating`, `Pending`, or blocked by pre-stop hooks.
- Confirm PVCs are attached and mounted.
- Correct the Kubernetes desired state before retrying database actions; otherwise the operator may revert manual fixes.

## State Machine Recovery

Use only after node, CCS, network, storage, and shard health are restored.

Retry the original operation when it should continue:

```bash
rlutil retry_bdb bdb=<db-id>
```

Reset the state machine when the operation should be cleared:

```bash
rlutil reset_bdb_sm bdb=<db-id>
```

Some environments use:

```bash
rlutil reset_bdb_sm uid=<db-id>
```

Stop if the same retryable/final error returns. Do not repeatedly reset without new evidence.

## Shard-Specific Cautions

- `info for shard not available` is usually a root problem, not a UI issue.
- Duplicate shard ownership requires identifying the valid holder and stale process/metadata before forcing changes.
- Repeated `LOADING` after heavy index deletion or persistence replay can require support-led persistence/restore decisions.
- Preserve persistence files for analysis before destructive recovery.

## Verification

After recovery:

```bash
rladmin status extra all
```

Confirm:

- Database is `active`.
- No node shows CCS errors.
- No shard shows stale, missing, duplicate, or replication-link-down state.
- State machine fields are clear.
- Endpoint watchdog and application traffic are healthy.

## Evidence Packet

Collect:

- Fresh support package for Redis Software.
- Kubernetes log collector and operator logs if applicable.
- `rladmin status extra all`.
- `rladmin cluster running_actions`.
- `rladmin cluster status`.
- Affected database ID and shard IDs.
- Incident start time and recent changes: maintenance, patching, master change, resize, migration, operator upgrade, TLS/cert change, firewall change, or heavy data operation.
- Logs before rotation if available.
