---
name: redis-software-node-maintenance-patching
description: "Safely place Redis Enterprise Software nodes into maintenance mode for OS patching, reboot, hardware work, or node service maintenance. Use when the user asks how to patch Redis Software nodes, run `maintenance_mode on/off`, demote a master node, migrate shards off a node, preserve quorum, avoid multiple nodes in maintenance, restore snapshots, or verify node maintenance completion."
---

# Redis Software Node Maintenance Patching

Use this skill for planned Redis Enterprise Software node maintenance, OS patching, reboots, and hardware work.

## Safety Rules

- Maintain quorum. Do not place a majority of cluster nodes into maintenance at the same time.
- Work one node at a time unless Redis Support has approved a different plan.
- Never start maintenance, patching, or reboot on a new node while any previous node is still in maintenance, unhealthy, or not fully restored.
- Verify cluster health before and after each node.
- Confirm remaining nodes have enough CPU, memory, storage, and shard capacity before migrating shards.
- Contact Redis Support before complex or high-risk production maintenance.

## Stop Gate Checklist

Before giving any `maintenance_mode on`, patch, or reboot instruction for the target node, answer these checks:

- Is another node already in maintenance or quorum-only mode?
- Did the previous node fully exit maintenance and return to healthy `rladmin status`?
- Are enough nodes online to preserve quorum if the target node goes down?
- Do remaining nodes have enough CPU, memory, storage, and shard capacity?
- Is the target node the cluster master?
- Are Active-Active or ReplicaOf relationships healthy, if relevant?

If any previous node is still in maintenance or unhealthy, stop the rotation. Do not run `maintenance_mode on`, do not create or overwrite a target-node snapshot, and do not patch or reboot the target node. Restore the previous node first, verify cluster health, collect evidence, then resume one node at a time.

If the stop-gate facts are unknown, ask for `rladmin status`, `rladmin status nodes`, backup/capacity/master/sync status, and previous-node maintenance state first. Do not provide target-node `maintenance_mode on`, patch, or reboot commands until the operator has confirmed the gate passes.

## Preflight

1. Schedule a maintenance window and notify stakeholders.
2. Confirm recent backups exist for critical databases.
3. Run:

   ```bash
   rladmin status
   rladmin status nodes
   ```

4. Verify all nodes are healthy, no other node is in maintenance, and the cluster is stable.
5. Identify whether the target node is the current cluster master.
6. Check Active-Active or ReplicaOf sync health if relevant.
7. Confirm other nodes can absorb migrated shards and endpoints.

## Enter Maintenance Mode

Proceed only if the stop gate passes.

If the target node is the cluster master, demote it as part of entering maintenance:

```bash
rladmin node <node_id> maintenance_mode on demote_node
```

Standard maintenance entry with snapshot overwrite:

```bash
rladmin node <node_id> maintenance_mode on overwrite_snapshot
```

If replica migration should be prevented for a specific plan:

```bash
rladmin node <node_id> maintenance_mode on evict_ha_replica disabled evict_active_active_replica disabled
```

Verify with:

```bash
rladmin status
rladmin status nodes
```

Proceed only when the node is in maintenance mode and shard/endpoint migration is complete enough for the intended work.

## Patch Or Reboot

1. Apply OS patches or perform the planned hardware operation.
2. Reboot if required.
3. Wait for the node to return and Redis Enterprise services to stabilize.
4. Check logs and `rladmin status` before leaving maintenance mode.

## Exit Maintenance Mode

Standard exit:

```bash
rladmin node <node_id> maintenance_mode off
```

Restore a specific maintenance snapshot:

```bash
rladmin node <node_id> maintenance_mode off snapshot_name <snapshot_name>
```

Skip shard restore only when intentionally planned:

```bash
rladmin node <node_id> maintenance_mode off skip_shards_restore
```

List snapshots if needed:

```bash
rladmin node <node_id> snapshot list
```

## Verification

After each node:

- `rladmin status` shows node healthy and out of maintenance.
- No other node remains in maintenance before the next node starts.
- Shards and endpoints are balanced or in expected placement.
- Database availability and replication are healthy.
- Active-Active or ReplicaOf sync is healthy.
- Cluster alerts are resolved or understood.
- Application metrics remain normal.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Maintenance mode does not complete | Check resource capacity on remaining nodes and shard migration progress. |
| Previous node is still in maintenance | Stop the rotation; restore and verify the previous node before touching the next node. |
| Node was cluster master | Use demotion path or verify master has moved before node outage. |
| Quorum warning | Stop; do not proceed with additional nodes until quorum risk is resolved. |
| Shards do not restore | Check snapshot list, maintenance exit options, capacity, and logs. |
| Active-Active sync unhealthy | Pause node rotation and resolve sync before continuing. |

## Blocked Rotation Response

When a user asks to patch another node while a prior node is still in maintenance:

1. State that the next node is blocked and no patch, reboot, or `maintenance_mode on` command should run for it yet.
2. Explain that maintenance-mode quorum checks do not replace the one-node-at-a-time rule.
3. Direct the operator to restore or finish the previous node first, then verify with `rladmin status` and `rladmin status nodes`.
4. Preserve evidence: version, node IDs, current statuses, maintenance timestamps, commands already run, snapshot names, capacity output, `event_log.log`, `cluster_wd.log`, and node logs.
5. End with this terminal format: `Final summary: Do not patch node <target> while node <previous> remains in maintenance. Restore node <previous>, verify healthy status, then continue one node at a time.`

## Evidence To Collect

- Redis Enterprise version.
- Node ID and whether it was cluster master.
- `rladmin status` before/after.
- Maintenance commands run.
- Snapshot name if used.
- OS patch/reboot timestamps.
- Relevant `event_log.log`, `cluster_wd.log`, and node logs for failures.
