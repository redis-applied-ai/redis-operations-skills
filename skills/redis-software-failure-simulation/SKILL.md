---
name: redis-software-failure-simulation
description: Use when planning or running Redis Software resiliency drills that simulate node reboot, Redis process kill, shard movement, endpoint migration, network isolation, replica failure, or client reconnect behavior. Use for pre-test readiness, maintenance-window planning, controlled failure execution, and deciding which evidence to collect before post-test failover analysis.
---

# Redis Software Failure Simulation

Use this skill to plan and execute controlled Redis Software failure simulations. Treat these tests as production-impacting unless the user proves the environment is disposable.

## Safety Gates

- Prefer staging or a maintenance window for production.
- Get explicit approval before running disruptive commands such as `kill -9`, node reboot, firewall blocking, supervisor stops, or shard/endpoint migration.
- Confirm current backups or persistence posture for critical data.
- Confirm the cluster has quorum before starting; use at least three nodes for HA testing.
- Confirm databases under test have replication enabled and primary/replica shards are on different nodes or failure domains.
- Confirm applications connect through DNS-based database endpoints, not node IPs or shard IPs.
- Confirm client libraries have reconnect, retry, timeout, and backoff settings appropriate for failover.

## Pre-Test Baseline

Collect:

```text
rladmin status
rladmin status database
rladmin status shards
rladmin status issues_only
```

Record:

- cluster name, version, node count, and quorum state
- database name, endpoint, shard count, replication status, and placement policy
- current primary and replica shard locations
- application client library, connection target, timeout, retry, and reconnect behavior
- baseline p95/p99 latency, throughput, connection count, CPU, memory, disk I/O, and replication lag
- exact planned start time, stop condition, and rollback contact

Keep a representative workload active during the test; idle connections do not validate resilience.

## Scenario Selection

Choose one scenario per test window.

| Scenario | Purpose | How to simulate | Expected result |
| --- | --- | --- | --- |
| Primary shard process stop | Validate replica promotion. | Stop or kill the Redis process for the selected primary shard. | Temporary errors, replica promotion, client reconnect. |
| Replica process or node stop | Validate HA while a replica is unavailable. | Stop the replica Redis process or reboot the replica host. | No client outage; replica recovers or is rebuilt. |
| Shard migration | Validate application behavior during data movement. | `rladmin migrate shard <SHARD_ID> target_node <NODE_ID>` | Service resumes on target node; latency may rise. |
| Endpoint migration | Validate endpoint rebind behavior. | Use the version-appropriate `rladmin migrate endpoint_to_shards` workflow. | Clients remain connected through DNS endpoint after migration. |
| Network isolation | Validate partition handling and client reconnect. | Temporarily block traffic with firewall rules or supervisor-controlled isolation. | Monitoring degrades; shards promote or resync after recovery. |
| Non-serving node reboot | Validate control-plane tolerance. | Reboot a node that does not host serving shards. | Temporary admin errors only; no data-path outage. |

## Execution Workflow

1. Reconfirm no unresolved `rladmin status issues_only` items affect the test.
2. Start monitoring dashboards and application log capture before inducing the failure.
3. Announce the scenario, target node/shard, exact command, and expected impact.
4. Apply only the selected failure action.
5. Measure disconnect duration, recovery time, errors, latency, throughput, and reconnect behavior.
6. Stop the test when the expected promotion, migration, or recovery condition is met.
7. Restore any blocked network path, stopped service, or rebooted node.
8. Capture post-test `rladmin status`, `rladmin status shards`, and `rladmin status issues_only`.

## Validation Handoff

After the simulation, use `redis-software-resiliency-test-analysis` for the post-test review.

The post-test answer should identify:

- whether the cluster returned to Optimal
- whether primary/replica roles and endpoints ended in the expected location
- whether clients used DNS endpoints and reconnected automatically
- the measured outage or degraded-service window
- any placement, client, routing, or capacity changes needed before the next drill

## Escalation Packet

If failover does not complete cleanly, collect a support package before attempting risky recovery. Include the test timeline, target node or shard, command used, `rladmin` outputs, logs from `/var/opt/redislabs/log/`, monitoring graphs, and application reconnect logs.
