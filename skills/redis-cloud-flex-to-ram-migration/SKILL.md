---
name: redis-cloud-flex-to-ram-migration
description: "Move a Redis Cloud database off Flex or auto-tiering by creating a new RAM-only database and migrating data. Use when the user asks to disable Flex in place, switch a Flex database to non-Flex, explain why endpoints change, size RAM-only replacement capacity, migrate data from Flex, troubleshoot evictions or OOM after moving off Flex, or decommission the old Flex database."
---

# Redis Cloud Flex To RAM Migration

Use this skill when a Redis Cloud Flex database must be replaced with a non-Flex, RAM-only database.

## Core Rule

Flex cannot be disabled or converted in place on an existing database. Flex is part of the database architecture. The supported path is to create a new non-Flex database, migrate data, cut over applications, and then decommission the Flex database.

## Preflight

1. Confirm the current database is Flex/auto-tiered.
2. Capture current configuration:
   - Dataset size.
   - Replication/HA.
   - Shard count and clustering.
   - Redis version.
   - Capabilities such as JSON or Search.
   - Persistence settings.
   - Eviction policy.
   - ACL users, passwords, TLS, and network allow lists/private connectivity.
3. Confirm downtime tolerance and migration method.
4. Size the new database so the full primary dataset, replica/HA overhead, fragmentation, growth, and operational headroom fit in RAM.

## Migration Workflow

1. Create a new non-Flex Redis Cloud database under the desired plan.
2. Ensure Flex/auto-tiering is not enabled.
3. Match critical source settings:
   - Capabilities/modules.
   - Persistence.
   - Replication/HA.
   - Eviction policy.
   - Security and network access.
4. Choose migration method:
   - Online sync or replication where supported for minimal downtime.
   - Backup/restore when planned downtime is acceptable.
   - Client-side export/import for controlled or custom migrations.
5. Validate target before cutover:
   - Key count and sampled values.
   - TTL behavior.
   - Memory usage and headroom.
   - Latency, throughput, and evictions.
   - Authentication and TLS behavior.
6. Update applications to the new endpoint. The old Flex endpoint cannot be reused.
7. Roll out gradually where possible and monitor errors, latency, throughput, memory, and evictions.

## Sizing Warnings

- Do not size the RAM-only database to only the active RAM portion of a Flex database.
- The full dataset must fit in memory after moving off Flex.
- Include replicas, HA overhead, fragmentation, and growth.
- Evictions or out-of-memory after cutover usually indicate undersizing or an eviction-policy mismatch.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Flex still enabled after plan change | Flex is tied to database architecture | Create a new non-Flex database and migrate. |
| New database evicts keys | RAM-only target is undersized or eviction policy differs | Increase memory and verify eviction policy. |
| Higher latency after migration | Shard sizing, CPU, or storage/feature mismatch | Check shard count, CPU, clustering, and query workload. |
| Authentication errors after cutover | ACL/TLS settings not replicated | Recreate ACL users, credentials, TLS, and network access settings. |
| Data mismatch | Migration incomplete or wrong source/target | Re-run migration or compare source/target before traffic cutover. |

## Decommission Safety

Deleting the old Flex database stops charges but is destructive. Before deletion:

1. Confirm applications use the new endpoint.
2. Confirm no active connections remain on the old database.
3. Confirm backups/rollback window requirements are satisfied.
4. Ask for explicit confirmation naming the old database before deletion.

## Escalation Packet

Collect:

- Source Flex database ID and configuration.
- Target non-Flex database ID and configuration.
- Dataset size and sizing calculation.
- Migration method and validation results.
- Cutover time and application endpoint changes.
- Memory, latency, throughput, and eviction metrics before and after.
