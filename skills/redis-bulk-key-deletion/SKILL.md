---
name: redis-bulk-key-deletion
description: "Safely delete large numbers of Redis keys without production latency spikes. Use when the user asks to delete keys by pattern, avoid `KEYS` or blocking `DEL`, use `SCAN` plus `UNLINK`, handle CROSSSLOT errors in clustered or Active-Active databases, use Redis Insight Bulk Actions, or reclaim memory after massive deletion."
---

# Redis Bulk Key Deletion

Use this skill for planned or emergency deletion of many Redis keys. Bulk deletion is destructive: require explicit confirmation before running deletion commands.

## Safety Gates

Before deleting:

1. Confirm the Redis deployment type: OSS/Stack, Redis Cloud, Redis Enterprise Software, clustered database, or Active-Active CRDB.
2. Confirm the target endpoint, database, and key pattern.
3. Sample matching keys with `SCAN` and review the sample with the user.
4. Estimate blast radius: approximate key count, value sizes, and affected applications.
5. Confirm backup/export or recovery posture if data must be recoverable.
6. Schedule large deletes during low-traffic windows when possible.
7. Ask for explicit confirmation with the exact pattern and database before deletion.

## Core Rules

- Prefer `UNLINK` for bulk deletion; it removes keys from the keyspace and reclaims memory asynchronously.
- Avoid `DEL` for large values or large batches because it can block the main thread.
- Never use `KEYS` in production keyspaces.
- Use `SCAN` to iterate incrementally.
- Throttle deletion with small batches and delays.
- Monitor latency, ops/sec, memory, and rejected/errors while deletion runs.

## Command Patterns

Preview matching keys:

```bash
redis-cli -h <host> -p <port> --scan --pattern '<pattern>' | head -50
```

Standard throttled delete by pattern:

```bash
redis-cli -h <host> -p <port> --scan --pattern '<pattern>' -i 0.01 \
  | xargs -n 100 redis-cli -h <host> -p <port> UNLINK
```

If the database requires TLS or authentication, include the same `-u rediss://...` or auth flags on both `redis-cli` invocations.

## Cluster And CRDB Handling

| Environment | Guidance |
| --- | --- |
| Standalone Redis | `SCAN` plus batched `UNLINK` is normally sufficient. |
| Clustered Redis | Multi-key operations work only when keys are in the same hash slot; otherwise delete per shard, per slot, or one key per command. |
| Redis Enterprise Active-Active CRDB | Avoid multi-key delete batches that span slots/regions; use per-key `UNLINK` or carefully generated one-key commands. |
| Redis Insight | Good for visual review and smaller interactive bulk actions; prefer CLI or automation for very large datasets. |

Per-key command stream for cross-slot-safe deletion:

```bash
redis-cli -h <host> -p <port> --scan --pattern '<pattern>' -i 0.01 \
  | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/^/UNLINK "/' -e 's/$/"/' \
  | redis-cli -h <host> -p <port>
```

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `CROSSSLOT Keys in request don't hash to the same slot` | Batch includes keys from multiple slots | Use per-key deletion or shard/slot-scoped batches. |
| Latency rises during deletion | Batch size too large or no throttle | Reduce batch size, add `-i`, pause, and monitor recovery. |
| Keys remain after run | `SCAN` pattern too narrow, wrong DB, or cursor not completed | Recheck endpoint/db number, pattern, and full cursor completion. |
| Permission denied | ACL lacks delete command permissions | Verify permissions for `UNLINK` or `DEL`. |
| Redis Insight bulk delete stalls | Selection too large for interactive UI | Use CLI/automation with throttling. |
| Memory does not drop immediately | Async free, allocator fragmentation, or CRDB tombstones | Wait for background freeing; consider `MEMORY PURGE` only during a maintenance window and with confirmation. |

## Monitoring During Deletion

Track:

- Redis latency and slowlog.
- CPU and ops/sec.
- Connected and blocked clients.
- Memory usage, fragmentation, and allocator behavior.
- Application error rate.
- CRDB replication or conflict/tombstone behavior where applicable.

## Completion Criteria

- A follow-up `SCAN` sample/count shows the targeted pattern is gone or reduced as intended.
- Latency and application error rates remain acceptable.
- Memory behavior is understood, even if allocator reclamation lags key deletion.
- Any cleanup command such as `MEMORY PURGE` is run only after separate confirmation.
