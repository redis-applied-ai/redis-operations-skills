---
name: redis-cloud-network-transfer-billing
description: "Explain and investigate new Redis Cloud data-transfer, network, egress, or CSP pass-through charges. Use when a Redis Cloud bill, invoice, cost report, credit burn-down, or billing portal shows new network fees, separate network line items, faster credit consumption, cross-zone traffic cost, cross-region replication cost, VPC peering transfer cost, or data transfer charges after a billing model or contract change."
---

# Redis Cloud Network Transfer Billing

Use this skill when the billing question is specifically about Redis Cloud network, data-transfer, or egress charges. For broad billing triage, use `redis-cloud-billing-triage`; for traffic reduction after the charge is understood, use `redis-cloud-network-load-optimization`.

## Current-State Rule

Network pricing, contract handling, marketplace behavior, and credit application are financial/current-state facts. Verify the customer's invoice, Redis Cloud billing portal, contract terms, marketplace account, and current Redis/cloud-provider documentation before stating exact current pricing or eligibility.

## Explain The Charge

Network charges usually come from cloud-provider data movement that Redis Cloud surfaces or passes through, such as:

- application traffic crossing availability zones, regions, VPCs, accounts, or clouds before reaching Redis Cloud
- Active-Active, replication, migration, export, or import traffic across regions or providers
- private networking paths such as VPC peering that still cross billable provider boundaries
- large response payloads, scans, query result sets, or bulk jobs that increase outbound traffic

Do not promise that Redis can waive or reverse the fee. Treat refunds, credits, and invoice adjustments as billing-support decisions.

## Billing Model Triage

1. Identify how the account is billed:
   - Redis-direct Pro or annual contract
   - AWS Marketplace
   - GCP Marketplace
   - Azure-managed or other integrated marketplace path
   - Essentials or free tier
2. Confirm the contract or renewal date and whether network charges are billed separately or consumed from credits.
3. Compare invoice, cost report, and cloud marketplace bill:
   - Redis usage charges
   - network/data-transfer line items
   - credits consumed
   - discounts, taxes, marketplace fees, and provider-side charges
4. If the customer references the 2025 Redis-direct billing model change, verify their contract and invoice before applying that explanation. Older contracts and marketplace plans can behave differently.

## Topology Investigation

Map the traffic path before attributing the charge:

1. Record application cloud, region, zone, VPC/VNet, and account/project/subscription.
2. Record Redis Cloud subscription/database cloud, region, zone placement if available, and private networking configuration.
3. Identify cross-boundary paths:
   - cross-zone or cross-region application access
   - Active-Active or replica synchronization
   - VPC/VNet peering across regions or accounts
   - migration, backup, export, or analytics jobs
   - multi-cloud or internet egress paths
4. Validate with cloud-provider billing and metrics, filtering by region, zone, VPC/VNet, subnet, interface, load balancer/NAT, and service where possible.
5. Correlate provider data-transfer spikes with Redis Cloud metrics and application deploys, batch jobs, migrations, or failovers.

## Cost Reduction Guidance

Recommend changes only after confirming the workload path:

- co-locate application compute and Redis Cloud in the same cloud and region when practical
- prefer same-zone placement when supported and operationally appropriate
- reduce cross-region Active-Active, replication, or migration traffic to what the business requires
- avoid routing Redis traffic through NAT, load balancers, peering paths, or regions that add avoidable transfer cost
- reduce payload size, full-object reads, unbounded range queries, and bulk export/import traffic
- schedule or throttle large jobs to make the cost pattern predictable

Mention availability and resiliency tradeoffs when recommending same-zone placement or reducing cross-region traffic.

## Troubleshooting Patterns

| Symptom | Likely checks |
| --- | --- |
| New network charge appeared | Contract or renewal change, new topology path, migration/export job, or newly surfaced pass-through charge. |
| Credits burn down faster than expected | Network transfer is consuming credits or usage increased; compare credit ledger, invoice, and cost report. |
| Separate network invoice remains | Legacy contract, marketplace billing, taxes/fees, or provider-side charge behavior. |
| Sudden egress spike | Cross-region replication, migration, backup/export, application deploy, retry storm, or AZ/region mismatch. |
| Charge seems unrelated to Redis | Check provider billing dimensions, NAT/load balancer/interface metrics, and whether traffic crosses Redis Cloud networking attachments. |

## Escalation Packet

Collect:

- Redis Cloud account, subscription, database, and billing period
- billing path: Redis-direct, AWS Marketplace, GCP Marketplace, Azure-managed, or other integrated path
- contract start/renewal date and whether credits are prepaid or marketplace-based
- invoice/cost report rows showing network, data transfer, egress, or credit usage
- application and Redis Cloud cloud/region/zone/VPC topology
- Active-Active, replication, migration, backup, export, or peering details
- cloud-provider billing or network metric screenshots with sensitive details redacted
- recent changes in topology, workload, deployment, import/export, or failover behavior
