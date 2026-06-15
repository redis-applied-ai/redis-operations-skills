---
name: redis-search-oss-cluster-compatibility
description: "Decide and troubleshoot FT.SEARCH compatibility when OSS Cluster API is enabled in Redis Software or Redis Cloud. Use when the user asks why `FT.SEARCH`, `FT.AGGREGATE`, Search and Query, or TimeSeries are unavailable, sees command not found or command not allowed, needs to choose proxy-based clustering versus OSS Cluster API, or sees CROSSSLOT, MOVED, or cluster-aware client issues while considering Redis Search."
---

# Redis Search OSS Cluster Compatibility

Use this skill when a Redis Software or Redis Cloud database needs both clustering and Redis Search commands such as `FT.SEARCH`.

## Compatibility Rule

`FT.SEARCH` and Redis Search are not supported when OSS Cluster API is enabled in Redis Software or Redis Cloud. If the workload needs Search and Query, keep OSS Cluster API disabled and use default proxy-based clustering.

## Decision Matrix

| Workload need | Use OSS Cluster API? | Use proxy-based clustering? |
| --- | --- | --- |
| High-throughput key-value workload with cluster-aware clients and no search | Yes | Optional |
| Search, Query, global indexing, or `FT.SEARCH` | No | Yes |
| Non-cluster-aware clients | No | Yes |
| Multi-key operations across unrelated keys | Usually no | Usually yes |

## Expected Symptoms

| Symptom | Meaning |
| --- | --- |
| `FT.SEARCH` command not found | Search is unavailable in OSS Cluster API mode. |
| `FT.SEARCH` command not allowed | Search is disabled or blocked because of database mode. |
| `CLUSTER KEYSLOT` not allowed | OSS Cluster API is disabled. |
| `MOVED` or `ASK` redirects | Client is using OSS Cluster API and must be cluster-aware. |
| `CROSSSLOT` | Multi-key operation spans hash slots. |

## Guidance Workflow

1. Confirm whether the database has OSS Cluster API enabled.
2. Confirm whether Search and Query or TimeSeries capabilities are required.
3. If `FT.SEARCH` is required, instruct the user to disable OSS Cluster API or create/migrate to a database where it is disabled.
4. If OSS Cluster API is required for throughput, confirm the application can give up Redis Search features.
5. If both appear required, propose architecture alternatives:
   - Separate database for search-enabled workloads.
   - Proxy-based clustering for search.
   - Application redesign to avoid Search on the OSS Cluster API database.

## Redis Software Commands

Inspect and change OSS Cluster API state:

```bash
rladmin tune db <db-name-or-id> oss_cluster enabled
rladmin tune db <db-name-or-id> oss_cluster disabled
```

Existing clients should reconnect after the setting changes.

## Redis Cloud Guidance

- Check database clustering settings in the Redis Cloud Console.
- If OSS Cluster API cannot be changed on the existing database, create a compatible database and migrate.
- Confirm Pro plan requirements for clustering and OSS Cluster API.

## Troubleshooting Position

Do not try to debug `FT.SEARCH` inside OSS Cluster API mode as if it should work. The remediation is to use a supported database mode for Search and Query.

## Escalation Packet

Collect:

- Product: Redis Software or Redis Cloud.
- Database ID/name and whether OSS Cluster API is enabled.
- Whether Search and Query, TimeSeries, or JSON indexing is required.
- Exact command and error.
- Client library and whether it is cluster-aware.
- Current clustering and proxy mode.
- Migration constraints if the setting cannot be changed in place.
