---
name: redis-software-platform-orientation
description: "Explain Redis Enterprise Software architecture and route onboarding or troubleshooting questions across nodes, clusters, quorum, cluster manager, shards, databases, endpoints, proxies, HA, and Redis 8 database capabilities. Use when the user asks what Redis Software is, how Redis Enterprise clusters work, why quorum matters, how endpoints route traffic, or how Redis 8 capabilities differ from older module-based databases."
---

# Redis Software Platform Orientation

Use this skill to orient users or agents before Redis Enterprise Software installation, database creation, cluster sizing, or distributed-system troubleshooting.

## Core Model

Redis Enterprise Software is a self-managed Redis platform deployed on customer-controlled infrastructure. It runs as a distributed cluster of nodes with a cluster manager, shard placement, database endpoints, proxy routing, replication, and optional Active-Active databases.

## Architecture Map

| Component | Role |
| --- | --- |
| Node | Physical machine, VM, or container running Redis Enterprise services. Nodes can host shards, proxies, and cluster manager processes. |
| Cluster | Group of nodes operating as one Redis Enterprise deployment. Production clusters require quorum. |
| Cluster manager | Coordinates cluster health, database lifecycle operations, shard placement, migrations, resharding, statistics, and alerts. |
| Quorum | More than half of cluster nodes must be online for cluster decisions. Use an odd node count, with 3 nodes as the practical minimum. |
| Master of cluster | The currently elected cluster manager leader for cluster-wide decisions. |
| Shard | Redis process that stores a full database or a partition of a clustered database. A shard can be master or replica. |
| Database | User-facing data container made from one or more shards, with settings for memory, persistence, replication, clustering, modules/capabilities, and access control. |
| Endpoint | Host/port abstraction that clients use. The proxy layer routes through the endpoint and updates routing after failover. |
| Proxy | Per-node routing layer that forwards Redis commands to the correct database shard while allowing standard Redis clients to connect through stable endpoints. |

## HA and Scale Patterns

| Configuration | Shape | Use when |
| --- | --- | --- |
| Standalone | One master shard | Development or simple workloads without HA needs. |
| HA | One master shard plus a replica on a different node | Workload needs automatic failover. |
| Clustered | Multiple master shards | Workload needs horizontal scale. |
| Clustered + HA | Multiple masters, each with a replica | Workload needs both scale and failover. |
| Active-Active | CRDB across clusters | Workload needs multi-region writes and conflict-free geo distribution. |

## Quorum Guidance

1. Confirm the node count and which nodes are online.
2. Use more-than-half availability as the quorum rule: 2 of 3, 3 of 5, 4 of 7, and so on.
3. Recommend odd node counts for decision safety.
4. Use quorum-only nodes when the deployment needs voting capacity without full data-node sizing.
5. Treat network splits as quorum problems before assuming a database-only issue.

## Redis 8 Capability Guidance

- For Redis Enterprise Software 8.0.2-17 and later with Redis 8 databases, Search and Query, JSON, Time Series, and Probabilistic capabilities are built into the database version and enabled according to database type and deployment mode.
- For earlier Redis Enterprise Software versions, capabilities may still be selected through explicit modules during database creation.
- When a user asks why a capability is missing, first identify the Redis Enterprise Software version, database version, database type, and whether the database was created under the module-picker model or the Redis 8 built-in capability model.

## Troubleshooting Routing

| User symptom | First concept to check |
| --- | --- |
| Cluster operations are unavailable | Quorum and cluster manager leader state. |
| Client cannot connect after failover | Endpoint and proxy routing state. |
| Database lacks expected Search/JSON/Time Series support | Version-specific capability model and database type. |
| Uneven node load | Shard placement, shard count, replication, and rack-zone awareness. |
| Concern about single points of failure | Shared-nothing architecture, replication, quorum, and rack-zone settings. |

## Response Pattern

When answering architecture questions:

1. State whether the topic is cluster-level, database-level, shard-level, endpoint/proxy-level, or version/capability-level.
2. Explain the relevant component in operational terms.
3. Tie the component to the next action: inspect cluster health, check quorum, review database configuration, verify endpoint routing, or confirm version/capability behavior.
4. Avoid giving installation or sizing claims as current fact unless checked against the exact version and deployment target.
