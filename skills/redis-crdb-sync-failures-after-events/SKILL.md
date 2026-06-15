---
name: redis-crdb-sync-failures-after-events
description: Use when Redis Software Active-Active CRDB sync fails after Redis Software upgrades, disaster recovery drills, cluster reboots, participant re-creation, certificate rotation, mTLS changes, module/version drift, `crdb-cli crdb update --force`, `--update-db-config-modules true`, CRDB metadata drift, replication backlog recovery, or links remain disconnected even though databases appear healthy.
---

# Redis CRDB Sync Failures After Events

Use this skill when CRDB replication stops after a triggering event such as an upgrade, DR rebuild, reboot, certificate rotation, or participant re-creation.

## Core Rule

Do not repeatedly run forced CRDB updates before identifying the root cause. First determine whether the failure is caused by connectivity, version alignment, local database health, certificate trust, credentials, or CRDB metadata drift.

## Scenario Classifier

| Trigger | First check | Likely repair |
| --- | --- | --- |
| Redis Software upgrade | All participating clusters run compatible/same expected version. | Complete version alignment, then refresh DB config/modules if required. |
| Cluster reboot or restart | Local shards, databases, and running actions are healthy. | Refresh CRDB sync only after local recovery is complete. |
| DR participant re-created | Database version, modules, CRDB metadata, credentials, and endpoints match. | Update CRDB metadata and align local database config. |
| Certificate or mTLS change | CA chain, SAN/SNI, cert/key match, and trust across all clusters. | Fix certs and refresh CRDB config. |
| Link disconnected or health report hangs | Endpoint, DNS, firewall, TLS listener, and load balancer path. | Use `redis-crdb-unreachable-participants`. |

## Required Evidence

Collect:

```bash
crdb-cli crdb health-report --crdb-guid <CRDB_GUID>
rladmin status extra all
rladmin cluster running_actions
```

Also collect syncer/proxy logs, Redis Software version for every participant, CRDB GUID, database IDs, recent event timeline, and whether a full sync may be required.

## Version And Module Alignment

After upgrades:

1. Verify every participating cluster is on the intended Redis Software version.
2. Confirm local databases are healthy and not still upgrading or recovering.
3. If versions or modules differ, finish alignment before sync repair.
4. Refresh CRDB database configuration/modules only when alignment is correct:

   ```bash
   crdb-cli crdb update --crdb-guid <CRDB_GUID> --update-db-config-modules true
   ```

Do not use a module/version JSON copied from another environment. Build it from the actual target database requirements.

## Certificate Or mTLS Changes

When syncer logs show certificate mismatch, TLS handshake failure, expired certs, or SNI problems:

1. Verify certificates and trust chains across all participants.
2. Confirm endpoint hostname and certificate SAN/SNI expectations match.
3. Apply certificate updates through supported Redis Software methods.
4. Refresh CRDB configuration:

   ```bash
   crdb-cli crdb update --crdb-guid <CRDB_GUID> --force
   ```

## Restart Sync Safely

Only after the root cause is fixed, refresh synchronization with one supported path.

CLI path:

```bash
crdb-cli crdb update --crdb-guid <CRDB_GUID> --force
```

REST path, using secure secret handling:

```bash
curl -k -u <user>:<password> -X PUT \
  -H "Content-Type: application/json" \
  -d '{"sync":"enabled"}' \
  https://<host>:<port>/v1/bdbs/<database-id>
```

Do not paste real passwords into chat, shell history, tickets, or logs.

## DR Configuration Drift

For deleted/recreated participants:

- compare database version, module list, CRDB metadata, credentials, endpoint, and certificates against healthy participants
- update CRDB metadata with documented `crdb-cli crdb update` options using environment-specific values
- align the local database after metadata is correct
- avoid participant removal/re-add unless Support or the documented recovery path requires it

## Recovery Expectations

- Partial sync should recover faster.
- Full sync can consume significant cross-region bandwidth and take longer.
- Extended downtime may exhaust backlog and require heavier synchronization.
- Sync lag should trend down after links reconnect and root cause is fixed.

## Escalation Packet

Collect:

- CRDB GUID, database IDs, and participating cluster list
- Redis Software version for each cluster
- triggering event and timeline
- `crdb-cli crdb health-report`
- `rladmin status extra all`
- `rladmin cluster running_actions`
- syncer and proxy logs
- certificate, endpoint, module, version, and credential changes
- diagnostic bundles from all participating clusters when Support review is needed
