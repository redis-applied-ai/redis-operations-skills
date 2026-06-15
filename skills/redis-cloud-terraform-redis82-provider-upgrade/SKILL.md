---
name: redis-cloud-terraform-redis82-provider-upgrade
description: Use when Terraform apply, plan, or CI fails for Redis Cloud databases after upgrading to Redis 8.2 or later, especially with RedisLabs/rediscloud provider schema errors, unknown fields, `query_performance_factor` module gating, Redis 8.x module list drift, ForceNew database replacement risk, stale `.terraform.lock.hcl`, provider constraints below compatible versions, or needing `terraform init -upgrade` guidance.
---

# Redis Cloud Terraform Redis 8.2 Provider Upgrade

Use this skill when Redis Cloud runtime service is healthy but Terraform can no longer plan or apply after a database reaches Redis 8.2 or later. Provider behavior changes over time, so verify the current RedisLabs/rediscloud provider release in the Terraform Registry before recommending an exact version.

## Core Safety Rule

If `terraform plan` proposes replacing a Redis Cloud database because of provider drift or schema mismatch, stop. Do not approve the apply until the provider is upgraded, Terraform is reinitialized, and a new plan no longer shows unintended replacement.

This issue affects Terraform state reconciliation and update flows; it does not by itself mean the running Redis Cloud database or data is damaged.

## Diagnosis

Collect:

```bash
terraform providers
terraform version
terraform init -upgrade
terraform plan
```

Inspect:

- `required_providers` constraint for `RedisLabs/rediscloud`
- `.terraform.lock.hcl` pinned provider version
- CI/CD provider cache or plugin cache
- Redis Cloud database Redis version
- plan output for `forces replacement` or `will be replaced`
- errors mentioning unsupported arguments, unknown attributes, modules, or `query_performance_factor`

## Version Behavior Baseline

Source-derived Redis 8.2 behavior:

| Provider range | Typical Redis 8.2 symptom | Action |
| --- | --- | --- |
| `< 2.1.2` | older plans could show replacement or module-list drift | Upgrade provider, reinitialize, and re-plan. |
| `>= 2.1.2` and `< 2.5.0` | creation or update can fail on Redis 8.x feature/module validation such as `query_performance_factor` | Upgrade provider, reinitialize, and re-plan. |
| `>= 2.5.0` | Redis 8.2 create/update behavior is compatible in the source baseline | Prefer a newer verified provider for full current 8.x coverage. |

The source recommends `>= 2.8.0` and treats `2.5.0` as the minimum compatible baseline. Verify the current recommended version before editing production IaC.

## Remediation Workflow

1. Update provider constraints:

   ```hcl
   terraform {
     required_providers {
       rediscloud = {
         source  = "RedisLabs/rediscloud"
         version = ">= 2.8.0"
       }
     }
   }
   ```

2. Reinitialize:

   ```bash
   terraform init -upgrade
   ```

3. Re-run plan:

   ```bash
   terraform plan
   ```

4. Confirm the plan does not replace the Redis database unless replacement is intentional and approved.
5. Apply only after the plan shows the intended update.
6. Commit the updated provider constraint and `.terraform.lock.hcl` so CI uses the same provider.

## CI/CD Fixes

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Local works, CI fails | CI uses old lock file or plugin cache. | Commit lock file, clear cache, run `terraform init -upgrade` in CI. |
| Provider did not upgrade | Constraint is pinned or too narrow. | Relax the constraint and reinitialize. |
| Plan still proposes replacement | Old state/provider cache or incompatible provider remains. | Re-check `terraform providers`, lock file, and plan diff before apply. |
| Urgent database change is blocked | Terraform provider path is broken. | Make the urgent change in Redis Cloud Console only with change approval, then upgrade provider and reconcile Terraform state. |

## Escalation Packet

Collect:

- provider constraint and resolved provider version
- Redis Cloud database ID and Redis version
- sanitized `terraform plan` excerpt showing the failure or replacement risk
- exact error text
- `.terraform.lock.hcl` provider entry
- whether the failure happens locally, in CI, or both
- whether any manual Console change was made while Terraform was blocked
