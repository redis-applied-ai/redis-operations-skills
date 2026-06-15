---
name: redis-cloud-plan-change-billing
description: "Explain and investigate Redis Cloud charges after mid-month plan changes. Use when a user asks why Redis Cloud charged for a full month after upgrading, downgrading, deleting, resizing, moving from Essentials to Pro, changing an Essentials tier, seeing prorated adjustment charges, missing refunds, internal credits, duplicate-looking monthly charges, or marketplace invoices after a Redis Cloud plan change."
---

# Redis Cloud Plan Change Billing

Use this skill when a Redis Cloud bill looks wrong after an upgrade, downgrade, deletion, or subscription-type move. For payment failures use `redis-cloud-payment-failure-triage`; for post-cancel charges use the cancellation billing skill when available or `redis-cloud-cancel-subscription`.

## Current-State Rule

Billing behavior, marketplace presentation, credit treatment, and refund policy are financial/current-state facts. Verify the Redis Cloud console, invoice, contract, marketplace bill, and current Redis billing documentation before stating exact policy as current.

## Core Explanation

For Redis Cloud Essentials-style monthly plans, the apparent full extra charge is often not a second complete month. The common pattern is:

- the original monthly plan charge was already billed in advance
- a mid-month upgrade adds an adjustment for the remaining days on the higher plan
- a mid-month downgrade or deletion may create account/internal credit instead of a card refund
- the billing history can show the regular monthly charge and adjustment close together

Do not promise a refund, charge reversal, or credit carryover. Treat those as billing-support decisions after invoice review.

## Triage Flow

1. Confirm plan and billing channel:
   - Essentials, Pro, Flex, free tier, or marketplace-linked subscription
   - direct Redis Cloud billing, AWS Marketplace, GCP Marketplace, or another integrated path
2. Identify the event:
   - upgrade
   - downgrade
   - deletion/cancellation
   - Essentials-to-Pro migration
   - marketplace plan change
3. Build a timeline:
   - billing cycle start and end
   - original plan charge date
   - plan-change date and time
   - second charge, credit, or invoice date
   - deletion/cancellation completion time if applicable
4. Compare old and new plan amounts:
   - if the plan became more expensive mid-cycle, expect a prorated upward adjustment
   - if the plan became less expensive or was deleted mid-cycle, check for internal credit rather than a card refund
   - if Essentials moved to Pro, separate the final monthly plan charge from the first usage-based invoice
5. If marketplace billing is involved, reconcile in the cloud provider billing console, not only the Redis Cloud console.

## Interpretation Matrix

| Situation | Likely interpretation | Check |
| --- | --- | --- |
| Upgrade mid-month shows a new charge | Prorated difference for remaining days on the higher tier | Compare amount to old/new plan and change date. |
| Downgrade did not refund card | Unused value may be handled as account/internal credit | Review billing history, credit ledger, and later same-month charges. |
| Deleted subscription still shows monthly charge | The month may already have been billed in advance | Confirm whether the charge predates deletion and whether cancellation completed. |
| Looks billed twice | Regular monthly charge and adjustment may be shown separately | Compare time period, invoice IDs, and line-item descriptions. |
| Essentials moved to Pro | Two billing models may overlap in visible history | Separate final Essentials charge from first Pro usage period. |
| AWS/GCP invoice looks different | Marketplace billing presentation may differ from Redis Console | Reconcile with provider invoice and marketplace order/subscription state. |

## Response Pattern

When answering, structure the explanation this way:

1. State the most likely reason based on plan type and event timing.
2. Explain that the visible second line is commonly an adjustment, not automatically a duplicate month.
3. Ask for non-sensitive evidence: invoice number, billing period, old/new plan, change date, amount, and billing channel.
4. Give the exact portal/provider places to compare.
5. Identify whether Support should review it as a possible duplicate or reconciliation issue.

## Support Escalation

Escalate when:

- the same plan appears billed twice for the same period
- the adjustment does not line up with the plan-change date
- Redis Cloud and marketplace/provider bills do not reconcile
- a deletion/cancellation was completed before the billed period began
- the user needs a refund, invoice correction, or credit exception

Provide:

- Redis Cloud account and subscription ID
- old and new plan names
- upgrade, downgrade, migration, deletion, or cancellation date
- invoice number and amount
- billing channel: direct Redis, AWS Marketplace, GCP Marketplace, or other integration
- redacted billing-history or marketplace-bill screenshots if needed
