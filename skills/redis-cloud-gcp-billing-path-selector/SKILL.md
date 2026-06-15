---
name: redis-cloud-gcp-billing-path-selector
description: "Choose the correct Redis Cloud Google Cloud Marketplace billing-account move workflow. Use when the user wants to move Redis Cloud billing to a new GCP Billing Account but contract type is unclear, or when deciding between PAYG/iSaaS unsubscribe-remap, Private Offer entitlement transfer, and legacy 3PIC support-assisted remap."
---

# Redis Cloud GCP Billing Path Selector

Use this skill before giving instructions for a Redis Cloud Google Cloud Marketplace billing-account move.

## First Question

Classify the Marketplace contract before suggesting actions:

| Contract type | How to recognize | Correct path |
| --- | --- | --- |
| PAYG / iSaaS On-Demand | Marketplace subscription is on-demand/pay-as-you-go | Temporary credit card, unsubscribe old order, resubscribe under target billing account, remap existing Redis Cloud account. |
| Private Offer | Marketplace order shows Private Offer terms | Entitlement transfer coordinated by Redis and Google. Do not unsubscribe. |
| Legacy 3PIC | Legacy contract; Redis/Support confirms 3PIC or legacy seller/order identifiers | Support-assisted coordination. Do not self-serve without Redis Support. |

If the type is unknown, pause and confirm in Google Cloud Marketplace and with Redis Support or the account team.

## Shared Preflight

1. Confirm Redis Cloud Account Owner access.
2. Confirm sufficient Google Cloud billing and Marketplace permissions in the current and target billing contexts; verify current IAM role requirements in GCP.
3. Identify current and target Billing Account IDs.
4. Identify GCP project and Marketplace order link/ID.
5. Identify Redis Cloud account name and subscription IDs.
6. Back up mission-critical databases before any billing mapping change.
7. Review risk if this is the last Marketplace-mapped account for the tenant/contract.

## Routing

- For PAYG/iSaaS On-Demand, use `redis-cloud-gcp-payg-billing-transfer`.
- For Private Offer, use `redis-cloud-gcp-private-offer-billing-transfer`.
- For legacy 3PIC, use `redis-cloud-gcp-3pic-billing-transfer`.

## Red Flags

| Situation | Action |
| --- | --- |
| User is about to unsubscribe a Private Offer | Stop; use entitlement transfer. |
| User is about to unsubscribe a legacy 3PIC contract | Stop; involve Redis Support. |
| Last mapped Marketplace account may be removed | Review unmapping/resource impact before proceeding. |
| Redis Cloud shows only Credit Card after change | Mapping was not restored; use `Manage on provider` or Support. |
| GCP order cannot be found | Check correct GCP project and billing account context. |

## Universal Verification

After any path:

- Redis Cloud payment method shows Google Cloud Marketplace for intended subscriptions.
- GCP Marketplace order status is active under the intended Billing Account.
- `Manage on provider` opens the expected Redis Cloud account.
- Databases remain accessible.
- No unintended credit-card billing remains.

## Escalation Packet

Collect:

- Contract type or reason it is uncertain.
- Redis Cloud account name and subscription IDs.
- GCP project ID.
- Current and target Billing Account IDs.
- Marketplace order link/ID.
- Current Redis Cloud payment method.
- Current GCP order status.
- Screenshots of missing order, missing provider link, or mapping mismatch.
