---
name: redis-cloud-prometheus-datadog-monitoring
description: "Configure and troubleshoot Redis Cloud Pro monitoring with Prometheus, Grafana, and Datadog OpenMetrics. Use when the user asks for the Redis Cloud metrics endpoint, why Essentials cannot be scraped, how to use port 8070 `/v2`, VPC peering or Private Service Connect requirements, Prometheus target DOWN errors, Datadog `rdsc` metrics, TLS verification, or Redis Cloud observability setup."
---

# Redis Cloud Prometheus Datadog Monitoring

Use this skill when integrating Redis Cloud metrics with Prometheus/Grafana or Datadog.

## Eligibility Checks

1. Confirm the subscription is Redis Cloud Pro or otherwise currently supports private metrics access.
2. Confirm private networking from the monitoring environment to Redis Cloud:
   - VPC peering, Private Service Connect, or the current supported private connectivity option.
   - Routes and security groups allow port `8070`.
3. Confirm the monitoring host/agent runs inside the connected VPC/network.
4. Locate the database internal host in Redis Cloud Console and use port `8070`.
5. Verify current Redis Cloud documentation/console if plan capabilities or endpoint details appear different.

Redis Cloud Essentials does not normally expose the private metrics endpoint required for Prometheus/Datadog scraping.

## Metrics Endpoint

Endpoint shape:

```text
https://<internal_host>:8070/v2
```

Prometheus targets often omit the path in `targets` and rely on the default metrics path or configured path; Datadog OpenMetrics uses the full endpoint URL.

## Prometheus Setup Shape

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: redis-cloud
    scheme: https
    metrics_path: /v2
    tls_config:
      insecure_skip_verify: true
    static_configs:
      - targets:
          - <internal_host>:8070
```

Use `insecure_skip_verify` only for testing or where the certificate trust path is intentionally handled elsewhere. Prefer a valid CA bundle in production.

Verify in Prometheus:

- `Status -> Targets`
- Target state is `UP`
- Scrape error field is empty

## Datadog Setup Shape

Redis Cloud Datadog OpenMetrics config shape:

```yaml
instances:
  - openmetrics_endpoint: https://<internal_host>:8070/v2
    namespace: rdsc
    ssl_verify: false
```

After restarting the Datadog Agent, verify:

- Agent status shows the Redis Cloud/OpenMetrics check.
- Agent logs show successful scrape attempts.
- Metrics Explorer contains `rdsc` metrics such as a database-up signal.

Use `ssl_verify: false` only for testing or when explicitly accepted. Prefer CA validation in production.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Prometheus target is DOWN | Routing, peering/PSC, security group, DNS, or port 8070 blocked | Test connectivity from the Prometheus host and verify private networking. |
| No Datadog metrics | Agent config path, OpenMetrics config, namespace, or restart issue | Check `conf.d/redis_cloud.d/conf.yaml`, agent status, and logs. |
| TLS handshake or cert error | CA trust mismatch | Use a valid CA bundle; only disable verification for controlled testing. |
| Authentication failure | Missing/wrong Redis Cloud API or integration credentials | Verify credentials and integration configuration. |
| Essentials subscription cannot scrape | Plan lacks required private metrics access | Move monitoring requirement to Pro or another supported subscription. |
| Metrics host unreachable | Using public endpoint instead of internal host | Copy the internal host from the database configuration and change the port to 8070. |

## Evidence To Collect

- Subscription plan/type and database ID.
- Internal host and target endpoint with secrets removed.
- Connectivity method: VPC peering, PSC, or other.
- Security group/firewall rules for port 8070.
- Prometheus scrape config and target error.
- Datadog Agent config, status output, and relevant logs.
- TLS verification mode and CA bundle details.
