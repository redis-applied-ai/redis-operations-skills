---
name: redis-cloud-zone-capacity-scaling-failure
description: "Troubleshoot Redis Cloud resize, scale-up, throughput, memory, Flex, Essentials, Pro, or database provisioning changes that fail because a selected cloud zone or VM/resource pool has insufficient capacity. Use when errors mention zone capacity, stockout, VM type unavailable, resource pool exhausted, provisioning error, pending resize, deletion blocked after failed scaling, or continued billing for an unusable Redis Cloud database stuck after a capacity-related scaling operation."
---

# Redis Cloud Zone Capacity Scaling Failure

Use this skill when a Redis Cloud scaling or resize request fails during provisioning because the selected cloud provider zone cannot allocate the requested resources. For deciding whether to scale in the first place, use `redis-cloud-throughput-sizing-decision`; for reducing capacity safely, use `redis-cloud-right-sizing`.

## Current-State Rule

Cloud-provider capacity, Redis Cloud region/zone availability, supported VM types, plan behavior, and billing impact are current-state facts. Verify the live Redis Cloud console state, task/error details, provider region health, and current Redis Support guidance before promising availability, retry timing, or billing outcomes.

## Recognize The Failure

Treat the issue as likely zone-capacity related when the failed operation includes language such as:

- resource pool exhausted
- insufficient capacity
- stockout
- selected zone unavailable
- VM or instance type unavailable in the selected zone
- provisioning error tied to a region or zone

This is usually an infrastructure allocation failure during provisioning, not a Redis command, data model, or application configuration problem.

## First Triage

1. Identify the operation:
   - memory increase
   - throughput increase
   - plan/tier change
   - Flex or storage-tier change
   - database creation
   - region/zone placement change
2. Record the exact error and task timestamp.
3. Check the database lifecycle state:
   - `Active`: the failed request rolled back or did not apply; retry strategy may be possible.
   - `Pending`, `Provisioning error`, or similar stuck state: avoid stacking more changes and prepare Support escalation.
4. Confirm whether deletion is available. If deletion is blocked by the provisioning state, Support intervention is likely required.
5. Check whether billing is still active and whether the user wants recovery or deletion.

## If The Database Is Active

Use a conservative retry plan:

1. Retry later only if the operation is not urgent and the database is otherwise healthy.
2. Reduce the requested size or apply smaller increments.
3. Try a different zone or region only after considering endpoint, latency, peering, data migration, and compliance impact.
4. Validate the database returns to `Active` after each attempt before applying another change.
5. If repeated attempts fail in the same zone, treat the zone as constrained and plan an alternate placement or Support review.

Do not run large repeated scaling attempts during an incident; each failed operation can leave control-plane state harder to reason about.

## If The Database Is Stuck

If the database is in a provisioning error, pending, or locked state:

- do not keep retrying scaling operations
- do not assume deletion has stopped billing unless the database/subscription is actually deleted
- do not tell the user the UI can always clear this state
- collect the escalation packet and ask Redis Support to clear the provisioning state or delete the resource

If the user needs to stop charges, make the request explicit: delete the database and, if appropriate, the subscription after the stuck state is cleared.

## Prevention And Planning

- Scale gradually instead of making a single large capacity jump.
- Avoid repeatedly choosing a zone that has already failed capacity allocation.
- Validate `Active` state after each resize before scheduling follow-up changes.
- For test or temporary environments, clean up unused databases promptly.
- For production moves to another zone or region, treat the change as an architecture/migration decision, not just a retry.
- Maintain current backups or migration options before major capacity changes.

## Troubleshooting Matrix

| Symptom | Likely meaning | Action |
| --- | --- | --- |
| Immediate failure with stockout or resource-pool text | Selected zone cannot allocate requested resources | Retry later, reduce size, or choose another zone/region. |
| Repeated failure in same zone | Zone remains constrained for the requested shape | Plan alternate placement or open Support review. |
| Database remains `Pending` or `Provisioning error` | Provisioning did not complete or cleanly roll back | Stop self-service retries and escalate. |
| Delete button unavailable | Control-plane state is locked | Ask Support to clear state or delete the resource. |
| Billing continues while unusable | Resource/subscription still exists | Request deletion/cleanup through Support and track billing period. |

## Escalation Packet

Collect:

- Redis Cloud account or organization name
- subscription ID/name
- database ID/name and BDB ID if available
- cloud provider, region, and selected zone
- plan type and requested change
- current database lifecycle state
- full error message and failed task timestamp with timezone
- whether deletion is blocked
- whether the desired outcome is retry, resize, state clear, database deletion, or subscription deletion
- invoice or billing-period context if charges are disputed
