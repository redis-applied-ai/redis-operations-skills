---
name: redis-crdb-multikey-command-guardrails
description: "Detect, prevent, and remediate unsupported multi-key command usage in Redis Software Active-Active CRDB. Use when the user sees command not supported in Active-Active errors, CRDB syncer or replication errors, workload instability after deployment, SINTERSTORE, ZUNIONSTORE, BITOP, MSETNX, SORT STORE, Lua scripts with multiple KEYS, MONITOR or SLOWLOG command capture, or CRDB command allowlist/ACL guardrails."
---

# Redis CRDB Multikey Command Guardrails

Use this skill when Active-Active CRDB workloads fail because an application issued commands that cannot be safely replicated across regions.

## Safety Rules

- Prefer application logs first; use `MONITOR` only in staging or a tightly controlled reproduction because it is high-volume and invasive.
- Use low-threshold `SLOWLOG` in staging or controlled windows, then restore settings.
- Stop or roll back the offending workload before deeper investigation if replication instability is active.
- Verify the supported command matrix for the Redis Software version and CRDB configuration before declaring a command unsupported.

## Error Signals

Look for:

- `ERR command is not supported in Active-Active/CRDB`
- Syncer failures.
- Replication errors after a deployment.
- Unexpected database instability tied to a new feature, script, job, or library update.
- Application logs showing failed Redis commands with multiple keys.

## Detection Workflow

1. Collect timestamps and client error messages.
2. Review application logs for the exact Redis command and service/client issuing it.
3. Review Redis Software cluster and database logs for syncer or replication errors.
4. If the command is not visible, reproduce traffic in staging.
5. In staging, capture commands with `MONITOR` or use `SLOWLOG` with a temporary low threshold:

   ```bash
   CONFIG SET slowlog-log-slower-than 0
   SLOWLOG GET
   ```

6. Restore the original slowlog threshold after capture.
7. Compare captured commands against the CRDB supported command matrix for the running version.

## Patterns to Audit

Common risky patterns include:

- `SINTERSTORE`, `SUNIONSTORE`, `SDIFFSTORE`
- `ZINTERSTORE`, `ZUNIONSTORE`
- `BITOP`
- `MSETNX`
- `SORT ... STORE`
- Lua scripts using multiple `KEYS`
- Cross-key atomic operations
- Rename or move flows that affect multiple keys

Not every multi-key command is necessarily blocked in every version; validate before remediation.

## Remediation Patterns

| Unsupported pattern | Safer approach |
| --- | --- |
| Store result of set/sorted-set intersection or union | Fetch inputs and compute in the application, then write one output key. |
| Cross-key atomic update | Redesign data model around single-key ownership or idempotent operations. |
| Multi-key Lua script | Restrict script to one key or move orchestration into application logic. |
| Batch writes requiring speed | Use pipelined single-key commands instead of atomic multi-key commands. |
| Feature introduced unsupported command | Disable feature flag or roll back deployment, then refactor. |

## Prevention

- Maintain a CRDB-approved command allowlist in application/platform guidance.
- Add integration tests that run against a CRDB-like environment before production rollout.
- Use ACLs to deny known unsupported commands where the platform supports it.
- Alert on CRDB unsupported-command errors and syncer failure patterns.
- Include command compatibility review in code review for features touching Redis.

## Escalation Packet

Collect:

- Redis Software version and CRDB topology.
- Exact error message and timestamps.
- Offending command, keys shape, and issuing service or client.
- Recent deployments, feature flags, scripts, or jobs.
- Application logs and Redis database/cluster logs with secrets redacted.
- Whether issue reproduced in staging.
- Mitigation already applied: rollback, traffic stop, ACL block, or code change.
