---
name: redis-software-index-documents
description: "Explain and troubleshoot how Redis Software indexes JSON and hash documents with Redis Search 2.x. Use when the user asks how to add documents to a Redis Software index, why `FT.ADD` is deprecated, how `HSET` or `JSON.SET` drives indexing, how prefixes work across shards, or why documents are missing from Redis Enterprise search results."
---

# Redis Software Index Documents

Use this skill when a Redis Software user needs to create a Search index, add JSON or hash documents, query the index, or troubleshoot missing documents in a Redis Enterprise cluster.

## Core Model

- Redis Software with Redis Search 2.x indexes hash and JSON keys automatically when writes match an index prefix.
- Do not use the legacy `FT.ADD` workflow for Redis Search 2.x.
- New matching documents are indexed synchronously when written.
- Preexisting matching keys may be indexed asynchronously after index creation.
- Schema changes usually require recreating the index.
- In clustered deployments, consistent prefixes and schema definitions matter across shards.

## Workflow

1. Confirm prerequisites:
   - Redis Software cluster is available.
   - Redis Search is enabled; RedisJSON is enabled if indexing JSON.
   - Module versions are Redis Search 2.x or later.
   - User has `redis-cli` access or authorized REST API access.
2. Identify data shape:
   - JSON: use `ON JSON` and JSONPath fields.
   - Hash: use `ON HASH` and hash field names.
3. Create an index with a prefix matching the target keys.
4. Add or update data using key writes such as `JSON.SET` or `HSET`.
5. Query the index and verify expected results.
6. If results are incomplete, check prefix, schema, module availability, background indexing, and shard distribution.

## Command Patterns

Create a JSON index with CLI:

```redis
FT.CREATE idx:employees ON JSON PREFIX 1 emp: SCHEMA $.name AS name TEXT $.dept AS dept TAG $.age AS age NUMERIC
```

Create the same index through the Redis Software REST command endpoint:

```bash
curl -k -u admin:<password> -X POST \
  https://<cluster>:9443/v1/redis/commands \
  -d '{"cmd":"FT.CREATE idx:employees ON JSON PREFIX 1 emp: SCHEMA $.name AS name TEXT $.dept AS dept TAG $.age AS age NUMERIC"}'
```

Write JSON documents:

```redis
JSON.SET emp:1 $ '{"name":"Alice","dept":"Engineering","age":30}'
JSON.SET emp:2 $ '{"name":"Bob","dept":"Finance","age":25}'
```

Write hash documents:

```redis
HSET hemp:1 name "Alice" dept "Engineering" age 30
HSET hemp:2 name "Bob" dept "Finance" age 25
```

Validate indexed results:

```redis
FT.SEARCH idx:employees "@dept:{Engineering}"
FT.SEARCH idx:employees "@age:[25 35]"
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Documents missing from search | Confirm key prefix and schema match the data structure. |
| Existing keys do not appear immediately | Wait for asynchronous background indexing after index creation. |
| Cross-shard inconsistency | Verify key prefixes, index distribution, and module availability across shards. |
| User is using `FT.ADD` | Explain that Redis Search 2.x indexes writes from `HSET` and `JSON.SET`. |
| Schema no longer matches data | Plan an index recreation and assess production impact before changing indexes. |

## Safety Checks

- Do not recommend index recreation until prefix, schema, document type, and module availability are checked.
- Before REST API command execution, confirm the target cluster, credentials, TLS expectations, and change window.
- For large datasets, call out that initial indexing of preexisting keys may take time and consume cluster resources.
- For application code that needs vector or hybrid search, prefer RedisVL patterns when appropriate.
