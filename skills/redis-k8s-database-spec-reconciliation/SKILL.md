---
name: redis-k8s-database-spec-reconciliation
description: "Explain and troubleshoot Redis Enterprise for Kubernetes database changes that revert during operator reconciliation, including REDB or REAADB YAML as source of truth, UI/API-only edits being overwritten, missing spec fields resetting to defaults, `tlsMode`, eviction, persistence, Redis 8 CRD apiVersion changes, REDB versus REAADB `moduleList` behavior, pinned module versions being ignored or reconciled, GitOps drift, operator logs, and safe manifest reapply workflows."
---

# Redis Kubernetes Database Spec Reconciliation

Use this skill when Redis Enterprise for Kubernetes database changes appear to apply in the UI or REST API but later revert. The core issue is usually controller reconciliation: the operator makes the live database match the Kubernetes custom resource spec.

## Core Rule

In Kubernetes deployments, the source of truth is the Kubernetes manifest or GitOps source for:

- `RedisEnterpriseCluster` (REC)
- `RedisEnterpriseDatabase` (REDB)
- `RedisEnterpriseActiveActiveDatabase` (REAADB)
- related Secrets, Services, Routes, Ingresses, and operator-managed resources

Manual UI/API edits to spec-managed fields can be reverted at the next reconciliation. Fix the manifest, apply it, and let the operator reconcile.

## Safety Rules

- Do not rely on UI/API-only changes for fields managed by REDB or REAADB specs.
- Do not edit generated StatefulSets, Services, or operator-managed resources unless current operator documentation explicitly requires it.
- If GitOps is active, update the Git source, not only the live object.
- Verify the installed operator and CRD versions before giving Redis 8 or `apiVersion` guidance.
- Do not change `redisVersion` and module version pins in the same upgrade unless the current release notes explicitly allow it.

## Triage Workflow

1. Identify the resource:

   ```bash
   kubectl get rec,redb,reaadb -A
   ```

2. Inspect the live custom resource:

   ```bash
   kubectl get redb <name> -n <namespace> -o yaml
   kubectl describe redb <name> -n <namespace>
   ```

   Use `reaadb` for Active-Active databases.

3. Compare:
   - desired manifest in Git or local YAML
   - live custom resource spec
   - live database UI/API state
   - operator status and events
4. Check operator logs:

   ```bash
   kubectl logs deployment/redis-enterprise-operator -n <operator-namespace> --tail=200
   ```

5. Add the intended field to the CR spec, not only the UI.
6. Apply through the approved deployment path:

   ```bash
   kubectl apply -f <file.yaml>
   ```

7. Wait for reconciliation and verify status/events before declaring success.

## Common Revert Cases

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| UI change reverts shortly after save | REDB/REAADB spec does not contain the change | Add the field to the manifest and reapply. |
| TLS returns to disabled | `tlsMode` missing or set differently in REDB | Set `tlsMode` in the REDB spec and apply. |
| Eviction or persistence resets | Field omitted from manifest, so default is reconciled | Add the explicit desired value to the spec. |
| `moduleList` version pin disappears on Redis 8 REDB | Regular Redis 8 REDB chooses built-in module versions from database version | Remove pinned built-in module versions for standard REDB unless current docs require them. |
| REAADB module versions revert | Active-Active requires explicit compatible module versions | Set required versions in `spec.moduleList` for REAADB. |
| Upgrade fails after changing `moduleList` and `redisVersion` together | Upgrade rule or compatibility violation | Revert module changes, complete version upgrade path, then apply compatible module spec if needed. |
| Manual `kubectl edit` works briefly, then reverts | GitOps controller reapplies repository state | Update the GitOps source and let it sync. |

## Redis 8 And CRD Version Notes

For Redis 8/operator-era deployments:

- Verify the current CRD storage version and installed operator release.
- Use the supported `apiVersion` for REC, REDB, and REAADB manifests. In Redis 8 guidance, `app.redislabs.com/v1` replaces deprecated `v1alpha1` flows.
- For standard REDB on Redis 8+, built-in Search and Query, JSON, Time Series, and probabilistic capabilities are usually selected by database version/type rather than pinned manually.
- For REAADB, module version fields can still be required because Active-Active compatibility must be explicit.

Check current release notes before making final claims about Redis 8 module or CRD behavior.

## Manifest Update Pattern

1. Locate the source manifest or Helm/GitOps values.
2. Add or correct the field that keeps reverting.
3. Validate YAML and API version.
4. Apply through the normal deployment channel.
5. Watch status:

   ```bash
   kubectl get redb <name> -n <namespace> -w
   kubectl describe redb <name> -n <namespace>
   ```

6. Confirm the operator reports the resource reconciled.
7. Only then verify the UI/API reflects the intended state.

## Troubleshooting Operator Reconciliation

If the manifest is correct but live state still reverts:

- Check CRD version and schema: unsupported fields may be ignored or pruned.
- Check operator logs for validation, permissions, or reconciliation errors.
- Check Kubernetes events on REDB/REAADB and REC.
- Check for multiple controllers: GitOps, Helm, external secret controllers, or CI jobs.
- Confirm the field is actually supported by the installed operator and Redis version.
- Avoid changes during maintenance, auto-upgrade, resharding, or another active database operation.

## Escalation Packet

Collect:

- Kubernetes context, namespace, REC name, REDB/REAADB name.
- Installed Redis Enterprise Operator version.
- CRD apiVersions in the manifests.
- Desired manifest excerpt and live `kubectl get ... -o yaml` excerpt.
- UI/API field that reverts.
- Operator logs and Kubernetes events around the change.
- GitOps/Helm controller name if present.
- Recent upgrades, resharding, maintenance, or module changes.

## Response Shape

When helping a user:

1. State whether reconciliation is likely.
2. Identify the owning custom resource and source-of-truth manifest.
3. Point to the exact missing or conflicting spec field.
4. Explain REDB versus REAADB and Redis 8 module behavior if relevant.
5. Provide an apply-and-verify sequence, then a support packet if reconciliation still fails.
