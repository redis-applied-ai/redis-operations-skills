---
name: redis-crdb-sync-stall-after-reboot
description: Use when Redis Software Active-Active CRDB remains syncing or stale after cluster reboot, UI sync status disagrees with `crdb-cli crdb health-report`, local syncer restart is being considered, syncer lag remains high after reboot, compression changes are needed for CRDB sync recovery, `crdb-cli coordinate crdb-list` shows config-version mismatch, state-machine or CCS errors appear after reboot, or diagnostic bundles are needed from all CRDB participant clusters.
---

# Redis CRDB Sync Stall After Reboot

Use this skill when a CRDB is stuck in syncing or stale state after a Redis Software cluster reboot or restart.

## Safety Rules

- Start with read-only health and state checks.
- Do not run `crdb-cli crdb update --force` if shards are unhealthy, state-machine errors exist, or config versions differ.
- Restart only the local syncer on the cluster where UI/status mismatch is observed, and only after CLI health checks support that action.
- Treat compression changes as operational changes; get approval and monitor lag before and after.
- Do not paste real admin passwords into chat, shell history, tickets, or logs.

## First Checks

Run:

```bash
rladmin status extra all
crdb-cli crdb health-report --crdb-guid <CRDB_GUID>
crdb-cli coordinate crdb-list
```

Review for:

- shards in `syncing`, `stale`, `STALE`, `DOWN`, or missing state
- CCS or state-machine errors
- health-report links disconnected or unhealthy
- `VERSION` mismatch across participating CRDB instances
- UI showing stale status while CLI health appears normal
- high syncer lag with otherwise clean health checks

## Decision Matrix

| Finding | Action |
| --- | --- |
| DNS, routing, or firewall issue | Fix connectivity first; use `redis-crdb-unreachable-participants` if needed. |
| Shard or state-machine errors | Stop; collect diagnostics from all participants and escalate. |
| CLI health report healthy but UI stale | Consider local syncer restart on the affected cluster only. |
| Config-version mismatch in `crdb-cli coordinate crdb-list` | Do not force-update; collect output and escalate. |
| High lag with clean health checks | Consider temporary compression disablement with approval and monitoring. |
| Syncer restart does not clear issue | Collect diagnostics from every participant and escalate. |

## Local Syncer Restart

Use only when the local cluster has a stale UI/status symptom but CLI health report shows healthy links.

Disable and re-enable local CRDB sync through the database REST API:

```bash
curl -vkLu <admin_user>:<admin_password> -X PUT \
  -H "Content-Type: application/json" \
  -d '{"crdt_sync":"disabled"}' \
  https://<FQDN>:9443/v1/bdbs/<uid>
```

```bash
curl -vkLu <admin_user>:<admin_password> -X PUT \
  -H "Content-Type: application/json" \
  -d '{"crdt_sync":"enabled"}' \
  https://<FQDN>:9443/v1/bdbs/<uid>
```

If running locally from the master node and appropriate for the environment, `<FQDN>` may be `localhost`.

## Compression Lag Test

Use only when network, DNS, shard health, and config versions are clean but syncer lag remains high.

Disable compression temporarily:

```bash
crdb-cli crdb update --crdb-guid <CRDB_GUID> --compression 0
```

Monitor lag and traffic. Restore the default compression level after stabilization:

```bash
crdb-cli crdb update --crdb-guid <CRDB_GUID> --compression 3
```

Do not leave compression changed without documenting why.

## Config-Version Mismatch

If `crdb-cli coordinate crdb-list` shows different `VERSION` values across participants:

- do not attempt to repair with `--force`
- capture the command output
- collect diagnostics from all participating clusters
- escalate for configuration consistency review

## Escalation Packet

Collect from every participating cluster:

- `rladmin status extra all`
- `crdb-cli crdb health-report --crdb-guid <CRDB_GUID>`
- `crdb-cli coordinate crdb-list`
- syncer and proxy logs
- timeline of reboot, restart, failover, or maintenance actions
- whether local syncer restart or compression changes were attempted
- diagnostic bundles from all participants

For large diagnostic archives, split them before upload using standard file-splitting tools if required by the upload path.
