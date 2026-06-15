---
name: redis-cloud-terraform-auto-minor-upgrades
description: Use when configuring or troubleshooting Redis Cloud Terraform auto_minor_version_upgrade, Redis minor version drift, maintenance-window timing, replicated versus non-replicated upgrade impact, rollback expectations, provider-version behavior, Pro opt-out, or Essentials auto-upgrade constraints.
---

# Redis Cloud Terraform Auto Minor Upgrades

Use this skill when a user asks how Redis Cloud automatic minor version upgrades interact with Terraform. Keep the distinction clear: Terraform can express participation in the policy, but Redis Cloud owns the maintenance workflow and upgrade execution.

## First Checks

1. Identify the database, subscription, plan type, current Redis version, replication setting, and Terraform provider version.
2. Verify the current Redis Cloud policy and Terraform provider documentation before making version-eligibility, opt-out, or provider minimum-version claims.
3. Confirm whether the user needs:
   - downtime expectation
   - maintenance-window timing
   - Terraform drift handling
   - rollback planning
   - opt-out behavior
   - production rollout checklist

## Key Boundaries

- `auto_minor_version_upgrade` is a database-level policy setting.
- It is not a scheduler and does not choose the exact maintenance date.
- Maintenance windows are subscription-scoped, not controlled by the database resource.
- Automatic minor upgrades stay within the same major version.
- Major version upgrades remain customer-controlled unless current policy explicitly says otherwise.
- Redis Cloud does not provide automatic rollback to the previous Redis version after an upgrade.

## Availability Guidance

Map expected impact to replication:

- With replication enabled: no planned downtime is expected, but failover can still cause brief latency spikes, reconnects, or short client interruptions.
- Without replication: expect temporary downtime while shards restart from persistence.

For sensitive workloads, review client retry, reconnect, DNS, timeout, and Smart Client Handoffs behavior before enabling the policy in production.

## Terraform Drift Guidance

When Redis Cloud advances a minor version service-side, Terraform state and configuration can appear out of sync with the running database version.

Before enabling auto minor upgrades:

1. Check the Redis Cloud Terraform provider changelog and upgrade to a version that explicitly supports the setting and current drift behavior.
2. Run `terraform init -upgrade`.
3. Review whether `redis_version` is pinned in configuration.
4. Run `terraform plan` in non-production after a service-side version change if possible.
5. For Active-Active resources, inspect provider behavior carefully because version fields may have replacement semantics.

If a plan appears to downgrade Redis after a service-side upgrade, stop and update provider/configuration strategy before applying.

## Rollout Checklist

Before production rollout:

- confirm the subscription maintenance window
- confirm replication and persistence settings
- review target-version release notes and application compatibility
- take a backup or verify an existing backup
- document restore-based recovery procedures
- validate Terraform provider behavior in staging
- communicate that rollback is manual, not automatic
- monitor latency, reconnects, failovers, and command errors during and after maintenance

## Troubleshooting

- Unexpected version drift in Terraform: upgrade the provider, review pinned `redis_version`, and avoid applying plans that attempt an unintended downgrade.
- Cannot find maintenance window on the database resource: check subscription settings instead.
- Older database did not auto-upgrade: verify current eligibility for that Redis version and plan.
- Brief disconnects occurred despite replication: validate client failover and retry behavior.
- Change-management asks for rollback: prepare backup/restore procedures rather than promising in-place version rollback.

## Response Pattern

Answer with:

1. What Terraform controls.
2. What Redis Cloud controls.
3. Availability impact based on replication.
4. Maintenance-window location.
5. Drift and provider-version checks.
6. Backup/restore rollback plan.
