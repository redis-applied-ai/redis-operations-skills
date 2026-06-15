---
name: redis-cloud-support-router
description: "Route Redis Cloud support questions to the right workflow area: REST API, onboarding, marketplace billing, observability, account access, database management, security, backups, VPC peering, scaling, Search, imports, connection limits, and deletion/cancellation. Use when the user asks a broad Redis Cloud question or the exact topic is ambiguous and needs triage before applying a more specific Redis Cloud skill."
---

# Redis Cloud Support Router

Use this skill when a Redis Cloud request is broad, ambiguous, or spans multiple product areas. It is a routing skill, not a detailed runbook.

## First Classification

Ask or infer:

- Plan: Essentials, Pro, Flex, Active-Active, marketplace, free/trial.
- Task type: setup, troubleshoot, billing, security, migration, monitoring, database operations, or account access.
- Interface: Console, REST API, Terraform, marketplace, Redis CLI, Redis Insight, or application client.
- Urgency: production incident, planned change, or informational.

## Topic Routing

| User intent | Route to |
| --- | --- |
| Create account, choose plan, create first database | Redis Cloud onboarding, subscription, and first-database skills. |
| Connect app, redis-cli, Redis Insight | Redis Cloud connection and Redis Insight connection skills. |
| REST API, automation, 429 errors | Redis Cloud REST API and automation rate-limit skills. |
| Billing, invoices, cancellations, deletion | Billing, cancellation, account deletion, and payment skills. |
| AWS/GCP Marketplace mapping or billing | Marketplace connection/disconnection and GCP billing path selector skills. |
| Team users, RBAC, account access | Team access, RBAC, account restore, and credential rotation skills. |
| TLS, ACLs, IP allow lists, private networking | Security, VPC peering, PSC, and access-control skills. |
| Monitoring, alerts, backups | Redis Cloud monitoring, alerts, backup, Prometheus/Grafana/Datadog skills. |
| High memory/network/throughput or resizing | Performance, sizing, right-sizing, network load, and scaling skills. |
| Imports, migrations, large datasets | Data migration/import skills. |
| Search, indexing, faceted search | Redis Search and indexing skills. |
| Free/trial inactivity deletion | Inactivity deletion prevention and free-database recovery skills. |

## Triage Questions

Use only the necessary questions:

1. Which Redis Cloud plan and subscription type is involved?
2. What is the database ID/name and region/provider?
3. What exact error or behavior is visible?
4. Which interface produced it: Console, API, Terraform, marketplace, Redis client, or Redis Insight?
5. Was there a recent change: deploy, resize, import, billing update, credential rotation, maintenance, or network change?

## Safety Rules

- Do not recommend destructive actions such as database deletion, account deletion, subscription cancellation, index deletion with `DD`, or marketplace unsubscribe without using the specific safety-focused skill.
- Do not quote current pricing, support windows, exact plan limits, or provider capability availability without live verification.
- For marketplace billing, classify contract type before giving steps.
- For production incidents, collect IDs, timestamps, exact errors, and evidence before proposing irreversible changes.

## Response Pattern

1. State the likely category.
2. Ask only missing classification details.
3. Route to the most specific skill/workflow.
4. If no specific workflow exists, provide a minimal diagnostic checklist and collect escalation evidence.

## Escalation Packet

Collect:

- Account, subscription, and database identifiers.
- Plan type and provider/region.
- Interface used.
- Error text and timestamp.
- Recent changes.
- Screenshots or command/API output with secrets removed.
