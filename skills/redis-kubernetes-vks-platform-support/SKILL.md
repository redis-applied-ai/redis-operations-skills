---
name: redis-kubernetes-vks-platform-support
description: Use when evaluating Redis Enterprise for Kubernetes or Redis Software for Kubernetes support on VMware vSphere Kubernetes Service, VKS, TKGI, or VMware TKG, including operator compatibility, Kubernetes version support, migration from TKG, VKS deployment prerequisites, REC creation, admission webhook issues, bundled Redis 8 capabilities, storage requirements, x86 architecture constraints, or VKS-specific troubleshooting.
---

# Redis Kubernetes VKS Platform Support

Use this skill for VMware VKS supportability, deployment, and troubleshooting questions for Redis Enterprise for Kubernetes. Support matrices change, so verify current Redis Kubernetes release notes and supported distribution docs before making final platform eligibility claims.

## Release-Scoped Baseline

For the Redis Enterprise for Kubernetes `8.0.2-2` operator release, the source material identifies this baseline:

- VMware VKS is supported for Kubernetes `1.32`.
- VMware TKG is not supported in that release; migration should target TKGI or VKS where appropriate.
- x86 architecture is supported.
- Upgrades to `8.0.2-2` require a supported previous operator version, with `7.4.2-2` or later called out in the source.
- Default Redis 8 bundled capabilities such as Search and Query, JSON, TimeSeries, and probabilistic structures do not require adding a separate `moduleList` for default deployments.

Treat these as release-specific facts, not current universal policy.

## Intake Checklist

Collect:

- Kubernetes distribution: VKS, TKGI, TKG, OpenShift, or community Kubernetes
- Kubernetes version and architecture
- Redis Enterprise operator version and intended upgrade path
- namespace and REC/REDB names
- storage class, volume mode, and filesystem
- node count, CPU, memory, and scheduling constraints
- whether a private registry is used for images
- exact pod, admission webhook, TLS, or service error

## Deployment Readiness

Before deployment or upgrade:

1. Confirm the platform and Kubernetes version are supported by current Redis docs.
2. Confirm at least three worker nodes for quorum and high availability.
3. Confirm image access through Docker Hub or a private registry.
4. Confirm `kubectl` context points to the target VKS cluster and namespace.
5. Confirm block storage with a supported filesystem; avoid NFS for Redis Enterprise persistent storage.
6. Confirm CPU and memory requests are realistic for the workload, not only the operator minimum.
7. Confirm certificate management and monitoring plans, especially REC and database proxy certificates.

## Basic Verification Commands

```bash
kubectl get nodes -o wide
kubectl get rec,redb -n <namespace>
kubectl get pods,pvc,svc -n <namespace>
kubectl describe rec <rec-name> -n <namespace>
kubectl logs deploy/redis-enterprise-operator -n <operator-namespace>
```

Check admission resources when REDB validation fails:

```bash
kubectl get validatingwebhookconfiguration
kubectl get secret admission-tls -n <namespace>
kubectl describe pod -n <namespace> -l app=redis-enterprise-operator
```

## VKS Troubleshooting Matrix

| Symptom | Likely area | First action |
| --- | --- | --- |
| Pods stuck or not ready | resources, PVCs, Secrets, scheduling | `kubectl describe pod`; inspect events, PVC binding, and node pressure. |
| TLS handshake failure | certificate chain or key mismatch | Verify `ca.crt`, `tls.crt`, and `tls.key` in the relevant Secrets. |
| Admission webhook errors | admission service, webhook, or certificate issue | Check `admission-tls`, webhook configuration, operator pod readiness, and operator logs. |
| Admission endpoint missing | operator/admission service issue in the release context | Restart only the operator pod if that is the documented fix for the verified release. |
| REDB update blocked during Redis 8 upgrade | module/version mismatch during transition | Preserve existing module versions during the upgrade; let Redis 8 choose bundled defaults after the transition. |
| Custom internode certificate upload fails | feature not supported in the verified release | Verify release notes; use supported certificate paths only. |
| Client connection refused or timed out | Service, DNS, TLS, or network policy | Inspect Services/endpoints and test from inside the cluster. |
| OOMKilled | insufficient REC pod memory | Increase requests/limits and inspect memory metrics. |
| PVC stuck terminating | orphaned resources or finalizers | Confirm pods and Redis processes are gone before any finalizer action. |
| Custom module does not load | custom modules disabled or unsupported | Verify whether the operator release supports custom modules. |

## Response Pattern

When advising:

1. State whether the question is supportability, deployment, upgrade, or troubleshooting.
2. Identify the exact Redis operator version and Kubernetes distribution/version that must be verified.
3. Give read-only Kubernetes checks first.
4. Separate release-specific known behavior from current docs that must be confirmed.
5. Call out destructive boundaries before suggesting pod deletion, PVC changes, or REC recreation.
