---
name: redis-cloud-high-memory-warning
description: "Interpret and respond to Redis Cloud high memory usage warnings. Use when the user sees high memory usage, dataset exceeds plan limit, OOM errors, evictions, memory above 80, 90, or 95 percent, noeviction write failures, cache hit-rate drops, Auto Tiering memory pressure, or needs to choose between optimizing keys and TTLs, increasing database size, or upgrading from Essentials to Pro."
---

# Redis Cloud High Memory Warning

Use this skill when Redis Cloud reports high memory usage or the database approaches its configured memory limit.

## Risk Levels

| Memory level | Meaning | Action |
| --- | --- | --- |
| Around 80 percent | Early warning | Review growth trend and alert settings. |
| 85 to 95 percent | Capacity pressure | Expect evictions, latency, or write risk depending on policy. |
| Above 95 percent or OOM errors | Capacity incident | Act immediately unless evictions are expected and healthy. |

Redis Cloud alert thresholds can be configured in database alert settings. Verify the user's actual alert configuration before assuming defaults.

## First Question

Determine workload type:

- Cache: data can be evicted and rebuilt.
- Persistent/source-of-truth: data loss or failed writes are unacceptable.

This determines whether eviction is a normal control mechanism or an incident.

## Impact by Workload

| Workload | Likely impact |
| --- | --- |
| Cache | Evictions, lower hit rate, higher backend load, latency increase. |
| Persistent workload | OOM errors, write failures, instability if eviction is not allowed. |
| `noeviction` policy | Writes fail when memory is exhausted. |
| Search/JSON heavy workload | Indexes or document overhead may be driving growth. |
| Auto Tiering | RAM still stores keys and metadata; hot or large values can still create RAM pressure. |

## Decision Tree

| Situation | Path |
| --- | --- |
| Growth is unexpected or stale data exists | Optimize data lifecycle and key/index footprint. |
| Data is legitimate and must remain | Increase database memory size. |
| Essentials database is near scale ceiling | Upgrade to Pro or choose a larger architecture. |
| Need horizontal scale or clustering | Move to Pro and evaluate clustering. |
| OOM, rising above 90 percent, or unexpected evictions | Stabilize immediately, then resize or reduce data. |

## Optimize Path

Check:

- Missing or too-long TTLs.
- Unused namespaces.
- Large keys or collections.
- Search or JSON index size.
- Expired data not being cleaned as expected.
- Unexpected ingestion or migration.

Actions:

- Add TTLs where lifecycle allows.
- Trim large collections.
- Remove unused prefixes after explicit confirmation.
- Optimize index schema or document shape.
- Reduce ingestion rate while investigating.

## Increase Size Path

Use when the data is valid and must remain:

1. Open the database in Redis Cloud Console.
2. Choose `Edit`.
3. Increase memory size within plan limits.
4. Monitor memory, evictions, latency, and error rates after resize.

## Upgrade Path

Use when Essentials limits block the needed size, throughput, or clustering behavior:

- Evaluate Pro plan.
- Consider clustering for larger datasets or throughput.
- Confirm cost and migration implications before changing plan.

## Immediate Response

Act now if:

- OOM errors appear.
- Memory is above 90 percent and still rising.
- Evictions spike unexpectedly.
- Latency rises with memory saturation.
- Writes fail under `noeviction`.

Temporarily pause non-critical ingestion or cleanup jobs if they are increasing memory pressure.

## Escalation Packet

Collect:

- Database ID, plan, memory limit, and current memory usage.
- Workload type: cache or persistent.
- Eviction policy and eviction metrics.
- OOM errors or write failures.
- Latency timeline and memory growth trend.
- Largest keys, namespaces, indexes, or document types if known.
- Auto Tiering status.
- Recent deploys, imports, migrations, or traffic changes.
