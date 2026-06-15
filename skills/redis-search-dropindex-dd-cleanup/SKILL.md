---
name: redis-search-dropindex-dd-cleanup
description: "Troubleshoot Redis Search `FT.DROPINDEX DD` not deleting all documents. Use when the user sees leftover hashes or JSON documents after dropping an index, needs to check `FT.INFO` indexing status, percent indexed, hash indexing failures, schema/type mismatches, prefix cleanup with SCAN and UNLINK, Redis Cloud Search behavior, or Active-Active CRDB deletion across peer clusters."
---

# Redis Search DROPINDEX DD Cleanup

Use this skill when `FT.DROPINDEX <index> DD` removed the index but some source documents still exist.

## Safety Rules

- `FT.DROPINDEX ... DD`, `UNLINK`, and prefix cleanup delete data; require explicit confirmation before giving final delete commands.
- Confirm the target index name and document key prefix before any cleanup.
- Prefer `UNLINK` over `DEL` for large keyspaces to avoid blocking the Redis main thread.
- In Active-Active CRDB, reason about all participating clusters before declaring deletion complete.

## Behavior to Explain

- `FT.DROPINDEX <index>` removes only the index structure.
- `FT.DROPINDEX <index> DD` removes the index and documents that were successfully indexed.
- Documents that failed indexing, were outside the index prefix, or were written after index build/drop timing can remain.
- Large index deletion can be asynchronous, so brief leftovers may be normal immediately after the command.

## Pre-Drop Checks

Before using `DD`, inspect the index:

```redis
FT.INFO <index>
```

Confirm:

- `indexing` is `0`.
- `percent_indexed` is `1` or 100 percent.
- `hash_indexing_failures` is `0`.
- Index prefixes match the keys intended for deletion.

If failures exist, identify whether schema/type mismatches or data shape issues prevented documents from being indexed.

## Post-Drop Triage

1. Check whether a specific key remains:

   ```redis
   EXISTS <key>
   ```

2. Scan the intended prefix:

   ```redis
   SCAN 0 MATCH <prefix>:* COUNT 1000
   ```

3. Classify leftovers:
   - Never indexed because of schema/type mismatch.
   - Outside the index prefix.
   - Written after indexing or during cleanup.
   - CRDB peer still has local copy.
   - Large deletion still in progress.

## Manual Cleanup Pattern

After explicit confirmation and prefix verification, use non-blocking deletion:

```bash
redis-cli --scan --pattern '<prefix>:*' | xargs redis-cli UNLINK
```

For TLS, ACL, cluster, or Cloud connections, adapt the `redis-cli` flags to the connection method and avoid exposing credentials in shell history.

## CRDB Considerations

- Run or coordinate deletion across all participating Active-Active clusters when global removal is required.
- Verify replication health and transient failures before assuming deletion propagated.
- Prefix-based cleanup may be safer than relying only on index membership when indexing was incomplete.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Some documents remain | `hash_indexing_failures`, prefix mismatch, or writes during deletion. |
| Numeric/text fields failed indexing | Schema/type mismatch in source documents. |
| Large dataset still visible briefly | Asynchronous cleanup may still be running; recheck after delay. |
| CRDB peers disagree | Deletion was not coordinated across all peer clusters or replication had transient failures. |
| Cleanup command is slow | Use `UNLINK`, batching, and controlled scan count. |

## Escalation Packet

Collect:

- Redis deployment type and Search module/version if available.
- Index name and `FT.CREATE` prefix/schema.
- `FT.INFO <index>` output before drop if available.
- `FT.DROPINDEX` command used, with timestamp.
- Remaining key examples and prefix scan results.
- Whether the database is Active-Active CRDB.
- Cleanup command attempted and any errors.
