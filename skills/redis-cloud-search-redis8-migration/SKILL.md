---
name: redis-cloud-search-redis8-migration
description: Use when migrating Redis Cloud Search workloads to Redis 8 or diagnosing Redis Query Engine errors from deprecated FT.ADD, FT.DEL, FT.GET, FT.CONFIG, FILTER, GEOFILTER, NOSTOPWORDS, older DIALECT values, stricter FT.SEARCH or FT.AGGREGATE parsing, BM25 ranking changes, or updated Search ACL behavior.
---

# Redis Cloud Search Redis 8 Migration

Use this skill to update Redis Cloud Search and Query workloads for Redis 8 compatibility. Focus on replacing deprecated command patterns, converting filters into query syntax, and validating application behavior under stricter parsing.

## Migration Checklist

1. Inventory application code, scripts, and dashboards for:
   - `FT.ADD`, `FT.SAFEADD`
   - `FT.DEL`
   - `FT.GET`, `FT.MGET`
   - `FT.CONFIG`
   - `FILTER`, `GEOFILTER`
   - `NOSTOPWORDS`
   - explicit `DIALECT 1`, `DIALECT 3`, or `DIALECT 4`
2. Replace Search document writes with native Redis writes:
   - HASH documents: `HSET`
   - JSON documents: `JSON.SET`
3. Replace Search document deletes with native key deletes:
   - use `UNLINK` for large keys or latency-sensitive deletion
   - use `DEL` for simple deletion where blocking cost is acceptable
4. Replace Search document reads with native key reads:
   - HASH: `HGET`, `HGETALL`, or related hash commands
   - JSON: `JSON.GET`
5. Convert query options into query-string syntax.
6. Set a compatible dialect explicitly in client code where needed.
7. Re-test ACLs for the Redis users that run Search, JSON, and write commands.

## Rewrite Rules

Use these replacements when reviewing old code:

| Old pattern | Preferred pattern |
| --- | --- |
| `FT.ADD idx doc ...` | `HSET key ...` or `JSON.SET key $ ...` |
| `FT.DEL idx doc` | `DEL key` or `UNLINK key` |
| `FT.GET idx doc` | `HGETALL key` or `JSON.GET key` |
| `FT.SEARCH idx * FILTER price 10 20` | `FT.SEARCH idx "@price:[10 20]"` |
| `FT.SEARCH idx * GEOFILTER loc lon lat radius unit` | `FT.SEARCH idx "@loc:[lon lat radius unit]"` |
| query-time `NOSTOPWORDS` | define stopword behavior at `FT.CREATE` time |
| old explicit dialects | use a supported dialect for the query syntax, commonly `DIALECT 2` |

## Parsing Changes To Check

Redis 8 returns explicit errors for malformed Search and Aggregate input that older workloads may have treated as empty results. Check:

- invalid `LIMIT` combinations
- malformed cursor reads
- malformed aliases
- aggregate `APPLY` expressions, especially exponent syntax
- filters passed as old options instead of query-string predicates
- code paths that assume an invalid query returns zero rows

## Validation Commands

Adapt these to the user's index and fields:

```text
FT.SEARCH idx "@price:[10 20]" LIMIT 0 10
FT.SEARCH idx "@loc:[-73.98 40.75 5 km]"
FT.SEARCH idx "*" LIMIT 0 5
```

Also test one intentionally deprecated pattern in staging to confirm the application captures command errors cleanly.

## Troubleshooting

- `Invalid argument`: look for removed options or malformed syntax.
- Empty results after upgrade: verify dialect, field names, index schema, and filter syntax.
- Ranking changes: compare result order and thresholds because scoring behavior may differ.
- ACL errors: confirm the Redis user has the categories or command grants needed for Search, JSON, HASH, and key deletion operations.
- Application crashes on `FT.*`: replace deprecated commands instead of suppressing errors.

## Response Pattern

When helping a user:

1. Identify the exact failing command and Redis Cloud database version.
2. Classify it as deprecated command, deprecated option, stricter parsing, ACL, or ranking behavior.
3. Provide the smallest safe rewrite.
4. Give one validation command and one regression test for the application path.
