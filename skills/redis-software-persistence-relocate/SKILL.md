---
name: redis-software-persistence-relocate
description: "Relocate Redis Software persistence storage after installation using maintenance mode, shard evacuation, service stops, data movement, and a symlink from `/var/opt/redislabs/persist`. Use when the user needs to move Redis Enterprise persistence to a new mount point, change persistent storage location, fix disk layout, or troubleshoot Redis startup/permissions after persistence relocation."
---

# Redis Software Persistence Relocate

Use this skill for Redis Software nodes where persistence data must be moved to a new filesystem location after installation.

## Safety Rules

- Test the procedure in staging before production.
- Take backups and generate a support package before the change.
- Perform one node at a time.
- Use a maintenance window and confirm rollback expectations.
- Do not run this on a node that still hosts master or replica shards unless an approved plan accepts that risk.
- Confirm every path, node ID, and mount before moving data.

## Preflight

1. Verify cluster health:

   ```bash
   rladmin status extra all
   sudo /opt/redislabs/bin/rlcheck --continue-on-error
   supervisorctl status
   ```

2. Confirm the node can be safely worked on:
   - No master or replica shards remain on the node, or migration plan is approved.
   - Endpoints and shards have been migrated away if applicable.
3. Move shards if needed:

   ```bash
   rladmin migrate shard <shard-id> to <target-node>
   ```

4. Confirm the new mount has enough capacity and expected performance.
5. Generate a support package and verify backups exist.

## Migration Workflow

1. Enable maintenance mode:

   ```bash
   rladmin node <node-id> maintenance_mode on
   ```

2. Stop Redis services:

   ```bash
   supervisorctl stop all
   cnm_ctl stop
   dmc_ctl stop
   sudo /opt/redislabs/bin/redis_ctl stop-all
   ```

3. Create the target persistence directory:

   ```bash
   sudo mkdir -p /u01/app/RedisSoftware/persistentstorage/<node-id>-persist
   sudo chown -R redislabs:redislabs /u01/app/RedisSoftware/persistentstorage/<node-id>-persist
   sudo chmod -R 755 /u01/app/RedisSoftware/persistentstorage/<node-id>-persist
   ```

4. Move data:

   ```bash
   sudo mv /var/opt/redislabs/persist/* /u01/app/RedisSoftware/persistentstorage/<node-id>-persist/
   ```

5. Replace the old persistence directory with a symlink:

   ```bash
   rmdir /var/opt/redislabs/persist
   ln -s /u01/app/RedisSoftware/persistentstorage/<node-id>-persist /var/opt/redislabs/persist
   ls -alR /var/opt/redislabs/persist
   readlink -f /var/opt/redislabs/persist
   ```

6. Start services:

   ```bash
   sudo /opt/redislabs/bin/redis_ctl start-all
   cnm_ctl start
   dmc_ctl start
   supervisorctl start all
   supervisorctl status
   ```

7. Disable maintenance mode:

   ```bash
   rladmin node <node-id> maintenance_mode off
   ```

8. Verify health:

   ```bash
   rladmin status extra all
   ```

9. Migrate workloads back if they were evacuated:

   ```bash
   rladmin migrate shard <shard-id> to <original-node>
   ```

10. Clean up old AOF predecessor files only after validation:

   ```bash
   find /u01/app/RedisSoftware/persistentstorage/<node-id>-persist/ -name '*.aof.prev' -delete
   ```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Cluster health degraded | Run `rladmin status extra all` and inspect Redis/system logs. |
| Symlink not followed | Confirm `ln -s` target and `readlink -f /var/opt/redislabs/persist`. |
| Permission denied | Ensure `redislabs:redislabs` ownership and writable path permissions. |
| Redis does not start | Confirm `redis_ctl`, `cnm_ctl`, `dmc_ctl`, and supervisor-managed services are running. |
| Rollback needed | Restore from backup and reverse the symlink setup under change control. |

## Escalation Packet

Collect:

- Node ID and target persistence path.
- Precheck `rladmin`, `rlcheck`, and `supervisorctl` output.
- Shards/endpoints migrated before the change.
- Symlink output and resolved target path.
- Service start/stop output.
- Relevant Redis and system logs.
