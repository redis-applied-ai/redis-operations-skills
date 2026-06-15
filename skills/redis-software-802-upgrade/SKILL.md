---
name: redis-software-802-upgrade
description: "Plan and execute Redis Enterprise Software 8.0.2 cluster upgrades using in-place, extra-node rolling, or replace-node rolling methods. Use when the user asks about RS 8.0.2 upgrade prerequisites, direct upgrade paths, primary node ordering, load balancer or F5 sequencing, `rlcheck`, license/FQDN checks, backups and test restores, `rladmin cluster join/remove`, Active-Active CRDB database upgrades, Kubernetes operator upgrade constraints, post-upgrade validation, or troubleshooting mixed-version upgrade failures."
---

# Redis Software 8.0.2 Upgrade

Use this skill for Redis Enterprise Software 8.0.2 upgrade planning and execution. Before production execution, verify the current official release notes, upgrade path matrix, and Kubernetes release notes for the exact target patch level.

## Safety Rules

- Do not start until backups are complete and a restore has been tested.
- Freeze topology changes, scaling, migrations, database edits, and module changes during the upgrade.
- Confirm the current version supports the intended direct upgrade path.
- Upgrade one node at a time and validate health before continuing.
- If Redis is behind a load balancer such as F5, contact Redis Support before committing to primary/master-first sequencing; some configurations need a different order.
- For destructive operations such as `rladmin cluster remove node`, require explicit confirmation naming the node.
- In production, prefer rolling upgrade methods over simple in-place upgrades.

## Readiness Gates

Do not proceed to execution until every gate has a clear pass or an explicit Support-approved exception.

| Gate | Check | Blocker Example |
| --- | --- | --- |
| Supported path | Verify current and target versions against current Redis release notes. | Source version is older than the direct-upgrade minimum for the target build. |
| Cluster health | `rladmin status extra all` and `rladmin cluster running_actions`. | Any node, shard, endpoint, or action is not healthy or still running. |
| Admin access | `rlcheck`, `rladmin`, and root or equivalent access on every node. | Sudo, PATH, authentication, or shell access is unreliable. |
| Database versions | Inventory every database version before cluster upgrade. | Any database version is below the supported minimum for the target cluster release. |
| Modules and Redis Flex | Confirm only supported built-in modules and target-compatible Flash/Flex behavior. | Custom or deprecated modules remain, or a Redis version/Flash combination is unsupported. |
| License | Validate expiration, cluster FQDN match, shard limits, and capacity. | Expired license, wrong FQDN, or insufficient entitlement. |
| Backup and restore | Full backup for every database plus a test restore on staging. | Backup exists but restore has not been proven. |
| Change control | Maintenance window, owner approval, monitoring plan, and change freeze. | Automation, autoscaling, migration, or config tooling can still modify the cluster. |
| Node order | Primary/master node identified and sequence confirmed. | Load balancer path or topology makes standard primary-first sequencing unsafe. |

## Version And Compatibility Checks

- Verify the exact 8.0.2 build, supported source versions, and database-version matrix from current official release notes before production use.
- Treat the common planning baseline as: 7.8.x, 7.22.x, 7.4.x, and 6.4.x can be direct candidates, while older 6.2.x or 6.0.x clusters need an intermediate upgrade first.
- For databases, inventory the Redis version on each database. Plan remediation before cluster upgrade if a database is below the supported minimum.
- Redis 8 changed Search, JSON, time series, probabilistic data structures, module packaging, and ACL-category behavior; use the dedicated Redis 8 Search and ACL skills when applications depend on those command surfaces.
- Redis Flex / Flash compatibility must be checked against the target patch level before upgrading Flash-enabled databases.

## Preflight

1. Record cluster version, target package version, node list, and database versions.
2. Review official release notes and supported upgrade paths for the exact versions.
3. Run on every node where relevant:

   ```bash
   rlcheck
   rladmin status extra all
   rladmin cluster running_actions
   rladmin status nodes
   ```

4. Proceed only when shards are healthy and no running actions remain.
5. Identify the primary/master cluster node. Upgrade it first when the runbook requires that ordering.
6. Confirm SSH/console and root access on every node.
7. Confirm `/opt/redislabs/bin` is in `PATH` or plan to call commands by full path.
8. Validate database versions are compatible with the target cluster upgrade.
9. Check custom/deprecated modules for compatibility before upgrade.
10. Validate the license in Cluster Manager or the supported CLI/API path:
    - license is valid and not expired
    - license FQDN matches the cluster FQDN
    - shard and capacity limits cover the current and post-upgrade state
