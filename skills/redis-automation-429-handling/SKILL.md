---
name: redis-automation-429-handling
description: "Prevent and troubleshoot HTTP 429 rate-limit errors in Redis-related automation, CI/CD pipelines, Terraform workflows, Redis Cloud API scripts, and scripted Redis Insight/client activity. Use when the user mentions 429 responses, Retry-After, bursty pipelines, polling loops, Terraform parallelism, CI job concurrency, API throttling, or retries that make rate limits worse."
---

# Redis Automation 429 Handling

Use this skill to harden automated Redis workflows against HTTP 429 rate limits by reducing bursts, adding backoff, and controlling parallelism.

## Triage Workflow

1. Identify the caller:
   - CI/CD system, Terraform, Redis Cloud API script, Redis Insight automation, client library, or vendor tool.
2. Capture evidence:
   - Endpoint or operation being called.
   - 429 timestamps.
   - Request IDs or correlation IDs.
   - Job count, concurrency, schedule, and retry behavior.
   - Whether `Retry-After` is present.
3. Determine the failure pattern:
   - Bursty parallel jobs.
   - Tight status polling.
   - Repeated discovery/list calls.
   - Immediate retries without backoff.
   - Organization-wide synchronized schedules.
4. Apply the least invasive control first:
   - Honor `Retry-After`.
   - Add exponential backoff with jitter.
   - Increase polling intervals.
   - Cache discovery data inside the job.
   - Batch operations.
   - Limit concurrency and stagger schedules.
5. Re-run with logging enabled and compare 429 rate, total duration, and successful completion.

## Fix Patterns

| Problem | Likely cause | Fix |
| --- | --- | --- |
| Intermittent CI failures with 429 | Too many parallel jobs | Limit job concurrency, stagger schedules, and avoid shared bursts. |
| Polling status endpoints trips limits | Poll interval too short | Increase intervals and use cached state when possible. |
| Retries worsen failures | No backoff or jitter | Use exponential backoff with jitter and respect `Retry-After`. |
| Terraform apply hits API limits | Provider calls in parallel | Reduce `-parallelism`, upgrade provider, or split modules. |
| Discovery calls dominate traffic | Repeated list/get loops | Cache discovery results per job and batch operations. |
| Vendor tool cannot throttle | Fixed behavior | Add throttling at a job queue, wrapper, or reverse proxy layer. |

## Backoff Guidance

- On first 429, wait at least 30 seconds unless `Retry-After` specifies a different wait.
- Double the wait after each repeated 429, with jitter to avoid synchronized retries.
- Cap retry count and fail with actionable diagnostics rather than retrying forever.
- Log the final backoff schedule and any `Retry-After` values for support analysis.

## Redis-Specific Notes

- Terraform: lower `-parallelism`, avoid unnecessary module fan-out, and check whether a provider upgrade improves retry behavior.
- Redis Cloud API scripts: cache subscription/database discovery results during the job; avoid per-resource polling loops.
- Redis Insight or client automation: avoid scripted login storms; prefer long-lived sessions, stable connection pools, and scheduled spacing.

## Escalation Packet

When escalation is needed, include:

- Automation system and job name.
- API endpoint or operation pattern.
- 429 count and timestamps.
- Request IDs or correlation IDs.
- Current concurrency and schedule.
- Retry/backoff behavior, including whether `Retry-After` is honored.
- Recent changes to job count, Terraform modules, provider versions, or client scripts.
