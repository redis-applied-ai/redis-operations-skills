---
name: redis-search-lua-function-limitations
description: "Diagnose and redesign Redis Lua scripts or Redis Functions that try to run Search and Query commands such as `FT.SEARCH` or `FT.AGGREGATE`. Use when the user sees `Command not allowed in script`, wants to call RediSearch from `EVAL`, Lua, or `FUNCTION LOAD`, or needs an alternative pattern for atomic updates after search results."
---

# Redis Search Lua Function Limitations

Use this skill when Search and Query commands are being attempted inside Lua scripts or Lua-based Redis Functions.

## Compatibility Rule

Do not call Redis Search and Query commands such as `FT.SEARCH`, `FT.AGGREGATE`, or vector search operations from Lua via `redis.call()` or `redis.pcall()`. Treat errors like `Command not allowed in script` as expected behavior, not a syntax issue.

Core Redis commands such as `GET`, `SET`, `HSET`, and similar key-local operations are the normal Lua scripting surface.

## Why It Fails

| Constraint | What it means |
| --- | --- |
| Atomic execution | Lua runs as one atomic operation; global index scans and distributed query work do not fit that model. |
| Key locality | Clustered scripting expects declared keys and compatible hash slots; Search indexes can span keys and shards. |
| Module isolation | Search and Query commands are not exposed to Lua as ordinary core commands. |
| Consistency | Redis blocks command classes that could produce partial or inconsistent results inside scripts. |

## Triage Workflow

1. Capture the exact script/function body and the error.
2. Identify every `redis.call()` or `redis.pcall()` command.
3. Separate commands into:
   - Core Redis commands that can stay in Lua.
   - Search/Query/module commands that must move out of Lua.
4. Check whether the database is clustered or uses OSS Cluster API. If OSS Cluster API is enabled, Redis Search compatibility may be a separate blocker.
5. Redesign with one of the supported patterns below.

## Supported Patterns

| Need | Pattern |
| --- | --- |
| Search for candidate keys | Run `FT.SEARCH` or `FT.AGGREGATE` from application/client code. |
| Atomically update known keys | Pass the resulting keys into a Lua script after the client-side search. |
| Combine query and business logic | Keep query orchestration in the application layer, then use transactions, pipelines, or Lua for key-local critical sections. |
| Cross-shard or programmable server-side coordination | Use only a function/runtime explicitly supported by the target Redis product and version; verify support before recommending it. |

## Hybrid Search-Then-Lua Pattern

1. Client runs the search:

   ```text
   FT.SEARCH idx "@status:{pending}" RETURN 1 __key LIMIT 0 100
   ```

2. Client extracts the document keys.
3. Client calls a Lua script with those keys declared in `KEYS`.
4. Lua performs only key-local core Redis operations, such as validation and updates.

This preserves atomicity for the update phase without trying to execute Search inside Lua.

## Common Errors

| Error or symptom | Diagnosis | Action |
| --- | --- | --- |
| `Command not allowed in script` | Search/Query command called from Lua | Move the command to client code. |
| Partial or missing results in cluster mode | Cross-shard query attempted in script-like flow | Use application orchestration or a supported distributed runtime. |
| Failure after Redis upgrade | Stricter validation exposed unsupported script behavior | Remove module/query calls from Lua. |
| `FT.SEARCH` unavailable in clustered database | OSS Cluster API compatibility issue | Use a Search-compatible database mode, commonly proxy-based clustering in Redis Enterprise environments. |

## Security Guidance

- Keep Lua scripts limited and auditable.
- Restrict scripting/function permissions to trusted users.
- Treat script changes that affect writes as production-risk changes and test with representative keys.
- Do not bypass unsupported Search-in-Lua behavior with undocumented command flags or eval wrappers.
