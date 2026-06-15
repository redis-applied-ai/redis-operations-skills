---
name: redis8-acl-category-migration
description: Use when auditing, migrating, or troubleshooting Redis 8 ACL category behavior across Redis Cloud, Redis Software, or Redis Open Source, especially Search, JSON, TimeSeries, Bloom, Cuckoo, TopK, CMS, T-Digest, @read, @write, @fast, @slow, @admin, @dangerous, @search, @json, @timeseries, @bloom, @cuckoo, @topk, @cms, @tdigest, ACL DRYRUN, NOPERM after upgrade, or unexpected module-command access.
---

# Redis 8 ACL Category Migration

Use this skill when Redis 8 ACL category changes may alter application or service-account permissions. The goal is to preserve intended access while making module command permissions explicit and testable.

## Safety Rules

- Inventory and export ACLs before changing production roles.
- Validate with `ACL DRYRUN` before applying new permissions.
- Do not assume Redis 7 and Redis 8 category behavior is identical.
- Avoid broad `+@all`, `+@admin`, and `+@dangerous` grants for non-admin users.
- In Redis Cloud, manage roles through Redis Cloud Data Access Control and supported APIs; do not assume direct `ACL SETUSER` changes are durable.
- In Redis Software, treat `ACL LOAD` as a change-control action because it can alter access cluster-wide.

## Core Change

Redis 8 aligns Redis Query Engine, JSON, TimeSeries, and probabilistic commands with standard Redis ACL categories and adds module-specific categories.

Standard categories such as these may now include more commands than older deployments:

- `@read`
- `@write`
- `@fast`
- `@slow`
- `@admin`
- `@dangerous`

Module-specific categories allow finer control:

- `@search`
- `@json`
- `@timeseries`
- `@bloom`
- `@cuckoo`
- `@topk`
- `@cms`
- `@tdigest`

Impact: existing roles using broad categories may gain access to module commands, while roles with broad denies may block commands that worked before.

## Who Needs Review

Review ACLs when:

- upgrading Redis 7.x databases to Redis 8
- using Search, JSON, TimeSeries, or probabilistic commands
- users have broad categories such as `+@read`, `+@write`, `+@all`, or `-@write`
- applications report `NOPERM` after upgrade
- auditors expect explicit separation between core Redis and module capabilities
- Redis Cloud roles or Redis Software ACLs were copied from older environments

## Audit Workflow

1. Identify Redis version and product: Cloud, Software, or Open Source.
2. Export or record current ACLs and role assignments.
3. List categories:

   ```text
   ACL CAT
   ```

4. Review users and rules:

   ```text
   ACL LIST
   ```

5. Test representative commands:

   ```text
   ACL DRYRUN <user> FT.SEARCH <index> "*"
   ACL DRYRUN <user> JSON.SET <key> . '{}'
   ACL DRYRUN <user> TS.ADD <key> * 1
   ```

6. Adjust roles to match intended access.
7. Retest all application service users with `ACL DRYRUN`.
8. Roll clients or jobs only after role behavior is confirmed.

## Strategy Choices

| Intent | Pattern |
| --- | --- |
| Accept Redis 8 broad category behavior | keep `+@read` or `+@write`, then validate module command access |
| Explicitly allow Search reads | add `+@search` and command/key patterns as needed |
| Explicitly allow JSON writes | add `+@json` with appropriate key patterns |
| Preserve older "no JSON/Search" intent | add targeted denies such as `-@json` or `-@search` |
| Block one risky command | deny the command directly, such as `-JSON.SET` |
| Validate without running command | use `ACL DRYRUN` |

Key patterns still matter. A user can have command permission but fail because the key pattern, channel pattern, or database role scope does not match.

## Redis Cloud Guidance

Use Redis Cloud Console or supported REST API role management.

Check:

- database Redis version
- Data Access Control roles
- users or service accounts assigned to each role
- ACL strings behind custom roles
- whether predefined roles are immutable and need to be cloned

After upgrade, test application users with `ACL DRYRUN` from the target database connection. If Cloud role export/import is used, redact secrets and verify current API behavior before relying on exact endpoint shapes.

## Redis Software Guidance

Before upgrade or role changes:

```bash
rladmin export acl
```

Then inspect and validate from a database endpoint:

```text
ACL CAT
ACL LIST
ACL DRYRUN <user> FT.SEARCH <index> "*"
```

After editing ACL files or role definitions, reload only through a controlled procedure:

```text
ACL LOAD
```

Confirm cluster-wide consistency after reload and watch for authentication or `NOPERM` errors.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| `FT.SEARCH` works unexpectedly | `@read` or role now includes Search read access | add `-@search` or explicit command denies if access should be blocked |
| `JSON.SET` denied after upgrade | deny rule or role pattern now blocks JSON writes | validate with `ACL DRYRUN`; add `+@json` or remove conflicting deny |
| service account gets `NOPERM` | missing module category, command grant, key pattern, or role scope | dry-run exact command and key |
| behavior differs by node | ACLs not loaded or synchronized consistently | use product-specific ACL reload/sync procedure |
| Cloud role looks right but command fails | database scope or key pattern mismatch | inspect role assignment and key pattern, not only command category |

## Evidence To Collect

- product and Redis version
- user or service account name, with passwords removed
- current ACL rule or role summary
- exact command and key pattern that fails or unexpectedly succeeds
- `ACL CAT` output for relevant categories
- `ACL DRYRUN` result
- recent upgrade, role import, or Data Access Control change timeline
