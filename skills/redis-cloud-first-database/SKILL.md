---
name: redis-cloud-first-database
description: "Help a user choose a Redis Cloud subscription tier and create their first Redis Cloud database. Use when the user asks about Essentials, Flex, or Pro, selecting cloud provider or region, Redis Cloud onboarding, creating a first database, Redis Stack or Redis 8 feature availability during creation, one-database limits, plan upgrades/downgrades, Flex availability, or database creation stuck in pending state."
---

# Redis Cloud First Database

Use this skill for Redis Cloud onboarding from subscription choice through first database creation and initial connection handoff.

## Current-State Rule

Redis Cloud plans, pricing, regions, versions, and feature availability can change. Before giving current limits, prices, support windows, or provider availability as fact, verify live Redis Cloud documentation or the user's console/API.

## Subscription Selection Workflow

1. Gather requirements:
   - Workload purpose: prototype, small production, large dataset, compliance, global deployment.
   - Memory size and expected growth.
   - Throughput and connection count.
   - Availability: single-zone, multi-AZ, multi-region, Active-Active.
   - Networking: public endpoint, VPC peering, private connectivity, dedicated VPC.
   - Billing path: direct Redis Cloud or marketplace.
2. Map to a likely tier:
   - Essentials: simple single-database workloads, prototypes, small apps.
   - Flex: larger single-database workloads that can use RAM plus SSD and do not need full Pro features.
   - Pro: dedicated infrastructure, multiple databases, high throughput, clustering, Active-Active, VPC peering, compliance, or advanced networking.
3. Verify live plan constraints before final recommendation.
4. Explain fixed choices:
   - Subscription cloud provider and region are chosen at subscription creation.
   - Databases in the subscription use that location.
   - Availability zone details may not always be exposed after provisioning.

## First Database Creation Workflow

1. Sign in to Redis Cloud or create an account.
2. Create a subscription:
   - Choose subscription type.
   - Select cloud provider and region.
   - Name the subscription.
   - Choose tier/size and availability options.
   - Add payment method if required.
3. Create the database after the subscription is active:
   - Name the database.
   - Select Redis version.
   - Choose memory size.
   - Choose TLS and persistence settings.
   - Create and wait for Active status.
4. Handoff:
   - Open database details.
   - Copy endpoint and credentials.
   - Connect with `redis-cli`, Redis Insight, or a client SDK.
   - Configure monitoring and alerts.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Cannot create more Essentials databases | Verify current one-database-per-subscription behavior and consider another subscription or Pro. |
| Upgrade or downgrade blocked | Check unpaid invoices, payment method, and whether current usage fits target tier. |
| Flex does not appear | Verify current Flex provider/region availability in live docs or console. |
| Redis version/module confusion | Verify current Redis Cloud creation flow; Redis 8+ may include Stack capabilities by default. |
| Database creation stuck | Confirm subscription is active, capacity is available, and no billing/payment block exists. |
| Need availability zone details | Check console first; if not shown, escalate with subscription ID, DB ID, provider, region, and business reason. |

## Safety Checks

- Do not state current pricing, regions, provider availability, or feature limits from memory.
- Do not recommend a plan without asking about size, availability, networking, and compliance needs.
- Do not assume module selection is available in current database creation; verify by version and console behavior.

## Escalation Packet

Collect:

- Account and subscription ID/name.
- Intended cloud provider and region.
- Plan/tier being selected.
- Database size, TLS, persistence, and availability settings.
- Current status or error message.
- Billing/payment status if creation or plan change is blocked.
