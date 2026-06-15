---
name: redis-large-cluster-safe-key-deletion
description: Use when deleting many keys in Redis OSS Cluster, Redis Cloud, or Redis Software without blocking shards, including SCAN plus UNLINK, cluster-aware deletion, per-shard scanning, CROSSSLOT errors, FLUSHALL risk, batching, pipelining, MEMORY PURGE, large key cleanup, ACL permission checks, and production deletion safety.
---

# Redis Large Cluster Safe Key Deletion

Use this skill when deleting large numbers of keys or large values from Redis. Deletion is destructive: confirm the target database, pattern, count, and data-loss intent before giving executable delete commands.

## Safety Gate

Before deletion, require:

- exact environment and database
- pattern or key list
- estimated key count
- whether this is production
- backup or disposable-cache confirmation
- maintenance window or rollback plan
- ACL permission for `UNLINK` or `DEL`

Never recommend `FLUSHALL`, broad `DEL`, or unbounded scripts without explicit confirmation.

## Preferred Production Pattern

Use `SCAN` plus `UNLINK` in bounded batches:

- `SCAN` avoids blocking full keyspace iteration.
- `UNLINK` frees memory asynchronously and reduces latency impact compared with `DEL`.
- Batching controls shard pressure.
- Sequential per-shard execution is safer than high parallelism.

Start with small batches, such as hundreds to low thousands of keys, and increase only if latency and CPU remain healthy.

## Cluster Behavior

For Redis OSS Cluster:

- scan each master shard or use a cluster-aware client
- avoid multi-key commands spanning hash slots
- use per-key or same-slot batched operations to avoid `CROSSSLOT`

For Redis Cloud or Redis Software:

- confirm supported commands and access mode
- monitor per-shard latency, CPU, memory, and replication impact
- be careful with CRDB/Active-Active because delete propagation may be more expensive

## When FLUSHALL Is Acceptable

Only use `FLUSHALL` when:

- the environment is non-production, or downtime and full data loss are explicitly accepted
- the user confirms all data should be removed
- in OSS Cluster, every master shard is targeted intentionally

Otherwise use bounded `SCAN` plus `UNLINK`.

## Monitoring During Deletion

Watch:

- latency percentiles
- slowlog
- CPU
- memory and fragmentation
- evictions
- replication lag
- AOF/RDB rewrite pressure
- client timeouts and error rates

After very large deletions, memory may remain high because of fragmentation. Use `MEMORY PURGE` only when supported and appropriate, or schedule controlled maintenance if required.

## Troubleshooting

- Keys remain: verify cursor reached `0`, pattern is correct, and all masters were scanned.
- High latency: reduce batch size, lower concurrency, or move to maintenance window.
- `CROSSSLOT`: switch to per-shard or cluster-aware per-key deletion.
- Permission denied: verify ACL grants for delete commands.
- Memory still high: check fragmentation, allocator behavior, and persistence rewrite state.

## Response Pattern

Answer with:

1. The destructive-action confirmation needed.
2. The safe deletion strategy for the deployment type.
3. Batch and concurrency guidance.
4. Monitoring checklist.
5. Post-delete fragmentation and persistence checks.
