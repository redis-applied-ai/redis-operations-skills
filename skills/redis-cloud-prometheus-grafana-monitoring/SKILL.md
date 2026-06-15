---
name: redis-cloud-prometheus-grafana-monitoring
description: "Set up and troubleshoot Redis Cloud Pro monitoring with Prometheus and Grafana dashboards. Use when the user asks how to scrape the Redis Cloud private metrics endpoint, configure port 8070 and `/v2`, deploy Prometheus/Grafana in a peered VPC, import Redis observability dashboards, diagnose Prometheus target DOWN, empty Grafana panels, or Essentials monitoring limitations."
---

# Redis Cloud Prometheus Grafana Monitoring

Use this skill for Redis Cloud Pro metrics scraping and Grafana visualization.

## Requirements

1. Redis Cloud Pro or a current plan that supports private metrics scraping.
2. Private connectivity from the monitoring environment to Redis Cloud:
   - VPC peering, Private Service Connect, or current supported equivalent.
3. Monitoring host in the connected private network, ideally same provider/region.
4. Outbound access from Prometheus to Redis Cloud metrics on TCP `8070`.
5. Administrative access to Prometheus and Grafana.

Essentials generally cannot use this integration because it lacks the required private metrics access.

## Endpoint

Use the Redis Cloud internal host and metrics port:

```text
https://<internal_host>:8070/v2
```

Find the internal host in the Redis Cloud database configuration. Do not use the public database endpoint for Prometheus scraping.

## Prometheus Configuration Shape

```yaml
scrape_configs:
  - job_name: redis-cloud
    scheme: https
    metrics_path: /v2
    scrape_interval: 30s
    scrape_timeout: 30s
    static_configs:
      - targets:
          - <internal_host>:8070
```

Add TLS CA configuration for production. Avoid disabling certificate validation unless this is a controlled test environment.

## Verification

1. Open Prometheus `Status -> Targets`.
2. Confirm the Redis Cloud target is `UP`.
3. Run basic queries:

   ```text
   up
   redis_memory_used_bytes
   redis_connected_clients
   ```

Metric names can vary by endpoint/version; if a query returns nothing, inspect the scraped metric list before assuming collection failed.

## Grafana Setup

1. Add Prometheus as a Grafana data source.
2. Confirm Grafana can query `up` from that data source.
3. Import Redis observability dashboards that match the Redis Cloud metric stream.
4. Validate panels for:
   - Subscription or service health.
   - Database latency, memory, throughput, connections, and errors.
   - Active-Active or ReplicaOf metrics if the database uses those features.
5. Configure alerting separately; dashboard import alone does not create a complete alerting policy.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Prometheus target `DOWN` | Peering/PSC, DNS, route, security group, or port 8070 issue | Test DNS and TCP reachability from the Prometheus host. |
| TLS scrape error | CA trust or certificate mismatch | Configure CA trust; use insecure skip only for test. |
| Grafana panels empty | Data source URL, dashboard/metric mismatch, or Prometheus scrape failure | Query Prometheus directly and inspect available metric names. |
| Metrics lag | Scrape interval/timeout too aggressive or network latency | Tune scrape interval and timeout, then verify target health. |
| No database tags expected by dashboard | Metric stream does not expose custom tags | Adjust dashboard variables or create manual panels. |
| Multi-cluster view missing | Dashboard is single-cluster oriented | Build a federated or manually combined dashboard. |

## Alerting Starters

Consider alert rules for:

- Database availability/up metric.
- High latency.
- High memory utilization.
- Evictions.
- Rejected connections.
- Error rates or failed operations.
- Active-Active sync/lag signals where applicable.

## Evidence To Collect

- Redis Cloud subscription and database ID.
- Internal host endpoint with secrets removed.
- Private networking type and route/security group details.
- Prometheus config, target status, and scrape error.
- Grafana data source config and failing panel query.
- Dashboard version/source.
