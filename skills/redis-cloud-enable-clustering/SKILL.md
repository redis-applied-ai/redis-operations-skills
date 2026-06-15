---
name: redis-cloud-enable-clustering
description: "Plan and troubleshoot enabling clustering on Redis Cloud databases. Use when the user asks to enable Redis Cloud clustering, scale beyond single-shard limits, raise memory above 25GB or 50GB with Auto-Tiering, handle CROSSSLOT errors, use hash tags for multi-key commands, enable OSS Cluster API, understand Pro plan requirements, or troubleshoot shard imbalance, hot keys, and module limitations."
---

# Redis Cloud Enable Clustering

Use this skill when a Redis Cloud database needs horizontal scaling through clustering or when a clustered database has compatibility or performance issues.

## Safety Rules

- Confirm the database is on a Redis Cloud Pro subscription; Essentials does not support clustering.
- Treat enabling clustering on an existing database as permanent for that database.
- Require explicit confirmation and backup/export review before hashing policy changes or any operation that can delete data.
- Verify current Redis Cloud behavior before describing account-date hashing defaults or destructive policy transitions.
- Confirm application clients and commands are cluster-safe before enabling clustering.

## When Clustering Fits

Use clustering when:

- Dataset size exceeds single-shard guidance.
- Throughput requires multiple shards.
- The database needs horizontal scaling.
- Shard-level observability and key-distribution management are acceptable operational requirements.

Do not recommend clustering without checking client compatibility, multi-key usage, module requirements, and rollback plan.

## Enable on Existing Database

1. Confirm account Owner or Admin access.
2. Confirm Redis Cloud Pro subscription.
3. Review application command usage:
   - Multi-key commands must target keys in the same hash slot.
   - Use hash tags such as `user:{123}:profile` and `user:{123}:settings` for related keys.
4. Back up or export data.
5. In Redis Cloud Console, open the database and choose `Edit`.
6. Increase memory above the clustering threshold, commonly above 25 GB or above 50 GB when Auto-Tiering is enabled.
7. Review shard count, throughput, and memory per shard.
8. Apply the change and monitor shard metrics.

## Create a New Clustered Database

1. Create a database under a Pro subscription.
2. Choose a clustered configuration or size above the relevant threshold.
3. Set shard count, throughput, and memory per shard.
4. Select compatible modules/capabilities and client access settings.
5. Migrate data and traffic through a planned cutover.

Use this path when the user wants a cleaner rollback option or needs to redesign keys before clustering.

## Compatibility Checks

| Topic | Check |
| --- | --- |
| Multi-key commands | Keys must share a hash slot; use hash tags for related keys. |
| Client library | Client must handle clustered routing if using OSS Cluster API. |
| OSS Cluster API | Pro-only; enabling it can affect module availability. |
| Search/Query or TimeSeries | Verify compatibility before enabling OSS Cluster API. |
| Hashing policy | Changing policy can delete data; test and back up first. |
| Reverting | To return to single shard, create a new smaller database and migrate data. |

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Cannot enable clustering | Essentials plan or unsupported configuration | Move to Pro or create a supported database. |
| `CROSSSLOT` errors | Multi-key command spans different slots | Add hash tags or redesign operation. |
| `CLUSTER` command not allowed | OSS Cluster API not enabled | Enable only if clients and module needs allow it. |
| Search/Query or TimeSeries stopped working | OSS Cluster API/module conflict | Disable OSS Cluster API or choose a compatible database design. |
| Performance drops after clustering | Hot keys or uneven slot distribution | Review shard metrics and redesign key distribution. |
| User wants to undo clustering | Not reversible on same database | Create a new single-shard database and migrate. |

## Monitoring

- Check shard-level memory, CPU, throughput, and latency in Redis Cloud metrics.
- Watch replica sync errors and resharding effects during changes.
- Alert on hot shard behavior and elevated latency.
- Use external observability integrations when available.

## Escalation Packet

Collect:

- Subscription plan and database ID.
- Current memory size, Auto-Tiering status, shard count, and throughput.
- Whether clustering is already enabled.
- Client libraries and whether OSS Cluster API is needed.
- Multi-key command patterns and key naming examples.
- Module/capability requirements.
- Backup/export status.
- Metrics showing hot shards, latency, CPU, memory, or replica sync errors.
