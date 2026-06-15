---
name: redis-cloud-high-memory-troubleshooting
description: Use when troubleshooting Redis Cloud high memory usage beyond alert interpretation, including `INFO memory`, `used_memory`, `maxmemory`, evictions, OOM errors, memory fragmentation, `redis-cli --bigkeys`, `SLOWLOG`, large hashes/lists/sets/streams/JSON documents, missing TTLs, unbounded collections, Search or JSON index overhead, `FT.INFO`, excessive SORTABLE or TEXT fields, SCAN plus UNLINK cleanup, right-sizing, clustering, or lifecycle policy fixes.
---

# Redis Cloud High Memory Troubleshooting

Use this skill when Redis Cloud memory pressure needs root-cause analysis and mitigation. For alert severity and resize decision framing, use `redis-cloud-high-memory-warning`.

## Safety Rules

- Treat key deletion, TTL changes, index rebuilds, and schema changes as production-impacting.
- Require explicit confirmation before deleting keys or changing retention.
- Use `SCAN`-based sampling and cleanup; avoid `KEYS` in production.
- Prefer `UNLINK` over `DEL` for large cleanup where supported and appropriate.
- For persistent/source-of-truth workloads, confirm backup/export and business approval before removing data.

## Read-Only Diagnosis

Start in Redis Cloud metrics:

- used memory versus limit
- memory growth trend
- evictions
- OOM errors
- latency percentiles

Then collect CLI evidence where access permits:

```redis
INFO memory
SLOWLOG GET 200
```

Focus on:

- `used_memory`
- `maxmemory`
- `evicted_keys`
- `mem_fragmentation_ratio`
- recent OOM or write failures

## Large Key And Structure Checks

Sample large keys:

```bash
redis-cli --bigkeys
redis-cli --memkeys
```

High-risk patterns:

- large hashes, lists, sets, sorted sets, streams, or JSON documents
- unbounded append-only collections
- per-tenant or per-user keys that never expire
- time-series/log-style data without trimming
- massive single JSON documents instead of smaller documents

## Slow Command Correlation

Check whether memory pressure correlates with expensive commands:

- `KEYS`
- broad scans with high count
- `HGETALL` on huge hashes
- `LRANGE 0 -1` on huge lists
- large `JSON.GET`
- bulk deletes

Memory pressure often combines with latency when large structures are read, scanned, or deleted.

## Search And JSON Index Overhead

For Query Engine workloads:

```redis
FT.INFO <index>
```

Review:

- document count
- indexed schema fields
- unnecessary `TEXT` fields
- unnecessary `SORTABLE` fields
- missing `NOINDEX` for fields never searched
- overly broad `PREFIX` scope

Indexes can be a major RAM consumer. Optimize schema and measure before and after rebuilds.

## Mitigation Choices

| Finding | Mitigation |
| --- | --- |
| stale or unused data | Plan explicit cleanup with `SCAN` and `UNLINK`; confirm owners first. |
| missing TTLs | Add TTLs to cache-like data and backfill expiration carefully. |
| unbounded collections | Trim, time-bucket, shard keys, or archive old data. |
| oversized JSON documents | Split documents or index fewer fields. |
| over-indexed data | Remove unused fields, avoid unnecessary `SORTABLE`, use `TAG` for categorical filters. |
| legitimate sustained growth | Increase database size or evaluate clustering/plan architecture. |

## Cleanup Pattern

Use a reviewed pattern and small batches:

```bash
redis-cli --scan --pattern 'prefix:*'
```

Pipe to controlled `UNLINK` batches only after confirmation and a backup/export decision for persistent data.

## Monitoring

Track:

- used memory versus `maxmemory`
- evictions and OOM errors
- latency percentiles
- largest keys/namespaces over time
- index size after schema changes

Use warning and critical thresholds appropriate for the workload and eviction policy.

## Escalation Packet

Collect:

- database ID, plan, memory limit, and current memory usage
- workload type: cache or persistent
- eviction policy and OOM/write-failure evidence
- memory growth timeline
- `INFO memory` and slowlog summary
- large-key or namespace sampling results
- `FT.INFO` for relevant indexes
- recent imports, deploys, migrations, TTL changes, or index changes
