---
name: redis-crdb-zero-memory
description: "Diagnose and fix Redis Enterprise Active-Active CRDB instances that show 0 memory after creation. Use when a user reports CRDB memory allocation is zero, `memory_size` was used instead of per-instance `memory_limit`, memory units look wrong, an Active-Active database was created through API but not allocated, or CRDB instance provisioning fails due to capacity, license, or shard configuration."
---

# Redis CRDB Zero Memory

Use this skill when an Active-Active CRDB shows 0 memory despite a requested size. Focus on payload shape, units, per-instance configuration, shard count, capacity, and license constraints.

## Core Rules

- CRDB memory must be defined per participating instance.
- Use `memory_limit` in MB for each instance.
- Do not rely on a top-level `memory_size`; it may be ignored or default to 0.
- Each instance needs a valid `shards_count` of at least 1.
- Capacity and license limits can prevent allocation even when the API request is accepted.

## Diagnosis Workflow

1. Confirm scope:
   - CRDB name or ID.
   - Participating clusters/instances.
   - Creation method: UI, API, Terraform, or automation.
   - Whether all instances or only some show 0 memory.
2. Inspect current CRDB and instance state:
   - Check Admin Console for instance health and memory.
   - Use API GET output for CRDB and each instance.
   - Confirm `memory_limit` exists on every instance.
   - Confirm instances are active/running.
3. Review the creation or update payload:
   - Look for top-level `memory_size`.
   - Look for missing per-instance `memory_limit`.
   - Check units are MB, not bytes.
   - Confirm `shards_count >= 1`.
4. Check environment readiness:
   - Available memory on every participating cluster.
   - License capacity.
   - Provisioning errors in UI/logs.

## Correction Workflow

1. Replace top-level `memory_size` with per-instance `memory_limit`.
2. Convert requested sizes to MB:
   - 2 GB -> `2048`
   - 5 GB -> `5120`
   - 10 GB -> `10240`
3. Set `shards_count` explicitly for each instance.
4. Update the CRDB with PATCH/PUT if supported for the field and environment.
5. If update is not supported or provisioning is inconsistent, plan a delete/recreate with the corrected payload.
6. Recheck each instance until status is healthy and memory is nonzero.

## Correct Payload Shape

```json
{
  "name": "my-crdb",
  "instances": [
    {
      "name": "my-crdb-us",
      "memory_limit": 5120,
      "shards_count": 1,
      "cluster": {"url": "https://cluster-us.example:9443"}
    },
    {
      "name": "my-crdb-eu",
      "memory_limit": 5120,
      "shards_count": 1,
      "cluster": {"url": "https://cluster-eu.example:9443"}
    }
  ]
}
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Memory still shows 0 | Confirm every instance has `memory_limit` and the value is in MB. |
| One instance shows 0 | Check that instance's payload, capacity, license, and provisioning events. |
| API accepts payload but allocation is wrong | Validate API version and schema expectations; check whether unsupported fields were ignored. |
| Instance fails to deploy | Check cluster capacity, license limits, and provisioning logs. |
| Shard-related errors | Confirm `shards_count` is present and at least 1. |

## Safety Checks

- Do not include credentials or secrets in shared API payloads or logs.
- Do not recommend deleting and recreating a CRDB until the user confirms data impact, backup/migration plan, and acceptable downtime or replication impact.
- For current API schemas and updateability of CRDB fields, verify live Redis Enterprise documentation or environment API behavior before making irreversible recommendations.

## Escalation Packet

Collect:

- Sanitized create/update payload.
- API endpoint and version.
- CRDB ID and participating instance IDs.
- Memory values shown in UI/API.
- Cluster capacity and license state.
- Provisioning timestamps and error messages.