11. Capture audit and rollback evidence:
    - `rladmin info`
    - current module list and database versions
    - `/etc/opt/redislabs/` configuration snapshot, handled according to local security policy
    - monitoring dashboard exports or screenshots for before/after comparison
12. Label pre-upgrade backups with cluster, database, and date, then verify restore in staging.

## Method Selection

| Method | Use when | Notes |
| --- | --- | --- |
| In-place per node | Dev/test or small non-critical clusters | Simpler, but expect service impact per node. |
| Extra-node rolling | Production and HA when spare capacity exists | Add a clean new-version node, migrate/remove old node, repeat. |
| Replace-node rolling | No spare node capacity exists | Remove, reinstall, and rejoin the same node identity carefully. |

## In-Place Method

Per node:

1. Run `rlcheck` and `rladmin status extra all`.
2. Disable or pause external automation that may modify Redis during upgrade.
3. Install the target package as root:

   ```bash
   sudo ./install.sh
   ```

4. Validate:

   ```bash
   rlcheck
   rladmin status extra all
   ```

5. Continue to the next node only after the cluster returns to expected health.

## Extra-Node Rolling Method

1. Install the target Redis Enterprise version on a clean new node.
2. Join it to the cluster:

   ```bash
   rladmin cluster join
   ```

3. If needed, move primary/master responsibility according to the official runbook.
4. Remove one old-version node after confirming capacity and migration state:

   ```bash
   rladmin cluster remove node <node_id>
   ```

5. Repeat one node at a time until all nodes run the target version.

## Replace-Node Rolling Method

1. Confirm the node can be safely removed and restored.
2. Remove the old node:

   ```bash
   rladmin cluster remove node <node_id>
   ```

3. Uninstall/reinstall the target Redis Enterprise package if required.
4. Rejoin with replace-node:

   ```bash
   rladmin cluster join nodes <cluster_ip> \
     username <username> password <password> replace_node <node_id>
   ```

5. Validate before continuing to the next node.

## Active-Active / CRDB

- Upgrade participating cluster instances before database upgrades.
- Resolve module configuration mismatches before upgrading databases.
- Use the official current commands for CRDB/database upgrade. Common command shapes include:

  ```bash
  crdb-cli crdb update --crdb-guid <guid> --update-db-config-modules true
  rladmin upgrade db db:<id> preserve_roles latest_with_modules
  ```

- Accept protocol upgrade prompts only after confirming the planned upgrade path.

## Post-Upgrade Validation

- `rladmin status extra all` is healthy.
- `rladmin cluster running_actions` is empty.
- `rladmin info` shows expected version on all nodes.
- Databases accept client connections.
- License is active.
- Backups can run and restore.
- Prometheus/Datadog/Grafana metrics still flow.
- Application latency, errors, and throughput are normal.

## Troubleshooting

| Symptom | Check | Action |
| --- | --- | --- |
| Cluster hangs after wrong node order | Primary/master upgrade ordering | Pause and follow the official recovery path. |
| Change-master returns HTTP 406 | Node still bootstrapping | Wait for ready state and retry. |
| Shard migration errors | Mixed node versions or running actions | Complete node upgrades before migrations and clear actions. |
| Port conflict | Old Redis process remains | Inspect processes and restart Redis Enterprise services. |
| Buffer too small | Replication buffer sizing | Increase buffer before retrying the affected upgrade step. |
| Custom module failure | Unsupported/deprecated module | Remove or replace unsupported modules before proceeding. |
| PATH lost | Environment not updated | Add `/opt/redislabs/bin` or use full command paths. |

## Evidence To Collect

- Current and target versions.
- Official release notes/upgrade path checked.
- License validity, FQDN match, and capacity/shard entitlement state.
- Node list and primary/master node.
- Load balancer or F5 presence and Support guidance if applicable.
- `rlcheck`, `rladmin status extra all`, and running actions output.
- Backup and test-restore evidence.
- `rladmin info`, module list, database versions, and config snapshot reference.
- Commands executed and timestamps.
- Error logs and support bundle if failure occurs.
