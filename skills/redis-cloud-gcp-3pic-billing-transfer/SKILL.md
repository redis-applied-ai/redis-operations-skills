---
name: redis-cloud-gcp-3pic-billing-transfer
description: "Coordinate Redis Cloud legacy 3PIC Google Cloud Marketplace billing transfer to a new GCP Billing Account. Use when the user asks to move Redis Cloud GCP Marketplace billing, sees Redis Cloud access lost after a billing-account change, sees only Credit Card after a Marketplace change, needs to confirm 3PIC versus iSaaS, or needs a support-assisted remap without unsubscribing."
---

# Redis Cloud GCP 3PIC Billing Transfer

Use this skill when a Redis Cloud subscription is billed through legacy Google Cloud Marketplace Third-Party Integrated Commerce (3PIC) and the payer or Google Cloud Billing Account must change.

## Critical Rule

Do not manually unsubscribe a legacy 3PIC Redis Cloud Marketplace contract to move billing. Unsubscribing can terminate or unmap linked Redis Cloud resources. Treat the change as Redis Support-assisted.

## Preflight

1. Confirm the contract type with Redis Support or the account team:
   - Legacy 3PIC and not current iSaaS.
   - Marketplace seller/order details match the legacy contract.
2. Confirm Google Cloud permissions to view and manage the Marketplace order and billing account. Verify current required IAM roles in Google Cloud before executing.
3. Confirm Redis Cloud account Owner access.
4. Open a Redis Support ticket before changing billing.
5. Collect:
   - Current GCP Marketplace order link or ID.
   - Current Billing Account ID.
   - Target Billing Account ID.
   - Project ID.
   - Redis Cloud account name and subscription IDs.
   - Desired maintenance window.
6. Back up mission-critical databases and define a service continuity plan.

## Support-Assisted Workflow

1. Share the collected identifiers and target timing with Redis Support.
2. Confirm whether any unmapping/remapping step is required.
3. Schedule the billing transition in a maintenance window.
4. During the change, keep Redis Support engaged and avoid repeated manual Marketplace actions.
5. If the Redis Cloud account becomes unmapped, follow Support guidance to reconnect it from the GCP order or provider-management link.
6. If advised by Support, configure a temporary credit-card fallback to maintain continuity until Marketplace mapping is restored.

## Verification

In Google Cloud:

- Redis Cloud Marketplace order is under the target Billing Account.
- Order status is active.
- `Manage on provider` opens the correct Redis Cloud account.

In Redis Cloud:

- Payment method shows Google Cloud Marketplace.
- Expected subscriptions are mapped to the Redis Cloud account.
- Databases are accessible.
- No grace, suspended, or unmapped state remains.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Redis Cloud access lost after billing change | 3PIC unmapping occurred | Contact Redis Support immediately with order/account details; act before any grace window expires. |
| Redis Cloud only shows Credit Card | Marketplace mapping was not restored | Use the GCP order provider-management link or Support-assisted remap. |
| Unsure if subscription is 3PIC | Legacy and current Marketplace models differ | Pause changes and confirm contract type first. |
| GCP order not under target account | Billing-account transfer incomplete | Verify Marketplace order status and GCP Billing Account selection with Google/Redis Support. |
| Billing changed but databases unavailable | Mapping or payment state still inconsistent | Keep fallback payment active if advised and escalate with timestamps/screenshots. |

## Escalation Packet

Provide:

- Redis Cloud account name and subscription IDs.
- GCP Marketplace order link/ID.
- Current and target Billing Account IDs.
- Project ID.
- Exact time of attempted change.
- Current Redis Cloud payment-method view.
- Current GCP Marketplace order status.
- Screenshots if UI states differ.
