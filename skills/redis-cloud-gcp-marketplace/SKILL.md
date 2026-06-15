---
name: redis-cloud-gcp-marketplace
description: "Connect, verify, manage, and troubleshoot Redis Cloud billing through Google Cloud Marketplace. Use when the user asks to map Redis Cloud to GCP Marketplace, subscribe from Google Cloud, use Manage on Provider, verify On-Demand versus Private Offer status, add multiple Redis Cloud accounts to one GCP Billing Account, fix IAM role errors, resolve Pending/In Progress marketplace mapping, move to a new GCP Billing Account, or safely unmap/disconnect GCP Marketplace billing."
---

# Redis Cloud GCP Marketplace

Use this skill for Redis Cloud account mapping and billing through Google Cloud Marketplace. For private-offer acceptance details, use the private-offer workflow as the narrower path when appropriate.

## Current-State Rule

GCP Marketplace listings, IAM roles, trial terms, iSaaS/3PIC behavior, multi-account support, and UI labels can change. Verify live GCP and Redis Cloud state before presenting current commercial or provider behavior as definitive.

## Safety Rules

- Unsubscribing or unmapping can delete or suspend resources. Require backup and explicit confirmation before destructive billing changes.
- Confirm the exact Redis Cloud account and GCP Billing Account before mapping.
- Only Redis Cloud Account Owners can map accounts.
- Do not ask users to share credentials or payment-card details.

## Mapping Workflow

1. Confirm prerequisites:
   - GCP Billing Account selected.
   - User has `roles/billing.admin`, or `roles/billing.user` plus `roles/consumerprocurement.orderAdmin`.
   - User is Redis Cloud Account Owner.
2. Subscribe in GCP Marketplace:
   - Open Google Cloud Marketplace.
   - Find the Redis Cloud listing or private-offer URL.
   - Subscribe, choose Billing Account, accept terms, and choose the Redis sign-up/provider path.
3. Connect Redis Cloud:
   - Redirect to Redis Cloud.
   - Select the correct Redis Cloud account.
   - Connect account.
   - Confirm Redis Cloud shows GCP Marketplace as payment method.
4. Verify from both sides:
   - Redis Cloud Billing & Payments shows GCP Marketplace.
   - GCP Marketplace subscription shows Manage on Provider.
   - Confirm order status and whether billing is On-Demand or Private Offer.

## Account Management

- To add more Redis Cloud accounts, use Redis Cloud Billing & Payments, Payment Methods, Add Marketplace account.
- A GCP Billing Account may pay for multiple Redis Cloud accounts when supported by the current listing/contract.
- At least one Redis account may need to remain mapped for an active contract.
- To move to a new GCP Billing Account, plan a controlled sequence: switch to card or alternate payment, unsubscribe old GCP Marketplace mapping, then resubscribe/map with the new Billing Account.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Redis account not listed | Account already tied to another marketplace/contract or POC state; disconnect old mapping or contact Support. |
| Redis account greyed out | User is not Account Owner. |
| IAM role error | Missing required GCP billing/procurement roles. |
| Mapping stuck Pending | Existing subscriptions still on old payment method or backend sync delay. |
| Manage on Provider missing | Wrong GCP project or Billing Account selected. |
| Subscription In Progress too long | Marketplace sync issue; escalate if it does not resolve. |
| Multiple account mapping fails | Use Add Marketplace Account in Redis Cloud, not the initial subscription flow. |
| Private offer accepted but Redis UI still says On-Demand | Validate contract in GCP; Redis UI label may not reflect private-offer status. |
| Last account unmapping needed | Unsubscribe directly in GCP and warn about deletion/suspension risk. |
| 3PIC resources deleted after unsubscribe | Grace period may have expired; backups are required for recovery. |

## Escalation Packet

Collect:

- GCP Billing Account and project.
- Marketplace subscription/order status.
- Redis Cloud account ID/name.
- Contract type if known: On-Demand, Private Offer, iSaaS, or 3PIC.
- Whether Manage on Provider appears.
- Redis Cloud payment method state.
- Exact IAM or mapping error.
- Whether any accounts are already mapped to another marketplace or contract.
