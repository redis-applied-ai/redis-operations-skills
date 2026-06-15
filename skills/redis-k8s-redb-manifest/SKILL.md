---
name: redis-k8s-redb-manifest
description: "Create, review, and troubleshoot RedisEnterpriseDatabase (REDB) Kubernetes YAML manifests for Redis Enterprise for Kubernetes. Use when the user asks for a consolidated REDB manifest, databaseSecretName, RedisEnterpriseCluster references, memorySize, shardCount, persistence, evictionPolicy, tlsMode, backup.s3, auto-tiering/ROF fields, or why REDB settings revert after creation."
---

# Redis Kubernetes REDB Manifest

Use this skill to design or troubleshoot a Redis Enterprise Database (REDB) custom resource for Redis Enterprise for Kubernetes.

## Current-State Rule

Before applying production manifests, verify the installed Redis Enterprise Operator version and current REDB API reference. CRD fields and supported Redis versions can vary by Operator and REC version.

## Bundle Files

- `templates/redb.yaml`: Starter REDB manifest with common production fields and placeholders.

## Workflow

1. Gather context:
   - Namespace.
   - REC name and whether the REDB is in the same namespace.
   - Redis version supported by the REC.
   - Database name.
   - Password secret name and key.
   - Memory size, shard count, replication, persistence, eviction policy.
   - TLS and backup requirements.
   - Auto-tiering/ROF requirements.
2. Validate prerequisites:
   - Redis Enterprise Operator is healthy.
   - REC exists and is healthy.
   - Password secret exists and contains key `password`.
   - TLS secret exists if `tlsMode` is enabled.
   - Backup target credentials exist and have required permissions.
3. Start from `templates/redb.yaml` and remove fields that are not needed.
4. Fill every required placeholder before applying.
5. Apply:

   ```bash
   kubectl apply -f redis-enterprise-database.yaml
   ```

6. Watch status and events:

   ```bash
   kubectl -n <namespace> get redb
   kubectl -n <namespace> describe redb <name>
   ```

## Field Guidance

| Field | Guidance |
| --- | --- |
| `version` | Must be supported by the REC and Operator. |
| `databaseSecretName` | Secret must exist and include key `password`. |
| `redisEnterpriseCluster.name` | Set when REDB and REC association must be explicit. |
| `memorySize` | Size for dataset, replicas, overhead, and headroom. |
| `shardCount` | Choose for throughput and client parallelism. |
| `replication` | Keep enabled for HA unless intentionally testing. |
| `persistence` | Match durability SLO; AOF every second is a common HA default. |
| `evictionPolicy` | Match workload semantics; avoid accidental eviction for durable data. |
| `backup.s3` | Verify bucket, path, secret, and IAM permissions. |
| `tlsMode` / `tlsSecret` | Required for TLS-enabled database connectivity. |
| `isRof` / `rofRamSize` | For auto-tiering; confirm sizing rules and support. |

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Settings revert after creation | Field is missing from manifest or managed by another controller. |
| Authentication fails | Secret name/key is wrong or password secret malformed. |
| Backup fails | S3 secret, bucket, path, or IAM permission is wrong. |
| TLS not active | `tlsMode` or `tlsSecret` missing/invalid. |
| Performance poor | `memorySize`, `shardCount`, persistence, and client parallelism. |
| Unexpected evictions | Eviction policy does not match workload. |

## Safety Checks

- Do not apply a manifest with placeholders still present.
- Do not change production persistence, TLS, shard count, or memory size without reviewing impact.
- Do not include real passwords or cloud credentials in the manifest; use Kubernetes secrets.
- For destructive spec changes, confirm whether the Operator supports in-place update or requires recreation.
