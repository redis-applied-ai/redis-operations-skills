---
name: redis-k8s-rec-pod-restart-triage
description: Use when Redis Enterprise for Kubernetes REC pods restart repeatedly, show CrashLoopBackOff, stay 1/2 Ready, OOMKill with exit 137, fail probes, loop during clusterRecovery, cannot elect a master, get stuck Terminating, or degrade after node drain, upgrade, storage, PVC, operator, RBAC, or quorum issues.
---

# Redis Kubernetes REC Pod Restart Triage

Use this skill to triage repeated Redis Enterprise for Kubernetes pod restarts before choosing a recovery path. The goal is to classify the restart pattern, stabilize Kubernetes infrastructure, and avoid recovery actions that make quorum or storage problems worse.

## Safety Rules

- Collect diagnostics before deleting pods, patching REC recovery flags, or changing StatefulSet-owned resources.
- Stop maintenance if multiple REC pods are unhealthy or a majority may have been restarted.
- Do not delete PVCs unless Redis Support has explicitly approved the action.
- Do not repeatedly toggle `clusterRecovery`; fix the blocking infrastructure issue first.
- If persistence is disabled and quorum is lost, warn that REC state may not be recoverable.

## First Checks

```bash
kubectl get rec -n <namespace>
kubectl get pods -n <namespace> -o wide
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl describe pod <redis-pod> -n <namespace>
kubectl logs <redis-pod> -n <namespace> --all-containers --tail=200
kubectl logs <redis-pod> -n <namespace> --all-containers --previous --tail=200
```

Record:

- REC status and whether it is degraded
- pod phase, readiness count, restart count, and node placement
- last termination reason and exit code
- whether the operator is healthy
- whether persistence is enabled
- recent upgrades, node drains, storage changes, or forced pod deletions

## Classify The Restart Pattern

| Pattern | Likely Class | First Action |
| --- | --- | --- |
| `OOMKilled` or exit `137` | memory pressure or node resource contention | inspect pod limits, node pressure, and Redis memory state |
| `1/2` Ready with bootstrapper waiting for master | quorum or bootstrap problem | check REC status, persistence, and number of healthy pods |
| `CrashLoopBackOff` with mount errors | PVC or storage attachment problem | inspect PVC/PV, node attachment, and storage events |
| recovery stuck in `RecoveringFirstPod` or `RecoveryReset` | recovery cannot bootstrap from storage | validate first pod, PVC contents, and volume attachment |
| pod stuck `Terminating` | node, preStop, storage unmount, or cluster task issue | inspect node, pod finalizers, and Redis running actions |
| operator restarts repeatedly | Kubernetes API, RBAC, or operator config issue | fix operator health before changing REC |

## Operator Health

```bash
kubectl get pods -n <operator-namespace> | grep redis-enterprise-operator
kubectl logs deployment/redis-enterprise-operator -n <operator-namespace> --all-containers --tail=200
```

If the operator is unstable, focus on Kubernetes API availability, RBAC, service account permissions, and operator pod resources before editing REC specs.

## Node And Scheduling Checks

```bash
kubectl get nodes
kubectl describe node <node-name>
kubectl get pod <redis-pod> -n <namespace> -o yaml
```

Resolve:

- CPU, memory, disk, or PID pressure
- taints, tolerations, affinity, and anti-affinity mismatches
- unavailable worker nodes after maintenance
- multiple Redis pods restarted at the same time
- pending pods caused by insufficient resources or PVC scheduling

## Storage And Persistence Checks

```bash
kubectl get pvc,pv -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>
kubectl describe pod <redis-pod> -n <namespace>
```

Check that PVCs are bound, mounted on the expected nodes, and not blocked by multi-attach or filesystem errors. If storage settings changed, verify they still match what the operator and StatefulSet expect; immutable storage fields cannot usually be changed in place.

## Quorum And Recovery Gate

Suspect quorum loss when multiple pods are not Ready, bootstrap cannot elect a master, or the REC remains degraded after Kubernetes infrastructure is stable.

Before recommending recovery:

- infrastructure is stable
- operator is healthy
- enough pods can start for recovery to proceed
- persistence is enabled and all expected PVCs are present
- current Redis Kubernetes docs support the chosen recovery method for the installed operator

If those conditions are met, patch recovery once and monitor:

```bash
kubectl patch rec <cluster-name> -n <namespace> --type merge --patch '{"spec":{"clusterRecovery":true}}'
kubectl get rec -n <namespace> -w
kubectl get pods -n <namespace> -w
```

Escalate if recovery loops, the first pod cannot start, PVCs are missing, or the cluster cannot elect a leader.

## Pods Stuck Terminating

Check Redis and Kubernetes state:

```bash
kubectl exec -it <redis-pod> -n <namespace> -- rladmin status extra all
kubectl exec -it <redis-pod> -n <namespace> -- rladmin cluster running_actions
kubectl get pod <terminating-pod> -n <namespace> -o yaml
kubectl describe node <node-name>
```

Do not force-delete as a default response. First determine whether the node is gone, the volume is still mounted, or Redis has unfinished actions. Escalate before clearing stuck actions or editing finalizers.

## Diagnostics

Collect logs early:

```bash
python3 log_collector.py -m all -n <namespace>
```

If collection is slow, collect lightweight diagnostics first:

```bash
python3 log_collector.py -m all -n <namespace> --skip_support_package
```

If the collector is unavailable and a Redis pod is reachable:

```bash
kubectl exec -it <redis-pod> -n <namespace> -- /opt/redislabs/bin/debuginfo
```

## Validate Stabilization

```bash
kubectl get rec -n <namespace>
kubectl get pods -n <namespace>
kubectl exec -it <redis-pod> -n <namespace> -- rladmin status
```

Confirm:

- REC is Running or healthy for the installed version's status fields
- Redis pods are Running and Ready
- restart counts stop increasing
- operator logs no longer show reconciliation failures
- databases and endpoints are reachable

## Response Shape

When advising a user, state:

1. The restart class.
2. The evidence that supports that class.
3. The lowest-risk next check or fix.
4. Whether recovery is safe yet.
5. What evidence to attach for Redis Support if escalation is needed.
