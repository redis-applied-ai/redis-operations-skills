---
name: redis-json-null-indexing
description: "Design Redis Search and Query indexes for JSON documents with null or missing fields. Use when the user asks why JSON null values are not searchable, missing fields are skipped, RediSearch or Query Engine returns no hits for nulls, needs sentinel values like `_null`, a `nulls` TAG array, FT.CREATE JSON schema changes, FT.SEARCH queries for nullable fields, reindexing after schema changes, or distinguishing null versus absent fields."
---

# Redis JSON Null Indexing

Use this skill when a user needs to search for JSON fields that are `null` or missing in Redis Search and Query.

## Core Rule

Native JSON `null` values and missing fields are not indexed as searchable field values. If an application must search for null or missing values, it must write an explicit searchable representation.

## Strategy Choice

| Requirement | Recommended pattern |
| --- | --- |
| Fixed schema and simple null checks | Store a sentinel value such as `_null`. |
| Query which fields are null or missing | Maintain a `nulls` TAG array listing field names. |
| Distinguish explicit null from missing | Store separate metadata, such as `nulls` and `missing` arrays, through application logic. |
| Existing data already contains nulls | Backfill sentinel values or metadata, then recreate/reindex. |
| Nested arrays contain nulls | Normalize or replace nulls before writing documents. |

## Sentinel Value Pattern

Write an explicit value instead of native null:

```json
{
  "exchange": "_null"
}
```

Index it:

```redis
FT.CREATE myIdx ON JSON SCHEMA $.exchange AS exchange TAG
```

Query it:

```redis
FT.SEARCH myIdx '@exchange:{_null}'
```

Use one sentinel consistently across all writers.

## Nulls TAG Array Pattern

Store metadata listing nullable fields:

```json
{
  "contractId": 21,
  "exchange": null,
  "nulls": ["exchange"]
}
```

Index the array as a tag:

```redis
FT.CREATE myIdx ON JSON SCHEMA $.nulls AS nulls TAG
```

Query documents where `exchange` is null or missing:

```redis
FT.SEARCH myIdx '@nulls:{exchange}'
```

This is usually better when many fields can be null and the user needs field-specific null queries.

## Update Rules

When documents change:

- If a nullable field receives a real value, remove it from `nulls` and remove any sentinel.
- If a real value becomes null, add the field to `nulls` or set the sentinel.
- If the schema changes, reindex or recreate the index as required.
- Keep all application writers consistent; mixed sentinels such as `_null`, `NULL`, and empty string will produce incomplete results.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Null fields not found | Native nulls are skipped; add sentinel or metadata. |
| Query returns no hits | Schema does not include the sentinel field or `nulls` TAG field. |
| Some documents missing | Writers did not update sentinel/null metadata consistently. |
| Existing data not searchable | Backfill documents and rebuild/reindex. |
| Need explicit null versus missing distinction | Application must store that distinction explicitly. |

## Escalation Packet

Collect:

- Redis product and Search/Query version.
- JSON document examples with sensitive fields redacted.
- Current `FT.CREATE` schema.
- Query being run.
- Whether fields are explicit null, missing, or mixed.
- Chosen null representation.
- Whether documents were backfilled and index recreated.
