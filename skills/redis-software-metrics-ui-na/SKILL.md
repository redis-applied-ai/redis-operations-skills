---
name: redis-software-metrics-ui-na
description: Use when Redis Software Metrics UI shows N/A, blank graphs, missing node/database/shard metrics, active change pending, shard migration or failover metric gaps, large-cluster UI limits, metrics exporter issues, /metrics versus /v1 versus /v2 exporter behavior, master-node resource pressure, or Prometheus/Grafana visibility gaps.
---

# Redis Software Metrics UI N/A

Use this skill when Redis Software Metrics UI shows `N/A` or blank values instead of expected metrics. Treat it as a visibility and metrics-pipeline issue unless Redis health checks show a deeper cluster problem.

## First Checks

1. Refresh the UI and reauthenticate.
2. Check whether the cluster is in an active change, failover, shard migration, or resharding window.
3. Run:

```text
rladmin status
rladmin status extra all
supervisorctl status all
```

4. Confirm nodes are healthy and reachable.
5. Check whether the cluster master node has CPU, memory, disk, and network headroom.

Temporary `N/A` during migrations, failovers, or resharding can be expected. Wait for the operation to settle before declaring metrics broken.

## Metrics Pipeline Checks

Inspect logs:

```text
/var/opt/redislabs/log/metrics_exporter.log
/var/opt/redislabs/log/event_log.log
```

Check for:

- metrics exporter errors
- API errors
- low disk, memory, or network alerts
- exporter service restarts
- external Prometheus or Grafana scrape failures

## Version And Exporter Guidance

Verify the Redis Software version before advising exporter changes.

- For Redis Software releases that support the stream metrics engine, confirm it is enabled.
- For Redis Software 8 and later, prefer the `/v2` stream exporter for external monitoring when supported by the deployment.
- For older deployments, confirm whether `/metrics`, `/v1`, or `/v2` is the supported path.
- For large clusters, external Prometheus/Grafana visibility may be more reliable than UI aggregation.

Do not assume exporter paths or PromQL mappings without checking the deployed version.

## Large Cluster And UI Limits

If the cluster has a high shard count and the UI does not fully populate:

- check external monitoring first
- inspect exporter data directly
- use Grafana/Prometheus for complete visibility
- treat UI gaps separately from actual database health

## Master Node Pressure

If metrics gaps correlate with cluster master resource pressure, consider moving the cluster master role to a healthier node:

```text
rladmin cluster master set <node_id>
```

Before doing this, confirm the target node is healthy and record current cluster state. This is an operational change and should be done during an appropriate window for production clusters.

## Escalation Package

Collect:

- Redis Software version
- screenshots of affected UI pages
- `rladmin status` and `rladmin status extra all`
- metrics exporter and event logs
- active change or migration timeline
- shard count and database count
- external monitoring scrape status

## Response Pattern

Answer with:

1. Whether the issue is likely transient active-change behavior, UI scale limits, exporter configuration, or master resource pressure.
2. The read-only health and log checks.
3. Version-specific exporter guidance.
4. Operational next steps and escalation evidence.
