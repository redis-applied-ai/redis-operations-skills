---
name: redis-cloud-del-latency-reduction
description: Use when Redis Cloud latency spikes, transient failures, slowlog entries, or unresponsiveness are caused by DEL on large keys, mass key deletion, Redis Insight bulk actions, UNLINK replacement, memory fragmentation after deletes, Active-Active CRDB delete behavior, or safe batching of production deletions.
---

# Redis Cloud DEL Latency Reduction

Use this skill when Redis Cloud latency spikes correlate with large or frequent `DEL` operations. Key deletion is destructive, so confirm the exact target keys, patterns, and data-loss intent before providing executable deletion commands.

## Diagnostic Flow

1. Confirm the symptom:
   - latency spike
   - timeout or transient failure
   - high slowlog latency for `DEL`
   - elevated shard CPU or memory pressure during deletes
2. Identify the deletion pattern:
   - one very large key
   - many keys in a single command
   - repeated batch jobs
   - cache cleanup or TTL replacement opportunity
3. Locate large or risky keys using Redis Insight, `SLOWLOG`, big-key analysis, or sampled `MEMORY USAGE`.
4. Check whether the database is Active-Active CRDB.

## Mitigation

Prefer:

- `UNLINK` instead of `DEL` for non-blocking key removal when supported and appropriate.
- smaller batches instead of deleting many keys at once.
- scheduled cleanup during off-peak windows.
- Redis Insight bulk key management when it fits the environment.
- TTL-based expiration for ephemeral data instead of manual cleanup jobs.

Avoid:

- broad production delete patterns without dry-run counts.
- deleting massive composite values during peak traffic.
- unbounded `xargs` pipelines that can overload a shard.

## CRDB Handling

For Active-Active CRDB databases, do not assume `UNLINK` gives the same latency benefit as in single-region databases. Cross-region coordination can make deletion behavior effectively synchronous.

For CRDB:

- split deletes into smaller key sets
- avoid large composite objects
- schedule heavy cleanup during low traffic
- monitor replication and conflict behavior after deletion

## Safe Batch Pattern

Before deleting by pattern:

1. Count or sample matching keys.
2. Confirm the pattern cannot match unintended keys.
3. Confirm backups or disposable-cache status.
4. Use bounded batches.
5. Monitor latency, CPU, slowlog, and memory fragmentation during the job.

## Troubleshooting After Delete

- Latency persists: check slowlog, CPU, blocked clients, and shard-local hot keys.
- Memory remains high: inspect fragmentation and allocator behavior; allow time for memory reclamation or use supported defragmentation guidance.
- Application errors appear: check whether clients depended on deleted keys, functions, streams, or cache warmup behavior.

## Response Pattern

Answer with:

1. Evidence that `DEL` is the cause.
2. Whether `UNLINK` is appropriate.
3. A safe batch or bulk-action plan.
4. CRDB caveats if Active-Active is involved.
5. Monitoring and rollback considerations.
