---
name: redis-cloud-monitoring-setup
description: "Set up and troubleshoot built-in Redis Cloud monitoring, console metrics, alerts, REST API metrics, and plan-specific external monitoring eligibility. Use when the user asks where to view Redis Cloud metrics, configure database alerts, enable alert email notifications, retrieve metrics through the Redis Cloud API, or understand when Prometheus, Grafana, Datadog, New Relic, or Dynatrace require Pro/private networking."
---

# Redis Cloud Monitoring Setup

Use this skill for Redis Cloud monitoring onboarding and built-in console/API monitoring.

## Plan-Aware Guidance

| Capability | Essentials | Pro |
| --- | --- | --- |
| Console metrics | Available | Available |
| Email alerts | Limited or plan-dependent | Available |
| REST API metrics/status | Available where API permissions allow | Available where API permissions allow |
| Prometheus/Grafana/Datadog/APM | Usually not available because private metrics access is absent | Available when private networking is configured |

Verify current plan capabilities in the Redis Cloud Console or current docs before making a final eligibility claim.

## Console Metrics Workflow

1. Sign in to Redis Cloud Console.
2. Select the subscription and database.
3. Open the database `Metrics` view.
4. Review:
   - Throughput / ops/sec.
   - Latency.
   - Memory usage.
   - Active connections.
   - CPU or plan-specific utilization signals.
5. Compare the time window against application incidents, deploys, imports, scaling, or maintenance.

## Alert Setup

1. Open the database configuration or alerts area.
2. Add alert rules for relevant conditions:
   - High memory usage.
   - Connection spikes.
   - Dataset approaching limits.
   - Throughput/latency symptoms where supported.
3. Confirm which users receive notifications. In Redis Cloud this often depends on each team member’s notification settings in Access Management.
4. Save the alert and verify it appears active.

Do not assume webhooks or third-party destinations are available for every plan; verify in the current console.

## REST API Monitoring

Use the Redis Cloud REST API when the user needs custom dashboards, automation, or CI/CD checks.

1. Create or identify an API key in account settings/API access.
2. Confirm the key has permission to read subscription/database status and metrics.
3. Use API calls for real-time status, historical snapshots where supported, alert state, or inventory.
4. Store API secrets securely and avoid logging them.

## External Monitoring Routing

When the user asks for external monitoring:

- Prometheus/Grafana: use the Redis Cloud Prometheus/Grafana monitoring skill.
- Datadog: use the Redis Cloud Prometheus/Datadog monitoring skill.
- New Relic/Dynatrace: verify current Redis Cloud integration guidance and private networking requirements.

External metrics scraping typically needs Redis Cloud Pro plus VPC peering, Private Service Connect, or equivalent private connectivity to the internal metrics endpoint.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Console metrics missing | Refresh console, verify database selection, permissions, and plan state. |
| Alerts not triggering | Check threshold, alert enabled state, metric availability, and user notification settings. |
| User not receiving alert emails | Confirm team member notification preferences and email delivery/spam handling. |
| API metrics missing | Verify API key permissions, endpoint path, subscription/database ID, and plan eligibility. |
| Prometheus not receiving data | Confirm Pro/private networking, internal host, port 8070, and security rules. |

## Evidence To Collect

- Subscription plan and database ID.
- User role and notification preference state.
- Alert rule configuration.
- Time window and metrics screenshot/API response.
- API key permission scope, without exposing secrets.
- Private networking status for external monitoring issues.
