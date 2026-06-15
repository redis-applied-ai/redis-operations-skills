---
name: redis-software-recovery
description: "Guide Redis Software cluster and database recovery after failure. Use when the user asks to recover a failed Redis Enterprise cluster, restore databases from persistence files, use `rladmin cluster recover`, use `rladmin recover`, resolve pending recovery or missing files, recover on clean nodes, or safely patch/reboot nodes with maintenance mode."
---

# Redis Software Recovery

Use this skill for Redis Software recovery planning and triage. Treat recovery actions as high impact and verify evidence before suggesting commands.

## Safety Rules

- Confirm backups and persistence files before any recovery action.
- Prefer recovery to new clean nodes with clean persistent storage.
- If reusing original nodes or drives, follow the official recovery preparation steps and do not assume the clean-node path applies.
- Confirm Redis Software version compatibility before recovery.
- Preserve logs and support packages before making changes when possible.

## Recovery Decision Tree

| Situation | Workflow |
| --- | --- |
| Cluster configuration is lost or cluster failed | Cluster recovery with `/ccs/ccs-redis.rdb`. |
| Cluster is healthy but databases are absent or pending | Database recovery with `rladmin recover`. |
| Single node needs OS patching/reboot | Maintenance mode, patch/reboot, exit maintenance mode. |
| Persistence files are missing or corrupt | Stop and validate backups; escalate if no valid copies exist. |
| DNS/port 53 issues appear during recovery | Check PowerDNS and cluster DNS configuration before proceeding. |

## Cluster Recovery Workflow

Prerequisites:

- Recent cluster configuration backup at `/ccs/ccs-redis.rdb`.
- Database persistence files or backups.
- Target nodes have no running Redis processes.
- Target nodes run matching Redis Software version.
- Cluster name and FQDN are unchanged.
- Persistent storage is clean and correctly mounted.

Steps:

1. Install Redis Software on clean target nodes.
2. Mount persistent storage with `/ccs/ccs-redis.rdb` and database persistence files.
3. Recover cluster configuration on the first node:

   ```bash
   rladmin cluster recover
   ```

4. Join remaining nodes:

   ```bash
   rladmin cluster join
   ```

5. Verify health and adjust DNS records if needed.

## Database Recovery Workflow

1. Confirm cluster health:

   ```bash
   rladmin status extra all
   ```

2. Confirm persistence files are accessible on every relevant node.
3. If files are mounted outside the default path, set recovery path as needed:

   ```bash
   rladmin node <id> recovery_path set
   ```

4. Recover databases:

   ```bash
   rladmin recover all
   rladmin recover db db:<id>
   rladmin recover db <name>
   rladmin recover db <name> only_configuration
   ```

5. Confirm required module versions are installed before recovery.
6. Verify databases are active and clients can connect.

## Maintenance Mode for Node Work

```bash
rladmin node <id> maintenance_mode on
# patch or reboot
rladmin node <id> maintenance_mode off
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Cluster does not recover | Correct `/ccs/ccs-redis.rdb`, recovery path, and Redis Software version. |
| Databases pending recovery | Persistence files are mounted and recovery path is set. |
| Missing files | File location, ownership `redislabs:redislabs`, and permissions such as `640`. |
| Corrupt persistence files | Replace with valid copies; escalate if none exist. |
| Nodes visible but no databases | Run targeted `rladmin recover db <name>` or verify auto-recovery. |
| Port 53 errors | Check PowerDNS binding and cluster DNS. |
| High resource use after recovery | Monitor shard migration/rebalancing; escalate if it does not settle. |

## Helpful Checks

```bash
rladmin status extra all
rladmin status extra all errors_only
supervisorctl status
rlcheck
```

## Escalation Packet

Collect:

- Failure timeline and recovery target.
- Redis Software version.
- Cluster FQDN/name.
- Availability of `/ccs/ccs-redis.rdb`.
- Persistence file paths and permissions.
- `rladmin status extra all` and `errors_only`.
- Supervisor and `rlcheck` output.
- Module versions required by recovered databases.
