---
name: redis-crdb-tombstone-memory
description: Use when Redis Software Active-Active CRDB shows high memory after deletes or expirations, few live keys but high `used_memory`, tombstone buildup, CRDT garbage collection lag, replication lag delaying tombstone cleanup, synchronized TTL expiration spikes, delete churn, `INFO CRDT` metrics such as `crdt_gc_attempted` or `crdt_gc_collected`, or memory pressure from CRDB tombstones.
---

# Redis CRDB Tombstone Memory

Use this skill when Active-Active CRDB memory remains high after deletes, expirations, or key lifecycle churn.

## Core Model

Active-Active CRDB uses tombstones so deleted keys are not resurrected by out-of-order replication. Tombstones are normal correctness metadata, but they consume memory until all participating regions observe the delete and background garbage collection removes the tombstone.

High tombstone memory is most likely when:

- large delete jobs recently ran
- many keys expired at the same time
- keys are repeatedly deleted and recreated
- a region was lagging, disconnected, or recently reconnected
- replication backlog or synchronization pressure delayed cleanup

## Detection Workflow

1. Check memory and fragmentation:

   ```redis
   INFO memory
   MEMORY STATS
   ```

2. Rule out live large keys:

   ```bash
   redis-cli --bigkeys
   redis-cli --memkeys
   ```

3. Check CRDB replication health in every participating region:
   - link status
   - replication lag
   - backlog growth
   - disconnected or stale replicas

4. Inspect CRDT metrics on representative shards:

   ```redis
   INFO CRDT
   ```

   Look for garbage-collection counters such as `crdt_gc_attempted` and `crdt_gc_collected`, and compare expired/deleted activity with remaining key count.

5. Correlate the memory rise with delete jobs, expiration waves, deployments, or regional network incidents.

## Interpretation

| Observation | Meaning | Action |
| --- | --- | --- |
| No large live keys, high `used_memory`, recent deletes | Tombstones are plausible. | Check CRDT GC and replication health. |
| Tombstone GC counters increase over time | Cleanup is progressing. | Wait while monitoring memory and lag. |
| GC counters do not move | GC may be stalled or blocked by replication/topology state. | Inspect region health and escalate if stable conditions do not improve. |
| Memory spikes at the same time as TTL expiry | Expiration wave created tombstones in bulk. | Add TTL jitter and stagger lifecycle jobs. |
| Memory remains high after a region reconnects | Lagging region delayed tombstone cleanup. | Wait for full synchronization, then verify GC progress. |

## Mitigation Patterns

- Fix replication health first; tombstones cannot safely clear while regions have not observed deletes.
- Reduce delete/recreate churn. Prefer updating existing values where the data model allows it.
- Add TTL jitter instead of assigning identical expiration times to many keys.
- Batch and throttle cleanup jobs during lower-traffic windows.
- Maintain memory headroom for transient tombstone growth.
- Tune tombstone retention only with version-aware guidance and a clear understanding of replication latency and topology.

## What Not To Do

- Do not assume `DBSIZE` or absence of big keys proves memory is leaked.
- Do not flush or mass-delete as a first response; that can create more tombstone work and is destructive.
- Do not reduce retention windows blindly in a multi-region topology.
- Do not evaluate only one region; every participating region affects cleanup.

## Escalation Packet

Collect:

- Redis Software version and CRDB topology.
- Regions, participating clusters, and recent disconnects.
- `INFO memory`, `MEMORY STATS`, and `INFO CRDT` from representative shards.
- Delete, expiration, and write rates during the spike.
- Replication lag and link status for every region.
- Big-key scan results showing live key contribution.
- Timeline of delete jobs, deployments, region outages, or resyncs.
