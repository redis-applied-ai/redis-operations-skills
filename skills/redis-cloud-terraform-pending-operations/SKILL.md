---
name: redis-cloud-terraform-pending-operations
description: Use when Redis Cloud Terraform creates, updates, or deletes databases and resources show Pending, Queued, Updating, Modifying, slow apply, provider timeout, or apparent stall because multiple database lifecycle operations in the same subscription are serialized, CI jobs conflict, Terraform targets too broad a scope, or the user worries queued databases are offline.
---

# Redis Cloud Terraform Pending Operations

Use this skill when Redis Cloud databases show `Pending` or `Queued` during Terraform automation. The main distinction is control-plane queueing versus data-plane downtime.

## Safety Rules

- Do not tell the user to delete or recreate databases to clear a pending state.
- Do not start another broad `terraform apply` until the active Redis Cloud operation is known.
- Verify live Redis Cloud Console/API state and current Terraform provider behavior before declaring an operation stuck.
- Treat provider timeouts as state-reconciliation events: confirm cloud state before reapplying.

## Core Model

Redis Cloud database lifecycle changes may be serialized at the subscription level. In that model:

- one database create, update, resize, version change, or delete runs actively
- additional database changes in the same subscription wait as `Pending` or `Queued`
- Terraform may appear slow while it waits for Redis Cloud to finish prior operations
- queued status does not itself mean existing databases are offline

Availability impact, if any, is usually tied to the database actively being modified, not every queued database in the subscription.

## First Checks

Collect:

- subscription ID, database IDs, plan type, region, and cloud provider
- Terraform provider version and resource names
- exact Terraform operation: create, update, delete, resize, version change, network change
- whether more than one database in the same subscription is changing
- whether other CI/CD jobs, manual Console changes, or API automation are running
- current Redis Cloud Console status for each database
- client impact for existing databases

## Determine Expected Queueing

Use Redis Cloud Console or API to identify the active operation:

- one database shows active update/modifying state
- other databases show pending/queued
- Terraform logs show resources waiting rather than failing
- existing databases continue to accept normal traffic

If this pattern holds, explain that Terraform is waiting on managed service serialization and that the safe action is to let the active operation complete.

## Terraform Workflow Guidance

Reduce avoidable contention:

```bash
terraform plan
terraform apply -target=<specific_resource_address>
```

Use `-target` sparingly for controlled operations, then return to normal full-plan reconciliation.

For large changes:

- split database lifecycle changes into separate applies
- sequence changes one database at a time within the same subscription
- prevent concurrent CI jobs from modifying the same subscription
- use pipeline locks or environment-level concurrency controls
- run broad drift checks only after active database operations finish
- use separate Redis Cloud subscriptions when parallel lifecycle changes are a real requirement

For API rate-limit failures, use the Redis Cloud API 429 skill instead.

## Provider Timeout Handling

If Terraform times out:

1. Stop retry loops.
2. Check Redis Cloud Console/API for the final resource state.
3. Confirm whether the active operation is still running.
4. Refresh state if needed:

   ```bash
   terraform plan -refresh-only
   ```

5. Reapply only after the previous operation is finished.
6. If the provider supports resource timeouts for the affected resource, adjust them through normal provider configuration after verifying current provider docs.

Do not assume a timeout means the Redis Cloud operation failed; it may have completed after Terraform stopped waiting.

## Data-Plane Availability Check

For existing databases that are merely queued:

```bash
redis-cli -h <endpoint-host> -p <port> PING
```

Adapt TLS, username, password, and CA flags without exposing credentials.

Interpretation:

- `PONG`: data path is healthy; focus on Terraform queueing and control-plane status.
- connection error on a database actively being modified: inspect the specific operation and maintenance expectations.
- multiple unrelated databases fail: check Redis Cloud status page, network path, and account/subscription status.

## Common Findings

| Symptom | Meaning | Action |
| --- | --- | --- |
| several DBs `Pending` during one apply | queued behind active subscription operation | wait and monitor the active operation |
| Terraform appears stuck but Console shows progress | provider is waiting for Redis Cloud lifecycle operation | avoid interrupting unless change window requires it |
| two pipelines both modify same subscription | automation contention | add CI lock or split environments |
| apply timed out | provider wait limit exceeded or operation still running | verify live state before reapplying |
| user worries queued DBs are down | pending is control-plane state | test data path and explain scope |

## Escalation Packet

Collect:

- Terraform provider version and resource addresses
- sanitized plan/apply output around the waiting or timeout
- subscription ID and database IDs
- Redis Cloud Console/API status for active and pending databases
- list of concurrent CI/manual/API operations
- elapsed time and start time of the active operation
- whether existing database traffic is impacted
- any Redis Cloud task or activity IDs visible in Console/API

## Response Shape

When answering, state:

1. Whether this looks like expected serialization or a stuck operation.
2. Which database operation is active.
3. Whether pending databases are data-plane healthy.
4. The safest next Terraform action.
5. How to prevent future contention.
