---
name: redis-k8s-stale-info-active-change
description: "Triage Redis Software on Kubernetes when `rladmin status` shows stale info and the UI shows Active Change pending after applying RedisEnterpriseDatabase YAML. Use for REDB reconciliation failures, stuck database changes, N/A shard memory, pending or crashing pods, operator allocation errors, shard placement issues, and Kubernetes capacity misconfiguration."
---

# Redis Kubernetes Stale Info Active Change

Use this skill when a RedisEnterpriseDatabase is stuck after `kubectl apply`, `rladmin status` reports `ERROR: stale info`, or the Redis UI shows `Active Change pending`.

## Safety Rules

- Do not recommend force-deleting shards or editing Redis Enterprise metadata by hand.
- For production databases, collect evidence and prefer Redis Support escalation before destructive recovery.
- Only suggest deleting and recreating the REDB when the database is newly created and confirmed non-critical.
- Verify the namespace, cluster, and database name before giving commands.

## What the Symptoms Mean

| Symptom | Likely meaning |
| --- | --- |
| `ERROR: stale info` | Shard metadata has not refreshed because a shard, hosting node, or cluster communication path is unhealthy. |
| `Active Change pending` | A database configuration change is still incomplete or blocked. |
| `N/A` memory for shards | Shards may not have initialized, scheduled, or attached successfully. |
| Issue begins after `kubectl apply` | REDB spec may exceed capacity, request unsupported topology, or trigger an interrupted reconciliation. |

## Triage Workflow

1. Check REDB state:

   ```bash
   kubectl get redb -n <namespace>
   kubectl describe redb <database-name> -n <namespace>
   kubectl get redb <database-name> -n <namespace> -o yaml
   ```

   Look for failed conditions, allocation errors, stuck `Progressing`, invalid versions, and rejected spec fields.

2. Check pod scheduling and health:

   ```bash
   kubectl get pods -n <namespace> -o wide
   kubectl describe pod <pod-name> -n <namespace>
   ```

   Investigate `Pending`, `CrashLoopBackOff`, PVC binding failures, node selectors, taints, and CPU or memory pressure.

3. Check Redis Enterprise cluster state from a cluster node:

   ```bash
   rladmin status
   rladmin cluster status
   ```

   Confirm all nodes are online, quorum is healthy, and no hosting node is failed, unreachable, quorum-only, or under maintenance.

4. Map affected shards to hosting nodes. For each affected shard, verify the node has available memory and can run database shards.
5. Review the applied YAML for unsafe combinations:
   - Memory request exceeds available capacity.
   - Shard count is too high for available nodes.
   - Replication factor cannot be satisfied.
   - Redis version is unsupported.
   - Persistence settings are invalid.
   - Shard count and replication topology changed in one apply.
6. Check operator logs:

   ```bash
   kubectl logs deployment/redis-enterprise-operator -n <namespace>
   ```

   Look for allocation failures, scheduling failures, internal API errors, and resource constraint messages.

## Recovery Options

| Situation | Action |
| --- | --- |
| Clear REDB misconfiguration | Correct the YAML and reapply, then watch `kubectl get redb -w`. |
| Newly created non-critical database | Delete the REDB and recreate from corrected YAML. |
| Production data, CRDB, or Replica Of involved | Stop and escalate with evidence. |
| Node or pod health problem | Recover Kubernetes node, pod, PVC, or resource capacity first; then let reconciliation continue. |

## Prevention

- Validate capacity before scaling shards, replicas, or memory.
- Avoid combining shard-count and replication changes in one operation.
- Confirm every Redis Enterprise node is online before topology changes.
- Watch operator logs during REDB changes.
- Test topology changes in staging before production.

## Escalation Packet

Collect:

- Namespace, REC name, REDB name, and applied YAML.
- `kubectl describe redb` output.
- `kubectl get pods -o wide` and relevant `describe pod` output.
- Operator logs around the failed reconcile.
- `rladmin status` and `rladmin cluster status`.
- Affected shard IDs and hosting nodes.
- Whether the database is new, production, CRDB, or Replica Of.
- Support package when production data or cross-cluster replication is involved.
