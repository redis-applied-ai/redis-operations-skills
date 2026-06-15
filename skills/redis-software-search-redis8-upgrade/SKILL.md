---
name: redis-software-search-redis8-upgrade
description: Use when preparing Redis Software databases for Redis 8 Search or Redis Query Engine upgrades, or when application queries fail after upgrade with `ERR syntax error`, `ERR unknown command`, `ERR invalid argument`, `NOPERM`, empty Search results, ranking changes, deprecated FT.ADD, FT.DEL, FT.GET, FT.CONFIG, FILTER, GEOFILTER, NOSTOPWORDS, old DIALECT values, strict Redis Query Engine parsing, BM25 ranking changes, RQE ACL categories, RESP3 client defaults, backups, maintenance windows, and post-upgrade validation.
---

# Redis Software Search Redis 8 Upgrade

Use this skill for Redis Software operators upgrading databases that use Search or Query features to Redis 8 or later. Treat this as both an application compatibility migration and a cluster operations change.

## First Response For Broken Applications

When the user reports application query failures after a Redis 8 upgrade:

1. Confirm whether the database itself is upgraded to a Redis 8.x feature set. Databases left on 7.4, 7.2, or 6.2 can keep legacy Search behavior.
2. Capture the exact error and query:
   - `ERR syntax error`
   - `ERR unknown command`
   - `ERR invalid argument`
   - `NOPERM`
   - empty results
   - ranking/order changes
3. Classify the failure as deprecated command, removed query option, dialect mismatch, stricter parser, ACL category change, scoring change, or client protocol issue.
4. Test the replacement query in staging or a controlled connection before changing production code.

## Pre-Upgrade Checklist

Before upgrade:

- create or verify a full database backup or snapshot
- schedule a maintenance window for validation
- inventory application code, scripts, Lua, functions, jobs, dashboards, and automation for deprecated `FT.*` patterns
- inventory Search/JSON client libraries and their RESP2/RESP3 defaults
- review ACL roles for Search, JSON, time series, read, and write coverage
- verify monitoring includes query errors, latency, throughput, worker utilization, and command failures
- prepare rollback or restore expectations according to the actual upgrade path

## Deprecated Patterns To Replace

Replace:

| Deprecated pattern | Replacement |
| --- | --- |
| `FT.ADD`, `FT.SAFEADD` | `HSET` or `JSON.SET` |
| `FT.DEL` | `DEL` or `UNLINK` |
| `FT.GET`, `FT.MGET` | `HGETALL`, `HGET`, or `JSON.GET` |
| `FT.CONFIG` automation | supported `CONFIG` operations for allowed parameters |
| `FILTER` / `GEOFILTER` options | query-string predicates such as `@price:[10 20]` |
| query-time `NOSTOPWORDS` | index-time stopword configuration |
| vector options such as `INITIAL_CAP` or `BLOCK_SIZE` | remove or use currently supported vector-index options |
| removed RQE config parameters | remove unsupported tuning scripts and verify current configuration APIs |
| explicit old dialects | a supported dialect for the query, commonly `DIALECT 2` |

## Parsing Changes

Redis 8 Query Engine behavior is stricter. Check for:

- invalid `LIMIT` combinations
- malformed `FT.CURSOR READ`
- malformed `FT.ALIASADD`
- aggregate `APPLY` expressions that need explicit parentheses
- application code that expects invalid queries to return empty results
- ranking assumptions affected by scoring changes

Make the dialect explicit in application code. If older code pins unsupported dialect values or omits dialect in a way that changes interpretation, standardize on the supported dialect for the target database, commonly `DIALECT 2`.

## ACL And Client Protocol Checks

Redis 8 expands or changes command category behavior for Search, JSON, Time Series, and probabilistic commands. Audit app users with `ACL DRYRUN` where available.

Examples of intent-driven ACL coverage:

```text
+@read +@write +@search +@json
```

For least privilege, prefer explicit categories and command allow/deny rules over assuming Redis 7 and Redis 8 category behavior is identical.

Some client libraries default to RESP3 in newer major versions. If Search/JSON commands fail only through the application but work through `redis-cli`, check the client protocol setting and test RESP2. For broader client migration planning, use `redis-mixed-version-client-migration` or `redis-software-resp-compatibility`.

## Validation Commands

Adapt to the user's index:

```text
FT.SEARCH idx "@price:[10 20]" LIMIT 0 10
FT.SEARCH idx "@loc:[-73.98 40.75 5 km]"
FT.SEARCH idx "*" LIMIT 0 5
```

Also run one intentionally old syntax test in staging to confirm the application handles the resulting error cleanly:

```text
FT.SEARCH idx * FILTER price 10 20
```

## Software Operations Checks

After upgrade:

- check database health in Admin UI or `rladmin`
- verify Search indexes exist and accept queries
- inspect logs for invalid argument, unknown command, ACL, and timeout errors
- compare query latency and ranking against pre-upgrade baselines
- confirm dashboards and alerts are receiving Redis Query Engine metrics
- validate restricted users can read and cannot write when that is the intended policy
- for Active-Active databases, avoid Search/JSON command assumptions while some participants remain pre-8.x; validate after every participating cluster reaches the planned version

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| `ERR syntax error` | Deprecated `FILTER`, `GEOFILTER`, malformed query, or stricter parser | Rewrite as supported query-string syntax and verify dialect. |
| Empty results after upgrade | Dialect, field name, schema, or parser behavior changed | Add supported dialect, inspect `FT.EXPLAINCLI`, and validate index schema. |
| `ERR unknown command` for `FT.ADD`, `FT.GET`, or `FT.CONFIG` | Deprecated command path removed | Replace with direct key writes/reads or supported config access. |
| `NOPERM` | App user lacks Search/JSON/RQE command category coverage | Audit ACL with `ACL DRYRUN` and add intended categories or commands. |
| Ranking differs | BM25 or scoring behavior changed | Recheck relevance thresholds and sort assumptions. |
| Works in CLI, fails in app | Client protocol, command builder, or library compatibility issue | Pin/test RESP2, upgrade client, and inspect generated command. |
| Active-Active inconsistent behavior | Participants are on mixed Redis feature sets | Finish planned participant upgrades before relying on Search/JSON behavior. |

## Response Pattern

Answer with:

1. The deprecated or changed behavior involved.
2. The replacement command or query syntax.
3. The pre-upgrade or post-upgrade validation step.
4. Whether ACL or client protocol settings must also change.
5. Any operational guardrail: backup, maintenance window, ACL, monitoring, or restore plan.
