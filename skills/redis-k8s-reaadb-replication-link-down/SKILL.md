---
name: redis-k8s-reaadb-replication-link-down
description: "Triage Replication Link Down for Redis Enterprise Active-Active databases on Kubernetes. Use when `kubectl get reaadb` shows replication status down, Active-Active sync fails between RECs, RERC or REAADB reconciliation is unhealthy, operator changes overwrite UI fixes, secrets or TLS credentials are missing, NetworkPolicy or Services block replication, PVCs are stuck, or pod logs show auth, TLS, DNS, route, or connectivity errors."
---

# Redis Kubernetes REAADB Replication Link Down

Use this skill when a Redis Enterprise Active-Active database on Kubernetes shows replication link down or unhealthy replication status.

## Safety Rules

- Treat Kubernetes manifests as the source of truth. Do not make UI-only fixes that the operator will revert.
- Do not edit Redis Enterprise internal metadata manually.
- Do not restart pods or shards before checking secrets, services, network policy, and operator state.
- Preserve operator logs and Redis pod logs before disruptive changes.

## Triage Workflow

1. Identify the Active-Active database and namespace:

   ```bash
   kubectl get reaadb -A
   kubectl describe reaadb <name> -n <namespace>
   ```

2. Inspect related REC and RERC resources:

   ```bash
   kubectl get rec,rerc -n <namespace>
   kubectl describe rec <name> -n <namespace>
   kubectl describe rerc <name> -n <namespace>
   ```

3. Check Redis Enterprise status in each participating REC:

   ```bash
   rladmin status extra all
   ```

4. Inspect pod health and logs:

   ```bash
   kubectl get pods -n <namespace> -o wide
   kubectl logs <pod-name> -n <namespace>
   ```

5. Review Redis Enterprise operator logs for reconciliation errors:

   ```bash
   kubectl logs deployment/redis-enterprise-operator -n <operator-namespace>
   ```

## Root Cause Checks

| Area | What to verify |
| --- | --- |
| Secrets | RERC credentials, REAADB password, client/TLS cert secrets, expected key names, and base64-decoded content shape. |
| Services and DNS | Service selectors, headless services, DNS names, ports, and endpoints for inter-cluster replication. |
| NetworkPolicy | Namespace-local, cross-namespace, and REC pod replication traffic are allowed. |
| Ingress or Routes | External routes required for cross-cluster replication exist and point to correct services. |
| Pod placement | REC pods have IPs, are Running, and are not blocked by taints, selectors, or resource pressure. |
| Storage | PVCs are Bound, mounted, and not stuck Terminating. |
| Operator reconciliation | Desired settings are represented in REAADB specs, not only changed in UI. |

## Secret Inspection

List and inspect secret metadata:

```bash
kubectl get secret -n <namespace>
kubectl get secret <name> -n <namespace> -o yaml
```

Decode only specific fields locally and avoid sharing secret values:

```bash
kubectl get secret <name> -n <namespace> -o jsonpath='{.data}'
```

Look for malformed, missing, or wrong secret references in REAADB and RERC specs.

## Repair Guidance

| Finding | Action |
| --- | --- |
| Secret missing or malformed | Recreate or update the secret and reference it in the manifest. |
| Service selector or port wrong | Fix Kubernetes Service configuration and reapply. |
| NetworkPolicy blocks traffic | Add the required pod/namespace/port allowance. |
| Route or ingress missing | Restore the required external path for participating clusters. |
| UI-only change keeps reverting | Add the supported setting to the REAADB manifest and apply it. |
| PVC or pod placement issue | Fix storage or scheduling first, then let the operator reconcile. |

After fixing the root cause, let the operator reconcile. Restart pods or shards only when the supported operational path requires it and after evidence is collected.

## Escalation Packet

Collect:

- Kubernetes context, namespaces, REC names, RERC names, and REAADB name.
- `kubectl get reaadb -A` and `kubectl describe reaadb`.
- REC/RERC describe output.
- Operator logs around the failed reconciliation.
- Pod status, pod logs, and pod IPs.
- Relevant Service, Endpoint, Route/Ingress, and NetworkPolicy YAML.
- Secret names and references, with values redacted.
- `rladmin status extra all` from all participating RECs.
- Support package or log collector output from each participating cluster.
