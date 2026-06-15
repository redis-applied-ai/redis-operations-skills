---
name: redis-software-cluster-upgrade
description: "Plan and execute general Redis Software cluster upgrades, including supported upgrade path checks, primary/master node ordering, in-place upgrades, extra-node rolling upgrades, replace-node rolling upgrades, database upgrades, Active-Active CRDB considerations, post-upgrade validation, and common failures such as running actions, port conflicts, buffer sizing, shard migration errors, or cluster hang after wrong node order."
---

# Redis Software Cluster Upgrade

Use this skill for Redis Software cluster upgrade planning and execution when the request is not specific to a dedicated release skill. For Redis Software 8.0.2, prefer `redis-software-802-upgrade` because that release has version-specific constraints and recovery guidance.

## Core Rules

- Verify the current official upgrade path matrix before choosing source, intermediate, and target versions.
- Do not skip unsupported major-version steps. If a direct path is not supported, plan intermediate upgrades.
- Upgrade one node at a time and wait for cluster health before continuing.
- Do not proceed while `rladmin cluster running_actions` shows active work.
- Do not perform topology changes, shard migrations, scaling, or configuration edits during the upgrade unless they are part of the approved runbook.
- Keep recent tested backups available; rollback planning must not depend on untested backup files.
- Redis for Kubernetes follows a separate operator and platform lifecycle; use Kubernetes-specific Redis skills for REC/REDB upgrades.

## Preflight Checklist

1. Identify:
   - current cluster version
   - target Redis Software version
   - node list and primary/master node
   - database versions
   - Active-Active or CRDB participation
   - custom modules or Redis Flex/Flash usage
2. Confirm the supported upgrade path in current Redis documentation.
3. Review release notes for every intermediate and target version.
4. Confirm database compatibility. Upgrade databases first if the target cluster release requires it.
5. Confirm root or equivalent administrative access and working command access:

   ```bash
   rlcheck
   rladmin
   ```

6. Check health:

   ```bash
   rladmin status extra all
   rladmin cluster running_actions
   rladmin status nodes
   ```

7. Proceed only when nodes, shards, and endpoints are healthy and no running actions remain.
8. Identify the primary/master node from Cluster Manager, `rladmin status nodes`, or the supported REST/API path.
9. Confirm backups are complete and a restore has been tested.
10. Pause external automation, monitoring remediation, autoscaling, and deployment pipelines that can modify Redis during the window.

## Method Selection

| Method | Use When | Tradeoff |
| --- | --- | --- |
| In-place per node | Smaller or lower-risk environments that can tolerate interruption per node | Simple, but each node is changed in place. |
| Extra-node rolling | Production clusters with spare capacity or ability to add nodes | Lower service risk, but needs additional nodes and capacity planning. |
| Replace-node rolling | Production clusters without spare nodes | Maintains rolling pattern but requires careful remove, reinstall, and replace-node join. |

## In-Place Upgrade

For each node, one at a time:

1. Run local checks:

   ```bash
   rlcheck
   rladmin status extra all
   ```

2. Download and extract the target package from the approved Redis distribution source.
3. Run the installer as root:

   ```bash
   sudo ./install.sh
   ```

4. Validate the node and cluster:

   ```bash
   rlcheck
   rladmin status extra all
   rladmin cluster running_actions
   ```

5. Continue to the next node only after the cluster returns to expected health.

## Rolling Upgrade

### Extra-Node Method

1. Install the target Redis Software version on a clean new node.
2. Join the new node to the cluster using the supported cluster join flow.
3. Update DNS or client routing only if the approved plan requires it.
4. Promote or move primary/master responsibility only through supported steps.
5. Remove old-version nodes one at a time after capacity, shard placement, and health checks pass.
6. Repeat until every node runs the target version.

### Replace-Node Method

For each old-version node:

1. Confirm the node can be safely removed and later replaced.
2. Remove the node with explicit operator confirmation naming the node ID.
3. Uninstall or reinstall Redis Software according to the supported procedure.
4. Rejoin the node as a replacement:

   ```bash
   rladmin cluster join nodes <cluster_member_ip_address> \
     username <username> password <password> replace_node <node_id>
   ```

5. Validate:

   ```bash
   rlcheck
   rladmin status extra all
   rladmin cluster running_actions
   ```

## Database And CRDB Steps

- Some cluster features are available only after all nodes run the target version.
- For Active-Active deployments, upgrade all participating cluster instances before upgrading databases.
- Upgrade databases only after the cluster state and version mix are safe for database upgrade.
- Use the current supported database upgrade command for the installed version. A common command shape is:

  ```bash
  rladmin upgrade db db:<db_id> preserve_roles latest_with_modules
  ```

- For CRDBs, answer protocol upgrade prompts only after confirming every participating cluster is healthy and ready.

## Post-Upgrade Validation

- All nodes report the expected target version.
- `rladmin status extra all` is healthy.
- `rladmin cluster running_actions` is empty.
- Databases accept client connections.
- Active-Active replication and CRDB sync are healthy, if applicable.
- Backups still run and restore.
- Monitoring and alerting continue to receive metrics and logs.
- Application latency, error rate, throughput, and reconnect behavior match the expected post-change baseline.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Running action stuck before upgrade | Background operation or failed task remains | Resolve or escalate before continuing. |
| Port conflict after upgrade | Old Redis process remains | Stop supported services cleanly, inspect processes, and restart according to Redis guidance. |
| Buffer too small | Replication or sync buffer cannot handle dataset movement | Increase the relevant buffer before retrying the affected step. |
| Shard migration errors | Mixed node versions or cluster still converging | Finish node upgrades and wait for health before moving shards. |
| Cluster hangs after wrong node order | Primary/master sequencing was not followed | Stop further changes and use the appropriate recovery or rollback skill. |
| Commands unavailable | PATH or shell profile changed | Use full paths under `/opt/redislabs/bin` or restore supported PATH configuration. |

## Evidence To Collect

- Current, intermediate, and target versions.
- Upgrade path matrix confirmation.
- Node list, primary/master node, and chosen upgrade method.
- `rlcheck`, `rladmin status extra all`, `rladmin status nodes`, and running-actions output.
- Backup and test-restore evidence.
- Database versions and module inventory.
- Active-Active/CRDB topology and sync state.
- Commands executed with timestamps.
- Relevant logs such as cluster watchdog, supervisor, and Redis database logs.
