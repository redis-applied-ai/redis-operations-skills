---
name: redis-software-disk-failure-shard-evacuation
description: "Safely evacuate shards from a Redis Software node after disk failure, AOF fsync/write errors, input/output errors, missing logs, failed persistence paths, or rebuilt empty disks; guide maintenance mode, capacity checks, quorum protection, node removal/replacement, clean reinstall, rejoin, rebalance, DNS updates, validation with `rlcheck` and `rladmin status extra all`, and recovery pitfalls such as maintenance-mode stacking or installer upgrade remnants."
---

# Redis Software Disk Failure Shard Evacuation

Use this skill when a Redis Software node has disk or persistence-path failure and the safest path is to move shards off the node, repair or rebuild the host, then return capacity to the cluster in a controlled way.

## Safety Rules

- Prioritize shard evacuation before in-place disk repair when the node still hosts shards.
- Do not manually clean Redis directories, persistence files, or packages while the node is still an active cluster member hosting shards.
- Confirm remaining nodes have enough CPU, memory, shard, and storage capacity before evacuation.
- Do not put multiple nodes into maintenance in a way that risks quorum loss or removes too much shard capacity.
- Maintenance mode can be stacked; if enabled multiple times, it must be disabled the same number of times.
- Node removal, node replacement, and rebalance operations are production-impacting. Require explicit confirmation naming the node ID or database ID before destructive actions.
- If AOF or persistence errors prevent safe shard movement, stop and escalate; do not disable persistence or apply advanced workarounds without Support-approved steps.

## Failure Signals

Treat these as disk or persistence-path failure until proven otherwise:

- OS `Input/output error`
- AOF errors such as failed `fsync` or write failures
- persistence directories unreadable or missing
- Redis logs missing because log paths were on the failed disk
- disk replaced and filesystem rebuilt, leaving Redis paths empty
- installer behaves like an upgrade on a supposedly clean host

## Preflight

1. Identify target node ID, hostname, IP, and role.
2. Capture current state:

   ```bash
   rladmin status extra all
   rladmin status shards
   rladmin cluster running_actions
   ```

3. Confirm no existing maintenance operation or running action blocks evacuation.
4. Verify capacity on other nodes for the target node's shards and endpoints.
5. Confirm backup and persistence expectations for affected databases.
6. Decide whether the node can be repaired in place or must be rebuilt as effectively new hardware.

## Preferred Path: Maintenance Mode Evacuation

Use Cluster Manager UI when available.

1. Put the failing node into maintenance mode.
2. Monitor until shards and endpoints migrate away from the node.
3. Confirm the node is not hosting serving shards before host repair.
4. Keep the node out of normal placement until disk repair or rebuild completes.

CLI shape, only when this matches the local runbook and version:

```bash
rladmin node <node_id> maintenance_mode on overwrite_snapshot
rladmin status
```

Maintenance mode performs quorum checks, but still confirm no other node is already in maintenance or degraded.

## Capacity-Constrained Evacuation

If the cluster cannot move every shard:

- Stop and reassess capacity before continuing.
- Avoid leaving the only healthy replica on the failing node.
- If the runbook offers an option to avoid evicting replica shards, use it only with explicit availability and durability risk acceptance.
- Consider adding capacity or moving lower-risk workloads before repairing the disk.

## Repair Or Rebuild Host

After evacuation:

1. Replace failed disk or repair the storage path with the infrastructure team.
2. Rebuild and remount filesystems with supported ownership, mount options, and persistence paths.
3. If Redis installation or persistence paths were affected, assume local Redis data is not trustworthy.
4. Prefer clean reinstall and re-add when Redis paths were lost or corrupted.

If reinstall acts like an upgrade, such as refusing socket-path configuration, old packages or directories remain. Clean residual Redis Software artifacts according to the official uninstall/reinstall procedure before installing again.

## Remove Or Replace Node

Use the Cluster Manager UI when possible.

If the node is effectively empty or rebuilt:

1. Remove or replace the old node entry from the cluster after resources are moved away.
2. Install the correct Redis Software version on a clean, supported OS.
3. Add the node back through the supported add-node or replace-node flow.
4. Verify the node before accepting it into service.

CLI removal shape, only after explicit confirmation:

```bash
rladmin node <node_id> remove
```

For rejoin/recovery, install the same Redis Software version and build as the cluster unless following an approved upgrade path.

## Rebalance And DNS

After the node is healthy and back in the cluster:

1. Rebalance shard placement according to the placement policy.
2. Use the supported UI or API path, such as database rebalance action, when appropriate:

   ```text
   PUT /v1/bdbs/{uid}/actions/rebalance
   ```

3. If DNS records reference nodes directly, update records for replaced nodes.
4. Confirm endpoints and clients use the intended DNS names rather than stale node IPs.

## Validation

Validate before returning the node to normal service:

```bash
rlcheck
rladmin status extra all
rladmin status shards
rladmin cluster running_actions
```

Expected state:

- node is healthy
- cluster, endpoints, and shards are OK
- no unexpected running actions remain
- AOF write/fsync errors are gone
- disk, mount, and filesystem metrics are healthy
- shard placement is balanced or intentionally skewed
- application latency and errors return to baseline

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| `Input/output error` on Redis paths | Disk or filesystem failure | Evacuate shards before repair; collect state if possible. |
| AOF `fsync` or write failures | Persistence path unstable | Evacuate; escalate if writes prevent shard movement. |
| Maintenance mode will not activate | Quorum or capacity risk | Add capacity, fix degraded nodes, or get Support-guided plan. |
| Shards remain on node | Capacity constraint, running action, or migration failure | Inspect `running_actions`, shard status, and capacity before retry. |
| Installer thinks clean host is an upgrade | Old packages/directories remain | Complete supported cleanup and reinstall. |
| Node returns but placement is uneven | Shards were not rebalanced | Run approved rebalance workflow and validate. |
| DNS points to old node | Node replacement changed address | Update DNS and verify client resolution. |

## Escalation Packet

Collect:

- Node ID, hostname, IP, and Redis Software version.
- Disk error text and first timestamp.
- AOF or persistence error messages.
- `rladmin status extra all`, `rladmin status shards`, and running-actions output.
- Whether maintenance mode was attempted and result.
- Capacity available on remaining nodes.
- Whether Redis paths were on the failed disk.
- Reinstall/removal/rejoin steps already performed.
- Current shard placement and any DNS changes.

## Response Shape

When helping a user:

1. Confirm disk failure signals and whether the node still hosts shards.
2. State the safest next action: evacuate, repair/rebuild, rejoin, rebalance.
3. Ask for explicit confirmation before node removal or destructive cleanup.
4. Route advanced persistence-workaround cases to Support.
5. Finish with validation commands and success criteria.
