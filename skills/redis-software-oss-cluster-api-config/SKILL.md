---
name: redis-software-oss-cluster-api-config
description: "Configure and troubleshoot Redis Enterprise Software OSS Cluster API for cluster-aware clients. Use when the user asks how to enable `oss_cluster`, choose proxy policy, configure preferred internal/external IP or endpoint type, connect with JedisCluster, redis-py cluster, go-redis, or node-redis cluster mode, fix MOVED/CROSSSLOT, handle Kubernetes in-cluster limitations, or understand Search/TimeSeries/Gears incompatibility."
---

# Redis Software OSS Cluster API Config

Use this skill when a Redis Enterprise Software database needs native Redis Cluster protocol behavior for cluster-aware clients.

## When To Use

Use OSS Cluster API for high-throughput workloads that benefit from client-side routing and Redis Cluster-compatible clients.

Do not enable it when the workload requires Redis Search, TimeSeries, Gears, or non-cluster-aware clients. Use proxy-based clustering for those cases.

## Prerequisites

Confirm before enabling:

- Database uses standard hashing policy.
- Sharding is enabled or planned.
- Proxy policy is `All primary shards` or `All nodes`.
- Proxy policy does not use include/exclude rules.
- Client library supports Redis Cluster topology and redirects.
- Multi-key commands are either avoided or use hash tags to keep related keys in one slot.
- For Kubernetes, clients are inside the same Kubernetes cluster unless current platform guidance says otherwise.

## Enable And Verify

CLI:

```bash
rladmin tune db <db-id> oss_cluster enabled
rladmin info db <db-id> | grep oss_cluster
```

REST API shape:

```bash
curl -k -X PUT -u <admin-email>:<password> \
  -H "Content-Type: application/json" \
  -d '{"oss_cluster": true}' \
  https://<cluster-host>:9443/v1/bdbs/<db-id>
```

Restart cluster-aware clients after changing the setting so they refresh topology.

## Preferred IP / Endpoint Type

By default, topology replies can expose internal addresses. For external clients, configure the preferred address type so `CLUSTER SLOTS` and related topology responses return routable values.

```bash
rladmin tune db db:<db-id> oss_cluster_api_preferred_ip_type external
```

If the platform supports preferred endpoint type, use it when hostnames are required instead of IPs.

Only one topology address style is returned at a time. Do not expect internal and external clients to use different topology replies from the same database setting.

## Client Rules

- Use cluster-aware clients such as JedisCluster, redis-py `RedisCluster`, go-redis ClusterClient, or node-redis cluster mode.
- Seed clients with multiple reachable node/endpoint addresses where supported.
- Use `redis-cli -c` for manual testing.
- Redis Insight may not behave as a cluster-aware client for this mode; validate with supported cluster clients.

Python connection shape:

```python
from redis.cluster import RedisCluster

rc = RedisCluster(
    host="<reachable-host>",
    port=<port>,
    decode_responses=True,
)
```

## Supported Cluster Commands

Expect only a subset of Redis Cluster commands, commonly:

- `CLUSTER SLOTS`
- `CLUSTER NODES`
- `CLUSTER INFO`
- `CLUSTER KEYSLOT`

Check command compatibility before depending on other `CLUSTER` commands.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `Cluster not enabled` | OSS Cluster API not enabled for the database | Verify `oss_cluster` in database info/config. |
| `MOVED` or `ASK` errors | Client is not cluster-aware or topology is stale | Use a cluster client and restart/reload topology. |
| `CROSSSLOT` | Multi-key operation spans hash slots | Use hash tags or redesign multi-key operations. |
| External client cannot connect | Topology returns internal addresses or firewall blocks node ports | Set preferred external IP/endpoint type and verify routing. |
| Search commands unavailable | OSS Cluster API is incompatible with Search/TimeSeries/Gears in this mode | Use proxy-based clustering or separate database. |
| Kubernetes external client fails | Topology returns pod/internal addresses | Keep clients in-cluster or use supported routing topology. |

## Evidence To Collect

- Database ID and `rladmin info db` output for clustering settings.
- Proxy policy and hashing policy.
- Preferred IP/endpoint type.
- Client library and cluster-mode configuration.
- `CLUSTER SLOTS` output with sensitive hosts redacted if needed.
- Exact MOVED/ASK/CROSSSLOT error.
