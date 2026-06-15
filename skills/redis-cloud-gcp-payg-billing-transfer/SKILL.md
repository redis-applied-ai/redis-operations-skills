---
name: redis-cloud-gcp-payg-billing-transfer
description: "Move Redis Cloud Google Cloud Marketplace iSaaS On-Demand PAYG billing to a new GCP Billing Account. Use when the user asks to transfer Redis Cloud PAYG Marketplace charges, switch temporarily to credit card, unsubscribe and resubscribe under a new billing account, remap an existing Redis Cloud account, fix Pending Marketplace mapping, or avoid accidentally creating a new Redis account."
---

# Redis Cloud GCP PAYG Billing Transfer

Use this skill for Redis Cloud subscriptions purchased through Google Cloud Marketplace as iSaaS On-Demand/PAYG. Do not use it for legacy 3PIC contracts.

## Preflight

1. Confirm order type is On-Demand/PAYG in Google Cloud Marketplace.
2. Confirm this is not a legacy 3PIC contract.
3. Confirm Redis Cloud Owner access and sufficient Google Cloud Marketplace/Billing permissions.
4. Identify:
   - Current GCP project and Billing Account.
   - Target GCP project and Billing Account.
   - Redis Cloud account name and subscriptions to remap.
   - Current Marketplace order.
5. Review implications if this is the last Marketplace-mapped account on the Redis tenant.
6. Confirm there is an approved temporary credit-card payment method.

## Safety

Unsubscribing a Marketplace order is a billing-control action. Before clicking unsubscribe:

1. Confirm the order is PAYG/iSaaS, not 3PIC.
2. Confirm Redis Cloud payment has been temporarily switched to Credit Card.
3. Confirm the target billing account/project is ready.
4. Ask for explicit confirmation naming the old order and target billing account.

## Transfer Workflow

1. In Redis Cloud, add or confirm a credit card payment method.
2. Set affected subscriptions to `Payment method = Credit Card`.
3. In Google Cloud Marketplace, open the old Redis Cloud order and unsubscribe it.
4. Switch to the project tied to the target Billing Account.
5. Subscribe to Redis Cloud from Google Cloud Marketplace under the target billing account.
6. From the new GCP order, use `Manage on provider`.
7. In Redis Cloud, choose `Connect account` and select the existing intended Redis Cloud account.
8. Set affected Redis Cloud subscriptions back to `Payment method = GCP Marketplace`.

Data and endpoints should remain unchanged when the existing account is remapped correctly; the change is to billing source.

## Verification

In Redis Cloud:

- Payment method shows Google Cloud Marketplace for the intended subscriptions.
- No subscriptions remain unintentionally on Credit Card.
- Databases and endpoints are unchanged and accessible.

In Google Cloud:

- Redis Cloud Marketplace order is active under the target Billing Account.
- `Manage on provider` opens the intended existing Redis Cloud account.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Mapping stuck on `Pending` | Subscriptions still set to Credit Card | In Redis Cloud, set payment method back to Google Cloud Marketplace after mapping. |
| Old order not visible | Wrong GCP project or billing account context | Switch to the project/account that owned the original order and check Marketplace orders. |
| New Redis account created | Wrong provider-management or mapping path | Use `Manage on provider` and connect the existing Redis Cloud account; escalate if already mis-mapped. |
| Redis Cloud still bills card | Payment method not reverted | Change intended subscriptions back to Google Cloud Marketplace and verify next invoice source. |
| Contract type uncertain | 3PIC and PAYG flows differ | Pause and confirm order type with Redis Support or the account team. |

## Escalation Packet

Collect:

- Redis Cloud account name and subscription IDs.
- Old and new GCP project IDs.
- Old and new Billing Account IDs.
- Old and new Marketplace order IDs/links.
- Current Redis Cloud payment-method state.
- Current GCP order status.
- Screenshots of Pending/mis-mapped states if relevant.
