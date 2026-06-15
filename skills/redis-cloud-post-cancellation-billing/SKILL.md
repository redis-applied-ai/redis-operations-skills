---
name: redis-cloud-post-cancellation-billing
description: "Investigate Redis Cloud charges after cancellation or deletion. Use when a user says they cancelled Redis Cloud but were still charged, deleted a database but billing continued, removed a card but charges continued, sees a final invoice after Pro cancellation, has AWS or GCP Marketplace billing after cancellation, cannot reconcile cancellation timing with invoice period, or needs to distinguish database deletion from subscription cancellation."
---

# Redis Cloud Post-Cancellation Billing

Use this skill to explain and investigate charges that appear after a Redis Cloud cancellation. For actually deleting databases or cancelling subscriptions, use `redis-cloud-delete-database` and `redis-cloud-cancel-subscription`.

## Current-State Rule

Billing, marketplace, refund, resource-deletion, and private-offer cancellation behavior can change and may depend on contract terms. Verify the customer's invoice, Redis Cloud console state, marketplace order, contract/private offer, and current Redis/cloud-provider guidance before stating exact policy as current.

## First Principles

Keep these distinctions explicit:

- deleting a database removes the database, but may leave the subscription billable
- deleting or cancelling the subscription is the action that stops future Redis Cloud subscription billing
- marketplace billing can require provider-side cancellation in addition to Redis Cloud cleanup
- Pro-style usage can produce a final invoice after resources are gone because usage is billed after the period
- Essentials-style monthly billing can show a final prepaid month if the invoice was generated before cancellation
- direct contracts or private offers may continue until the commercial commitment is ended

Do not promise refunds, waivers, or charge reversals. Escalate those to Support or billing operations with evidence.

## Investigation Flow

1. Confirm the billing path:
   - direct Redis Cloud billing
   - AWS Marketplace
   - GCP Marketplace
   - private offer, annual commitment, or other contract
2. Confirm what was actually cancelled or deleted:
   - database only
   - all databases in the subscription
   - Redis Cloud subscription
   - marketplace order/subscription
   - full account or organization
3. Check for remaining billable resources:
   - subscription still exists
   - another database remains under the subscription
   - another organization/account under the same login has resources
   - marketplace order is still active
4. Compare invoice dates:
   - invoice generation date
   - billing or usage period
   - database deletion timestamp
   - subscription cancellation timestamp
   - marketplace cancellation timestamp
5. Classify the charge as likely expected final invoice, incomplete cancellation, marketplace mismatch, prior failed payment retry, or possible billing error.

## Plan-Specific Interpretation

| Plan or channel | How to interpret a post-cancel charge |
| --- | --- |
| Essentials | Monthly plan is commonly billed in advance; a charge generated before cancellation may be the final expected charge. |
| Pro or usage-based | Charges can appear after cancellation for usage that occurred before cancellation. |
| Database deleted only | Subscription may continue billing until subscription cancellation is complete. |
| AWS or GCP Marketplace | Check both Redis Cloud and the provider marketplace; one side can remain active. |
| Private offer or annual contract | Resource deletion may not end the commercial commitment; review contract and Support path. |
| Removed payment card | Card removal does not itself cancel subscriptions; prior failed invoices may later retry or remain due. |

## Account And Organization Checks

If the user sees no active resources but still sees charges:

- check the Redis Cloud account switcher for other organizations
- check whether they used Google, GitHub, SSO, or email/password login variants
- verify the invoice account ID or marketplace order against the currently visible account
- check whether a teammate or former Owner controls the billed organization

## Stop Future Charges

Only provide as guidance unless the user explicitly asks to perform destructive cleanup:

1. Delete or migrate all databases that are no longer needed.
2. Cancel/delete the Redis Cloud subscription after databases are removed.
3. For marketplace purchases, cancel/unsubscribe in AWS Marketplace or GCP Marketplace as required.
4. Verify no active subscription, marketplace order, or unpaid invoice remains.

Require explicit confirmation before any destructive action.

## Escalation Criteria

Open Support/billing review when:

- no subscriptions or databases remain and billing still continues
- invoice period starts after confirmed cancellation
- the same period appears charged twice
- marketplace and Redis Cloud states disagree after cleanup on both sides
- a private offer or annual commitment needs formal cancellation
- the customer requests a refund, credit, or invoice correction

Collect:

- Redis Cloud account email or account ID
- subscription ID/name if available
- invoice number, amount, charge date, and billing/usage period
- cancellation/deletion timestamps and what was deleted or cancelled
- billing channel: direct, AWS Marketplace, GCP Marketplace, or private offer
- redacted screenshots of active subscription list, billing history, and marketplace order state when needed
