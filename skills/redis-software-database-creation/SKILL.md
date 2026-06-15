---
name: redis-software-database-creation
description: "Guide Redis Software database creation and configuration. Use when the user asks to create a Redis Enterprise Software database, choose memory size, replication, persistence, backups, TLS, ACLs, Redis 8 capabilities, modules, clustering, shard placement, OSS Cluster API, proxy policy, or eviction policy."
---

# Redis Software Database Creation

Use this skill to plan or review a Redis Software database before creation. Confirm the cluster FQDN, DNS or load balancer access, and cluster health are ready before database work starts.

## Current-State Rule

Verify Redis Software version before giving module or capability guidance. Redis 8 changes capability behavior compared with earlier module-selection workflows, and version-specific defaults can drift.

## Creation Checklist

1. Confirm workload goal: cache, session store, search, JSON document store, time series, queue, vector search, or primary datastore.
2. Estimate dataset size, write rate, growth rate, and acceptable data loss.
3. Choose availability:
   - Without replication: memory limit can match expected dataset size.
   - With high availability: plan roughly twice expected data size because replicas consume memory.
4. Choose persistence:
   - None for disposable cache data.
   - Snapshots for lighter durability with wider recovery point.
   - AOF every second for stronger durability with some performance cost.
5. Choose security:
   - Avoid unauthenticated databases except for isolated test environments.
   - Prefer ACLs or password authentication.
   - Enable TLS for client-to-database traffic when required by policy.
6. Configure backups if data must survive cluster or operator failures.
7. Decide clustering and shard behavior for scale.
8. Choose an eviction policy aligned to the data model.
9. Validate connection strings and client compatibility before application cutover.

## Capabilities and Modules

| Redis Software version | Agent guidance |
| --- | --- |
| Redis 8 databases | Capabilities are generally built in and enabled according to database type; verify exact capability set for RAM, Flash/Flex, and Active-Active database types. |
| Earlier versions | Modules such as Search, JSON, Bloom, and TimeSeries may need to be selected at creation time. Adding modules later can require recreation or migration. |
| Redis Flex or Flash | Verify engine generation and database version before assuming Flash behavior or RAM requirements. |

## Sizing and Availability

- Recommend replication for production unless the workload is disposable and can tolerate node loss.
- Use rack zone awareness when available to reduce correlated failure risk.
- For datasets larger than about 25 GB or workloads needing horizontal scaling, evaluate database clustering.
- Sparse shard placement favors resilience; dense placement favors fewer nodes and higher packing.

## Persistence and Backups

| Requirement | Recommendation |
| --- | --- |
| Lowest latency cache, disposable data | No persistence and no backup may be acceptable. |
| Recoverable but lower write overhead | Snapshots. |
| Minimize data loss after failure | AOF every second. |
| Operational restore point | Periodic backup to approved storage. |

For backups, confirm storage type, path, credentials, permissions, and whether the Redis service account can write to the target.

## Security Setup

- Prefer ACLs for named users and least privilege.
- Use TLS for production client connections when policy requires encryption in transit.
- For replication, Active-Active, or ReplicaOf workflows, verify TLS requirements between databases.
- Confirm client libraries support the selected TLS, ACL, and clustering options.

## Advanced Options

| Option | Use when |
| --- | --- |
| Database clustering | Dataset size or throughput requires shard-based scale. |
| OSS Cluster API | Applications use cluster-aware Redis clients; non-aware clients can hit `MOVED` errors. |
| Proxy policy | Traffic placement or proxy count needs explicit control. |
| Shard placement policy | Resilience or packing requirements need explicit tradeoff. |

## Eviction Policy Guidance

| Data model | Common policy |
| --- | --- |
| Must never evict | `noeviction`; size the database for all required keys. |
| General cache | `allkeys-lru` or `allkeys-lfu`. |
| Cache with meaningful frequency signal | `allkeys-lfu`. |
| Only expiring keys should be evicted | `volatile-lru`, `volatile-lfu`, `volatile-random`, or `volatile-ttl`. |
| Random sampling acceptable | `allkeys-random` or `volatile-random`. |

## Escalation Packet

Collect:

- Redis Software version and database type.
- Expected data size, growth, write rate, and durability goal.
- HA, rack awareness, clustering, and shard placement choices.
- Persistence and backup configuration.
- Authentication, ACL, and TLS requirements.
- Required capabilities or modules.
- Eviction policy and reason.
- Client library and whether it is cluster-aware.
