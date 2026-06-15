---
name: redis-data-import
description: "Import data into self-managed Redis or Redis Software using RDB restore, AOF restore, replication, or key-by-key migration. Use when the user asks to load an RDB file, restore appendonly.aof, migrate with REPLICAOF, use MIGRATE AUTH or AUTH2, capture an RDB with `redis-cli --rdb`, fix Unknown option errors, verify CONFIG GET dir/dbfilename, or validate INFO persistence and INFO keyspace after import."
---

# Redis Data Import

Use this skill when importing data into self-managed Redis or Redis Software with OS-level access.

## Safety Rules

- Restoring RDB or AOF at startup replaces the target's existing in-memory dataset.
- Replication makes the target match the source and can remove pre-existing target keys.
- Keep original persistence files and take a fresh backup before cutover.
- Test the procedure in staging before production.
- Do not put passwords in shell history; use secure secret handling and quote or URL-encode special characters.

## Method Selection

| Need | Method |
| --- | --- |
| Fresh instance or controlled restart | RDB restore. |
| Append-only persisted dataset | AOF restore. |
| Minimal downtime migration | Replication with `REPLICAOF`. |
| Selective or incremental key transfer | `MIGRATE` or SCAN-based tooling. |
| Snapshot from live source | `redis-cli --rdb`, then RDB restore. |

## Compatibility Checks

- Target Redis must be the same version as source or newer for RDB compatibility.
- Older Redis cannot load RDB files created by newer Redis.
- `MIGRATE AUTH2` requires Redis 6 or newer on both sides.
- Confirm command support with:

  ```redis
  HELP <command>
  COMMAND DOCS <command>
  ```

## RDB Restore Workflow

There is no Redis command to import an RDB. Redis loads the RDB at startup.

1. Find persistence settings:

   ```redis
   CONFIG GET dir
   CONFIG GET dbfilename
   ```

2. Stop Redis.
3. Copy the RDB into the configured `dir`.
4. Ensure filename matches `dbfilename`.
5. Set ownership and permissions:

   ```bash
   chown redis:redis /path/to/dump.rdb
   chmod 640 /path/to/dump.rdb
   ```

6. Start Redis.
7. Verify:

   ```redis
   INFO persistence
   INFO keyspace
   ```

Confirm `rdb_last_load_status:ok`, `loading:0`, and expected keys.

## AOF Restore Workflow

1. Confirm AOF config:

   ```text
   appendonly yes
   appendfilename appendonly.aof
   ```

2. Stop Redis.
3. Copy the AOF into the configured directory.
4. Set ownership and permissions.
5. If corruption is suspected, repair a copy:

   ```bash
   redis-check-aof --fix appendonly.aof
   ```

6. Start Redis.
7. Check `INFO persistence`, `INFO keyspace`, and logs.

## Replication Migration Workflow

On the target:

```redis
CONFIG SET masteruser <user>
CONFIG SET masterauth <password>
REPLICAOF <source-host> <source-port>
```

For older Redis without ACL users, use only `masterauth`.

Monitor:

```redis
INFO replication
```

Confirm `master_link_status:up` and `master_sync_in_progress:0`.

For exact cutover, pause writes on the source, wait for zero lag, then promote target:

```redis
REPLICAOF NO ONE
CONFIG REWRITE
```

Update applications to the new endpoint.

## Key-by-Key Migration

Use `SCAN` to batch keys and avoid blocking.

Redis 6+ ACL example shape:

```redis
MIGRATE <dest> <port> "" 0 5000 KEYS key1 key2 COPY REPLACE AUTH2 <user> <password>
```

Older password-only example shape:

```redis
MIGRATE <dest> <port> "" 0 5000 KEYS key1 key2 COPY REPLACE AUTH <password>
```

Validate supported flags before use.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `Unknown option` | Redis server/CLI version mismatch or unsupported command flag. |
| RDB restored but no keys | Wrong `dir`, wrong `dbfilename`, permissions, or startup load error. |
| AOF restore fails | AOF corruption, wrong filename/path, permissions, or incompatible format. |
| Replication does not sync | Network, auth, TLS, version compatibility, memory, or source accessibility. |
| `MIGRATE AUTH2` fails | Source or destination is older than Redis 6. |
| Startup flag unknown | Move settings into `redis.conf` and use supported flags only. |

## Escalation Packet

Collect:

- Source and target Redis versions.
- Import method and dataset size.
- `CONFIG GET dir` and `dbfilename`.
- File names, permissions, and ownership.
- `INFO persistence`, `INFO keyspace`, and logs.
- Replication status if using `REPLICAOF`.
- Exact unknown-option or startup error.
- Rollback files/backups available.
