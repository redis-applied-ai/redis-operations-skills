---
name: redis-crdb-cloud-low-downtime-migration
description: "Plan low-downtime migration from on-prem Redis Enterprise Active-Active CRDB to Redis Cloud CRDB using RIOT-style live replication. Use when the user asks how to migrate CRDB to Redis Cloud, why RESTORE-based migration fails, how to handle keyspace notifications, stream ID limitations, live cutover, data comparison, or missing keys after CRDB migration."
---

# Redis CRDB Cloud Low-Downtime Migration

Use this skill when moving an on-prem Redis Enterprise Active-Active database to Redis Cloud Active-Active with minimal downtime.

## Preflight

1. Identify source and target:
   - Source CRDB endpoints, regions, credentials, TLS, and versions.
   - Target Redis Cloud CRDB endpoints, credentials, TLS, and networking.
   - Dataset size, key count, streams usage, big keys, hot keys, and write rate.
2. Define success criteria:
   - Acceptable cutover downtime.
   - Data consistency tolerance.
   - Rollback plan.
   - Validation method.
3. Create backups before migration.
4. Confirm the migration host can reach both source and target endpoints.
5. Verify current RIOT/RIOT-REDIS command syntax against the installed version before production execution.

## Critical CRDB Rules

- Use a data-structure-aware replication mode for CRDB migration; RESTORE-based modes are not suitable when the target CRDB does not support `RESTORE`.
- Live migration is best-effort until cutover. Pause or drain writes during the final switch if strict consistency matters.
- Stream IDs may not be preserved across CRDBs. Plan to use a tool option that generates compatible stream IDs or reinitialize streams after migration.
- Keyspace notifications are commonly required for live change capture. Confirm they can be enabled in both environments using the supported configuration path.

## Live Migration Workflow

1. Prepare source and target.
2. Enable required keyspace notifications when supported:

   ```text
   CONFIG SET notify-keyspace-events KA
   ```

3. Run the migration tool from a host with stable network access to both CRDBs.
4. Use live mode so the initial dataset and ongoing changes are copied.
5. Watch migration metrics, errors, retry counts, and throughput.
6. When lag is low and stable, start cutover:
   - Pause or reduce writes.
   - Wait for the final changes to replicate.
   - Point applications to the Redis Cloud CRDB endpoint.
   - Restart or reload clients as needed.
7. Validate data and application behavior before decommissioning source writes.

## Example Command Shape

Use this as a shape only; adjust for the installed migration tool version:

```bash
riot-redis --info \
  -h <source_host> -p <source_port> --pass <source_password> \
  replicate-ds \
  -h <target_host> -p <target_port> --pass <target_password> \
  --mode live
```

Add TLS, username, stream, batch, thread, and filtering flags according to the tool version and environment.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Connection fails | Firewall, allow list, TLS, auth, or endpoint issue | Test connectivity from the migration host to both endpoints and verify credentials. |
| Missing keys | Notifications disabled, tool version issue, or missed live changes | Confirm notification setting, upgrade tool, and compare source/target. |
| RESTORE errors | Wrong migration mode for CRDB | Switch to CRDB-compatible data-structure replication. |
| Streams missing or changed | Stream ID compatibility limitation | Use compatible stream migration options or re-seed streams. |
| Migration slow | Big keys, high write rate, low batch/thread settings, or network latency | Tune batch/thread settings and analyze big/hot keys. |
| Data inconsistency after cutover | Writes continued while lag existed | Pause writes briefly and rerun comparison or targeted sync. |

## Validation

- Compare key counts and representative values.
- Compare TTL behavior on sampled keys.
- Validate application read/write paths against Redis Cloud CRDB.
- Check latency from each application region.
- Monitor CRDB sync health, errors, CPU, memory, and network usage.
- Keep source available until validation and rollback window are complete.

## Escalation Packet

Collect:

- Source and target CRDB IDs, regions, and versions.
- Migration tool name and version.
- Command shape with secrets removed.
- Dataset size, write rate, stream usage, big-key findings.
- Keyspace notification settings.
- Error logs and migration metrics.
- Cutover timeline and validation results.
