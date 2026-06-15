---
name: redis-software-slowlog-scan-safe-diagnostics
description: "Use Redis Enterprise Software Slow Log and `SCAN` safely for production diagnostics, including replacing `KEYS`, tuning `slowlog-log-slower-than` and `slowlog-max-len`, exporting slow log history before rotation, interpreting expensive commands, running pattern scans with `MATCH` and `COUNT`, batching follow-up reads, limiting scan concurrency, monitoring latency/CPU during scans, and explaining why slow commands do not automatically trigger failover."
---

# Redis Software Slow Log And SCAN Diagnostics

Use this skill when investigating expensive commands or safely iterating large keyspaces in Redis Software. Slow Log is a bounded recent-event tool; `SCAN` is safer than `KEYS`, but full traversal still creates load and needs pacing.

## Safety Rules

- Do not use `KEYS` on production-sized databases for discovery. It performs a blocking full keyspace scan.
- Treat `CONFIG SET` changes as operational changes; confirm permissions, intended values, and rollback expectations.
- Start large scans during a low-traffic window and monitor latency, CPU, shard responsiveness, and errors.
- Begin with one scan worker per database and small batches; increase only after metrics remain healthy.
- Stop when the operational objective is met. Do not traverse the whole keyspace unnecessarily.
- Active-Active CRDB environments can behave differently for large iteration and follow-up operations; use CRDB-specific deletion or sync skills when applicable.

## Slow Log Expectations

Slow Log records commands whose execution time exceeds the configured threshold. It is cyclic and entry-count based.

It is useful for:

- recent expensive commands
- recurring application anti-patterns
- proof that a command crossed the configured threshold

It is not a replacement for:

- long-term historical telemetry
- audit logging
- full workload replay

Default-style baselines are commonly around `slowlog-log-slower-than` of `10000` microseconds and `slowlog-max-len` of `128`, but always check the active database configuration.

## View Slow Log

Cluster Manager:

- Open the database.
- Use the `Slowlog` tab.

CLI:

```bash
redis-cli -h <endpoint> -p <port> SLOWLOG GET <count>
```

Check configuration:

```bash
redis-cli -h <endpoint> -p <port> CONFIG GET slowlog-log-slower-than
redis-cli -h <endpoint> -p <port> CONFIG GET slowlog-max-len
```

## Tune Slow Log For Future Collection

Increase retained entries or adjust threshold only when needed:

```bash
redis-cli -h <endpoint> -p <port> CONFIG SET slowlog-log-slower-than <microseconds>
redis-cli -h <endpoint> -p <port> CONFIG SET slowlog-max-len <entries>
```

Guidance:

- Increasing `slowlog-max-len` helps future retention only; it does not recover entries already rotated out.
- Lower thresholds capture more commands and more noise.
- Higher thresholds reduce noise but can miss moderately expensive operations.
- For long-term history, poll/export Slow Log before entries rotate out and store it in the logging or monitoring platform.

## Interpret Slow Log

Focus on recurring patterns, not one isolated entry.

Common expensive patterns:

- `KEYS`
- `HGETALL` on large hashes
- `SMEMBERS` on large sets
- broad range queries
- `EVAL` or `EVALSHA` over large datasets
- large `PUBLISH` payloads
- wildcard-heavy Search and Query Engine operations

A Slow Log entry does not automatically mean Redis Software is faulty. It means the command exceeded the configured threshold. Correlate with latency, CPU, memory, network, client timeouts, and application deploys.

## Replace KEYS With SCAN

Basic pattern:

```bash
redis-cli -h <endpoint> -p <port> SCAN 0 MATCH '<pattern>' COUNT 1000
```

CLI helper:

```bash
redis-cli -h <endpoint> -p <port> --scan --pattern '<pattern>'
```

Important `SCAN` expectations:

- `COUNT` is a hint, not a guarantee.
- Continue until the cursor returns to `0` for a full traversal.
- Results are not a point-in-time snapshot.
- Duplicates are possible; de-duplicate if exact processing matters.
- Match patterns should be as narrow as practical.

## Safe Large-Scale SCAN Workflow

For retrieving about 10k matching records:

1. Run `SCAN <cursor> MATCH <pattern> COUNT 1000`.
2. Collect returned keys.
3. Batch follow-up reads with pipelining.
4. Use follow-up read batches of roughly 500 to 1000 keys, then adjust based on latency.
5. Add short pauses between batches when latency or CPU rises.
6. Stop after the objective is met, or continue until cursor `0` if full traversal is required.

Start conservative:

- one scan worker per database
- `COUNT` around 500 to 1000
- bounded follow-up reads
- no expensive per-key operations against very large values unless sampled first

## Redis Insight Use

Use Redis Insight for:

- Slow Log inspection
- profiler and command timeline analysis
- hot key and big key identification
- interactive workload investigation

Redis Insight does not extend Redis Slow Log retention. Export externally if history matters.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Slow Log is empty | Threshold too high, event rotated out, or event was not slow enough | Check config, increase future retention, and export externally if needed. |
| Expected command missing | Slow Log retention window was missed | Poll more frequently or raise max length for future evidence. |
| `KEYS` appears in Slow Log | Blocking full keyspace scan | Replace with `SCAN` and bounded follow-up reads. |
| `SCAN` causes load | Count too high, too many workers, or expensive follow-up reads | Lower `COUNT`, reduce concurrency, use smaller pipelines, add pauses. |
| `SCAN` misses expected keys | Pattern too restrictive, cursor loop stopped early, topology/client issue | Validate pattern, continue to cursor `0`, confirm client path for deployment topology. |
| Duplicate processing | Expected `SCAN` behavior | De-duplicate keys in the client workflow. |
| Slow command did not cause failover | Shard stayed responsive to health checks | Explain that failover depends on unresponsiveness/crash, not simply a long command. |

## Response Shape

When helping a user:

1. Identify whether they need recent slow-command evidence, long-term history, or keyspace iteration.
2. Give read-only checks first: `SLOWLOG GET`, config reads, and sampled `SCAN`.
3. Warn explicitly against `KEYS` on production-sized data.
4. Propose conservative `SCAN` settings and monitoring.
5. If tuning Slow Log, explain that changes only affect future entries.
6. If the issue involves large deletes, CRDB coordination, or Search query latency, route to the more specific deletion, CRDB, or `FT.PROFILE` skill.
