---
name: redis-cloud-pro-rest-api-automation
description: "Automate Redis Cloud Pro subscriptions and databases through the Redis Cloud REST API, including API key authentication, Swagger UI discovery, cURL/REST clients, subscription and database create/update/delete operations, payment method lookup, async task polling with `/v1/tasks/{taskId}`, Terraform/Pulumi/IaC integration, Active-Active database enumeration gaps in Terraform, API key CIDR allowlists, rate limiting, 429 retries, and Pro endpoint troubleshooting."
---

# Redis Cloud Pro REST API Automation

Use this skill when a Redis Cloud Pro user wants to automate subscription or database lifecycle operations through the Redis Cloud REST API. For Essentials-specific endpoint eligibility questions, use `redis-cloud-essentials-rest-api`.

## Safety Rules

- Never ask users to paste API secrets, account keys, Terraform variables containing secrets, or full request headers into chat.
- Store API credentials in a secrets manager, CI/CD secret store, or protected environment variables.
- Restrict API key usage with CIDR allowlists when the account supports it and the automation source networks are stable.
- Treat create, update, and delete calls as production changes requiring change approval.
- Require explicit confirmation before any `DELETE` operation, naming the subscription ID or database ID.
- Log task IDs and request IDs, but redact secrets and sensitive billing details.

## Authentication Model

Redis Cloud API requests use account-scoped API keys tied to a Redis Cloud user and that user's permissions.

Headers:

```text
x-api-key: <account-key>
x-api-secret-key: <secret-key>
```

Base endpoint:

```text
https://api.redislabs.com/v1
```

Safe read-only smoke test:

```bash
curl -sS "https://api.redislabs.com/v1/subscriptions" \
  -H "accept: application/json" \
  -H "x-api-key: ${REDIS_CLOUD_API_KEY}" \
  -H "x-api-secret-key: ${REDIS_CLOUD_API_SECRET}"
```

API keys may not expire automatically. Rotate them periodically and immediately after suspected exposure or staff changes.

## Access Method Selection

| Method | Use For | Avoid For |
| --- | --- | --- |
| Swagger UI | Endpoint discovery, schema inspection, ad-hoc testing, payload validation | Production automation or repeatable workflows |
| REST client or script | Operational automation, custom checks, advanced workflows | Declarative infrastructure ownership |
| Terraform or Pulumi | Repeatable subscription/database management | Capabilities not modeled by the provider or urgent one-off recovery |
| Direct REST plus IaC | Provider gaps such as full enumeration or read-only checks | Making unmanaged changes that create IaC drift |

## Lifecycle Operations

Common Pro API operations:

| Goal | Endpoint Shape |
| --- | --- |
| List subscriptions | `GET /v1/subscriptions` |
| Create subscription | `POST /v1/subscriptions` |
| Update subscription | `PUT /v1/subscriptions/{subscriptionId}` |
| Delete subscription | `DELETE /v1/subscriptions/{subscriptionId}` |
| List databases in subscription | `GET /v1/subscriptions/{subscriptionId}/databases` |
| Create database | `POST /v1/subscriptions/{subscriptionId}/databases` |
| Update database | `PUT /v1/subscriptions/{subscriptionId}/databases/{databaseId}` |
| Delete database | `DELETE /v1/subscriptions/{subscriptionId}/databases/{databaseId}` |
| List payment methods | `GET /v1/payment-methods` |

Before create or update:

1. Verify current request schema in Swagger or API docs.
2. Confirm provider, region, network CIDR, payment method, size, and database settings.
3. Validate the payload in non-production or with a low-risk account when possible.
4. Confirm the operation is supported for Pro and the current account role.

## Async Task Handling

Most create, update, and delete operations are asynchronous and return a `taskId`.

Automation must:

1. Persist the `taskId`.
2. Poll task status:

   ```text
   GET /v1/tasks/{taskId}
   ```

3. Wait for completion before dependent operations.
4. Treat failure, timeout, or unknown status as blocking.
5. Fetch the affected subscription/database after completion to verify final state.

Do not start dependent database, peering, alert, backup, or deletion steps until the parent task is complete.

## IaC Guidance

For Terraform:

```hcl
provider "rediscloud" {
  api_key    = var.redis_cloud_api_key
  api_secret = var.redis_cloud_api_secret
}
```

Guidance:

- Use variables backed by secret storage, not literals in `.tf` files.
- Pin and periodically update the Redis Cloud provider after checking the registry and changelog.
- Reduce Terraform parallelism when API throttling appears.
- Re-run plan after provider upgrades and verify no unintended database replacement is proposed.
- Some Active-Active database scenarios may not be fully modeled by Terraform; use REST API reads such as database listing for visibility, then avoid unmanaged writes unless approved.

## Rate Limits And 429

Redis Cloud enforces per-key request limits, and those limits can change. Verify current docs and response headers before building fixed limits into automation.

For 429 responses:

1. Honor retry headers when present.
2. Use exponential backoff with jitter.
3. Stagger CI/CD jobs and scheduled automation.
4. Cache repeated reads within a job.
5. Use separate API keys for independent workflows when policy allows.
6. Use `redis-cloud-api-429-troubleshooting` for persistent throttling or Terraform-specific failures.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Authentication fails | Wrong, revoked, exposed, or mismatched key pair | Rotate or regenerate keys and update secret stores. |
| `Access Denied` | User/key lacks permissions or wrong account context | Verify key owner role, account, and operation permissions. |
| `Endpoint Not Allowed` | Plan, API version, or feature eligibility mismatch | Verify Pro endpoint support in live API docs or Swagger. |
| 429 Too Many Requests | Shared key, synchronized jobs, or excessive polling | Add backoff, reduce concurrency, and cache repeated reads. |
| Task never completes | Async operation still running, failed, or blocked | Poll task status, fetch final resource state, and escalate with task ID. |
| Terraform misses Active-Active databases | Provider coverage gap | Use REST API listing for visibility and confirm provider limitations before changing state. |
| Swagger payload fails | Example payload not adjusted to account state | Verify required fields, payment method, region, network CIDR, and database settings. |
| Unexpected 4xx/5xx | Bad payload, invalid ID, service issue, or transient failure | Capture redacted request, response, timestamp, and request/task ID. |

## Escalation Packet

Collect without secrets:

- Account or organization.
- Pro subscription ID and database ID, if relevant.
- Endpoint, method, and purpose.
- Redacted payload shape.
- HTTP status, response body, request ID, and timestamp.
- `taskId` and task status history.
- Automation tool and version, such as Terraform provider version.
- Whether Swagger, cURL, and IaC fail the same way.
- Recent key rotation, role change, plan change, or API provider upgrade.

## Response Shape

When helping a user:

1. Confirm Pro subscription context and API key permissions.
2. Start with a safe read-only smoke test.
3. For lifecycle operations, identify the endpoint, payload, expected task, and post-task verification.
4. Call out destructive operations and require explicit confirmation before deletion.
5. For automation, include rate limiting, task polling, secret storage, and IaC drift controls.
