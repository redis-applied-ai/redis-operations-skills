---
name: redis-cloud-essentials-pro-upgrade-decision
description: Use when deciding whether a Redis Cloud Essentials database should move to Redis Cloud Pro, especially for bandwidth warnings, throughput caps, connection limits, private networking needs, per-database observability, Active-Active requirements, billing changes, endpoint changes, or Essentials-to-Pro migration planning.
---

# Redis Cloud Essentials To Pro Decision

Use this skill to help a user decide whether Redis Cloud Essentials is still sufficient or whether Redis Cloud Pro is the right operating model. Verify current Redis Cloud plan capabilities and pricing before making definitive commitments.

## Stay On Essentials When

Essentials is usually still appropriate when:

- workload demand is predictable and remains comfortably under plan limits
- bandwidth usage is well below quota during normal and peak periods
- latency stays stable during expected traffic
- public endpoints with TLS and CIDR allowlists satisfy security requirements
- private networking is not required
- one database per subscription fits the environment
- subscription-level usage metrics are enough for operations
- the workload is development, staging, or small production with stable traffic

Avoid recommending Pro just because a single warning appeared. First determine whether the limit pressure is occasional or structural.

## Upgrade Signals

Evaluate Redis Cloud Pro when the user consistently sees:

- bandwidth warnings near quota or sustained high monthly transfer
- throughput close to the configured plan cap
- throttling, timeouts, or latency spikes during normal business peaks
- `ERR max number of clients reached`, "too many connections", or similar connection pressure
- one workload consuming shared subscription capacity and affecting another workload
- requirements for VPC peering, PrivateLink, Private Service Connect, Transit Gateway, or private-only access
- compliance or isolation requirements that shared public-endpoint infrastructure cannot satisfy
- need for per-database metrics, monitoring integrations, or deeper workload attribution
- Active-Active geo-distribution requirements

## Migration Facts To Preserve

When recommending a move from Essentials to Pro:

1. Treat it as a migration to a new Pro database, not an in-place plan conversion.
2. Expect the endpoint to change unless a supported endpoint-redirection approach is intentionally used and validated.
3. Require application cutover planning.
4. Confirm the new Pro database is sized for memory, throughput, persistence, replication, and networking requirements.
5. Explain that downgrading back to Essentials also requires a new database and migration.
6. Confirm billing model and cost impact from current Redis Cloud pricing or account data.

## Migration Approach

Choose the migration path based on downtime tolerance:

- Active-Passive sync for low-downtime migration when supported by the source and target configuration.
- Backup and restore when downtime is acceptable and compatibility is verified.
- Client-side migration tools when application-specific control is needed.

Before cutover, validate:

- data count and representative key samples
- TTL preservation where relevant
- module and command compatibility
- connection strings, TLS, ACL users, and network allowlists
- application retry and reconnect behavior
- monitoring and alerting on the new database

## Response Pattern

When advising a user:

1. State whether their symptoms are temporary, sustained, or still unknown.
2. Map each symptom to a concrete Essentials limit or Pro capability.
3. Recommend stay, monitor, or migrate.
4. If migrating, outline the new-database, data-migration, cutover, and decommission sequence.
5. Call out endpoint and billing changes explicitly.
