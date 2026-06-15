---
name: redis-large-key-delete-shrink
description: Use when safely deleting, renaming, expiring, replacing, or shrinking a very large Redis key without latency spikes, including UNLINK versus DEL, RENAME then UNLINK, EXPIRE, HSCAN/HDEL, SSCAN/SREM, ZSCAN/ZREM, LTRIM, XTRIM, MEMORY USAGE, bigkeys, memkeys, slowlog, and large-key data modeling fixes.
---

# Redis Large Key Delete Or Shrink

Use this skill when a single very large key or large data structure must be removed or reduced safely. This differs from deleting many keys by pattern.

## Safety Gate

Before modifying data, confirm:

- exact key name
- data type
- whether the key can be deleted or only shrunk
- production or non-production environment
- backup, cache-only status, or rollback plan
- acceptable maintenance window
- expected application behavior after removal

Key deletion and member removal are destructive. Do not provide executable delete commands until the user confirms the target.

## Identify Size And Type

Use:

```text
TYPE <key>
MEMORY USAGE <key>
HLEN <key>
SCARD <key>
ZCARD <key>
LLEN <key>
XLEN <key>
SLOWLOG GET 128
```

For broader discovery:

```text
redis-cli --bigkeys
redis-cli --memkeys
```

Check shard CPU, latency, and existing slowlog before starting.

## Delete A Very Large Key

Prefer:

```text
UNLINK <key>
```

Use `UNLINK` to remove the key reference while memory is reclaimed asynchronously.

If the application must stop seeing the key immediately and cleanup can proceed afterward:

```text
RENAME <key> tmp:<key>:to_delete
UNLINK tmp:<key>:to_delete
```

If immediate cleanup is not required:

```text
EXPIRE <key> <seconds>
```

## Shrink By Data Type

Shrink incrementally with conservative batches.

Hashes:

```text
HSCAN <key> 0 COUNT 1000
HDEL <key> <field> [field ...]
```

Sets:

```text
SSCAN <key> 0 COUNT 1000
SREM <key> <member> [member ...]
```

Sorted sets:

```text
ZSCAN <key> 0 COUNT 1000
ZREM <key> <member> [member ...]
```

Lists:

```text
LTRIM <key> <start> <stop>
```

Streams:

```text
XTRIM <key> MAXLEN ~ <count>
```

Start with small batches, reduce if latency increases, and pause between batches when needed.

## Monitoring

Watch during the operation:

- latency percentiles
- slowlog
- CPU on the owning shard
- memory and fragmentation
- client timeouts
- replication lag
- network throughput

Memory may not drop immediately because `UNLINK` is asynchronous and allocator fragmentation can remain.

## Prevention

If large-key issues repeat, recommend data model changes:

- partition large collections by tenant, time, or hash tag
- keep values smaller
- use TTLs for ephemeral data
- avoid unbounded lists, streams, sets, hashes, or sorted sets
- archive or compact old data outside hot Redis paths

## Response Pattern

Answer with:

1. The key type and size checks.
2. The least disruptive delete or shrink method.
3. Confirmation needed before destructive commands.
4. Batch size and monitoring guidance.
5. Data model prevention advice if this is recurring.
