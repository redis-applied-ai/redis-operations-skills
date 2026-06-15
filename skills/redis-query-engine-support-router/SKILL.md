---
name: redis-query-engine-support-router
description: Use when a user asks broad Redis Query Engine or Redis Search troubleshooting questions and you need to route between query latency, throughput, worker utilization, coordinator-to-shard costs, Query Performance Factor, FT.EXPLAIN, FT.PROFILE, Redis 8 Search deprecations, timeout behavior, multi-shard filter breadth, MAXPREFIXEXPANSIONS, index design, or post-upgrade health validation.
---

# Redis Query Engine Support Router

Use this skill to classify Redis Query Engine questions and route to the right analysis path. Start from observed query behavior and topology, then choose profiling, index design, throughput, latency, or upgrade-compatibility guidance.

## Classify The Issue

Route to one of these tracks:

- Latency: slow `FT.SEARCH`, `FT.AGGREGATE`, vector, hybrid, or full-text queries.
- Throughput: low QPS, saturated workers, client-side bottlenecks, or scaling after resharding.
- Query plan: confusing `FT.EXPLAIN`, broad filters, prefix expansion, or poor index selectivity.
- Profiling: `FT.PROFILE` analysis, slowlog evidence, or support package metrics.
- Multi-shard behavior: coordinator-to-shard network costs, fan-out, broad filters, or uneven shard load.
- Upgrade compatibility: Redis 8 Search command deprecations, parsing changes, timeout behavior, or post-upgrade validation.
- Maintenance: validating health after configuration changes, resharding, upgrades, or capacity changes.

## Evidence To Gather

Ask for:

- Redis product and version
- index schema and document type: HASH or JSON
- exact query and expected result count
- query latency percentiles and QPS
- shard count, cluster topology, and recent resharding
- `FT.EXPLAIN` output for query-shape issues
- `FT.PROFILE` output for runtime analysis
- slowlog entries and client-side timing
- worker, CPU, memory, network, and coordinator metrics when available

## Analysis Order

1. Confirm the issue is server-side, client-side, or network/coordinator-side.
2. Check query selectivity and whether filters narrow work early enough.
3. Inspect the index schema for missing fields, nonselective tags, broad text predicates, or unnecessary sortable fields.
4. Use `FT.EXPLAIN` to reason about query structure.
5. Use `FT.PROFILE` to inspect actual runtime costs.
6. Compare latency and QPS before and after resharding, upgrade, or configuration changes.

## Common Routes

- Broad multi-shard filters: narrow by tenant, tag, numeric range, or other selective fields.
- Prefix expansion pressure: tune query shape before relying on expansion limits alone.
- Low throughput after scaling: inspect Query Performance Factor, worker utilization, shard balance, and client concurrency.
- Upgrade errors: check Redis 8 deprecated commands and stricter parsing first.
- Ranking or result-order changes: compare scoring behavior and application thresholds.
- Timeouts: distinguish query complexity, server timeout behavior, client timeout, and network timeout.

## Response Pattern

When answering:

1. Identify the selected RQE track.
2. Request or provide the minimum diagnostic command set.
3. Interpret query shape before recommending capacity changes.
4. Offer one schema/query change and one measurement to validate it.
5. Escalate to support-package collection when metrics or profiles show internal engine saturation.
