---
name: redis-k8s-rec-degraded-recovery
description: "Recover Redis Enterprise for Kubernetes when a RedisEnterpriseCluster is degraded, Redis pods are unreachable, not Ready, Pending, CrashLoopBackOff, or quorum is lost. Use when the user asks about REC degraded status, pod scheduling/storage/readiness failures, node drain PDB errors, operator reconciliation stuck, or when to run `rladmin cluster recover` from a Redis pod."
---

# Redis Kubernetes REC Degraded Recovery

Use this skill when a RedisEnterpriseCluster (REC) is degraded or Redis Enterprise pods/nodes are unreachable.

## Core Rule

REC degradation is often caused by Kubernetes infrastructure, scheduling, storage, or pod health. Fix those first. Run `rladmin cluster recover` only when quorum is lost and pod/node/network/storage issues have been corrected.

## First Checks

```bash
kubectl get rec -n <namespace>
kubectl get pods -n <namespace> -o wide
```

Identify:

- REC Healthy vs Degraded.
- Pods not `Running`.
- Pods not `Ready`.
- Pending pods.
- CrashLoopBackOff.
- Node placement and unavailable nodes.

## Pod Investigation

For each unhealthy pod:

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --all-containers --tail=200
```

Look for:

- PVC attach/mount errors.
- Insufficient CPU/memory.
- Taints, affinity, or scheduling constraints.
- Node pressure.
- Readiness/liveness probe failures.
- Crash or startup errors.
- REC spec or secret/config mismatch.

## Recovery Sequence

1. Fix scheduling, capacity, storage, node, and network issues.
2. Let the Redis Enterprise Operator reconcile.
3. Recheck pod readiness and REC status.
4. If quorum is lost after infrastructure is healthy, run cluster recovery from a stable Redis pod:

   ```bash
   kubectl exec -it <redis-enterprise-pod> -n <namespace> -- rladmin cluster recover
   ```

5. Wait for cluster state to stabilize.
6. Validate REC and pods again.

## Troubleshooting Matrix

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Pods `Pending` | Capacity, taints, affinity, PVC, or scheduling constraints | Add capacity or fix scheduling/storage constraints. |
| Pods `CrashLoopBackOff` | Config, secret, storage, runtime, or service startup failure | Inspect logs and events; fix root cause before recovery commands. |
| REC remains Degraded | Unhealthy pods or quorum loss | Fix pods first; recover quorum only if needed. |
| Node drain blocked by PDB | Redis pods not healthy enough for disruption | Restore readiness before retrying drain. |
| Operator changes not applying | Reconciliation blocked by pod/REC/infrastructure issue | Inspect operator logs and Kubernetes events. |

## Validation

```bash
kubectl get rec -n <namespace>
kubectl get pods -n <namespace>
kubectl exec -it <redis-enterprise-pod> -n <namespace> -- rladmin status
```

Confirm:

- REC status is healthy.
- All Redis pods are `Running` and `Ready`.
- Cluster status is healthy.
- Databases and endpoints are reachable.

## Avoid

- Deleting Redis pods or PVCs as a first response.
- Running `rladmin cluster recover` before fixing infrastructure.
- Editing generated resources directly when the operator owns them.
- Draining more nodes while REC is already degraded.

## Evidence To Collect

- REC YAML/status.
- Pod list with node placement.
- `describe pod` output for failing pods.
- Recent Kubernetes events.
- Operator logs.
- Storage/PVC status.
- `rladmin status` from a healthy Redis pod if available.
