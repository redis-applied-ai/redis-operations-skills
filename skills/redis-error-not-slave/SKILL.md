---
name: redis-error-not-slave
description: "Diagnose and resolve Redis Enterprise or Redis Cloud `ERROR: NOT SLAVE` shard role mismatches. Use when a user reports `ERROR: NOT SLAVE`, a replica shard acting as master, Redis process role disagreement with CCS/control-plane metadata, replication role errors after failover or upgrade, or stuck database state machine reconciliation."
---

# Redis ERROR NOT SLAVE

Use this skill to triage `ERROR: NOT SLAVE` by proving whether Redis process role and control-plane shard metadata disagree, then select the least invasive remediation.

## Safety Rules

- Treat role-changing commands as production-impacting. Confirm the target database, shard ID, intended topology, and maintenance window before advising execution.
- Before any manual `SLAVEOF`/enslave action, confirm the intended master is authoritative, writable, stable, and the source of truth. Wrong replication direction can overwrite good data.
- Use state-machine reset only as a last resort after confirming the DB state machine is stuck in FINAL ERROR and normal reconciliation cannot proceed.
- If writing customer-facing guidance, avoid exposing low-level repair tooling unless the user explicitly needs an authorized support or platform-operator runbook.

## Diagnosis

1. Identify product and scope: Redis Software, Redis Cloud, CRDB, replica-of, affected DB ID, shard ID, host, port, and recent failover, upgrade, maintenance, or infrastructure events.
2. Check the Redis process role:

   ```bash
   redis-cli -h <host> -p <port> INFO replication
   ```

   Capture `role`, `master_host`, `master_port`, and `master_link_status`.
3. Check shard/control-plane state:

   ```bash
   rladmin status shards
   rladmin status shards db <db-id>
   rladmin status extra all
   ```

   Look for `STATUS: ERROR: NOT SLAVE` and compare the expected shard role with the Redis process role.
4. Corroborate with logs around the first error timestamp. Look for promotions, failed syncs, state-machine transitions, restarts, network partitions, or orchestration actions.

## Remediation Decision Tree

Use the least invasive action that matches the evidence.

| Evidence | Action |
| --- | --- |
| Shard status shows `ERROR: NOT SLAVE` and topology says the shard should be a replica | Reconfigure then restart the shard: `rlutil redis_reconf redis=<SHARD_ID>`, then `rlutil redis_restart redis=<SHARD_ID> force=yes`. |
| CCS/control-plane metadata already lists the shard as replica, but the Redis process role is wrong | Restart the shard only: `rlutil redis_restart redis=<SHARD_ID> force=yes`. |
| Multiple shards have wrong roles or metadata is out of sync and a direct attach is required | Identify the authoritative master IP/port from CCS/topology, then run `shard-cli <SHARD_ID> SLAVEOF <MASTER_IP> <MASTER_PORT>` or `ShardCliSlaveOf <SHARD_ID> <MASTER_IP> <MASTER_PORT>`. |
| Database state machine is in FINAL ERROR and normal restart/reconfigure does not reconcile | With change-control approval, reset the DB state machine: `rlutil reset_bdb_sm uid=<DB_ID> resume=yes`, then rerun role checks. |
| Error persists even though Redis reports `role:slave` and `master_link_status:up` | Escalate to Redis Support or platform engineering with full evidence. |

## Verification

After remediation, verify both control-plane and process state:

```bash
rladmin status extra all
redis-cli -h <shard_host> -p <shard_port> INFO replication
```

Expected outcome:

- The affected shard is listed as replica/slave in cluster status.
- `INFO replication` shows `role:slave`.
- `master_link_status:up` after synchronization.
- Logs no longer show repeated role mismatch, failed sync, or stuck state-machine messages.

## Prevention

- Add `INFO replication` and `rladmin` role checks before role-sensitive maintenance or automation.
- Avoid hardcoded role assumptions in clients and operational scripts.
- Check whether failover, upgrade, Kubernetes/operator actions, or external orchestration repeatedly changes shard role.
- Document external replica-of or CRDB topologies after failover, migration, or maintenance.

## Escalation Packet

When escalating, include:

- DB ID, shard ID, host, port, cluster, and product context.
- `INFO replication` output.
- `rladmin status shards`, `rladmin status shards db <db-id>`, and `rladmin status extra all`.
- Recent cluster/DB logs with timestamps.
- Exact commands already run and their timestamps.
- Evidence used to choose the authoritative master, if manual reattachment was attempted.
