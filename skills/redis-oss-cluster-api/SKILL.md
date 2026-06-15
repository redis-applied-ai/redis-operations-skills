---
name: redis-oss-cluster-api
description: "Plan, enable, and troubleshoot OSS Cluster API for Redis Cloud, Redis Software, and Redis Enterprise for Kubernetes. Use when the user asks to support open-source Redis cluster clients, enable cluster-aware routing, configure `oss_cluster`, set Kubernetes `ossCluster`, handle MOVED or ASK redirects, fix internal IPs in CLUSTER SLOTS, decide between proxy routing and OSS Cluster API, or understand Search and Query, JSON indexing, TimeSeries, module, and multi-key limitations."
---

# Redis OSS Cluster API

Use this skill when deciding whether to enable OSS Cluster API or when activating it across Redis Cloud, Redis Software, or Kubernetes deployments.

## Decision Gate

Enable OSS Cluster API when:

- Applications use cluster-aware Redis clients.
- The workload is high-throughput key-value access.
- The user is migrating from open-source Redis Cluster.
- Direct shard routing is more important than proxy simplicity.

Avoid OSS Cluster API when:

- The application cannot handle `MOVED` and `ASK` redirects.
- Search and Query, JSON indexing, global indexing, or cross-shard aggregation is required.
- Multi-key operations span unrelated keys.
- Simpler proxy-based routing is good enough.

## Cross-Product Requirements

- Sharding must be enabled.
- Standard hashing policy is required.
- Applications must use cluster-aware clients and reconnect after enablement.
- Multi-key operations require keys in the same hash slot.
- Use hash tags for related keys:

  ```text
  user:{123}:profile
  user:{123}:settings
  ```

- Verify key slot alignment:

  ```redis
  CLUSTER KEYSLOT user:{123}:profile
  CLUSTER KEYSLOT user:{123}:settings
  ```

## Redis Cloud

Requirements:

- Redis Cloud Pro plan.
- Sharded database.
- Owner or Admin permissions for subscription upgrades or database changes.

Recommended workflow:

1. Confirm the subscription is Pro.
2. Prefer creating a new sharded database with OSS Cluster API enabled if the setting is creation-time only.
3. If editing an existing database, enable the OSS Cluster API toggle and save.
4. Update applications to use the cluster-aware endpoint.
5. Test redirects, failover, slot migration, and multi-key behavior.

If the toggle is unavailable, create a new compatible database and migrate data.

## Redis Software

Requirements:

- Standard hashing policy.
- Proxy policy set to `all-master-shards` or `all-nodes`.
- No node include/exclude proxy rules.
- No unsupported modules for OSS cluster mode.

Enable and verify:

```bash
rladmin tune db <db-name-or-id> oss_cluster enabled
rladmin info db <db-name-or-id> | grep oss_cluster
```

Disable if needed:

```bash
rladmin tune db <db-name-or-id> oss_cluster disabled
```

Existing client connections must reconnect for changes to take effect.

If `CLUSTER SLOTS` returns internal IPs to external clients, prefer external IPs:

```bash
rladmin tune db db:<db-id> oss_cluster_api_preferred_ip_type external
```

## Kubernetes

Cluster-level REC example:

```yaml
spec:
  ossClusterSettings:
    externalAccessType: LoadBalancer
```

Database-level REDB example:

```yaml
spec:
  ossCluster: true
  ossClusterSettings:
    enableExternalAccess: true
```

Apply and verify:

```bash
kubectl apply -f rec.yaml
kubectl apply -f redb.yaml
kubectl get svc
```

Cost warning: external OSS cluster access can create one LoadBalancer for the cluster endpoint and one LoadBalancer per Redis Enterprise node running a pod.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `CLUSTER` command not allowed | OSS Cluster API is disabled or unsupported for the plan/database. |
| Client does not follow redirects | Client is not cluster-aware or is configured for proxy mode. |
| `CROSSSLOT` errors | Keys do not share a hash slot; use hash tags or redesign operation. |
| Search/Query fails | OSS Cluster API is incompatible with required cross-shard indexing/query behavior. |
| External clients see internal IPs | Set preferred IP type to external or fix Kubernetes external access. |
| Toggle missing in Redis Cloud | Setting may be creation-time only; create a new database and migrate. |
| Kubernetes costs rise | External access provisioned per-node load balancers. |

## Escalation Packet

Collect:

- Product: Redis Cloud, Redis Software, or Kubernetes.
- Version, plan, database ID/name, and sharding status.
- Hashing policy and proxy policy.
- Client library and cluster-aware configuration.
- Module/capability requirements.
- `CLUSTER SLOTS` output with sensitive addresses redacted if needed.
- `MOVED`, `ASK`, `CROSSSLOT`, or module error messages.
- Kubernetes REC/REDB specs and service list if applicable.
