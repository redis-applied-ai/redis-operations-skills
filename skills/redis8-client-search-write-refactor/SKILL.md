---
name: redis8-client-search-write-refactor
description: Use when refactoring application write paths for Redis 8 or Redis Query Engine, replacing FT.ADD, FT.SAFEADD, or FT.DEL helpers with native HSET, JSON.SET, DEL, or UNLINK in Go-Redis, Lettuce, Node-Redis, or other clients, while avoiding double-writes, schema mismatches, prefix mismatches, and index desynchronization.
---

# Redis 8 Client Search Write Refactor

Use this skill when application code still writes indexed documents through legacy Search commands. Redis 8-compatible write paths should write the underlying HASH or JSON key directly; the index updates from the index definition.

## Core Rule

Replace legacy Search document writes:

- `FT.ADD` and `FT.SAFEADD` -> `HSET` or `JSON.SET`
- `FT.DEL` -> `DEL` or `UNLINK`
- `FT.GET` and `FT.MGET` -> native HASH or JSON reads

Writes are indexed only when the key and payload match the index definition:

- correct `ON HASH` or `ON JSON`
- correct `PREFIX`
- field names or JSONPaths match the schema
- data types match expected field types

## Migration Workflow

1. Inventory every service, library wrapper, job, script, and test helper that calls `FT.ADD`, `FT.SAFEADD`, or `FT.DEL`.
2. Identify the index data model: HASH or JSON.
3. Replace write helpers with native client calls.
4. Ensure only one write path is active during rollout.
5. Validate index schema and key prefix alignment.
6. Confirm writes appear in search results.
7. Remove legacy Search write wrappers after all services are upgraded.

## Client Patterns

Go-Redis:

```go
client.HSet(ctx, "user:1", map[string]interface{}{"name": "Alice", "age": 30})
client.Del(ctx, "user:1")
```

Lettuce:

```java
redis.hset("user:1", Map.of("name", "Alice", "age", "30"));
redis.del("user:1");
```

Node-Redis:

```javascript
await client.hSet("user:1", { name: "Alice", age: "30" });
await client.del("user:1");
```

Use `JSON.SET` instead of `HSET` when the index is defined on JSON documents.

## Rollout Risks

- Double writes: old and new services both write the same logical document.
- Mixed Redis versions: services route writes to databases with different Search behavior.
- Legacy deleters: old consumers keep issuing `FT.DEL`.
- Missing index updates: keys do not match `PREFIX`, HASH fields do not match schema fields, or JSON paths do not match index paths.
- Stale abstractions: internal repository or DAO helpers still call legacy Search commands.

## Validation

Use:

```text
FT.INFO <index>
FT.SEARCH <index> "@field:{value}" LIMIT 0 10
```

Also validate:

- written key exists with native read command
- key prefix matches the index
- fields or JSONPaths match schema
- delete path removes the key and the document disappears from search

## Response Pattern

Answer with:

1. The legacy command being replaced.
2. The native write or delete command for the user's data model.
3. The index definition checks needed for automatic indexing.
4. Rollout guardrails for mixed services and double writes.
5. A validation query.
