---
name: redis-aof-flushdb-recovery
description: "Recover a Redis Enterprise Software database after accidental `FLUSHDB` by preserving and trimming AOF files. Use when the user asks about AOF-based recovery, locating per-shard appendonly files, removing destructive commands from AOF, disabling/enabling watchdogs, using `preload-file`, restarting shards with `redis_ctl force-start`, or deciding when to restore from backup instead. Do not use for Active-Active CRDB recovery when healthy replicas exist."
---

# Redis AOF FLUSHDB Recovery

Use this skill only for emergency Redis Enterprise Software recovery after an accidental destructive command such as `FLUSHDB`, when AOF persistence may contain the pre-destruction command history.

## Stop Conditions

Do not proceed without expert review or Redis Support if:

- The database is Active-Active CRDB and healthy replicas still exist.
- You cannot stop writes to the affected database.
- AOF files or shard IDs are uncertain.
- Persistence files may be corrupted or missing.
- You do not have a copy of the original AOF files.

Manual AOF manipulation is risky and can make recovery worse.

## Immediate Actions

1. Stop application writes to the affected database.
2. Identify affected database ID and shard IDs.
3. Copy all impacted AOF directories to safe storage before editing anything:

   ```bash
   cp -r /var/opt/redislabs/persist/redis/appendonly-<shard-id>.aof.dir /tmp/aof_backup_<shard-id>
   ```

4. Capture current status and logs.
5. Decide whether backup/snapshot restore is safer than AOF editing.

## Locate AOF Files

Typical per-shard path:

```text
/var/opt/redislabs/persist/redis/appendonly-<shard-id>.aof.dir/appendonly-<shard-id>.aof.*.aof
```

Search for destructive commands:

```bash
grep -iahn flushdb appendonly-<shard-id>.aof.*.aof
```

Also search for other destructive commands if relevant, such as `FLUSHALL`, broad deletes, or scripts that performed the deletion.

## Trim Strategy

Create a new AOF ending before the destructive command:

```bash
head -n <line-before-destructive-command> appendonly-<shard-id>.aof.*.aof > trimmed.aof
```

Validate the trimmed file on a non-production copy if possible before replacing live shard persistence.

## Replacement Procedure Shape

Require explicit confirmation before each production-impacting step.

1. Disable database watchdogs:

   ```bash
   rlutil disable_watchdogs uid=<bdb-id>
   ```

2. Replace the target AOF with the trimmed copy, preserving a backup of the original.
3. Set ownership and permissions:

   ```bash
   chown redislabs:redislabs <aof-file>
   chmod 644 <aof-file>
   ```

4. Configure the shard to preload the intended AOF manifest by editing the shard config:

   ```text
   /var/opt/redislabs/redis/redis-<uid>.conf
   ```

   Add the appropriate `preload-file` path to the AOF manifest.

5. Restart the shard:

   ```bash
   redis_ctl stop <shard-id>
   redis_ctl force-start <shard-id>
   ```

6. Validate recovered data.
7. Remove the temporary `preload-file` directive after validation.
8. Re-enable watchdogs:

   ```bash
   rlutil enable_watchdogs uid=<bdb-id>
   ```

## Troubleshooting

| Symptom | Action |
| --- | --- |
| No destructive command found in AOF | AOF recovery may not be possible; restore from snapshot/backup. |
| Redis fails to start | Check AOF syntax, file path, ownership, permissions, and logs. |
| Data still missing | AOF was already rewritten/truncated after the destructive command or wrong shard/file was used. |
| Preload appears ignored | Verify manifest path and shard config; inspect `/var/opt/redislabs/log/`. |
| Active-Active attempted | Stop manual recovery and use CRDB-safe recovery/support guidance. |

## Evidence To Preserve

- Original AOF directory copies.
- Trimmed AOF file.
- Database ID and shard IDs.
- `rladmin status extra all` before/after.
- Exact destructive command and timestamp if known.
- Watchdog disable/enable timestamps.
- Shard logs from `/var/opt/redislabs/log/`.
