---
name: redis-cloud-large-dataset-import-validation
description: "Validate and troubleshoot large dataset imports into Redis Cloud using RDB upload, Replica Of, RIOT, Redis Data Integration, or logical loading. Use when import completes but data or Search results look incomplete, `FT.INFO` shows indexing still active or failures, key counts differ from source, memory headroom is low, module or schema mismatches appear, import fails from S3/GCS/Azure storage, `SUBSCRIPTION_NOT_ACTIVE` appears, or users need a post-import validation checklist before running operational queries."
---

# Redis Cloud Large Dataset Import Validation

Use this skill after or during large Redis Cloud imports. The goal is to prove the target dataset is complete, indexed, compatible, and healthy before applications or operational queries depend on it.

## Safety Rules

- Imports can overwrite or replace target data. Confirm the target database and backup/export posture before rerunning an import.
- Avoid importing into an active production database unless the migration plan explicitly accepts overwrite and latency risk.
- Treat Replica Of, RIOT, Redis Data Integration, and RDB upload as different import paths with different validation and cutover steps.
- Do not rebuild or drop Search indexes without an impact plan and confirmation.
- Do not assume module, Redis version, or Search behavior is compatible; verify the source and target.

## Import Method Intake

Identify:

- import method: RDB upload, Replica Of, RIOT, Redis Data Integration, app-specific loader, or other
- source Redis product/version and target Redis Cloud plan/version
- dataset size, expected key count, and expected document count
- modules/capabilities used: Search, JSON, TimeSeries, probabilistic data structures, streams, functions, or custom modules
- whether Search indexes existed before import or will be created after import
- object storage path and permissions if importing from S3, GCS, Azure Blob, or similar storage
- expected downtime and whether applications are writing during import

## Core Validation Checklist

1. Verify target database state is active and stable in Redis Cloud Console.
2. Compare key counts:

   ```text
   DBSIZE
   ```

   Compare against pre-export or source-side totals. For clustered or filtered imports, compare against the expected subset, not a generic source total.

3. Sample representative keys:
   - data type
   - value shape
   - TTL behavior
   - encoding-sensitive fields
   - application-critical namespaces
4. Check memory and resource headroom in Redis Cloud metrics:
   - memory percentage
   - CPU
   - network
   - ongoing import or indexing activity
   Treat sustained memory near the limit as a risk even if the import technically completed.
5. Validate application smoke tests before cutover.

## Search Index Validation

For every expected Search index:

```text
FT.INFO <index>
```

Confirm:

- `indexing` is complete, commonly shown as `0`
- `num_docs` matches the expected indexed document count
- `hash_indexing_failures` or equivalent failure counters are `0`
- schema fields match the imported HASH or JSON shape
- JSON paths and hash field names match the imported data

If indexing is still active, wait and monitor resource impact before declaring the import incomplete.

If failures appear, inspect sample failed documents for:

- wrong type for indexed field
- missing JSON path
- TAG separator mismatch
- NUMERIC field storing text
- vector dimension or datatype mismatch
- documents loaded under a prefix not covered by the index

## Module And Capability Compatibility

Before judging missing data:

- Compare source and target Redis versions.
- Confirm required Redis Cloud capabilities are enabled.
- Confirm modules or features used by the source are supported in the target plan.
- For unsupported or mismatched modules, use logical migration tools or re-export without unsupported data when appropriate.
- For Search-heavy imports, consider creating or rebuilding indexes after bulk load when the import method allows it, to reduce parallel write and indexing pressure.

## Common Failure Modes

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Import fails immediately | Object storage path, permissions, region, or URL issue | Recheck bucket/blob path, credentials, access policy, and signed URL validity. |
| Import fails midway | Memory too small, timeout, target state change, or file too large | Check Redis Cloud memory, resize or split source files, then retry safely. |
| `SUBSCRIPTION_NOT_ACTIVE` | Database or subscription is in maintenance or another lifecycle state | Wait until active; do not stack another import or resize operation. |
| Query results incomplete | Search indexing still running | Check `FT.INFO` and wait for indexing to finish. |
| Missing keys | Partial import, unsupported data, wrong target, or filtered source | Compare `DBSIZE`, sample namespaces, and import logs/status. |
| `hash_indexing_failures` nonzero | Schema/type mismatch | Fix schema or data, then plan index rebuild if needed. |
| High latency during import | Writes and indexing compete for resources | Reduce traffic, delay index creation when possible, or schedule a larger window. |
| Module mismatch | Target lacks source capability | Use a supported migration path or adapt data model before retry. |

## Rerun Decision

Before rerunning:

1. Confirm whether rerun overwrites target data.
2. Confirm the source is still available and consistent.
3. Confirm target database memory and plan capacity are adequate.
4. Decide whether to import into a fresh database instead of retrying in place.
5. Capture current target state for support analysis if the prior run failed unexpectedly.

## Escalation Packet

Collect:

- Redis Cloud account, subscription, and database ID.
- Import method and source type.
- Dataset size, expected key count, and observed `DBSIZE`.
- Object storage provider/path type, without secrets.
- Import start/end timestamps and status/error text.
- Redis versions and required modules/capabilities.
- `FT.INFO` output for affected indexes.
- Memory, CPU, and network metrics during import.
- Whether applications were writing during import.
- Any recent maintenance, resize, backup, or subscription-state change.

## Response Shape

When helping a user:

1. Identify import method and target state.
2. Run the validation sequence: database active, key count, samples, memory, Search index state.
3. Classify the issue as storage access, capacity, target lifecycle state, module compatibility, Search indexing, or schema mismatch.
4. Recommend retry, wait, resize, rebuild index, or open Support only after evidence supports that path.
