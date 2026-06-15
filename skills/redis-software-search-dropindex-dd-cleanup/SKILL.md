---
name: redis-software-search-dropindex-dd-cleanup
description: "Troubleshoot Redis Software `FT.DROPINDEX DD` leaving documents behind. Use when Search index deletion does not remove all hashes or JSON keys, `FT.INFO` shows indexing or hash_indexing_failures, schema or type mismatches leave unindexed keys, Redis Software cluster load interrupts deletion, CRDB peer cleanup is needed, or manual prefix cleanup with SCAN, UNLINK, RedisGears, or batch scripts is required."
---

# Redis Software Search DROPINDEX DD Cleanup

Use this skill when `FT.DROPINDEX <index> DD` in Redis Software removes an index but leaves some source keys behind.

## Safety Rules

- `FT.DROPINDEX ... DD`, `UNLINK`, RedisGears cleanup, and batch deletion scripts delete data; require explicit confirmation.
- Confirm the index, database, and key prefix before cleanup.
- Prefer `UNLINK` and batched cleanup over `DEL` for large datasets.
- In clustered or CRDB deployments, confirm every shard/peer plan before calling cleanup complete.

## Behavior to Explain

- Without `DD`, `FT.DROPINDEX` removes only the index definition.
- With `DD`, it deletes keys that were successfully indexed.
- Keys can remain if indexing was incomplete, documents failed schema validation, load interrupted cleanup, or keys were written during/after index build.
- Large deletions can be asynchronous, so short-lived leftovers may not indicate failure.

## Investigation Workflow

1. Inspect the index before deletion when possible:

   ```redis
   FT.INFO <index>
   ```

2. Confirm:
   - `indexing` is `0`.
   - `percent_indexed` is `1` or 100 percent.
   - `hash_indexing_failures` is `0`.
   - The `PREFIX` matches the intended source keys.
3. If `hash_indexing_failures` is nonzero, look for schema/type mismatches, such as text stored where `NUMERIC` was expected.
4. After drop, scan the intended prefix:

   ```redis
   SCAN 0 MATCH <prefix>:* COUNT 1000
   EXISTS <key>
   ```

5. Determine whether leftovers were unindexed, newly written, outside the prefix, or not cleaned due to cluster load.

## Cleanup Options

For modest key counts, after confirmation:

```bash
redis-cli --scan --pattern '<prefix>:*' | xargs redis-cli UNLINK
```

For larger Redis Software clusters:

- Use batched deletion with controlled scan count and throttling.
- Consider RedisGears or an approved async cleanup mechanism if already supported in the environment.
- Monitor latency, CPU, memory, and command backlog during cleanup.

Adapt `redis-cli` flags for TLS, ACL, cluster endpoint, and authentication without exposing secrets.

## Cluster and CRDB Considerations

- Run cleanup from an endpoint that can reach all relevant keys.
- For Active-Active CRDB, coordinate deletion or prefix cleanup in all peer clusters.
- Check replication health before and after cleanup.
- Review Redis Software and Search module versions when propagation behavior looks wrong; verify current release guidance before attributing to a known version issue.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Keys remain after `DD` | They were not successfully indexed or were created after indexing. |
| `hash_indexing_failures` greater than zero | Schema/type mismatch or malformed source documents. |
| Cleanup stalls under load | Use batched `UNLINK`, throttle, or async cleanup tooling. |
| CRDB peers retain keys | Deletion was not applied or propagated across every peer cluster. |
| Prefix scan finds unexpected keys | `FT.CREATE PREFIX` did not match application key conventions. |

## Escalation Packet

Collect:

- Redis Software and Search module versions.
- Database name/ID and cluster topology.
- Index name, schema, and prefix.
- `FT.INFO <index>` output if available.
- Command used and timestamp.
- Remaining key examples and scan count.
- Whether cluster is sharded or Active-Active CRDB.
- Cleanup method attempted and observed latency/errors.
