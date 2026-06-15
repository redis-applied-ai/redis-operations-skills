---
name: redis-k8s-rec-license
description: "Apply, update, verify, and troubleshoot Redis Enterprise Cluster licensing in Kubernetes through the REC custom resource. Use when the user mentions Redis Enterprise for Kubernetes, REK, REC license fields, LICENSE STATE invalid, Kubernetes license updates, REC FQDN mismatch, expired licenses blocking database changes, or operator reconciliation of license changes."
---

# Redis Kubernetes REC License

Use this skill for Redis Enterprise for Kubernetes licensing tasks where the license is applied through the Redis Enterprise Cluster (REC) custom resource.

## Safety Rules

- Treat the license text as sensitive commercial configuration. Do not paste it into public logs, tickets, or chat unless policy allows it.
- Confirm namespace and REC name before editing.
- Treat license updates as production configuration changes; use change control for production clusters.
- Confirm the license FQDN matches the REC FQDN before applying it when the license is FQDN-bound.

## Workflow

1. Gather prerequisites:
   - Kubernetes namespace.
   - REC name.
   - `kubectl` context and permissions.
   - Complete license block containing `----- LICENSE START -----` and `----- LICENSE END -----`.
   - REC FQDN, commonly `<rec-name>.<namespace>.svc.cluster.local`.
2. Inspect current REC state:

   ```bash
   kubectl -n <namespace> get rec <rec-name>
   kubectl -n <namespace> describe rec <rec-name>
   ```

3. Edit the REC custom resource:

   ```bash
   kubectl -n <namespace> edit rec <rec-name>
   ```

4. Add or update `spec.license` as a YAML block scalar:

   ```yaml
   spec:
     license: |
       ----- LICENSE START -----
       <license-text>
       ----- LICENSE END -----
   ```

5. Save and let the Redis Enterprise Operator reconcile the REC.
6. Verify license state:

   ```bash
   kubectl -n <namespace> get rec <rec-name>
   kubectl -n <namespace> describe rec <rec-name>
   ```

   Expected result: `LICENSE STATE: Valid`.
7. Optionally confirm through Cluster Manager UI or REST API:
   - UI: Cluster, Configuration, General, License.
   - API: `GET /v1/license`.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| YAML error when saving REC | Missing `|`, broken indentation, or incomplete license block | Fix YAML block formatting and reapply. |
| `LICENSE STATE` is not valid | Wrong, expired, incomplete, or FQDN-mismatched license | Verify license text and REC FQDN; request corrected license if needed. |
| Cluster is restricted after expiry | License expired | Apply a new valid license; databases should continue serving reads and writes, but configuration changes may be blocked. |
| Cannot create or modify databases | License missing or expired | Apply or renew license, then retry the configuration change. |
| Upgrade fails due to license | Upgrade attempted with expired or invalid license | Apply a valid license before retrying upgrade. |
| REC remains stuck | Operator reconciliation problem or failed prior update | Check REC events and operator logs; reapply the REC manifest or escalate. |

## Diagnostic Commands

```bash
kubectl -n <namespace> describe rec <rec-name>
kubectl -n <namespace> logs deploy/redis-enterprise-operator
```

## Escalation Packet

Collect these details before escalating:

- Namespace and REC name.
- REC FQDN used for license matching.
- Current `kubectl get rec` and `kubectl describe rec` status.
- Redis Enterprise Operator logs around the update.
- Whether the license is expired, newly issued, or recently changed.
- Exact validation or reconciliation error, with license contents redacted unless secure handling is approved.
