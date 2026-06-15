---
name: redis-cloud-api-429-troubleshooting
description: Use when Redis Cloud REST API calls return HTTP 429 Too Many Requests, including Terraform provider applies, CI/CD jobs, scripts, polling loops, shared Redis Cloud API keys, `x-rate-limit-retry-after-seconds`, request quota errors, throttling, exponential backoff with jitter, Terraform `-parallelism`, provider upgrades, split plans, or bulk migration windows needing Redis Support review.
---

# Redis Cloud API 429 Troubleshooting

Use this skill for non-interactive Redis Cloud API rate-limit errors. For browser login throttling, use `redis-login-429-triage`.

## First Classification

Confirm the 429 comes from Redis Cloud API automation:

- Terraform plan/apply
- CI/CD pipeline
- custom script or SDK
- repeated polling of Redis Cloud resources
- automation sharing one API key across jobs

If the 429 occurs during user login, Captcha, SSO, or Redis Insight sign-in, switch to the login 429 workflow.

## Evidence To Collect

- API key or service identity name, not the secret value
- endpoint or Terraform resource/data source involved
- 429 timestamps and request IDs/correlation IDs if available
- request count per minute or job-level call count
- concurrency: job count, Terraform parallelism, worker count
- retry behavior and whether retry delays are honored
- Terraform provider version and `.terraform.lock.hcl` provider entry
- whether multiple pipelines share the same API key

## Immediate Mitigation

1. Stop tight retry loops.
2. Honor the Redis Cloud response delay header when present:

   ```text
   x-rate-limit-retry-after-seconds
   ```

3. If no delay header is available, use exponential backoff with jitter and a conservative fallback wait.
4. Reduce concurrency:

   ```bash
   terraform apply -parallelism=2
   ```

   Use `1` for particularly noisy or urgent recovery runs.

5. Stagger pipeline schedules and avoid synchronized starts.
6. Cache subscription, database, and account discovery results within a job.
7. Batch operations and remove unnecessary polling/data-source loops.

## Terraform-Specific Checks

| Symptom | Check | Action |
| --- | --- | --- |
| Apply fails with 429 | Provider parallel calls or repeated data sources | Lower `-parallelism`, split modules, cache data lookups. |
| CI fails but local run works | CI has more parallel jobs or stale provider cache | Limit job concurrency and upgrade/reinitialize provider in CI. |
| Same resources are read repeatedly | Duplicated data sources or module fan-out | Consolidate data sources and pass outputs between modules. |
| Provider is old | Retry or polling behavior may be less efficient | Upgrade the Redis Cloud Terraform provider after verifying current registry version. |

## API Key Strategy

- Use separate API keys for independent high-throughput pipelines where policy allows.
- Do not share one key across unrelated scheduled jobs that start at the same time.
- Rotate keys through normal secret-management channels; never paste API secrets in chat or tickets.
- Keep key permissions scoped to the automation task.

## Escalation Criteria

Escalate only after reducing request volume, honoring retry delay, and controlling concurrency, unless a time-sensitive migration or customer event requires advance coordination.

Provide:

- account/subscription context
- API endpoints or Terraform resources involved
- 429 timestamps and request IDs
- current concurrency and schedule
- retry/backoff behavior
- provider/tool versions
- changes already made to reduce calls
- reason for any requested temporary throughput accommodation
