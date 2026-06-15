---
name: redis-software-resharding
description: Use when safely resharding a Redis Software database, increasing shard count, using REST revamp dry_run, validating multi-key hash tags, avoiding CROSSSLOT errors, checking large or hot keys, handling rack-aware reshard failures, monitoring shard balance, or explaining why shard count reduction requires new-database migration.
---

# Redis Software Resharding

Use this skill when increasing shard count for a Redis Software database. In-place resharding scales out; reducing shard count requires creating a new database with fewer shards and migrating data.

## Preflight Checklist

Before resharding, confirm:

- administrator access
- database ID and current shard count
- target shard count
- current backup exists and restore path is known
- maintenance window or low-traffic period
- monitoring for latency, throughput, memory, and shard balance
- CPU and memory headroom on all nodes
- no active change or stuck action is already running
- replication state is healthy
- rack awareness prerequisites are satisfied if enabled

For production, rehearse in staging when possible.

## Key And Workload Checks

Check multi-key command behavior:

```text
INFO COMMANDSTATS
```

For clustered databases, related keys used together by multi-key commands should share hash tags or follow the configured hashing policy.

Find large and hot keys:

```text
redis-cli -h <host> -p <port> --bigkeys
redis-cli -h <host> -p <port> --hotkeys
```

Very large or hot keys can slow migration, create shard imbalance, or cause latency spikes. Split or refactor them before resharding when feasible.

## Execution Paths

UI path:

- database configuration
- shard or reshard panel
- increase shard count
- apply change

REST API path:

Use a dry run before executing:

```text
PUT /v1/bdbs/<uid>/actions/revamp?dry_run=true
{"shards_count": <new_count>}
```

Execute after dry run succeeds:

```text
PUT /v1/bdbs/<uid>/actions/revamp
{"shards_count": <new_count>}
```

Track action progress:

```text
GET /v1/actions/<action_uid>
```

Use the cluster's approved authentication and TLS validation method; avoid disabling certificate checks in production automation.

## Rack Awareness

For rack-aware databases:

- confirm replication is enabled
- confirm primary and replica placement can satisfy rack or zone rules
- if resharding fails due to placement constraints, fix replication or placement first
- temporarily disabling rack awareness is a risk decision and should be planned, confirmed, and re-enabled after resharding

## Validation

After resharding:

```text
rladmin status extra all
rlcheck
```

Validate:

- shard count matches target
- shard balance is reasonable
- database is active
- latency and throughput return to baseline or improve
- memory usage is balanced
- no unexpected `CROSSSLOT` errors
- hot-key and big-key checks are acceptable

## Troubleshooting

- `CROSSSLOT`: add hash tags or adjust hashing policy for multi-key operations.
- Latency spikes: check large/hot keys, reduce traffic, and inspect migration progress.
- Shard imbalance: inspect key distribution and hash tag usage.
- Rack-aware failure: verify replication and rack/zone placement.
- Stuck or slow reshard: inspect logs under `/var/opt/redislabs/log/`, running actions, and node resources before restarting any service.

## Response Pattern

Answer with:

1. Whether the request is shard increase or shard reduction.
2. Preflight resource, backup, replication, and key-pattern checks.
3. Dry-run and execution path.
4. Monitoring and validation commands.
5. Troubleshooting path for rack awareness, hot keys, or stuck actions.
