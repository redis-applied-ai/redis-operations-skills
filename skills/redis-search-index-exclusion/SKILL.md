---
name: redis-search-index-exclusion
description: "Prevent selected HASH or JSON documents from being indexed by Redis Search / Redis Query Engine. Use when the user asks how to exclude keys from an index, use `FT.CREATE FILTER`, combine `PREFIX` and filters, use `@__key`, index only matching field values, use `NOINDEX`, fix documents still being indexed, or recreate an index because FILTER logic is immutable."
---

# Redis Search Index Exclusion

Use this skill when a Redis Search index should cover only part of the keyspace or exclude specific documents.

## Design Rule

Index exclusion is normally decided at index creation time. Use `PREFIX` to narrow the keyspace and `FILTER` to exclude or include documents based on key name or field values. `FILTER` logic cannot be edited in place; recreate the index when it changes.

## Pattern

Exclude one key by key name:

```text
FT.CREATE item_idx ON JSON PREFIX 1 item: FILTER '@__key!="item:2"' SCHEMA $.id AS id NUMERIC
```

Index only documents matching a field value:

```text
FT.CREATE config_idx ON JSON PREFIX 1 config: FILTER "@serviceId=='workflow'" SCHEMA $.config.serviceId AS serviceId TAG
```

Store but do not index a field:

```text
SCHEMA $.metadata.owner AS owner TAG NOINDEX
```

## Workflow

1. Identify the document model: HASH or JSON.
2. Choose the narrowest safe `PREFIX`.
3. Decide whether exclusion is based on:
   - Key name using `@__key`.
   - Field values.
   - A logical expression over document attributes.
4. Create a small test dataset and index.
5. Validate with:

   ```text
   FT.INFO <index>
   FT.SEARCH <index> * RETURN 0
   ```

6. Confirm `num_docs` matches expectations and indexing failure counters are clean.
7. Apply the same pattern to the production index only after testing.

## Recreate Procedure

If the filter is wrong:

1. Capture the current index schema.
2. Build the corrected `FT.CREATE` command.
3. Plan index recreation during a safe window for large datasets.
4. Drop only the index, not the underlying documents, unless deletion is explicitly intended.
5. Require confirmation before `FT.DROPINDEX`, especially if using `DD`.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Documents still indexed | Prefix too broad or filter expression does not match data | Test expression against sample keys and recreate index. |
| Too few documents indexed | Filter excludes more than intended or schema path mismatch | Check sample documents and `FT.INFO` failure counters. |
| Filter change not applied | Filters are immutable after index creation | Drop/recreate the index with corrected filter. |
| Search memory too high | Index scope too broad | Narrow prefix, add filter, and avoid indexing unused fields. |
| Need field stored but not searchable | Field included as searchable schema field | Use `NOINDEX` where supported for that field type/use case. |
| Need to delete unwanted keys | Exclusion only affects index, not stored data | Use a safe `SCAN` plus `UNLINK` deletion workflow with confirmation. |

## Safety Notes

- `FT.DROPINDEX <index>` removes the index; `FT.DROPINDEX <index> DD` also deletes documents and is destructive.
- Excluding a document from an index does not remove it from Redis.
- Avoid broad production tests that create large replacement indexes without memory headroom.

## Evidence To Collect

- Index creation command.
- Document type and example document.
- Intended include/exclude rule.
- `FT.INFO` output.
- Sample `FT.SEARCH` results showing unexpected inclusion/exclusion.
- Whether index recreation or document deletion is intended.
