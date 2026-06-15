---
name: redis-search-ftcreate-transaction-limits
description: Use when Redis Search index creation with FT.CREATE, FT.ALTER, or related module commands fails inside MULTI/EXEC, especially with multi-shard Redis, Redis Cluster, Redis Cloud clustering, Redis Software clustered databases, distributed transactions, index bootstrap workflows, or the error that FT.CREATE is not allowed inside MULTI in a multi-shard configuration.
---

# Redis Search FT.CREATE Transaction Limits

Use this skill when a user tries to create or alter a Redis Search index inside `MULTI/EXEC` and sees different behavior between standalone and clustered deployments.

## Core Rule

- Standalone Redis can run `FT.CREATE` inside `MULTI/EXEC` because the transaction executes on one node.
- Multi-shard or clustered Redis must run `FT.CREATE` outside `MULTI/EXEC` because index metadata must be coordinated across shards.
- Do not design distributed atomicity around `MULTI/EXEC`; it is not a cross-shard transaction mechanism.

## Diagnostic Workflow

1. Confirm deployment mode:
   - standalone
   - Redis Open Source Cluster
   - Redis Cloud clustered database
   - Redis Software clustered database
2. Capture the exact command sequence and error.
3. Check whether the transaction contains `FT.CREATE`, `FT.ALTER`, or other module commands that may be disallowed in clustered transactions.
4. Move index DDL outside the transaction.
5. Verify index creation with:

```text
FT.INFO <index>
```

6. Only then run data population or application startup writes.

## Recommended Bootstrap Pattern

Use this shape for clustered deployments:

1. Create or alter the index outside `MULTI/EXEC`.
2. Poll or validate with `FT.INFO`.
3. Insert or update documents with normal HASH or JSON writes.
4. Make the bootstrap idempotent by handling "index already exists" as a safe outcome when appropriate.
5. Fail application startup clearly if the index cannot be created or validated.

## Troubleshooting

- `ERR FT.CREATE is not allowed inside MULTI in a multi-shard configuration`: remove `FT.CREATE` from the transaction and run it before data writes.
- Index missing after startup: inspect queued transaction errors and verify bootstrap did not ignore command failures.
- Need atomic index plus data creation: explain that clustered Redis cannot provide that atomic DDL plus data transaction; use an initialization phase and idempotent writes.
- Works locally but fails in production: compare local standalone Redis with production clustered topology.

## Response Pattern

When answering:

1. State whether the deployment is standalone or clustered.
2. Explain the transaction boundary.
3. Rewrite the command sequence with `FT.CREATE` outside `MULTI/EXEC`.
4. Add `FT.INFO` validation and startup error handling.
