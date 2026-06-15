---
name: redis-data-migration-options
description: "Choose and plan Redis data migration methods across Redis OSS, managed cloud Redis, files, relational databases, and NoSQL sources. Use when the user asks whether to use export/import, ReplicaOf, RIOT, RDI, snapshot migration, live migration, low-downtime cutover, or Redis migration professional services."
---

# Redis Data Migration Options

Use this skill to select a Redis migration strategy and outline the execution plan. Always recommend a non-production test before production migration.

## Selection Questions

Ask or infer:

- Source type: Redis OSS, Redis Cloud, another managed Redis service, files, RDBMS, or NoSQL.
- Destination: Redis Cloud, Redis Software, or another Redis deployment.
- Downtime tolerance: planned outage versus near-zero downtime.
- Data change rate during migration.
- Connectivity between source, migration host, and destination.
- Access level to source backups, commands, network, and credentials.
- Required validation: key count, sampled values, TTLs, modules, data types, or application tests.

## Method Matrix

| Source | Snapshot options | Live options |
| --- | --- | --- |
| Redis OSS | Export/import, RIOT | ReplicaOf, RIOT live mode |
| Managed cloud Redis | Export/import, RIOT | RIOT live mode when source access allows |
| Files | RIOT | Usually not applicable |
| RDBMS | RIOT for batch loads | RDI for CDC-based ongoing sync |
| NoSQL | Case-specific | RDI when supported by the RDI connector path |

## Export / Import

Use for one-time snapshot migration from Redis sources when downtime is acceptable.

Workflow:

1. Confirm source backup/export access and destination import support.
2. Generate or obtain an RDB file, commonly through `BGSAVE` or provider backup export.
3. Place the file in a supported import location such as local mount, SFTP, S3, Azure Blob, or GCS.
4. Import into the destination database.
5. Validate key counts, sample keys, TTL behavior, modules, and application reads.

Watchouts:

- Writes that occur after the snapshot are not included.
- Large RDB imports need capacity and time-window planning.
- Managed providers can restrict export paths or backup formats.

## ReplicaOf

Use for ongoing one-way replication from Redis OSS into Redis Software when network access and compatibility are available.

Workflow:

1. Confirm source endpoint, authentication, TLS, and network reachability from the destination.
2. Configure the destination database as a replica of the source.
3. Monitor sync progress and lag.
4. Freeze or drain source writes for final cutover if strict consistency is required.
5. Move application traffic to the destination.
6. Remove the replica configuration after cutover.

Watchouts:

- Major drift or restart can force destination flush and resync.
- Validate Redis version, module, data type, and command compatibility.
- Plan rollback before switching application traffic.

## RIOT

Use RIOT for flexible migrations from Redis, files, and some relational sources. It can run as a snapshot copy or live replication, depending on source and mode.

Prerequisites:

- A migration host with Java 11 or later.
- Network connectivity to source and destination.
- Credentials and TLS material supplied through secure channels.

Example shapes:

```bash
riot -h <source-host> -p <source-port> replicate -h <destination-host> -p <destination-port>
riot -h <source-host> -p <source-port> replicate -h <destination-host> -p <destination-port> --mode live
```

Tune the actual command for authentication, TLS, selected databases, filters, batching, and target data model.

## RDI

Use Redis Data Integration when the source is an operational database and the goal is ongoing change-data-capture sync into Redis.

Good fit:

- RDBMS or supported NoSQL sources.
- Read-heavy workloads need Redis as a derived serving layer.
- Schema transformation and real-time updates are part of the requirement.

Before recommending RDI, verify connector support, source database permissions, Debezium/CDC prerequisites, target schema, and ownership with the Redis account team when appropriate.

## Cutover Checklist

1. Run a non-production trial with representative data.
2. Estimate transfer time and resync risk.
3. Define validation queries before migration starts.
4. Freeze, queue, or dual-write source traffic if consistency requires it.
5. Switch clients through a controlled connection-string or DNS change.
6. Monitor latency, errors, memory, evictions, key count, and application behavior.
7. Keep rollback instructions and source access until validation is complete.

## Escalation Packet

Collect:

- Source and destination platform/version.
- Data size, key count, data types, modules, and write rate.
- Downtime tolerance and cutover date.
- Chosen migration method and reason.
- Network path and authentication/TLS constraints.
- Test migration results and validation deltas.
- Any RIOT, ReplicaOf, import, or RDI errors with secrets redacted.
