---
name: redis-cloud-platform-orientation
description: "Explain Redis Cloud architecture, plan differences, connectivity, access control, monitoring, and onboarding sequence. Use when the user asks what Redis Cloud is, how Essentials, Flexible, and Pro differ, how Redis Cloud databases are isolated, which connectivity model applies, or what to do first when starting Redis Cloud."
---

# Redis Cloud Platform Orientation

Use this skill to orient a user or agent before choosing a Redis Cloud subscription, creating a database, or troubleshooting plan-specific behavior.

## Core Model

Redis Cloud is a managed Redis service. The customer chooses a plan, cloud provider, region, database size, throughput, and security settings; Redis operates the underlying infrastructure, patching, availability mechanisms, backups, and maintenance workflow according to the selected plan.

## Plan Boundaries

| Plan | Isolation and infrastructure | Typical fit | Important limits |
| --- | --- | --- | --- |
| Essentials | Shared infrastructure with logical database isolation | Simple entry-level workloads and trials | No high availability or persistence. |
| Flexible | Shared multi-tenant infrastructure with configurable scale and high availability options | Production workloads that do not need private VPC isolation | Public endpoint model; advanced networking is limited. |
| Pro | Dedicated customer VPC/network resources | Production workloads needing private networking, stronger isolation, or advanced support | More setup decisions: region, CIDR, peering, and private connectivity. |

## Component Map

| Component | What to explain |
| --- | --- |
| Database | Logical Redis database with its own endpoint, password/ACLs, memory, throughput, persistence, and replication settings. |
| Subscription | Billing and plan container for one or more databases, depending on plan type. |
| Endpoint | Host and port used by clients, Redis Insight, or `redis-cli`; TLS is normally represented by `rediss://`. |
| Provider and region | Cloud and geography selected for latency, compliance, and cost reasons. |
| Access management | Console users use roles such as Owner, Manager, Member, and Viewer; database access is controlled separately through credentials, ACLs, and network allow lists. |
| Networking | Public access is common for Essentials/Flexible; Pro supports private networking such as VPC peering where available. |

## Guidance Workflow

1. Identify whether the user needs orientation, plan selection, initial setup, or troubleshooting.
2. Ask for workload requirements: expected size, throughput, availability, persistence, public/private networking, cloud provider, region, and compliance constraints.
3. Map those requirements to plan boundaries before giving setup instructions.
4. For first-time setup, route the user through this sequence:
   - Create or confirm the Redis Cloud account.
   - Choose the subscription plan.
   - Create the first database in the desired provider and region.
   - Configure access control and allowed source networks.
   - Connect with `redis-cli`, Redis Insight, or an application client.
   - Add monitoring, alerts, backups, and maintenance preferences if the plan supports them.
5. If the user asks for exact current pricing or plan availability, verify against live Redis Cloud pricing or console information before giving a definitive answer.

## Connection Baseline

Use this form when explaining client connectivity:

```bash
redis-cli -u rediss://default:<password>@<host>:<port>
```

Do not imply that application access and console user roles are the same thing. Console roles control portal operations; database credentials, ACLs, TLS, and network rules control data-plane access.

## Common Clarifications

- Essentials and Flexible databases are logically isolated but do not provide dedicated customer VPC infrastructure.
- Pro is the plan to evaluate when the user needs private VPC networking or dedicated network isolation.
- Backups, persistence, high availability, maintenance windows, and alerting are plan-dependent.
- The endpoint type and network path matter as much as the Redis command syntax when debugging connection failures.
