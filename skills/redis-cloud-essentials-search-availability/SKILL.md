---
name: redis-cloud-essentials-search-availability
description: Use when Redis Search, FT.CREATE, FT.SEARCH, FT.INFO, FT._LIST, or Search advanced capabilities appear unavailable on a Redis Cloud Essentials database, especially with Redis 8 creation flows, Flex databases, OSS Cluster API, RAM-only replacement databases, module validation, or missing capability selectors.
---

# Redis Cloud Essentials Search Availability

Use this skill to determine whether Redis Search is available on a Redis Cloud Essentials database and to choose the right remediation path when `FT.*` commands are unavailable. Verify current Redis Cloud feature compatibility before making plan- or version-specific claims.

## Evidence To Gather

Collect:

- subscription and database name
- Redis version
- database type: RAM-only or Flex
- advanced capabilities shown in the database details page
- whether OSS Cluster API is enabled
- exact `FT.*` command and error
- whether this is a new database, an existing database, or a migration target

## Validation Commands

Run from a successful client connection:

```text
MODULE LIST
FT._LIST
```

Interpretation:

- Search available: Search-related module is listed, `FT._LIST` succeeds, and Search commands are recognized.
- Search unavailable: no Search-related module is listed, `FT._LIST` or `FT.CREATE` fails, or Redis returns an unknown command error.

## Diagnostic Flow

1. Check Redis version and current database capabilities in the Redis Cloud Console.
2. Do not rely on the presence or absence of a module selector during creation flows; validate from the provisioned database.
3. Check database type:
   - If it is Flex and Search is unsupported for that configuration, use a RAM-only database for Search workloads.
4. Check OSS Cluster API:
   - If enabled and Search commands fail in that access mode, use a supported routing mode for Search or create a compatible database.
5. Validate with `MODULE LIST` and `FT._LIST`.
6. If the database should support Search but does not, reproduce on a new test database in the same account and region before escalating.

## Remediation Paths

- Flex database requires Search: create a RAM-only replacement database, recreate indexes, and migrate or repopulate data.
- OSS Cluster API conflicts with Search: disable OSS Cluster API if supported and acceptable, or use the default routing model.
- Existing database lacks required advanced capability: create a new compatible database; do not assume capabilities can be added in place.
- Disposable dataset: reprovision and rebuild indexes from source data.
- Production dataset: plan migration, endpoint update, index recreation, data validation, and cutover.

## Escalation Package

For Redis Support, collect:

- database details screenshot or exported details showing version, type, and capabilities
- `MODULE LIST` output
- `FT._LIST` output
- exact `FT.*` error
- confirmation of Flex status
- confirmation of OSS Cluster API setting
- account, subscription, and database IDs if available

## Response Pattern

Answer with:

1. The likely compatibility blocker.
2. The command evidence needed to confirm it.
3. The remediation path: change access mode, create RAM-only replacement, or recreate a compatible database.
4. Migration and endpoint-update implications if replacement is required.
