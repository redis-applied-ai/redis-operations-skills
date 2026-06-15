---
name: redis-shard-count-reduction-migration
description: Use when a Redis Cloud or Redis Software user wants to reduce shard count, scale shards down, unshard a database, move from more shards to fewer shards, migrate to a right-sized database, preserve data while changing shard topology, or plan backup/restore, live sync, cache rebuild, endpoint cutover, and rollback for shard-count reduction.
---

# Redis Shard Count Reduction Migration

Use this skill when a user wants fewer shards on an existing Redis database. The supported pattern is to create a new database with the desired shard count, migrate data, and cut traffic over.

## Core Rule

Do not promise in-place shard reduction. Existing clustered databases can be scaled up according to supported patterns, but reducing shard count requires a new target database and migration.

## Planning Checks

Before creating the target database, collect:

- Redis product: Redis Cloud or Redis Software
- current shard count and target shard count
- dataset size, key count, memory usage, and growth rate
- peak throughput and latency targets
- Redis version and modules
- clustering mode and client cluster awareness
- persistence, eviction, TLS, ACLs, timeouts, and backup settings
- downtime tolerance and rollback requirement
- endpoint constraints, including whether a stable DNS name or load balancer is available

Fewer shards reduce parallelism and can increase CPU, memory, and network pressure per shard. Validate target capacity against peak load.

## Migration Options

Choose by workload and downtime tolerance:

- Backup and restore: simplest when downtime is acceptable. Quiesce writes, take final backup, restore to target, validate, then cut over.
- Live copy or sync: use when downtime must be minimized. Run full sync, keep source and target aligned, freeze writes or run final delta sync, then cut over.
- Application-driven rebuild: use for cache-only workloads where the dataset can be regenerated naturally.

For custom migration scripts, preserve TTLs and avoid oversized pipelines. Be careful with scripts, Redis functions, streams, consumer groups, modules, ACLs, and keyspace notification behavior.

## Target Database Setup

Match intentionally:

- Redis version and module compatibility
- memory size and eviction policy
- persistence mode
- TLS, authentication, ACL users, and permissions
- timeouts and client-facing behavior
- network allowlists, VPC or VNet connectivity, certificates, and credentials

Record new endpoints and credentials. For clustered clients, plan for slot-map refresh during cutover.

## Validation Before Cutover

Check:

- representative key count and sampled values
- sampled TTL preservation
- memory usage and headroom
- scripts, functions, modules, streams, consumer groups, and ACLs
- application read and write paths
- latency, CPU, memory, evictions, and errors under test load

## Cutover

1. Announce maintenance window if required.
2. Pause heavy writers or run final delta sync.
3. Update application endpoint, DNS, or load balancer target.
4. Restart or roll applications that cache connections or cluster slot maps.
5. Monitor latency, errors, evictions, CPU, memory, and connection behavior.
6. Keep the source database idle or read-only until rollback risk is acceptable.

## Gotchas

- Exact endpoint reuse is not guaranteed; plan with stable DNS or support coordination if endpoint continuity is mandatory.
- Pub/Sub subscriptions and live client connections do not migrate.
- Cluster-aware clients may need restart or topology refresh.
- Fewer shards can change multi-key behavior, hot-key pressure, and eviction patterns.
- Directly reducing shard count on the existing database is not the supported path.

## Response Pattern

Answer with:

1. The no-in-place-reduction rule.
2. The target database and migration method.
3. Validation checklist.
4. Cutover and rollback plan.
5. Endpoint and client-topology caveats.
