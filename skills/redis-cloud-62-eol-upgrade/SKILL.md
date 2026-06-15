---
name: redis-cloud-62-eol-upgrade
description: "Plan Redis Cloud upgrades for databases running Redis 6.2 ahead of end-of-life and automatic upgrade deadlines. Use when the user asks about Redis 6.2 EOL in Redis Cloud, automatic upgrades during maintenance windows, choosing a target Redis version, Pro single-region self-serve upgrades, Active-Active Redis-assisted upgrades, Terraform `redis_version`, maintenance exclusions, breaking-change review, or support/TAM upgrade planning."
---

# Redis Cloud 6.2 EOL Upgrade

Use this skill when a Redis Cloud database is running Redis 6.2 and needs EOL planning or upgrade guidance.

## Verify Current Dates

EOL dates, automatic-upgrade timing, supported target versions, and maintenance-exclusion policy are time-sensitive. Before quoting a date or committing to a plan, verify the current Redis Cloud version-management documentation, Redis Cloud Console notice, or Redis Support guidance.

The source guidance for this skill described Redis 6.2 EOL planning and automatic upgrades for Redis Cloud; do not assume those details remain current without verification.

## Planning Checklist

1. Inventory all Redis Cloud databases running Redis 6.2.
2. Classify deployment type:
   - Pro single-region.
   - Pro Active-Active / multi-region.
   - Mixed subscription.
   - Terraform-managed.
3. Choose a target Redis version deliberately after reading release notes and breaking changes.
4. Test application behavior in non-production.
5. Review client compatibility, command behavior, modules/capabilities, RESP behavior, and Search/JSON changes.
6. Plan maintenance window and rollback/failover expectations.
7. Engage TAM or Redis Support for complex environments or target-version uncertainty.

## Upgrade Method Selection

| Deployment | Typical method |
| --- | --- |
| Pro single-region database | Self-serve upgrade in Redis Cloud Console, API, or Terraform. |
| Pro Active-Active / multi-region | Redis-assisted upgrade request through the subscription workflow. |
| Mixed subscription | Use self-serve for eligible single-region databases and Redis-assisted request for Active-Active databases. |
| Terraform-managed | Update `redis_version` in Terraform and apply through the normal change process after validation. |

Verify exact UI/API/Terraform fields against current Redis Cloud docs before execution.

## Self-Serve Upgrade Flow

1. Confirm database and subscription.
2. Open the Redis Cloud Console database actions.
3. Select version upgrade.
4. Choose the target version.
5. Confirm maintenance/failover expectations.
6. Run the upgrade only after staging validation.
7. Monitor application errors, latency, memory, client connections, and command behavior.

## Active-Active Flow

1. Open the subscription upgrade request path.
2. Request Redis-assisted version upgrade.
3. Confirm target version, maintenance windows, and all databases included.
4. Coordinate with Redis on schedule and validation.
5. Monitor each region and client after the maintenance window.

## Compatibility Review

Check:

- Removed or deprecated commands.
- Query/Search parser and dialect changes.
- JSON/module capability behavior.
- RESP2/RESP3 client behavior.
- ACL category expansion or permission changes.
- Client library support for target version.
- Operational changes such as scaling, shard, or maintenance behavior.

## Automatic Upgrade Handling

If the database is approaching an automatic upgrade deadline:

- Treat automatic upgrade as a backstop, not a substitute for testing.
- Upgrade proactively in a controlled window.
- If requesting a maintenance exclusion, document the business justification and a target completion plan.
- Confirm whether exclusions are allowed for the current support policy.

## Escalation Packet

Collect:

- Account, subscription, and database IDs.
- Current Redis version and target version.
- Deployment type and regions.
- Maintenance windows.
- Non-production validation results.
- Client library versions.
- Known module/Search/JSON/RESP dependencies.
- Terraform/API configuration if managed as code.
