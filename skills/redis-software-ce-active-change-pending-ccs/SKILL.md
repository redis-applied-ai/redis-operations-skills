---
name: redis-software-ce-active-change-pending-ccs
description: "Recover Redis Software Community Edition databases stuck in `active-change-pending` with `CCS ERROR: DOWN` or `CCS ERROR: TIMEOUT`. Use when `rladmin status extra all` shows CCS errors, state machines such as `SMStandaloneRedisMigrate` or `SMRedisFailover`, shard startup failures, stale info, or when deciding whether to run `rlutil retry_bdb`, `rlutil reset_bdb_sm`, or `redis_ctl start/restart/force-start`."
---

# Redis Software CE Active Change Pending CCS

Use this skill when a Redis Software Community Edition database is stuck in `active-change-pending`, especially with node-level CCS errors.

## Critical Safety Rule

Do not run `rlutil retry_bdb`, `rlutil reset_bdb_sm`, or shard force-start commands until the underlying node, CCS, storage, network, and shard health issues are understood and fixed.

If CCS files, persistent directories, or shard files are missing, stop and escalate. Do not manually rebuild or copy CCS data unless Redis Support directs it.

## Initial Status

Run:

```bash
rladmin status extra all
```

Look for:

- Nodes with `CCS ERROR: DOWN` or `CCS ERROR: TIMEOUT`.
- Databases in `active-change-pending`.
- `EXEC_STATE` or `EXEC_STATE_MACHINE` values such as migration, failover, maintenance, or shard start state machines.
- Shards in `ERROR`, `TIMEOUT`, `REPLICATION LINK DOWN`, `stale info`, or `missing`.

## Recovery Sequence

1. Fix node and CCS health first.
2. Fix storage/mount/permissions/network blockers.
3. Confirm shard files are present and shards can start.
4. Restart or start affected shards only after the root cause is fixed.
5. Retry or reset the database state machine only when nodes and shards are healthy.
6. Verify the database returns to `active`.

## Node / CCS Checks

Investigate recent changes:

- Reboot or OS patching.
- Storage mount changes.
- Firewall or network changes.
- SELinux or OS hardening.
- Redis Software service failures.

Check for:

- Missing persistent mounts.
- Missing CCS directories/files.
- Blocked cluster ports.
- Failed services.
- Permissions or ownership changes.

If `CCS ERROR` remains, do not proceed with database recovery commands.

## Shard Checks

Check shard status:

```bash
redis_ctl status <shard-id>
```

After the root cause is fixed, use the least forceful action needed:

```bash
redis_ctl restart <shard-id>
redis_ctl start <shard-id>
```

Use only with clear impact understanding:

```bash
redis_ctl force-start <shard-id>
```

## Database State Machine Actions

Retry the original operation when it should continue:

```bash
rlutil retry_bdb bdb=<database-id>
```

Reset a stuck state machine when nodes and shards are healthy but the database remains stuck:

```bash
rlutil reset_bdb_sm bdb=<database-id>
```

Some versions may expect:

```bash
rlutil reset_bdb_sm uid=<database-id>
```

Use `resume=yes` only when Redis Support or a validated runbook confirms the operation should resume immediately.

## Verification

Run:

```bash
rladmin status extra all
```

Confirm:

- No nodes show CCS errors.
- Database is `active`.
- State machine fields are `N/A` or clear.
- Shards are healthy.
- Application traffic is healthy.

## Troubleshooting

| Symptom | Meaning | Action |
| --- | --- | --- |
| `retry_bdb` does not clear state | Original blocker still exists or retry is wrong action | Recheck node/shard health; use reset only if healthy. |
| `reset_bdb_sm` clears state but shard unhealthy | State machine was not root cause | Troubleshoot shard startup, storage, permissions, SELinux, network. |
| CCS error returns after reboot | Persistent storage, CCS startup, or firewall issue | Fix node/platform issue before retrying DB recovery. |
| Issue began during maintenance | Patch/reboot/storage/network change caused blocker | Stop further maintenance and restore node health. |
| Kubernetes deployment | Host-based procedure may not apply | Use Redis Enterprise for Kubernetes troubleshooting instead. |

## Escalate To Support When

- CCS files or persistent directories are missing.
- Required shard files are missing.
- A node remains in CCS error after storage/network checks.
- Active-Active or Replica Of is involved.
- Multiple nodes show stale info, timeouts, or connection resets.
- You are unsure whether retry or reset is safe.

Collect `rladmin status extra all`, affected database ID, shard IDs, recent change history, and a fresh support package.
