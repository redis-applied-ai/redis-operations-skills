---
name: redis-deployment-monitoring-baseline
description: "Build baseline monitoring and alerting for Redis deployments across cluster, node, database, shard, proxy, and CRDB layers. Use when the user asks what Redis metrics to monitor, how to use Redis Enterprise UI, port 8070 metrics exporter, REST API, Prometheus, Grafana, Datadog, New Relic, Dynatrace, or how to triage memory, CPU, latency, connections, evictions, disk, network, and sync lag."
---

# Redis Deployment Monitoring Baseline

Use this skill to establish or audit monitoring coverage for Redis Cloud, Redis Enterprise Software, or Redis Enterprise on Kubernetes deployments.

## Monitoring Surfaces

| Surface | Best for | Limits |
| --- | --- | --- |
| Redis UI Console | Quick cluster, node, database, and shard checks | Limited history and granularity. |
| Metrics exporter on port `8070` | Prometheus-style time series and dashboards | Endpoint path and metric names depend on product/version. |
| REST API on `9443` | Automation and real-time stats | Not a replacement for time-series retention. |
| Logs | Incident timelines and root-cause evidence | Requires node/file access for full detail in Redis Software. |
| External monitoring | Alerts, history, dashboards, SLOs | Requires network, auth, and dashboard maintenance. |

Verify the correct exporter path for the deployed version, commonly `/v2` for newer Redis Enterprise metrics streams and `/metrics` or `/v1` for older environments.

## Metric Layers

Monitor at each layer instead of relying on one aggregate:

- Cluster: health, quorum, alerts, users count, provisioning errors.
- Node: CPU, RAM, disk, network, process health.
- Database: ops/sec, memory, latency, connections, evictions, persistence, endpoint availability.
- Shard: CPU, memory, key distribution, hot keys, slow commands.
- Proxy: routing health, connection errors, TLS failures, endpoint pressure.
- CRDB/ReplicaOf/Syncer: sync status, lag, replication errors, backlog.

## Baseline Metrics

Treat thresholds as workload-specific starting points.

| Signal | Watch for |
| --- | --- |
| Memory | Growth trend, high utilization, evictions, fragmentation, swap. |
| CPU | Sustained high shard/node CPU, especially when latency rises. |
| Latency | Spikes, p95/p99 changes, or trend regression. |
| Throughput | Unexpected drops or spikes in commands/sec. |
| Connections | Sudden growth, churn, rejected clients, near-limit behavior. |
| Evictions/expiry | Unexpected evictions or expiration bursts. |
| Disk/storage | Low persistent or ephemeral storage for logs, backups, persistence, or configs. |
| Network I/O | Throughput spikes, saturation, inter-region or client egress changes. |
| Sync lag/status | CRDB or ReplicaOf lag and out-of-sync status. |

## Setup Workflow

1. Identify deployment type, version, network topology, and monitoring tool.
2. Confirm metrics endpoint access from the monitoring system:

   ```text
   https://<host>:8070/<path>
   ```

3. Configure Prometheus, Datadog, New Relic, Dynatrace, OpenTelemetry, Telegraf, or another scraper/API integration.
4. Import or build dashboards for cluster, node, database, shard, proxy, and CRDB views.
5. Add alerts for availability, memory pressure, CPU, latency, connections, disk, evictions, sync lag, and exporter health.
6. Create runbook links from alerts to first-check commands and dashboards.

## Symptom Triage

| Symptom | First checks |
| --- | --- |
| Memory at limit | Database memory, shard distribution, eviction policy, big keys, TTL coverage, fragmentation. |
| High CPU | Slowlog, hot keys, query workload, shard imbalance, proxy/syncer CPU. |
| Latency drop or throughput drop | CPU, slow commands, hot keys, network, persistence, resharding, failover events. |
| Connection failures | Endpoint reachability, TLS/auth, max clients, proxy logs, reconnect storms. |
| Disk pressure | Log growth, backup/persistence files, configuration storage, cleanup policy. |
| CRDB lag | Syncer status, inter-region network, write rate, conflict/tombstone behavior. |

## Logs To Pair With Metrics

For Redis Enterprise Software, pair metric anomalies with logs under `/var/opt/redislabs/log/`, especially:

- `event_log.log`
- `cluster_wd.log`
- `node_wd.log`
- `dmcproxy.log`
- `cnm_exec.log`
- `redis-<ID>.log`

## Evidence To Collect

- Deployment type and version.
- Metrics endpoint path and scrape status.
- Dashboard screenshots or metric query output for the incident window.
- Alert names and thresholds.
- Relevant logs from the same time window.
- Recent changes: deploys, maintenance, scaling, failover, imports, resharding, network changes.
