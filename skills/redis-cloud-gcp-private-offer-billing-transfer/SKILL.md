---
name: redis-cloud-gcp-private-offer-billing-transfer
description: "Coordinate Redis Cloud Google Cloud Marketplace Private Offer billing transfer to a new GCP Billing Account. Use when the user asks to move Private Offer billing, transfer a Marketplace entitlement, confirm Redis Cloud stays mapped, troubleshoot missing Manage on provider, or avoid unsubscribing a Private Offer while changing payer."
---

# Redis Cloud GCP Private Offer Billing Transfer

Use this skill for Redis Cloud Google Cloud Marketplace Private Offers that need to move billing to a new Google Cloud Billing Account.

## Critical Rule

Do not unsubscribe a Redis Cloud Google Cloud Marketplace Private Offer to move billing. Private Offers move through a Cloud Marketplace entitlement transfer coordinated with Redis and Google.

## Preflight

1. Confirm the Marketplace order is a Private Offer in Google Cloud Marketplace.
2. Confirm access to both current and target Billing Accounts and the relevant project/order context.
3. Confirm Redis Cloud Account Owner access.
4. Identify the Redis Account Team, Deal Desk, or Support path for requesting the transfer.
5. Collect:
   - Current Marketplace order link or ID.
   - Target Billing Account ID.
   - Redis Cloud account name that must remain mapped.
   - Current project/account context.
6. Back up mission-critical databases and plan a low-risk verification window.

## Entitlement Transfer Workflow

1. Contact the Redis Account Team or open a Support case requesting a Google Cloud Marketplace Private Offer entitlement transfer.
2. Provide the order ID/link, target Billing Account ID, and Redis Cloud account name.
3. Wait for Redis and Google coordination. Do not attempt a PAYG-style unsubscribe/resubscribe flow.
4. After transfer, check the Google Cloud Marketplace order under the target Billing Account.
5. Use `Manage on provider` to confirm it opens the expected Redis Cloud account.
6. In Redis Cloud, verify impacted subscriptions still show Google Cloud Marketplace as the payment method.

## Verification

In Google Cloud:

- Order status is active.
- Order is associated with the target Billing Account.
- `Manage on provider` is available and opens the expected Redis Cloud account.

In Redis Cloud:

- Payment method remains Google Cloud Marketplace.
- Intended subscriptions remain mapped to the expected account.
- No unexpected switch to credit card billing occurred.
- Databases remain accessible.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Transfer not taking effect | Entitlement transfer not initiated or still pending | Ask Redis Account Team/Support for transfer status with Google. |
| Someone proposes unsubscribing | PAYG flow confused with Private Offer flow | Stop and use entitlement transfer. |
| `Manage on provider` missing | Wrong GCP project, billing account, or order context | Switch context and reopen the Marketplace order. |
| Redis Cloud shows credit card | Mapping/payment state inconsistent | Capture screenshots and escalate to Redis Support. |
| Multiple Redis Cloud accounts exist | Wrong account may be connected | Confirm the expected account name before and after transfer. |

## Escalation Packet

Provide:

- Redis Cloud account name and subscription IDs.
- Marketplace order link/ID.
- Current and target Billing Account IDs.
- GCP project ID.
- Transfer request timestamp.
- Current GCP order status.
- Redis Cloud Billing & Payments screenshot/state.
- Description of any missing provider-management link or mapping mismatch.
