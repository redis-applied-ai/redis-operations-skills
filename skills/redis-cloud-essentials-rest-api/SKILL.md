---
name: redis-cloud-essentials-rest-api
description: "Enable, authenticate, and troubleshoot Redis Cloud REST API access for Essentials subscriptions, including API key creation, Swagger UI authorization, cURL requests, `x-api-key` and `x-api-secret-key` headers, endpoint availability differences, Access Denied or Endpoint Not Allowed responses, expired keys, HTTP 4xx/5xx errors, and API rate limiting or 429 handling."
---

# Redis Cloud Essentials REST API

Use this skill when a Redis Cloud Essentials user wants to use the Redis Cloud REST API or debug an API access problem. Essentials can use the REST API, but endpoint availability can differ from Pro and can change over time, so verify current API documentation or live Swagger behavior before promising a specific endpoint.

## Safety Rules

- Never ask the user to paste API secrets, account keys, full headers, or bearer material into chat.
- Prefer a secrets manager, environment variables, or local protected shell variables for API credentials.
- Treat account IDs, subscription IDs, database IDs, and billing/API outputs as sensitive operational data.
- Regenerate and rotate keys if credentials were exposed.
- For automation, apply rate limiting, backoff, and jitter before increasing concurrency.

## Enable API Access

1. Sign in to Redis Cloud with an account that can manage API keys.
2. Open `Access Management`.
3. Open the `API Keys` tab.
4. If API access is not enabled, use the Console action to enable it and generate the account key.
5. Copy the account key and secret key into approved secret storage.
6. Record which user or automation owns the key and what workflows use it.

## Authentication Headers

Redis Cloud REST API requests use:

```text
x-api-key: <account-key>
x-api-secret-key: <secret-key>
```

Base endpoint:

```text
https://api.redislabs.com/v1
```

Do not place real key values directly in shell history. Prefer environment variables:

```bash
curl -sS "https://api.redislabs.com/v1/subscriptions" \
  -H "accept: application/json" \
  -H "x-api-key: ${REDIS_CLOUD_API_KEY}" \
  -H "x-api-secret-key: ${REDIS_CLOUD_API_SECRET}"
```

## Swagger UI Smoke Test

Use Swagger UI for first-time validation:

1. Open the Redis Cloud API Swagger UI for the current API version.
2. Choose `Authorize`.
3. Enter the account key as `x-api-key`.
4. Enter the secret key as `x-api-secret-key`.
5. Run a low-risk read operation such as listing subscriptions.
6. If it fails, capture the status code, response body, operation name, and timestamp with secrets redacted.

## Essentials Endpoint Eligibility

When an endpoint fails:

1. Confirm the request is authenticated.
2. Confirm the user/key has the required account role.
3. Check whether the endpoint is available for Essentials.
4. Compare Swagger/API docs with the live response.
5. If the endpoint is Pro-only or unsupported for the account, state that clearly and suggest the Console path or plan change only after verifying current Redis Cloud behavior.

## Rate Limits And 429

Redis Cloud API rate limits can change. Do not hard-code a request-per-minute limit into production automation without verifying current API documentation or response headers.

For 429 responses:

1. Stop tight retry loops.
2. Honor retry headers when present.
3. Use exponential backoff with jitter.
4. Reduce worker count, Terraform parallelism, or scheduled-job overlap.
5. Cache repeated discovery calls such as subscriptions and databases within the job.
6. Use `redis-cloud-api-429-troubleshooting` for persistent automation throttling.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Authentication fails | Wrong, expired, revoked, or mismatched key pair | Regenerate or rotate keys and update secret storage. |
| `Access Denied` | Role, account, or endpoint eligibility issue | Verify account role, account context, and Essentials endpoint support. |
| `Endpoint Not Allowed` | Endpoint not available for the plan or API version | Check current API reference and Swagger operation status. |
| 429 Too Many Requests | Burst or concurrency exceeds current limit | Add backoff/jitter, stagger jobs, and reduce parallel requests. |
| Swagger JSON or payload errors | Example payload not adjusted for the account | Validate required fields and IDs before executing mutating operations. |
| 4xx response | Malformed request, missing header, wrong ID, or unsupported action | Compare request against current API docs and redact output before sharing. |
| 5xx response | Service-side issue or transient failure | Retry conservatively and collect request ID/timestamp for Support. |

## Escalation Packet

Collect without secrets:

- Redis Cloud account or organization name.
- Essentials subscription ID or database ID, if relevant.
- API endpoint and method.
- HTTP status code and redacted response body.
- Timestamp and request ID/correlation ID if provided.
- Whether Swagger UI and cURL both fail.
- API key owner or automation name, not the key/secret.
- Recent key rotation, role change, or plan change.

## Response Shape

When helping a user:

1. Confirm this is an Essentials subscription.
2. Verify API key setup and role.
3. Give a safe read-only smoke test.
4. Classify the failure as auth, endpoint eligibility, request shape, rate limit, or service error.
5. Route 429, credential rotation, or plan-upgrade decisions to the relevant focused skill when needed.
