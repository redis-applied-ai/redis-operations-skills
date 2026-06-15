---
name: redis-database-connection-methods
description: "Choose and troubleshoot Redis database connection methods across Redis Software, Redis Cloud, Redis Open Source, load balancers, Sentinel/Discovery Service, OSS Cluster API, redis-cli, Redis Insight, and official client libraries. Use when the user asks how to connect to a Redis database, find endpoints, choose `redis://` vs `rediss://`, connect through a load balancer, enable OSS Cluster API, use Sentinel discovery on port 8001, configure TLS or mTLS, or pick Java/.NET/Python/Go/Node client patterns."
---

# Redis Database Connection Methods

Use this skill to choose the correct connection path for a Redis database based on networking, clustering, TLS, and client behavior.

## Decision Tree

1. Identify deployment:
   - Redis Cloud.
   - Redis Software.
   - Redis Open Source.
2. Identify endpoint source:
   - UI database details.
   - `rladmin status extra all`.
   - Load balancer hostname and port.
   - Kubernetes/ingress route.
3. Choose connection model:
   - Direct DNS endpoint for most databases.
   - Load balancer endpoint when traffic is fronted by a load balancer.
   - Sentinel/Discovery Service for HA master discovery in Redis Software.
   - OSS Cluster API for cluster-aware clients and Redis Cluster semantics.
   - Redis Insight for GUI/workbench workflows.
   - Official client library for application code.
4. Confirm security requirements:
   - Password or ACL username/password.
   - TLS with CA certificate.
   - mTLS with client certificate and key.
   - IP allowlist/firewall/network route.

## Endpoint Discovery

Redis Software:

```bash
rladmin status extra all
```

Redis Cloud:

- Use database details in the Redis Cloud Console.
- Use private endpoint when private connectivity is configured.

Load balancer:

```text
redis://<load-balancer-hostname>:<port>
rediss://<load-balancer-hostname>:<port>
```

## redis-cli Patterns

Password auth:

```bash
redis-cli -h <endpoint> -p <port> -a <password>
```

Safer password handling:

```bash
export REDISCLI_AUTH=<password>
redis-cli -h <endpoint> -p <port>
```

TLS without client auth:

```bash
redis-cli -h <endpoint> -p <port> --tls --cacert proxy_cert.pem
```

mTLS:

```bash
redis-cli -h <endpoint> -p <port> --tls --cacert proxy_cert.pem --cert client_cert.pem --key client_key.pem
```

## Sentinel / Discovery Service

For Redis Software HA discovery:

- Use multiple cluster node hostnames/IPs.
- Use port `8001` for the Sentinel-compatible Discovery Service.
- Use the Redis Enterprise database name as the master name.
- Include authentication if required.

## OSS Cluster API

Before recommending OSS Cluster API:

- Confirm the database uses supported sharding and hashing policy.
- Confirm proxy policy is compatible.
- Confirm the client supports Redis Cluster mode.
- Be careful with modules and command compatibility.
- Multi-key operations require keys in the same hash slot; use hash tags when needed.
- If clients receive internal addresses from `CLUSTER SLOTS` or `CLUSTER SHARDS`, tune preferred IP behavior for external exposure when appropriate.

Example tuning:

```bash
rladmin tune db <db_name> oss_cluster enabled
rladmin tune db <db_name> oss_cluster_api_preferred_ip_type external
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Cannot connect | Endpoint, port, password, allowlist, firewall, and load balancer route. |
| TLS failure | Client TLS support, CA certificate, SNI, certificate chain, and mTLS files. |
| Load balancer connection fails | Database proxy policy and backend routing. |
| Sentinel client fails | Port 8001 reachability, master name, and multiple node addresses. |
| Cluster client fails | OSS Cluster API enabled, client cluster mode, exposed IP type, and compatible modules. |
| Multi-key command fails | Keys are in different hash slots; use a shared hash tag. |
| Redis Insight fails | Use the Redis Insight connection workflow for logs and UI-specific settings. |

## Safety Checks

- Do not paste real passwords, private keys, or client certificates into examples.
- Prefer `rediss://` and TLS where required by the database.
- Verify current client-library APIs from official docs before writing production code.
- For vector or AI application code, prefer RedisVL patterns when applicable.
