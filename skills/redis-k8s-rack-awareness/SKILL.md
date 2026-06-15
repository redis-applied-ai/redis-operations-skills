---
name: redis-k8s-rack-awareness
description: "Troubleshoot Redis Enterprise for Kubernetes rack awareness when REC pods or REDB shards do not spread across zones. Use when `rackAwarenessNodeLabel`, `spec.rackAware`, node labels, operator RBAC, `rladmin verify rack_aware`, primary/replica zone collisions, shard placement drift after pod restarts, or optimize_shards_placement blueprint workflows are involved."
---

# Redis Kubernetes Rack Awareness

Use this skill when Redis Enterprise for Kubernetes rack or zone awareness is configured but pod or shard placement is not behaving as expected.

## Key Distinction

There are two layers:

- Kubernetes layer: the Redis Enterprise Operator schedules REC pods across nodes using `spec.rackAwarenessNodeLabel`.
- Redis Enterprise layer: Redis assigns rack IDs and places primary/replica shards to avoid same-rack or same-zone placement when rack awareness and database replication are enabled.

Pod spread does not guarantee shard primary/replica separation.

## Prerequisites

- Redis Enterprise Operator-managed REC and REDB resources.
- At least three REC nodes for meaningful zone-aware HA.
- Stable node labels across eligible Kubernetes nodes.
- Operator ServiceAccount can `get`, `list`, and `watch` nodes.
- Database replication enabled if primary/replica separation is expected.

## Configuration Checks

1. Verify node labels:

   ```bash
   kubectl get nodes -o custom-columns="name:metadata.name","zone:metadata.labels.topology\\.kubernetes\\.io/zone"
   ```

2. Confirm the REC uses the exact label key:

   ```yaml
   spec:
     rackAwarenessNodeLabel: topology.kubernetes.io/zone
   ```

3. If node selectors are used, confirm eligible nodes still span the intended zones.
4. Check operator logs for RBAC errors reading nodes.
5. Confirm the REDB enables rack awareness:

   ```yaml
   spec:
     rackAware: true
   ```

6. Confirm database replication is enabled.

## Verification

Check pod spread:

```bash
kubectl get pods -l app=redis-enterprise -o wide
```

Check Redis Enterprise rack awareness inside a REC pod:

```bash
kubectl exec -it <rec-pod> -- rladmin verify rack_aware
```

Use the output to distinguish:

- Rack awareness not configured.
- Rack awareness enabled but collisions exist.
- Placement is healthy.

## Fix Matrix

| Symptom | Likely cause | Action |
| --- | --- | --- |
| REC pods land in one zone | Missing labels, wrong label key, nodeSelector excludes zones, or RBAC prevents node reads | Fix labels, REC spec, node eligibility, or operator RBAC. |
| Pods spread but shards collide | DB replication off, Redis rack awareness not enabled, or existing shard placement predates config | Enable replication/rack awareness and optimize shard placement. |
| `rladmin verify rack_aware` says not configured | Redis Enterprise layer lacks rack IDs/policy | Configure rack IDs/policy through supported operator/API workflow and verify again. |
| Drift after pod restarts | Placement is not automatically repaired after some restart scenarios | Detect collisions and run shard placement optimization. |
| Some co-location remains | Not enough eligible capacity or zones | Add capacity/zones or accept documented limitation. |

## Shard Placement Re-Optimization

When rack awareness is enabled after shards already exist, generate and apply an optimized placement blueprint:

1. Request optimized shard placement:

   ```text
   GET /v1/bdbs/<uid>/actions/optimize_shards_placement
   ```

2. Capture the `cluster-state-id` response header.
3. Apply the returned `shards_blueprint` with:

   ```text
   PUT /v1/bdbs/<uid>
   ```

4. Verify again with `rladmin verify rack_aware`.

Treat blueprint application as production-impacting. Review the returned plan and confirm before applying.

## Operations Guidance

- Add a periodic check for rack collisions using `rladmin verify rack_aware`.
- Alert when primary/replica pairs share a rack/zone.
- Recheck after node pool changes, operator upgrades, pod restarts, and database resharding.

## Evidence To Collect

- REC and REDB YAML.
- Node labels and nodeSelector/affinity settings.
- Operator RBAC and relevant logs.
- `kubectl get pods -o wide` output.
- `rladmin verify rack_aware` output.
- Database replication and shard placement details.
- Optimize placement response if used.
