---
name: redis-cloud-rbac-acl
description: "Design, configure, audit, and troubleshoot Redis Cloud RBAC and ACLs. Use when the user mentions Data Access Control, Redis ACLs, roles, users, service accounts, `NOPERM`, `ACL DRYRUN`, key patterns, Pub/Sub channel restrictions, default user disablement, Redis 8 ACL category expansion, or Search/JSON/TimeSeries permissions in Redis Cloud."
---

# Redis Cloud RBAC ACL

Use this skill for Redis Cloud database access control. Model Redis Cloud permissions as ACL definitions, roles that scope ACLs to databases, and users or service accounts assigned to roles.

## Version-Aware Rule

Always identify the database Redis version before designing or auditing ACLs. Redis 7 and Redis 8 category behavior differs, especially for Search, JSON, TimeSeries, and probabilistic commands. Verify current Redis ACL category behavior before production upgrades.

## Workflow

1. Gather context:
   - Redis Cloud database and Redis version.
   - User/service account being configured.
   - Required commands or workload behavior.
   - Key patterns and Pub/Sub channels.
   - Whether Terraform/API automation is used.
2. Design ACL:
   - Prefer categories and key patterns over broad full access.
   - Use command categories such as `+@read`, `+@write`, `+@search`, `+@json`, `+@timeseries`.
   - Restrict keys with `~pattern`, read-only `%R~pattern`, or write-only `%W~pattern`.
   - Restrict Pub/Sub with channel rules such as `&events:*` when needed.
3. Create or update Redis Cloud role:
   - Data Access Control, Redis ACLs: define allowed commands and key/channel patterns.
   - Roles: attach ACLs and database scope.
   - Users: assign roles to users or service accounts.
4. Validate with `ACL DRYRUN`.
5. Disable the default user if policy requires RBAC-only access.

## ACL Syntax Reference

| Element | Meaning |
| --- | --- |
| `+COMMAND` | Allow one command. |
| `-COMMAND` | Deny one command. |
| `+@category` | Allow command category. |
| `~pattern` | Restrict key scope. |
| `&channel` | Restrict Pub/Sub channel scope. |
| `%R~pattern` | Read-only key access. |
| `%W~pattern` | Write-only key access. |

High-risk access:

- Restrict `@dangerous`, `@admin`, `@connection`, and `@scripting`.
- Avoid `@all` and `~*` for non-admins.

## Version Patterns

Redis 7-style explicit module permissions:

```text
+@read +FT.SEARCH +JSON.GET ~data:*
```

Redis 8-style category permissions:

```text
+@read +@search +@json ~data:*
```

Example roles:

```text
readonly_analytics: +@read +@search ~index:*
json_writer: +@write +@json ~data:*
metrics_viewer: +@read +@timeseries ~metrics:*
```

## Validate Safely

Use `ACL DRYRUN` to test without executing the target command:

```redis
ACL DRYRUN analytics_user FT.SEARCH index "@field:value"
ACL DRYRUN json_writer JSON.SET data:1 . '{"k":1}'
ACL DRYRUN testuser FT.SEARCH other_index "*"
```

Remember: Redis Cloud roles do not appear as roles in `ACL LIST` or `ACL GETUSER`; inspect role assignments in the Redis Cloud Console.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `NOPERM` or access denied | Missing category, command, key pattern, channel pattern, or database scope. |
| Search/JSON/TimeSeries blocked | Check Redis version and whether module/category permissions are included. |
| Permissions changed after upgrade | Redis 8 category expansion may grant or deny differently than Redis 7 policies. |
| Cannot edit Full-Access ACL | Predefined ACLs are immutable; clone and edit a copy. |
| Multi-key command fails | Every key must match allowed patterns; consider hash tags when appropriate. |
| Pub/Sub not restricted as expected | Reset channels and explicitly allow channels when strict channel control is required. |
| Default user still works | Disable default user in database settings if RBAC-only access is required. |

## Safety Checks

- Validate in staging before production rollout.
- Do not grant `@all`, `~*`, `@dangerous`, or `@admin` unless the role is truly administrative.
- Review ACLs before Redis major-version upgrades.
- Do not paste real passwords or secrets while debugging ACLs.
