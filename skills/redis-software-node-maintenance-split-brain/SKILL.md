---
name: redis-software-node-maintenance-split-brain
description: "Prevent and triage Redis Software split-brain risk from incomplete node maintenance. Use when the user asks how to put a node into maintenance mode, service or reboot a node, demote a master node, verify shard migration, avoid quorum loss, fix maintenance mode failures, resolve shard imbalance after maintenance, or handle split-brain, network partition, or too many nodes offline."
---

# Redis Software Node Maintenance Split Brain

Use this skill when planning or troubleshooting Redis Software node maintenance where quorum, shard migration, or split-brain risk matters.

## Safety Rules

- Do not take multiple nodes down without verifying quorum and capacity.
- Do not perform maintenance until shards and endpoints have migrated away from the node.
- If quorum is lost or split-brain is suspected, stop changes and escalate to Redis Support.
- Capture status before and after maintenance.
- Follow Redis Software maintenance mode instead of ad hoc shutdowns.

## Preflight Checks

1. Confirm the target node ID and role.
2. Check cluster health:

   ```bash
   rladmin status
   rladmin status extra all
   rlcheck
   ```

3. Confirm remaining nodes can host migrated shards.
4. Confirm no pending migrations or active cluster actions.
5. Confirm maintenance window and owner approval.
6. Confirm the node is not required for quorum.

## Maintenance Workflow

If the target is a master, demote or use maintenance mode with demotion behavior:

```bash
rladmin node <node-id> maintenance_mode on demote_node
```

For normal maintenance mode:

```bash
rladmin node <node-id> maintenance_mode on overwrite_snapshot
```

Verify migration:

```bash
rladmin status extra all
```

Proceed with OS, hardware, network, or reboot work only after migration is complete.

Disable maintenance mode:

```bash
rladmin node <node-id> maintenance_mode off
```

Verify:

```bash
rladmin status
rladmin verify balance
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Maintenance mode fails | Insufficient capacity, quorum risk, pending migrations, or unhealthy cluster. |
| Shards still on node | Migration incomplete; do not proceed with maintenance. |
| Shard imbalance after maintenance | Run balance verification and use supported rebalance process if needed. |
| Too many nodes offline | Stop maintenance and escalate; quorum/split-brain risk is high. |
| Cluster partitions or divergent behavior | Treat as possible split-brain and contact Redis Support. |

## API Health Check

Use the REST health check when appropriate:

```bash
curl -s -k -u "$username:$password" https://<fqdn>:9443/v1/cluster/check
```

Handle credentials securely and avoid exposing them in logs.

## Escalation Packet

Collect:

- Redis Software version and cluster name.
- Target node ID and role.
- Maintenance timeline and commands run.
- `rladmin status`, `status extra all`, and `rlcheck`.
- `rladmin verify balance` output.
- Running actions or migration state.
- Nodes offline and quorum status.
- Any network partition or split-brain symptoms.
