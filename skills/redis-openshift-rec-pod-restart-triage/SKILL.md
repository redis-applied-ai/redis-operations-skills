---
name: redis-openshift-rec-pod-restart-triage
description: Use when Redis Enterprise or Redis Software pods in OpenShift restart repeatedly, enter CrashLoopBackOff, remain stuck Terminating, show OOMKilled exit 137, fail liveness/readiness probes, hit PVC mount or multi-attach errors, lose quorum after maintenance, or fail due to OpenShift SCC/RBAC/operator configuration.
---

# Redis OpenShift REC Pod Restart Triage

Use this skill to triage Redis Enterprise for Kubernetes or Redis Software pods running on OpenShift when pods restart, crash, or do not terminate cleanly.

## Safety Rules

- Capture state before deleting pods, editing finalizers, or changing cluster recovery settings.
- Drain or delete one Redis Enterprise Cluster pod at a time unless the user is intentionally decommissioning the cluster.
- Do not force-delete a majority of REC pods in a quorum-based cluster.
- Do not manually clear CCS, cluster tasks, or state-machine records unless Redis Support has explicitly directed the action.
- Verify the current Redis operator and OpenShift support matrix from official docs before making support-window claims.

## First Response

Ask for or collect:

- namespace, REC name, operator version, Redis version, OpenShift version, and deployment method
- exact pod state: `Restarting`, `CrashLoopBackOff`, `Terminating`, `Pending`, `ContainerCreating`, or probe failure
- recent node drains, upgrades, storage changes, SCC/RBAC edits, or forced pod deletions
- whether persistence is enabled and whether all expected PVCs still exist
- whether application impact is single-shard, database-wide, or cluster-wide

## Evidence Collection

Use `oc` in OpenShift. Use `kubectl` equivalents only when the environment is not OpenShift.

```bash
oc get rec,redb,reaadb -n <namespace>
oc get pods -n <namespace> -o wide
oc get events -n <namespace> --sort-by=.lastTimestamp
oc describe pod <pod> -n <namespace>
oc logs <pod> -n <namespace> --all-containers --previous
oc logs deploy/redis-enterprise-operator -n <operator-namespace>
oc get pvc,pv -n <namespace>
```

If the Redis log collector is available, run it with the correct namespace:

```bash
python log_collector.py -m all -n <namespace>
```

If collection is too slow, skip the large diagnostic archive first, then collect the archive later if needed:

```bash
python log_collector.py -m all -n <namespace> --skip_support_package
```

## Classify the Failure

### OOMKilled or Exit 137

Check pod events, container termination reason, node pressure, and Redis provisional memory.

```bash
oc describe pod <pod> -n <namespace>
oc describe node <node>
rladmin status extra all
```

Likely actions:

- increase pod/container memory requests and limits where appropriate
- reduce shard or database memory pressure before retrying disruptive maintenance
- move other workloads away from saturated worker nodes
- confirm persistence and replication before any restart-heavy recovery plan

### Pods Stuck Terminating

Look for unavailable worker nodes, preStop hooks that cannot finish, storage unmount failures, pending cluster actions, and Redis tasks such as node rejoin or replica attachment.

```bash
oc get pod <pod> -n <namespace> -o yaml
oc describe node <node>
rladmin cluster running_actions
rladmin status extra all
```

Likely actions:

- restore or recover the worker node if it still owns mounted storage
- wait for Redis state-machine actions to finish when they are progressing
- escalate before clearing stuck Redis tasks or editing finalizers
- only force-delete after confirming the node/container is gone and storage will not be mounted twice

### PVC or Mount Problems

Check for PVCs stuck Terminating, lost PV binding, storage class errors, and volume multi-attach events.

```bash
oc get pvc,pv -n <namespace>
oc describe pvc <pvc> -n <namespace>
oc describe pod <pod> -n <namespace>
```

Guidance:

- Redis Enterprise persistent storage should use supported block storage with a filesystem such as EXT4 or XFS.
- Treat NFS or shared filesystem use as a likely root cause unless current Redis guidance explicitly supports the exact configuration.
- PVCs may be expanded when the storage class allows it; do not plan a shrink operation.
- Do not delete PVCs while Redis processes are still active or a pod is still terminating.

### Probe Failures

For liveness or readiness failures, separate Redis process health from OpenShift networking and operator reconciliation.

Check:

- pod logs and previous container logs
- `oc describe pod` probe error text
- network policies, routes, DNS, and service endpoints
- operator logs for reconciliation errors
- API slowness or node pressure that delays probe responses

### SCC, RBAC, or Operator Errors

When pods fail immediately after REC creation or operator install, inspect OpenShift events and operator logs for permission errors.

Check:

- whether the expected SCC is present and bound to the REC service account when required by the installed Redis version and configuration
- whether automatic resource adjustment changes the SCC requirement for that version
- whether OLM or OperatorHub deployment assumptions require a specific REC service account or cluster name
- whether custom namespaces copied manifests without matching service account and role bindings

Do not assert version-specific SCC requirements without verifying the installed version and current Redis documentation.

### Lost Quorum or REC Recovery

When multiple REC pods are down or Terminating, treat the situation as a recovery workflow rather than a normal pod restart.

Before using recovery mode:

- confirm which pods are healthy and which PVCs still exist
- confirm persistence files are present and accessible
- capture operator logs, REC YAML, pod YAML, and events
- identify whether a majority of nodes was drained or deleted

Only recommend `clusterRecovery` when the current operator supports it and the PVC set is valid:

```bash
oc patch rec <cluster-name> -n <namespace> --type merge --patch '{"spec":{"clusterRecovery":true}}'
```

Escalate if PVCs are missing, REC cannot elect a leader, or databases remain inaccessible after the cluster returns.

## Output Format

When helping a user, return:

1. The most likely failure class.
2. The exact evidence that supports it.
3. The lowest-risk next command or change.
4. What not to do yet.
5. Escalation criteria and artifacts to attach if Redis Support is needed.

## Escalate When

- a majority of REC pods is down, Terminating, or force-deleted
- PVCs are missing, mounted to the wrong node, or suspected of data loss
- `rladmin cluster running_actions` shows stuck critical actions
- CCS or state-machine cleanup appears necessary
- the REC remains degraded after storage, resource, and SCC/RBAC issues are corrected
