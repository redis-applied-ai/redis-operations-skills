---
name: redis-software-convergence-endpoint-rebinding
description: Use when explaining, planning, or troubleshooting Redis Software cluster convergence and endpoint rebinding during failover, node maintenance, shard migration, topology changes, upgrades, or resiliency tests, especially when clients must re-resolve DNS, retry after disconnects, avoid hardcoded IPs, refresh topology, tune timeouts, or validate endpoint availability after maintenance.
---

# Redis Software Convergence Endpoint Rebinding

Use this skill when topology changes affect Redis Software endpoints and client reconnect behavior. It is for explaining expected behavior, planning maintenance, and validating recovery after failover or node movement. For rapid repeated endpoint churn, use the endpoint-flapping skill.

## Core Concepts

- Cluster convergence: Redis nodes and control-plane services settle on a consistent post-change topology after failover, maintenance, migration, or upgrade.
- Endpoint rebinding: database endpoints move or update so clients connect to the current serving shard or proxy path.
- Client impact: disconnects can be expected during topology changes; resilient clients reconnect through the FQDN and do not pin old IPs.

## Safety Rules

- Do not recommend permanent direct-IP connection strings; they bypass endpoint rebinding and failover behavior.
- Treat proxy policy, endpoint binding, and DNS changes as production-impacting.
- Verify cluster convergence before declaring maintenance complete.
- Preserve a timeline of failover, migration, DNS, and client reconnect events.

## Monitor Convergence

Run:

```bash
rladmin status
rladmin status endpoints
rladmin status databases
rladmin cluster running_actions
rlcheck
```

Check:

- all nodes are healthy
- shards are placed and serving as expected
- endpoints are present and bound to healthy database paths
- failover, migration, or maintenance actions are no longer running
- CPU, memory, disk, and network are not saturated during convergence

If cluster actions remain stuck or health is degraded, handle that before focusing on client DNS.

## Validate Endpoint Rebinding

From the client network path:

```bash
dig <database-endpoint>
nslookup <database-endpoint>
redis-cli -h <database-endpoint> -p <port> PING
redis-cli -h <database-endpoint> -p <port> INFO
```

Add TLS and auth flags according to the database configuration.

From a Redis cluster node, isolate internal DNS behavior:

```bash
dig @localhost <database-endpoint>
```

Compare:

- client resolver result
- cluster-node resolver result
- expected endpoint from `rladmin status databases`
- endpoint state from `rladmin status endpoints`

If DNS differs by resolver, inspect delegation, TTL, cache, corporate DNS, or split-horizon configuration.

## Client Robustness Checklist

Applications should:

- use Redis endpoint FQDNs, not static node or shard IPs
- retry connections with backoff and jitter
- re-resolve DNS after disconnects
- set connection and read timeouts long enough to tolerate short topology changes
- recycle stale idle connections
- refresh topology in cluster-aware clients
- avoid infinite DNS caching in runtimes such as JVM-based clients
- validate TLS using the endpoint hostname that matches the certificate

For Java-style pools, review idle validation and eviction settings such as `testWhileIdle` and idle eviction timing. For cluster-aware clients, verify topology refresh options in the installed client version.

## Expected Versus Problematic Behavior

| Observation | Interpretation | Next Step |
| --- | --- | --- |
| brief disconnects during failover | often expected | verify retry and reconnect behavior |
| clients keep using old IP | DNS cache or hardcoded endpoint | force FQDN usage and tune DNS caching |
| cluster still has running actions | convergence incomplete | wait or troubleshoot the action before client changes |
| Redis CLI works from cluster but not app host | client DNS, firewall, TLS, or network path | compare resolver and network path |
| repeated endpoint state changes | endpoint flapping | switch to `redis-software-endpoint-flapping` |
| connection failures only after upgrade | client retry/topology settings or endpoint rebinding delay | validate client behavior and maintenance timeline |

## Maintenance Planning

Before maintenance or failover tests:

1. Record database endpoint, port, TLS/auth requirements, and expected clients.
2. Confirm clients use FQDN and reconnect logic.
3. Check DNS TTL and runtime DNS cache behavior.
4. Confirm monitoring covers endpoint availability, latency, error rate, reconnects, and Redis cluster health.
5. Communicate that brief disconnects may occur during failover or endpoint movement.
6. Define success criteria: cluster healthy, endpoint resolves, clients reconnect, latency returns to baseline.

## Escalation Packet

Collect:

- maintenance or failover timeline
- `rladmin status`, `rladmin status endpoints`, and `rladmin cluster running_actions`
- database endpoint and proxy policy
- DNS results from app host and Redis cluster node
- client library, version, retry, timeout, and DNS cache settings
- app logs showing reconnect behavior
- TLS error text if certificate validation is involved
- monitoring graphs for latency, errors, connections, CPU, memory, and network

## Response Shape

When answering:

1. State whether the issue is convergence, rebinding, client DNS/cache, client retry behavior, or active endpoint flapping.
2. Provide the next status or DNS check.
3. Explain expected client-visible impact.
4. Recommend the smallest client or DNS change that improves resilience.
5. Define validation after the topology change settles.
