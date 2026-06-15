---
name: redis-cloud-alert-setup
description: Use when configuring, troubleshooting, or automating Redis Cloud alerts for database health, dataset size, throughput, latency, connection count, Replica Of sync failures, replication lag, email recipients, verified users, webhooks, REST API alert rules, Terraform-managed alerts, Test Notification, or plan-specific alert availability.
---

# Redis Cloud Alert Setup

Use this skill to configure and troubleshoot Redis Cloud alerting. Alert names, ranges, webhook support, and plan eligibility can change; verify current Console, API, or Terraform provider behavior before quoting exact thresholds.

## Setup Workflow

1. Identify the subscription, database, plan, and user role.
2. Open the database alert settings in Redis Cloud Console.
3. Select alert types relevant to the workload:
   - dataset size or plan usage
   - high or low throughput
   - high latency
   - connection count
   - replica sync failure or replication lag
4. Set thresholds based on baseline metrics and SLOs.
5. Configure recipients through Access Management.
6. Save rules and send a test notification if available.
7. Confirm alert state appears in activity logs, API output, or external incident tooling.

## Recipient Checks

For email alerts:

- recipient must be a team member or allowed recipient according to current Redis Cloud rules
- email must be verified
- user role must permit alert visibility or management where applicable
- spam filtering and email allowlists must not block Redis Cloud messages

For webhooks:

- verify plan support
- use HTTPS endpoint
- check firewall, allowlist, and TLS certificate validity
- test delivery from Redis Cloud
- confirm incident platform response codes and retries

## Programmatic Management

Use REST API or Terraform when:

- alerts must be consistent across many databases
- infrastructure is managed as code
- change review is required
- drift detection matters

Before automating, inspect an existing alert rule from the API or provider to confirm current field names, metric IDs, and allowed ranges.

## Troubleshooting

- Emails not received: verify recipient, email verification, spam folder, and role/access settings.
- Alert not firing: confirm database load actually crosses threshold and that the rule is enabled.
- Too noisy: raise threshold, add runbook context, or use downstream deduplication.
- Webhook not firing: test notification, inspect endpoint TLS, firewall, response code, and payload handling.
- Alert type missing: verify plan, database type, subscription type, and user permissions.
- Terraform drift: compare provider version and live API rule output.

## Response Pattern

Answer with:

1. The database and metric that need alerting.
2. Baseline-driven threshold recommendation.
3. Recipient or webhook setup.
4. Test and verification step.
5. Plan/API/Terraform current-state checks when needed.
