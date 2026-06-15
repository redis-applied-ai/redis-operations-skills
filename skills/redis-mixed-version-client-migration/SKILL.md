---
name: redis-mixed-version-client-migration
description: "Guide client-side migration for mixed Redis 7.x and Redis 8.x environments. Use when rolling upgrades or phased migrations involve different database versions, Search/JSON behavior changes, RQE parsing errors, `FT.ADD` or `FT.DEL` removal, RESP2 versus RESP3 issues, ACL category changes, per-database feature flags, or microservices connecting to multiple Redis versions."
---

# Redis Mixed Version Client Migration

Use this skill when applications must run against both Redis 7.x and Redis 8.x databases during a migration or rolling upgrade.

## Core Principle

Mixed-version environments need explicit per-database capability configuration. Do not rely on one global Redis client, one query builder, or runtime version detection through `INFO SERVER` when proxies or managed services can hide details.

## Preflight Checklist

1. Inventory every service and Redis database it connects to.
2. Record Redis database versions and enabled capabilities.
3. Upgrade Redis clients to currently supported versions before upgrading databases.
4. Add per-database feature flags such as:
   - `requires_dialect_2`
   - `search_parser=strict|legacy`
   - `supports_legacy_search_commands`
   - `protocol=resp2|resp3`
   - `json_behavior=module|builtin`
5. Audit ACLs and validate with `ACL DRYRUN`.
6. Test with a real mixed-version staging topology before production.

## Client Configuration Rules

| Area | Guidance |
| --- | --- |
| Connection ownership | Use separate client instances/configuration per database version or capability profile. |
| Query building | Drive syntax from feature flags, not ad hoc version detection. |
| RESP | Pin RESP2 unless the client and application are fully validated for RESP3 and push messages. |
| Pooling | Recycle pools at each upgrade step so stale connections do not carry old assumptions. |
| Retries | Use realistic timeouts and exponential backoff to avoid upgrade-time reconnect storms. |
| Routing | Avoid sticky service-mesh behavior that pins clients to nodes in a way that breaks rolling upgrades. |

## Search And Query Changes

When targeting Redis 8.x Search and Query behavior:

- Add `DIALECT 2` to `FT.SEARCH` queries.
- Test `FT.AGGREGATE` dialect behavior against older module builds before applying globally.
- Remove deprecated options such as `FILTER`, `GEOFILTER`, and `NOSTOPWORDS`.
- Replace removed commands:
  - `FT.ADD` -> write the document with `HSET` or `JSON.SET`.
  - `FT.DEL` -> delete the document key with `DEL` or `UNLINK` as appropriate.
- Expect stricter parsing and update query construction rather than retrying the same syntax.

## JSON And ACL Changes

- Redis 8.x may expose JSON as a built-in capability rather than as separately selected module behavior.
- Error shapes and command availability can differ from older module-based deployments.
- Review ACL roles after upgrading because broader categories such as read/write can cover additional command groups.
- Prefer clear ACL categories for Search and JSON access when supported by the target environment.

## Rollout Order

1. Upgrade application clients and wrappers.
2. Add feature flags and per-database client configuration.
3. Refactor deprecated Search/JSON commands.
4. Validate ACLs with `ACL DRYRUN`.
5. Test against both old and new database versions.
6. Upgrade databases or nodes according to the platform runbook.
7. Recycle connection pools and restart long-lived services.
8. Remove legacy code paths only after all relevant databases are on the new version and validation has passed.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `ERR syntax error` on Search query | Deprecated syntax or stricter Redis 8 parser | Remove deprecated options and add the intended dialect. |
| Empty Search results | Legacy dialect or parser mismatch | Compare `FT.EXPLAINCLI` and pin dialect. |
| `FT.ADD` or `FT.DEL` missing | Removed command path | Use `HSET`/`JSON.SET` for writes and `DEL`/`UNLINK` for deletion. |
| `NOPERM` | ACL categories changed or role lacks Search/JSON | Update ACLs and validate with `ACL DRYRUN`. |
| RESP3 client errors | Push messages or wrapper incompatibility | Pin RESP2 until RESP3 handling is validated. |
| Failures only in some microservices | Shared global client or stale pool | Use per-DB clients and recycle pools. |
| Latency spikes during upgrade | Reconnect storm or no maintenance handoff | Enable platform maintenance notifications where available and stagger reconnects. |

## Evidence To Collect

- Redis database versions and capability profiles.
- Client library names and versions.
- Protocol mode for each service.
- Feature flag values.
- Failing command/query with secrets removed.
- ACL role and `ACL DRYRUN` result.
- Rollout step where the failure appeared.
