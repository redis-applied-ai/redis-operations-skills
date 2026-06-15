---
name: redis-oss-cluster-flush-all-keys
description: "Safely remove all keys from a Redis OSS Cluster. Use when the user asks to flush a Redis Cluster, `FLUSHALL` only cleared one shard, needs to discover masters with `CLUSTER SLOTS`, run `FLUSHALL` on every master shard, use a cluster-aware client to fan out deletion, handle ACL dangerous-command permission errors, or delete subsets with SCAN and UNLINK without CROSSSLOT failures."
---

# Redis OSS Cluster Flush All Keys

Use this skill when a user needs to remove all keys from an open-source Redis Cluster.

## Safety Rules

- `FLUSHALL` is destructive and cannot be undone. Require explicit confirmation of the exact cluster before final commands.
- Confirm backup/export status if recovery may be needed.
- Confirm this is Redis OSS Cluster, not Redis Software CRDB or another managed workflow with different flush semantics.
- Avoid putting passwords directly in shell history; prefer environment variables, ACL user handling, or secure secret injection.
- Schedule destructive flushes during a maintenance window for production.

## Why One FLUSHALL Is Not Enough

Redis OSS Cluster stores hash slots across multiple master shards. Running `FLUSHALL` against one node clears only that node's local dataset. A full cluster wipe requires flushing every master shard or using a cluster-aware client that fans out to masters.

## Preflight Checklist

Confirm:

- Cluster host and port.
- Authentication and ACL permissions for dangerous commands.
- Number of master shards.
- Whether the goal is all keys or only a prefix/subset.
- Backup/export decision.
- Maintenance window and application shutdown/drain plan.

## Manual Full Flush Workflow

Discover master shards:

```bash
redis-cli -c -h <cluster-host> -p <cluster-port> CLUSTER SLOTS
```

For each master shard returned, run:

```bash
redis-cli -h <master-host> -p <master-port> FLUSHALL
```

Include TLS, ACL, and authentication flags as required by the environment.

Verify from each master or through a cluster-aware scan that no keys remain.

## Cluster-Aware Client Workflow

Use a cluster-aware client only if it is known to fan out `FLUSHALL` to every master. Verify behavior in a non-production cluster first.

Example shape:

```python
from redis.cluster import RedisCluster

client = RedisCluster(host="<cluster-host>", port=<cluster-port>)
client.flushall()
```

Review the client library documentation for authentication, TLS, and fan-out semantics.

## Selective Deletion

For prefix cleanup such as `user:*`, do not issue multi-key deletes across slots. Use per-shard `SCAN` plus batched `UNLINK`, or a proven cluster-aware cleanup tool.

Pattern:

```bash
redis-cli -h <master-host> -p <master-port> --scan --pattern '<prefix>:*' \
  | xargs redis-cli -h <master-host> -p <master-port> UNLINK
```

Throttle batches for large keyspaces.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Keys remain | Only one master was flushed or replicas/masters were confused. |
| Permission denied | ACL user lacks `FLUSHALL` or dangerous-command permissions. |
| `redis-cli --cluster call` fails | Environment or CLI does not support the shortcut; connect to each master directly. |
| `CROSSSLOT` during cleanup | Multi-key delete spans slots; delete per shard or per key with `UNLINK`. |
| Latency spike during deletion | `FLUSHALL` or huge cleanup ran during traffic; use maintenance window or batched cleanup. |

## Escalation Packet

Collect:

- Redis version and cluster topology.
- `CLUSTER SLOTS` output with sensitive hostnames redacted if needed.
- Exact deletion goal: all keys or prefix subset.
- Backup/export status.
- Commands attempted and errors.
- ACL user permissions.
- Key counts before and after cleanup.
