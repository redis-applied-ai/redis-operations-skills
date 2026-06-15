---
name: redis-k8s-lost-quorum-upgrade-recovery
description: Use when Redis Enterprise for Kubernetes or OpenShift loses quorum after an Operator, Kubernetes, OpenShift, or cluster upgrade, REC is degraded with no master, pods run without leader election, databases are inactive after upgrade, or rladmin quorum recovery must be planned with safety guardrails.
---

# Redis Kubernetes Lost Quorum Recovery

Use this skill for Redis Enterprise for Kubernetes or OpenShift quorum loss after upgrade activity. Treat this as a high-risk recovery workflow: collect state first, avoid broad restarts or deletes, and escalate to Redis Support when quorum cannot be restored cleanly.

## Guardrails

Do not recommend these actions as first-line recovery:

- deleting Redis Enterprise pods blindly
- scaling down the StatefulSet
- recreating the REC resource
- restarting all nodes at once
- running simultaneous recovery attempts from multiple pods

These can extend downtime, increase split-brain risk, or make data recovery harder.

## Initial State Capture

Collect before changing anything:

```text
kubectl get pods -n <namespace>
kubectl get rec -n <namespace>
kubectl get nodes
kubectl get pvc,pv -n <namespace>
kubectl describe rec <rec-name> -n <namespace>
```

For OpenShift, use `oc` equivalents and also check SCC and operator permissions.

Confirm:

- Redis Enterprise pods exist
- REC is degraded or has no master
- nodes are Ready and schedulable
- PVCs are Bound and attached
- Operator pod is running
- CRDs are present and healthy

## Quorum Reasoning

Quorum requires a majority of nodes: `floor(N / 2) + 1`.

Before recovery, verify enough valid nodes and attached volumes exist to form a majority. If storage is missing, nodes are NotReady, or pod state is inconsistent, fix infrastructure first.

## Recovery Node Selection

Choose one stable Redis Enterprise pod:

- not crash-looping
- attached to healthy storage
- not newly recreated if older stateful pods are available
- on a healthy node
- likely to have the most recent cluster state

Avoid pods stuck initializing, pods on nodes with volume problems, and recently restarted pods if a more stable candidate exists.

## Recovery Workflow

1. Capture state and logs.
2. Validate infrastructure health.
3. Select exactly one recovery pod.
4. Exec into that pod:

```text
kubectl exec -it <redis-enterprise-pod> -n <namespace> -- bash
```

5. Use the `rladmin` recovery command appropriate for the installed Redis Enterprise version. Confirm the exact command from official version-specific docs or Redis Support when uncertain.
6. If stale or unreachable nodes must be removed, treat that as a destructive recovery step and require explicit confirmation with the target node names.
7. After quorum is restored, let the Operator reconcile. Do not keep manually restarting pods while reconciliation is in progress.

## Validation

After recovery:

- REC returns to a healthy state
- Redis Enterprise pods are Ready
- Admin Console shows a healthy cluster
- all expected nodes are present or intentionally removed
- databases are Active
- modules are loaded
- representative reads and writes succeed
- Operator logs show reconciliation settling

## Escalation

Contact Redis Support when:

- quorum cannot be restored
- recovery command fails repeatedly
- cluster state looks inconsistent
- there is any split-brain concern
- database state remains inactive after quorum returns

Provide Operator logs, Redis Enterprise pod logs, REC YAML, events, node/PVC state, and a timeline of upgrade and recovery actions.

## Response Pattern

Give the user:

1. A no-touch state-capture command set.
2. The quorum and infrastructure checks.
3. Criteria for selecting one recovery pod.
4. The version-verified recovery path.
5. Validation and escalation criteria.
