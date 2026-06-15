---
name: redis-kubernetes-support-router
description: Use when a user asks broad Redis for Kubernetes questions and you need to route between deployment, Redis Enterprise Cluster configuration, REDB or REAADB management, operator reconciliation, database changes reverting, REC degraded states, pod scheduling, storage, rack awareness, Istio ingress, replication link down, monitoring, or Kubernetes/OpenShift troubleshooting.
---

# Redis For Kubernetes Support Router

Use this skill to classify Redis for Kubernetes questions and route to the right operator, custom-resource, infrastructure, or database workflow.

## Classify The Request

Route into one of these tracks:

- Deployment and setup: operator install, namespaces, CRDs, Redis Enterprise Cluster creation, licensing, and initial validation.
- Configuration and management: REDB, REAADB, REC settings, secrets, certificates, rack awareness, ingress, and service exposure.
- Reconciliation behavior: database changes reverting because Kubernetes custom resources remain the source of truth.
- Troubleshooting: degraded REC, unreachable nodes, replication link down, stale info, active-change-pending, PVC or scheduling problems.
- Networking: DNS, Istio, ingress, services, TLS, wildcard hostnames, and client access paths.
- Monitoring and performance: operator logs, Redis Enterprise metrics, Prometheus, Grafana, pod lifecycle, and resource pressure.

## Intake Checklist

Ask for:

- Kubernetes distribution and version, or OpenShift version
- Redis Enterprise operator version
- namespace and resource names
- whether the target is REC, REDB, REAADB, or application connectivity
- exact custom resource YAML or relevant fields
- `kubectl get` and `describe` output for affected resources
- pod status, events, PVC status, and operator logs
- recent changes by UI, CLI, `kubectl apply`, Helm, GitOps, or operator upgrade

## First Diagnostics

Use the relevant namespace:

```text
kubectl get rec,redb,reaadb -n <namespace>
kubectl get pods,pvc,svc,ingress -n <namespace>
kubectl describe rec <name> -n <namespace>
kubectl logs deploy/<operator-deployment> -n <operator-namespace>
```

Use `oc` equivalents on OpenShift.

## Routing Guidance

- If changes revert, inspect the Kubernetes custom resource and GitOps source before editing through UI or CLI.
- If REC is degraded, check nodes, pods, PVCs, operator logs, and events before any manual recovery.
- If a database is stuck in active-change-pending or stale state, compare desired custom resource status with Redis Enterprise internal state.
- If networking fails, inspect services, ingress, DNS, TLS, and service mesh policy from the pod network, not only the client machine.
- If rack awareness fails, confirm Kubernetes labels, node placement, anti-affinity, and operator reconciliation status.

## Safety Rules

- Do not delete PVCs, recreate REC resources, scale StatefulSets, or restart all Redis Enterprise pods without explicit confirmation.
- Capture YAML, events, logs, and current status before recovery actions.
- Treat the custom resource as the intended state unless the user explicitly wants an emergency manual intervention.

## Response Pattern

When answering:

1. Name the selected Kubernetes track.
2. Ask for or provide the first read-only `kubectl` commands.
3. Identify whether Kubernetes desired state or Redis Enterprise internal state is authoritative for the fix.
4. Call out any destructive boundary before suggesting changes.
