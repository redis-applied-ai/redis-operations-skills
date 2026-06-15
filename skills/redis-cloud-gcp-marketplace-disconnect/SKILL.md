---
name: redis-cloud-gcp-marketplace-disconnect
description: "Safely disconnect Redis Cloud from Google Cloud Marketplace billing. Use when the user asks to unmap GCP Marketplace from Redis Cloud, remove Marketplace account, switch Redis Cloud subscriptions to credit card, troubleshoot cannot unmap while resources use Marketplace, handle last account cancellation in Google Cloud Console, identify 3PIC versus iSaaS account behavior, or resolve missing Manage on Provider buttons."
---

# Redis Cloud GCP Marketplace Disconnect

Use this skill when moving a Redis Cloud account away from Google Cloud Marketplace billing. The main risk is accidental resource deletion or billing interruption.

## Safety Rules

- Confirm Redis Cloud Account Owner role before unmapping.
- Confirm GCP billing account permissions before asking the user to act in Google Cloud Console.
- Back up critical databases before marketplace billing changes.
- For iSaaS accounts, move every subscription to direct payment before disconnecting.
- For legacy 3PIC accounts, warn that no fallback card path may exist and unsubscribe can lead to resource deletion after the provider grace period.
- Verify current GCP Marketplace UI and contract terms for urgent cancellation decisions.

## Preflight Checklist

1. Confirm Redis Cloud account ID and Account Owner access.
2. Confirm GCP billing account and project are the intended ones.
3. Confirm GCP IAM:
   - `roles/billing.admin`, or
   - `roles/billing.user` plus `roles/consumerprocurement.orderAdmin`.
4. Determine account model:
   - iSaaS: supports switching subscriptions to a credit card.
   - 3PIC legacy: Marketplace-only billing; no fallback payment method in Redis Cloud.
5. For iSaaS, add a credit card and move every active subscription to it.
6. Clear outstanding billing issues.
7. Back up important databases.

## Disconnect Decision Tree

| Situation | Correct path |
| --- | --- |
| iSaaS account, not last marketplace account | Move subscriptions to card, then disconnect in Redis Cloud. |
| iSaaS account, last marketplace account | Move subscriptions to card, then unsubscribe/cancel in Google Cloud Console. |
| 3PIC legacy account | No Redis Cloud card fallback; unsubscribe in GCP can delete resources after grace period. |
| UI says resources still use Marketplace | Update every subscription payment method before retrying. |
| Missing provider management option | Verify GCP project, billing account, order, and IAM roles. |

## iSaaS Disconnect Workflow

1. In Redis Cloud Console, open `Billing & Payments`.
2. Add a valid credit card.
3. Update every active subscription to use the card instead of Google Cloud Marketplace.
4. If this is not the last marketplace-mapped account, choose `Disconnect` or `Remove Marketplace Account` in Redis Cloud.
5. If this is the last mapped account, unsubscribe from the Redis Cloud order in Google Cloud Console Marketplace orders.
6. Verify Redis Cloud no longer shows Marketplace as a payment option and subscriptions remain active.

## 3PIC Legacy Workflow

1. Confirm there is no option to add a credit card in Redis Cloud.
2. Explain that the account is likely Marketplace-only.
3. Back up all databases before unsubscribe.
4. Unsubscribe from the order in Google Cloud Console if the user accepts the risk.
5. Monitor the grace period and resource status.
6. Escalate to Redis Support for complex migrations or if preserving resources is required.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Cannot unmap while resources use Marketplace | One or more subscriptions still have Marketplace as payment method. |
| Last account cannot be unmapped in Redis Cloud | Use Google Cloud Console Marketplace order cancellation. |
| No credit card option appears | Likely 3PIC legacy account. |
| Resources deleted after unsubscribe | Subscriptions were not migrated or account was 3PIC; gather timeline and escalate. |
| Manage on Provider is missing | Wrong GCP project, wrong billing account, or missing IAM roles. |
| Marketplace still appears after disconnect | Check every subscription payment method and GCP order status. |

## Escalation Packet

Collect:

- Redis Cloud account ID and subscription IDs.
- GCP billing account ID and project ID.
- Account model: iSaaS or 3PIC, with evidence.
- Current payment method for every subscription.
- Whether this is the last marketplace-mapped account.
- GCP order status.
- IAM roles confirmed for the acting GCP user.
- Error text or UI blocker with sensitive information redacted.
- Backup status and resource preservation requirement.
