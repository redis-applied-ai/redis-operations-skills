---
name: redis-open-source-support-router
description: Use when a user asks broad Redis Open Source or OSS Cluster questions and you need to route between safe key deletion, OSS Cluster API configuration, cluster performance troubleshooting, FT.SEARCH compatibility with Redis Software or Redis Cloud OSS Cluster API, migration from Redis Open Source to Redis Software, or upgrade troubleshooting.
---

# Redis Open Source Support Router

Use this skill to classify Redis Open Source questions and route to the right runbook or design workflow. Verify current Redis Open Source, Redis Software, and Redis Cloud compatibility before making version- or feature-specific claims.

## Classify The Request

Route the user into one of these tracks:

- Data handling: remove keys safely, bulk deletion, TTL cleanup, large-key handling.
- OSS Cluster operations: cluster slots, node health, resharding, redirects, and client compatibility.
- OSS Cluster API in managed products: command support, Search compatibility, and endpoint behavior.
- Performance: hot keys, slow commands, high CPU, high memory, network saturation, latency spikes.
- Migration: Redis Open Source to Redis Software, Redis Cloud, or another managed Redis deployment.
- Upgrade troubleshooting: client compatibility, command behavior, persistence, modules, and cluster topology changes.

## Intake Checklist

Ask for:

- Redis version and deployment type
- standalone, Sentinel, OSS Cluster, Redis Software, Redis Cloud, or Kubernetes
- client library and cluster-mode support
- exact command, error, or symptom
- key count, memory usage, largest keys, and TTL behavior
- cluster node count, shard count, and slot distribution when relevant
- persistence, replication, and backup state before destructive actions

## Safety Rules

- Do not recommend `FLUSHALL`, `FLUSHDB`, broad `DEL`, or destructive cluster changes without explicit confirmation.
- Prefer incremental deletion and `UNLINK` for large key removal.
- Confirm backups or acceptable data-loss scope before migration, resharding, or mass deletion.
- For cluster operations, confirm client redirect handling and slot coverage before changing topology.

## Routing Guidance

- For removing all keys in an OSS Cluster, use a cluster-aware deletion workflow and confirm the target namespace or database.
- For Search command compatibility, distinguish Redis Open Source, Redis Stack, Redis Software, Redis Cloud, and OSS Cluster API behavior.
- For migration to Redis Software, inspect data size, downtime tolerance, module usage, persistence format, ACLs, and endpoint cutover.
- For performance issues, begin with `SLOWLOG`, `INFO`, latency monitoring, hot-key checks, and client connection behavior.

## Response Pattern

When answering:

1. Name the selected track.
2. State the first safe diagnostic commands.
3. Call out any destructive boundary and ask for confirmation if needed.
4. Route to the product-specific workflow once deployment type and version are known.
