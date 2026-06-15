---
name: redis-software-onboarding-sequence
description: Use when guiding a Redis Software onboarding or first production deployment, including architecture orientation, infrastructure requirements, installation, cluster naming, DNS setup, cluster deployment, security hardening, database creation, connection setup, and data migration planning.
---

# Redis Software Onboarding Sequence

Use this skill to guide a Redis Software deployment from planning through a usable production-ready database. Keep the user in the correct order so later steps do not hide earlier infrastructure or DNS mistakes.

## Onboarding Order

1. Explain the core model: nodes, cluster, databases, endpoints, shards, proxies, replication, and management plane.
2. Confirm system and infrastructure requirements:
   - supported OS and package prerequisites
   - CPU, memory, disk, network, DNS, time sync, and firewall readiness
   - persistence and backup storage design
3. Install Redis Software using the supported path for the target environment.
4. Choose a cluster name that works with licensing, DNS naming, and operational conventions.
5. Configure DNS for stable cluster and database endpoint access.
6. Deploy and initialize the cluster.
7. Apply security controls before production use:
   - TLS and certificates
   - users, roles, and ACLs
   - LDAP or identity integration if required
   - audit logging and access restrictions
8. Create the first database with memory, shard, replication, persistence, TLS, and clustering choices.
9. Connect with supported clients and verify endpoint behavior.
10. Plan data migration using snapshot import/export, ReplicaOf, RIOT-style tooling, or another supported approach.

## Intake Checklist

Ask for:

- environment: bare metal, VM, cloud VM, Kubernetes, or lab
- Redis Software version target
- node count and failure-domain layout
- DNS ownership and naming convention
- network/firewall constraints
- security requirements
- first database workload profile
- migration source, data size, downtime tolerance, and rollback requirements

## Readiness Checks

Before declaring onboarding complete, verify:

- all nodes are healthy
- cluster name and DNS resolve correctly
- management UI and API are reachable only from intended networks
- database endpoint is stable and reachable
- TLS and authentication work with a real client
- backups or persistence are configured according to recovery requirements
- monitoring, logging, and alerting are enabled
- migration or load test has been validated

## Response Pattern

When helping a user:

1. Identify their current onboarding step.
2. State the next blocking decision.
3. Provide the checks or commands for that step.
4. Do not skip DNS, security, or backup planning just to create a database faster.
