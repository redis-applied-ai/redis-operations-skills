---
name: redis-cloud-index-documents
description: "Explain and troubleshoot how Redis Cloud Search and Query indexes JSON and hash documents. Use when the user asks how to add documents to an index, why `FT.ADD` is not used, why documents are missing from search results, how prefixes and schemas affect indexing, or how to validate Redis Cloud RediSearch results."
---

# Redis Cloud Index Documents

Use this skill when a Redis Cloud user needs to create a Search and Query index, add JSON or hash documents, or troubleshoot why documents are not appearing in query results.

## Core Model

- Redis Cloud indexes JSON and hash documents by tracking keyspace writes for databases with Search and Query enabled.
- `FT.ADD` is a legacy RediSearch 1.x workflow and should not be used for Redis Search 2.x.
- New or changed documents are indexed when keys are written with commands such as `JSON.SET` or `HSET`.
- Existing matching data may be indexed asynchronously after creating a new index.
- Only keys matching the index `PREFIX` and fields matching the schema are eligible.

## Workflow

1. Confirm prerequisites:
   - Redis Cloud subscription is active.
   - Search and Query is enabled on the database.
   - The client or CLI supports Search and JSON commands when JSON documents are involved.
2. Identify document type:
   - JSON documents need `ON JSON` and JSONPath schema fields.
   - Hash documents need `ON HASH` and direct hash-field schema fields.
3. Create the index with a prefix that matches the keys that will be written.
4. Add or update documents by writing keys, not by calling `FT.ADD`.
5. Query the index and verify results.
6. If documents are missing, inspect prefix, schema, JSONPath, field types, and asynchronous indexing delay.

## Command Patterns

Create a JSON index:

```redis
FT.CREATE idx:users ON JSON PREFIX 1 user: SCHEMA $.name AS name TEXT $.city AS city TAG $.age AS age NUMERIC
```

Create a hash index:

```redis
FT.CREATE hash-idx:users ON HASH PREFIX 1 huser: SCHEMA name TEXT city TAG age NUMERIC
```

Write JSON documents:

```redis
JSON.SET user:1 $ '{"name":"Alice","city":"London","age":30}'
JSON.SET user:2 $ '{"name":"Bob","city":"Paris","age":25}'
```

Write hash documents:

```redis
HSET huser:1 name "Alice" city "London" age 30
HSET huser:2 name "Bob" city "Paris" age 25
```

Validate indexed results:

```redis
FT.SEARCH idx:users "@city:{London}"
FT.SEARCH idx:users "@age:[25 35]"
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Documents do not appear | Confirm Search and Query is enabled and key prefixes match the index schema. |
| Index does not update immediately | Wait briefly for asynchronous indexing of existing data, then retry. |
| JSON fields are missing | Confirm JSONPath expressions match the actual document structure. |
| Hash fields are missing | Confirm hash field names and field types match the schema. |
| User is trying `FT.ADD` | Explain that writes such as `JSON.SET` and `HSET` update Redis Search 2.x indexes. |

## Safety Checks

- Do not suggest dropping and recreating indexes as a first response. First verify prefixes, schema, and indexed key type.
- Before advising production index changes, ask about query traffic, index size, and acceptable rebuild impact.
- For vector search or AI application design, prefer RedisVL patterns when the user is building application code rather than only validating Redis CLI behavior.
