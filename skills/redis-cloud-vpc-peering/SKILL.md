---
name: redis-cloud-vpc-peering
description: "Configure and troubleshoot Redis Cloud Pro VPC peering for AWS and Google Cloud. Use when the user asks to peer an application VPC with Redis Cloud, approve AWS or GCP peering, update route tables, switch to Redis Cloud private endpoints, fix CIDR overlap, add CIDR allowlists, or troubleshoot traffic still using public endpoints after peering."
---

# Redis Cloud VPC Peering

Use this skill for Redis Cloud Pro private connectivity through AWS or Google Cloud VPC peering.

## Current-State Rule

Cloud provider console flows, IAM permissions, peering quotas, route behavior, and Redis Cloud UI labels can change. Verify live Redis Cloud and provider documentation or console state before giving current setup details as definitive.

## Preflight

1. Confirm Redis Cloud Pro subscription. VPC peering is not an Essentials feature.
2. Identify provider: AWS or Google Cloud.
3. Collect application VPC details:
   - Account/project.
   - Region.
   - VPC/network ID or name.
   - CIDR ranges.
   - Route tables/subnets used by the application.
4. Confirm CIDR ranges do not overlap with Redis Cloud VPC CIDRs.
5. Confirm whether database IP access control/allowlists are enabled.

## AWS Workflow

1. In Redis Cloud:
   - Open Subscriptions, Connectivity, VPC Peering.
   - Add peering.
   - Enter consumer AWS account, region, VPC ID, and VPC CIDRs.
   - Initiate peering and save the Peering ID.
2. In AWS:
   - Locate the incoming VPC peering request.
   - Accept it.
3. Update AWS route tables:
   - Add route from application subnet route tables to the Redis Cloud VPC CIDR.
   - Target the peering connection ID.
4. In Redis Cloud:
   - Complete any remaining peering status steps.
   - Find the database private endpoint.
5. Update application connection strings to use the private endpoint.
6. If IP allowlists are enabled, add the peered VPC CIDRs under IP Access Control.

## Google Cloud Workflow

1. In Redis Cloud:
   - Open Subscriptions, Connectivity, VPC Peering.
   - Add peering.
   - Enter Google Cloud project ID and network name.
   - Copy the generated `gcloud` command.
   - Initiate peering and save the Cloud Peering ID.
2. In Google Cloud:
   - Run the generated `gcloud` command with an identity that has required networking permissions.
3. In Redis Cloud:
   - Confirm peering status.
   - Find the database private endpoint.
4. Update application connection strings to use the private endpoint.
5. If IP allowlists are enabled, add the GCP VPC CIDRs under IP Access Control.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Peering request fails | CIDR overlap, wrong account/project, wrong region/network, or missing permissions. |
| AWS traffic does not route privately | Application subnet route table has route to Redis Cloud CIDR targeting the peering connection. |
| GCP traffic does not route privately | Generated peering command completed and routes are active for the selected VPC network. |
| App still uses public path | Connection string still points at public endpoint; switch to private endpoint. |
| Connection blocked after peering | Database IP allowlist does not include peered VPC CIDRs. |
| Multiple peerings fail | Each peered VPC must use unique non-overlapping CIDR ranges. |
| Public access remains open | Peering does not disable public access; restrict access with database allowlists/security settings. |

## Safety Checks

- Do not assume peering disables public access.
- Do not change route tables without confirming affected subnets and rollback.
- Do not recommend CIDR changes without checking existing network dependencies.
- Treat provider account/project IDs and network details as sensitive operational information.

## Escalation Packet

Collect:

- Redis Cloud subscription and database.
- Provider, account/project, region, VPC/network ID.
- Application VPC CIDRs and Redis Cloud VPC CIDRs.
- Peering ID or Cloud Peering ID.
- Route table or GCP routing state.
- Private endpoint being used by the app.
- IP allowlist entries.
- Exact error message and timestamp.
