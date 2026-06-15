---
name: redis-software-802-rollback-recovery
description: Use when Redis Software or Redis Enterprise Software 8.0.2 upgrade rollback or recovery is needed, including failed rolling upgrades, mixed-version nodes, unstable clusters after upgrade, database-level restore, CRDB FeatureSet or bad_featureset_version errors, Kubernetes REC upgrade failures, clusterRecovery patching, or post-upgrade TLS and module issues.
---

# Redis Software 8.0.2 Rollback Recovery

Use this skill for Redis Software 8.0.2 upgrade failures and recovery planning. Verify current release notes and support guidance before acting, because rollback behavior and fixed builds can change by patch level.

## Core Rule

Do not promise binary downgrade after an 8.0.2 upgrade. Recovery normally uses backups, node replacement, database restore, CRDB repair, Kubernetes recovery, or cluster recreation depending on failure scope.

## Guardrails

- Confirm valid backups before restore-based recovery.
- Capture state before changes: `rladmin status extra all`, database status, running actions, logs, and support bundle when possible.
- Pause, drain, or redirect client traffic where the recovery path requires it.
- Require explicit confirmation before node removal, database restore, cluster recreation, or Kubernetes patch actions.
- Use Redis Support for inconsistent cluster state, unclear backup validity, or suspected split-brain/data consistency risk.

## Recovery Path Selection

Choose the narrowest path that matches the failure:

- Failed rolling upgrade, one node cannot rejoin: replace-node recovery.
- Upgrade completed but cluster is unstable: full cluster restore or support-guided recovery.
- Only specific databases are affected: database-level restore.
- CRDB FeatureSet or module mismatch: CRDB configuration/module update workflow.
- Kubernetes REC stuck or pods restarting: Kubernetes recovery flow.

## Initial Diagnostics

Collect:

```text
rladmin status extra all
rladmin status bdbs
rladmin status databases extra all
rladmin cluster running_actions
rladmin info
```

For CRDB:

```text
crdb-cli crdb status
crdb-cli task list
```

For Kubernetes:

```text
kubectl get rec,pods,pvc -n <namespace>
kubectl describe rec <name> -n <namespace>
kubectl logs deploy/<operator-deployment> -n <operator-namespace>
```

## Recovery Patterns

Replace-node recovery:

- use when a rolling upgrade leaves one upgraded node unhealthy or unable to rejoin
- remove and replace only with a confirmed target node and supportable version path
- validate all nodes return OK

Database-level restore:

- use when only selected databases are unhealthy
- restore from the most recent valid backup
- validate shard layout and application connectivity

CRDB recovery:

- use when FeatureSet or module version mismatch blocks Active-Active state
- update CRDB module config only after confirming all participating clusters and versions
- validate all CRDB instances are active and synced

Kubernetes recovery:

- confirm operator and REC health
- inspect PVCs and resource constraints
- use `clusterRecovery` only when the installed operator and current guidance support it
- validate REC convergence and pod startup

## Post-Recovery Verification

Confirm:

- all nodes report OK
- databases are active and serving traffic
- CRDB instances are active and synchronized
- monitoring and metrics return to baseline
- clients reconnect normally
- version audit matches the expected recovered state
- no running actions remain unexpectedly

## Response Pattern

Answer with:

1. The failure scope and selected recovery path.
2. The state-capture commands.
3. Backup and traffic-control requirements.
4. The destructive action boundary requiring confirmation.
5. Post-recovery validation and support escalation criteria.
