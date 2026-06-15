---
name: redis-software-node-offline-maintenance
description: Use when safely taking a Redis Software node offline for OS patching, reboot, hardware maintenance, upgrade, or replacement, including maintenance_mode on or off, shard and endpoint draining, cluster master migration, rladmin rebalance, CRDB traffic considerations, persistence sync checks, and post-maintenance cluster validation.
---

# Redis Software Node Offline Maintenance

Use this skill when a Redis Software node must be patched, upgraded, rebooted, or taken offline. Treat maintenance mode and reboot as operational changes requiring explicit target-node confirmation.

## Preflight Checks

Before starting:

- confirm target `node_id`
- confirm cluster is healthy
- confirm no other node is already in maintenance mode
- confirm backups or snapshots exist when required
- check persistence sync state if RDB or AOF is enabled
- check Active-Active CRDB participation
- inspect client connection distribution
- consider `rladmin rebalance` before maintenance if shards are uneven

Run:

```text
rladmin status
rladmin status extra all
```

## Maintenance Workflow

1. Enable maintenance mode on the target node:

```text
rladmin host <node_id> maintenance_mode on
```

2. If the target node is cluster master, move the role:

```text
rladmin cluster master set <other_node_id>
```

3. Validate the node is drained:

```text
rladmin status
```

The target node should not hold shards, endpoints, or the cluster master role before OS work begins.

4. Perform patching, upgrade, reboot, or hardware work.

5. After the node returns and is stable, disable maintenance mode:

```text
rladmin host <node_id> maintenance_mode off
```

6. Validate cluster health and balance.

## REST API Shape

If using the API, set the node maintenance flag through the supported node endpoint for the deployed Redis Software version. Verify endpoint path and payload in current docs before automation.

## CRDB And Persistence Notes

For CRDB-hosting nodes:

- verify replication and sync health before and after maintenance
- drain client traffic when the application design requires it
- confirm all regions remain active and synchronized

For persistent databases:

- verify RDB/AOF state before maintenance
- avoid maintenance during active backup or rewrite pressure where possible

## Post-Maintenance Validation

Confirm:

- node status is OK
- no shards or endpoints are stuck migrating
- cluster master is on an intended node
- databases are active
- CRDBs are synchronized, if applicable
- no maintenance alerts remain
- client latency, reconnects, and errors are normal

## Response Pattern

Answer with:

1. Target node confirmation.
2. Preflight health checks.
3. Maintenance-mode and master-role steps.
4. Drain validation before OS work.
5. Return-to-service validation after maintenance.
