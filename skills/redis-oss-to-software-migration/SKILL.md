---
name: redis-oss-to-software-migration
description: "Plan and execute migration from Redis Open Source or Redis Stack to Redis Enterprise Software. Use when the user asks how to migrate OSS Redis to Redis Software, choose Replica Of versus RDB import versus RIOT, handle logical DBs and `SELECT`, enable OSS Cluster API for cluster-aware clients, validate data consistency, or troubleshoot migration cutover issues."
---

# Redis OSS To Software Migration

Use this skill to choose and run a migration path from Redis Open Source to Redis Enterprise Software.

## Preflight Checklist

1. Inventory the source:
   - Redis version.
   - Standalone, Sentinel, or OSS Cluster topology.
   - Logical database usage with `SELECT`.
   - Modules/capabilities used.
   - Dataset size, key count, TTL behavior, hot keys, and big keys.
2. Confirm connectivity from Redis Enterprise Software or the migration host to the source endpoint.
3. Confirm credentials, TLS requirements, firewall rules, and allow lists.
4. Create the target Redis Enterprise database with matching memory, persistence, replication, clustering, and capability requirements.
5. Define the cutover window, rollback plan, and validation method.

## Migration Path Decision

| Requirement | Recommended path |
| --- | --- |
| Minimal downtime and source supports replication | Configure target database with Replica Of from source OSS. |
| Planned downtime is acceptable | Export/import an RDB snapshot. |
| Selective key migration or logical DB filtering | Use RIOT or a custom migration process. |
| Continuous sync from a non-Redis source | Evaluate Redis Data Integration. |
| Need strong comparison tooling | Use RIOT compare/diff where suitable. |

## Live Migration With Replica Of

1. Confirm source endpoint, port, auth, TLS, and network reachability.
2. Configure the Redis Enterprise destination database to replicate from the OSS source.
3. Monitor initial sync and ongoing replication state in the Redis Enterprise Admin Console.
4. Before cutover:
   - Stop application writes to the source.
   - Wait for replication to catch up.
   - Validate key counts and representative values.
5. Redirect applications to the Redis Enterprise endpoint.
6. Remove Replica Of from the destination so it becomes writable standalone.
7. Monitor latency, errors, memory, and application behavior.

## Offline RDB Import

1. Produce or retrieve a source RDB snapshot.
2. Import the RDB through Redis Enterprise database import tooling from the supported storage location.
3. Validate data after import.
4. Update application connection strings during the planned downtime window.

## RIOT Pattern

Use RIOT when you need selective migration, filtering, live copy behavior, or comparison.

Snapshot style:

```bash
riot -h <source_host> -p <source_port> replicate -h <target_host> -p <target_port>
```

Live style:

```bash
riot -h <source_host> -p <source_port> replicate -h <target_host> -p <target_port> --mode live
```

Verify current RIOT command syntax against the installed RIOT version before running in production.

## Compatibility Watchpoints

| Issue | Guidance |
| --- | --- |
| Source uses `SELECT` logical DBs | Redis Enterprise Software databases do not map to OSS logical DBs; migrate each logical DB to a separate database or redesign namespaces. |
| Source is OSS Cluster and clients expect redirects | Enable OSS Cluster API on the target only if the application requires cluster-aware behavior and target features support it. |
| Multi-key commands | Review hash-slot behavior and use hash tags or proxy-compatible patterns as needed. |
| Blocked or renamed commands | Check Redis Enterprise command compatibility before cutover. |
| Big/hot keys | Analyze before migration; they can distort sync, cutover, and post-migration performance. |

## Validation

- Compare key counts and representative samples.
- Verify TTL preservation for sampled keys.
- Validate application read/write paths against the target.
- Check memory use, fragmentation, CPU, latency, and rejected connections.
- Use RIOT compare/diff or application-level checks when exact consistency matters.

## Escalation Packet

Collect:

- Source Redis version and topology.
- Target Redis Enterprise Software version and database configuration.
- Migration path selected.
- Dataset size, key count, big-key/hot-key findings.
- Error messages from Replica Of, import, RIOT, or application clients.
- Cutover timestamp and validation results.
