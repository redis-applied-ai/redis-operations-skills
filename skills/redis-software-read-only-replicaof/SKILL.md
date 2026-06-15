---
name: redis-software-read-only-replicaof
description: "Choose and configure read-only access patterns for Redis Enterprise Software using ACLs or Replica Of Active-Passive databases. Use when the user asks for a read-only replica endpoint, reporting or analytics endpoint, read-only ACL user, `replica_read_only`, why endpoints cannot pin to replica shards, how Replica Of differs from HA replication, or how to promote a DR Replica Of database to read-write."
---

# Redis Software Read-Only Replica Of

Use this skill when a user asks for "read-only replica" behavior in Redis Enterprise Software.

## First Clarification

Ask what "read-only replica" means:

| Goal | Correct design |
| --- | --- |
| Prevent selected applications from writing | Same database endpoint plus a read-only ACL user. |
| Provide a separate reporting/analytics endpoint | Separate Replica Of database with its own endpoint. |
| Maintain DR copy | Replica Of database, ideally on a separate cluster/failure domain. |
| Force Replica Of destination to reject writes | Use `replica_read_only=true` at creation time if supported by the deployed version. |
| Send reads directly to replica shards in the same database | Not supported through Redis Enterprise proxy endpoints. |

## Important Distinctions

- Database HA replication inside one database is not the same as Replica Of Active-Passive replication between databases.
- Redis Enterprise database endpoints are proxy-based and cannot be pinned to only primary or replica shards.
- Replica Of is one-way source-to-destination replication.
- Initial sync or resync can erase existing destination data.
- Replica Of destinations have replication lag and are eventually consistent.

## Option A: Same Endpoint With Read-Only ACL

Use when the goal is access control rather than workload isolation.

1. Create a Redis ACL that permits reads and denies writes. Minimal shape:

   ```text
   +@read ~*
   ```

2. Create a database role with that ACL.
3. Create a user assigned to that role and database.
4. Update the read-only application to authenticate with that user:

   ```text
   AUTH <username> <password>
   ```

This does not isolate reporting workload from the primary database.

## Option B: Separate Replica Of Database

Use when the user needs a separate endpoint, DR, or reporting isolation.

1. Choose a destination database, preferably in a separate cluster for DR.
2. Enable the source database for Replica Of and copy the source URL.
3. Create the destination database and configure the source URL.
4. Confirm the destination can reach the source endpoint/port.
5. Validate sync state and lag.
6. Test by writing to the source and reading from the destination.

Warn that destination data may be deleted during initial sync or resync.

## Enforced Read-Only Destination

If the deployed Redis Enterprise Software version supports `replica_read_only`, create the Replica Of destination with the flag set at creation time through the REST API. Verify current version support before recommending this as available.

Payload shape:

```json
{
  "bdb": {
    "name": "readonly_replica_db",
    "memory_size": 1073741824,
    "replica_sources": [
      {
        "uri": "redis://admin:<password>@source-host:port"
      }
    ],
    "replica_read_only": true
  }
}
```

The flag cannot be assumed editable later.

## DR Promotion Warning

To make a Replica Of destination writable during an outage:

1. Disable Replica Of on the destination.
2. Confirm replication has stopped.
3. Redirect clients to the destination endpoint.
4. Allow writes only after the destination is no longer replicating from source.

If writes occur before disabling Replica Of, later resync from the source can overwrite destination data.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| User wants endpoint for replica shards | Proxy endpoints cannot target shard role | Use ACLs or a separate Replica Of database. |
| Reporting load affects primary | ACL only controls permissions, not isolation | Use a separate Replica Of database. |
| Destination accepts writes | `replica_read_only` not set/supported or not created with it | Verify version and creation payload; otherwise enforce with ACLs/app routing. |
| Destination data disappeared on sync | Replica Of initial sync/resync replaced destination data | Treat destination as replica-only and back up before reconfiguring. |
| DR writes overwritten | Replica Of was not disabled before promotion | Stop Replica Of before write traffic. |

## Evidence To Collect

- Redis Enterprise version.
- Requirement: access control, reporting, DR, or enforced read-only.
- Source and destination database IDs.
- Replica Of configuration and sync status.
- ACL/role/user definitions if same-endpoint read-only is used.
- Whether destination must be writable during failover.
