---
name: redis-software-del-latency-troubleshooting
description: Use when Redis Software or Redis Open Source latency spikes, command timeouts, blocked clients, dropped connections, or shard unresponsiveness are caused by synchronous `DEL` on large keys or many keys, and the user needs SLOWLOG, MONITOR, Redis Insight, `--bigkeys`, `UNLINK`, batching, Transparent Huge Pages checks, shard logs, CPU/memory diagnostics, or large-key redesign guidance for non-CRDB deployments.
---

# Redis Software DEL Latency Troubleshooting

Use this skill when `DEL` on Redis Software or Redis Open Source blocks the server thread and causes latency or failures. For Active-Active CRDB delete behavior, use `redis-crdb-delete-latency`.

## Safety Gate

Key deletion is destructive. Before providing executable deletion commands, confirm:

- exact keys or pattern
- database and environment
- whether the data is cache-only or persistent
- backup/export or rollback decision
- acceptable maintenance window
- expected application behavior after deletion

## Confirm DEL Is The Source

Check slow commands:

```redis
SLOWLOG GET 200
```

Use live observation only when the overhead is acceptable:

```redis
MONITOR
```

Correlate `DEL` timestamps with latency, blocked clients, dropped connections, shard CPU, and application timeouts.

## Find Large Or Risky Keys

Sample large keys:

```bash
redis-cli --bigkeys
redis-cli --memkeys
```

For known keys:

```redis
TYPE <key>
MEMORY USAGE <key>
HLEN <key>
LLEN <key>
SCARD <key>
ZCARD <key>
XLEN <key>
```

High-risk keys are large in memory, contain many elements, or are deleted in large batches.

## Prefer UNLINK

Use `UNLINK` instead of `DEL` for large keys or production cleanup when supported:

```redis
UNLINK <key>
```

`UNLINK` removes the key reference and frees memory asynchronously, reducing server-thread blocking. For many keys, use bounded batches and pauses; do not send unbounded delete pipelines to a busy shard.

For a single very large key that may need type-specific shrinking, use `redis-large-key-delete-shrink`.

## Infrastructure Amplifiers

Blocking delete impact is worse under resource pressure. Check:

```bash
top
vmstat 1
cat /sys/kernel/mm/transparent_hugepage/enabled
```

Review Redis Software logs:

- `redis-server.log`
- shard logs such as `shard-*.log` or `redis-<id>.log`
- cluster or proxy logs if clients are disconnected

Look for blocked clients, command timeouts, high CPU, memory pressure, and shard restarts.

## Prevention

- Use TTLs for cache-like data instead of manual large purges.
- Keep collection sizes bounded.
- Split large datasets by tenant, time bucket, or logical partition.
- Schedule cleanup jobs during low-traffic windows.
- Alert on slowlog entries for `DEL` and other blocking commands.
- Educate application teams to use `UNLINK` for large cleanup in non-CRDB Redis.

## Response Pattern

Answer with:

1. Evidence that `DEL` is causing latency.
2. Large-key or batch pattern found.
3. Whether `UNLINK` or type-specific shrinking is safer.
4. Confirmation required before destructive cleanup commands.
5. Monitoring plan during cleanup.
6. Data model or TTL change to prevent recurrence.
