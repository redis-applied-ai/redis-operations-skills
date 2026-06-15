---
name: redis-software-support-router
description: Use when a user asks a broad Redis Software or Redis Enterprise Software question and you need to route between installation, onboarding, DNS, database creation, connection setup, migration, firewalld, TLS, certificates, logging, auditing, Prometheus, Datadog, resiliency testing, support packages, node maintenance, upgrades, endpoint flapping, CRDB, split brain, hot keys, recovery, licensing, host and port discovery, OSS Cluster API, or Redis Open Source migration topics.
---

# Redis Software Support Router

Use this skill to classify Redis Software questions and choose the right operating or troubleshooting workflow. It is a router: gather enough context, identify the track, and then use the specific runbook or product documentation for the detailed procedure.

## Classify The Request

Route into one of these tracks:

- Onboarding: system requirements, installation, cluster naming, DNS, cluster deployment, security, first database, and connection setup.
- Operations: firewalls, IPv6, node maintenance, OS patching, socket or persistence location changes, UI session timeout, cluster licensing.
- Database management: database creation, host and port discovery, imports, replica-of, scaling, shards, and OSS Cluster API.
- Security: TLS failures, certificate expiration, credential rotation, ACLs, RESP compatibility, audit logs.
- Observability: Prometheus, Datadog, Redis Insight, logging, support packages, metrics UI, and cluster health analysis.
- Performance: hot keys, slow commands, DEL/UNLINK latency, memory pressure, endpoint flapping, distributed-system symptoms.
- Recovery: AOF recovery after `FLUSHDB`, cluster recovery, database recovery, split brain, node unreachable, active-change-pending states.
- CRDB and Active-Active: sync stalls, resize, credential issues, multi-key command limits, delete latency.
- Upgrade and mixed versions: Redis Software upgrades, mixed 7.x/8.x client behavior, Search command changes.
- Redis OSS: safe key deletion, OSS Cluster compatibility, migration into Redis Software.

## Intake Checklist

Ask for:

- Redis Software version
- deployment type: bare metal, VM, cloud VM, Kubernetes, or OpenShift
- cluster size, node health, and database count
- exact symptom, command, error text, or UI state
- recent changes: upgrade, patching, resharding, DNS, certificate rotation, firewall, node maintenance, migration
- support package availability
- whether the requested action is diagnostic, operational, recovery, or destructive

## Safety Rules

- Do not recommend deleting data, dropping indexes, recreating clusters, restarting all nodes, or force-removing nodes without explicit confirmation.
- Capture state before recovery actions: `rladmin status`, issues, relevant logs, events, and support package when possible.
- For cluster and database recovery, prefer version-specific official guidance or Redis Support when data consistency is at risk.
- For firewall, DNS, TLS, and certificate changes, identify the exact node, endpoint, and certificate chain before editing configuration.

## First Diagnostic Commands

Use the commands that fit the selected track:

```text
rladmin status
rladmin status issues_only
rladmin status shards
rladmin status database
```

For Redis-level issues, also consider:

```text
INFO
SLOWLOG GET 128
CLIENT LIST
```

## Response Pattern

When answering:

1. Name the selected Redis Software track.
2. Ask for the smallest missing context needed to proceed.
3. Provide safe read-only diagnostics first.
4. Call out destructive or high-risk boundaries explicitly.
5. Route to the specific runbook or procedure once deployment, version, and symptom are clear.
