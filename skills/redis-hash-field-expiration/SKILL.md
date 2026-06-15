---
name: redis-hash-field-expiration
description: "Use Redis hash field-level expiration for per-field TTLs, rolling logs, granular session cleanup, sliding-window counters, active-session hashes, and atomic hash helpers such as `HGETEX`, `HSETEX`, and `HGETDEL`. Use when troubleshooting `HEXPIRE`, `HPEXPIRE`, `HEXPIREAT`, `HPEXPIREAT`, `HTTL`, `HPTTL`, `HEXPIRETIME`, `HPEXPIRETIME`, `HPERSIST`, unknown-command errors, TTL disappearing after `HSET`, immediate field deletion, key TTL precedence, SDK support, or migration from whole-key TTLs to hash-field TTLs."
---

# Redis Hash Field Expiration

Use this skill when a user wants independent TTLs on fields inside a Redis hash instead of expiring the entire key. Confirm the target Redis deployment supports the hash-field expiration commands before designing around them.

## Core Rules

- Verify command availability with the target database version and client SDK before rollout.
- A field TTL expires only the field; the hash key remains until it is empty or the key itself expires.
- If the hash key has its own TTL, the key expiration wins over any longer field TTL.
- Updating a field with `HSET` can clear that field's expiration; reapply the field TTL or use atomic helpers where supported.
- A zero TTL or an expiration timestamp in the past deletes the field immediately.
- Field expiration operations work on the listed fields; avoid large synchronized batches that create expiration or CPU spikes.

## Command Groups

Field TTL commands:

| Command | Purpose | Time Unit |
| --- | --- | --- |
| `HEXPIRE` | Set relative TTL on fields | seconds |
| `HPEXPIRE` | Set relative TTL on fields | milliseconds |
| `HEXPIREAT` | Set absolute expiration timestamp on fields | seconds |
| `HPEXPIREAT` | Set absolute expiration timestamp on fields | milliseconds |
| `HTTL` | Return remaining TTL for fields | seconds |
| `HPTTL` | Return remaining TTL for fields | milliseconds |
| `HEXPIRETIME` | Return absolute expiration time | seconds |
| `HPEXPIRETIME` | Return absolute expiration time | milliseconds |
| `HPERSIST` | Remove field expiration | not applicable |

Atomic helper commands, when supported:

| Command | Use |
| --- | --- |
| `HGETEX` | Get field value and set or refresh its TTL atomically. |
| `HSETEX` | Set field value with expiration atomically. |
| `HGETDEL` | Get field value and delete it atomically. |

## Basic Patterns

Set a TTL on two fields:

```text
HEXPIRE myhash 60 FIELDS 2 field1 field2
```

Set an absolute expiration timestamp:

```text
HEXPIREAT myhash 1715704971 FIELDS 2 field1 field2
```

Inspect TTLs and expiration times:

```text
HTTL myhash FIELDS 2 field1 field2
HEXPIRETIME myhash FIELDS 2 field1 field2
```

Remove field expiration:

```text
HPERSIST myhash FIELDS 1 field1
```

If the client library lacks typed helpers, use its raw command interface after verifying the server supports the command.

## Use Cases

| Pattern | Model |
| --- | --- |
| Rolling logs or recent events | Store each event as a field; expire fields after the retention window; use `HLEN` for current count. |
| Sliding counters | Use timestamped fields that expire after the analysis window. |
| Session attributes | Expire sensitive or temporary attributes without deleting the entire user/session hash. |
| Active session registry | Store session IDs as fields and let field TTLs prune inactive sessions. |

## Correctness Checks

Before production use:

1. Check command availability on the exact database endpoint:

   ```text
   COMMAND INFO HEXPIRE HTTL HGETEX HSETEX HGETDEL
   ```

2. Check SDK support for the needed commands. If wrappers are missing, use raw commands or upgrade the client.
3. Validate semantics with a small test hash:
   - set a field
   - set field TTL
   - verify `HTTL`
   - update with `HSET`
   - verify whether TTL must be reapplied
4. Confirm key-level TTL does not expire the whole hash before field-level TTLs matter.
5. Add jitter or spread batches when setting many field expirations.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| `unknown command` | Server version, product capability, or SDK path lacks the command | Verify `COMMAND INFO`; upgrade database/client or use raw command only if server supports it. |
| `HTTL` returns `-2` | Field is missing or already expired | Verify field name, recreate the field, and set TTL again. |
| `HTTL` returns `-1` | Field exists without expiration | Apply `HEXPIRE`, `HPEXPIRE`, `HEXPIREAT`, or `HPEXPIREAT`. |
| TTL disappears after `HSET` | Field update removed expiration | Reapply TTL after update or use `HSETEX` where supported. |
| Field disappears immediately | TTL is zero or timestamp is in the past | Use a positive TTL or future timestamp. |
| Whole hash disappears early | Key-level TTL expired | Inspect key `TTL` and remove or adjust key-level expiration if field TTLs should control lifecycle. |
| Counts look lower than expected | Expired fields are no longer counted | Treat `HLEN` as count of live fields; inspect field TTLs before assuming data loss. |
| Expiration workload spikes | Too many fields expire at the same time | Add TTL jitter and batch updates over time. |

## Migration Guidance

- Replace extra per-field keys with one hash only when hash size, access patterns, and expiration behavior remain manageable.
- When moving from key-level TTLs to field-level TTLs, audit application code that assumes the whole object disappears together.
- Use atomic helpers for get-and-refresh, set-with-expiration, and get-and-delete flows when supported.
- Keep lifecycle-sensitive fields indexed or mirrored only if downstream systems can tolerate asynchronous expiration.

## Response Shape

When advising a user:

1. Confirm command support and client support.
2. Explain whether key-level or field-level TTL should own lifecycle.
3. Provide the minimal command sequence for their pattern.
4. Call out `HSET` TTL clearing and immediate-deletion cases.
5. Add scale guidance for batch size, TTL jitter, monitoring, and migration testing.
