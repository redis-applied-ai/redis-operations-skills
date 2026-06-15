---
name: redis-software-prometheus-datadog-monitoring
description: "Configure and troubleshoot Redis Enterprise Software monitoring with Prometheus, Grafana, and Datadog. Use when the user asks about scraping every Redis Software node on port 8070, checking `metrics_exporter`, choosing `/v2` versus `/v1` or `/metrics`, Datadog `redis_enterprise.d` and `rdse` metrics, empty dashboards, 401/403 metrics errors, v1-to-v2 PromQL migration, or shard/proxy CPU hotspots."
---

# Redis Software Prometheus Datadog Monitoring

Use this skill to integrate Redis Enterprise Software node metrics with Prometheus/Grafana or Datadog.

## Requirements

1. Network access from Prometheus or the Datadog Agent to every Redis Enterprise cluster node on TCP `8070`.
2. `metrics_exporter` running on every node:

   ```bash
   rladmin status metrics_exporter
   ```

3. Correct exporter path for the deployed Redis Enterprise version:
   - Prefer `/v2` where supported.
   - Use `/v1` or `/metrics` only for older deployments that do not expose `/v2`.
4. TLS trust configuration and metrics authentication settings, if enabled.

Verify endpoint/version details against the deployed cluster before changing dashboards.

## Prometheus Configuration Shape

Scrape all cluster nodes:

```yaml
scrape_configs:
  - job_name: redis-enterprise
    scheme: https
    metrics_path: /v2
    tls_config:
      insecure_skip_verify: true
    static_configs:
      - targets:
          - <node1_ip>:8070
          - <node2_ip>:8070
          - <node3_ip>:8070
```

Use a real CA bundle in production instead of disabling TLS verification.

Verify:

- Prometheus `Status -> Targets` shows every Redis node as `UP`.
- Scrape errors are empty.
- Queries return node, database, shard, proxy, and syncer metrics.

## Grafana

1. Add Prometheus as a Grafana data source.
2. Import Redis Enterprise dashboards that match the metric endpoint generation (`/v1` versus `/v2`).
3. Validate cluster, node, database, shard, proxy, and CRDB panels.
4. If dashboards are empty after an endpoint migration, update PromQL queries using the appropriate mapping or import dashboards designed for the new metric stream.

## Datadog Configuration Shape

Use the Redis Enterprise integration and configure one OpenMetrics endpoint per node:

```yaml
instances:
  - openmetrics_endpoint: https://<node1_ip>:8070/v2
    namespace: rdse
    ssl_verify: false
  - openmetrics_endpoint: https://<node2_ip>:8070/v2
    namespace: rdse
    ssl_verify: false
```

After editing:

```bash
sudo systemctl restart datadog-agent
```

Verify in Datadog Agent status/logs and Metrics Explorer for `rdse` metrics.

## v1 To v2 Migration Guidance

- `/v2` metrics are more suitable for raw time-series collection and large multi-node deployments.
- Metric names and query shapes can change between endpoint generations.
- Do not assume existing dashboards continue to work after switching paths.
- Migrate dashboards and alerts deliberately, using a mapping guide or endpoint-specific dashboard set.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Prometheus target down | Exporter stopped, port 8070 blocked, wrong node address, TLS/auth issue | Check `rladmin status metrics_exporter`, firewall, endpoint path, and scrape logs. |
| `/v2` does not scrape | Cluster version or patch level lacks `/v2` | Use the supported legacy endpoint until upgraded. |
| 401/403 errors | Metrics auth enabled or wrong credentials | Check `metrics_auth` and scraper credentials. |
| Grafana panels empty | Dashboard/PromQL does not match endpoint generation | Import matching dashboards or update queries. |
| Datadog metrics missing | Agent config path, namespace, endpoint, or restart issue | Check `redis_enterprise.d/conf.yaml`, agent status, and logs. |
| Metrics differ by node | Mixed exporter versions or inconsistent scrape config | Verify node versions and consistent scrape intervals/paths. |
| High shard/proxy CPU | Load hotspot or routing pressure | Identify hot shard/proxy metrics, inspect slowlog, and evaluate resharding or scaling. |

## Evidence To Collect

- Redis Enterprise Software version and node list.
- `rladmin status metrics_exporter` output.
- Metrics path used per node.
- Prometheus target status and scrape errors.
- Datadog Agent config/status/logs.
- Grafana dashboard source/version and failing PromQL.
- TLS/auth configuration for metrics scraping.
