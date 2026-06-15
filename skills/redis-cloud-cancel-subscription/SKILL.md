---
name: redis-cloud-cancel-subscription
description: "Guide safe cancellation of Redis Cloud subscriptions across direct Redis billing, AWS Marketplace, and GCP Marketplace. Use when the user asks to cancel or delete a Redis Cloud subscription, cannot find the Cancel Subscription button, is blocked by unpaid invoices, needs to cancel marketplace billing, or asks why billing continued after cancellation."
---

# Redis Cloud Cancel Subscription

Use this skill for Redis Cloud subscription cancellation. Cancellation is destructive because databases under the subscription must be deleted first.

## Safety Rules

- Require explicit confirmation before any action that deletes databases or cancels subscriptions.
- Confirm the account owner is performing the cancellation; only owners can cancel subscriptions.
- Confirm backups, exports, migration, or data-retention needs before database deletion.
- Explain that charges stop only after subscription deletion is complete.
- Do not promise refunds. Treat refunds and billing exceptions as Support decisions.

## Preflight Checklist

1. Identify subscription type:
   - Essentials.
   - Flex or Pro.
   - AWS Marketplace.
   - GCP Marketplace.
2. Confirm prerequisites:
   - User is Account Owner.
   - All required data has been backed up or migrated.
   - All databases under the subscription are deleted or ready to delete.
   - Outstanding balances are paid.
   - Marketplace-linked accounts have a direct Redis Cloud payment method if continued service is needed.
3. Confirm billing context:
   - Essentials is typically prepaid.
   - Flex/Pro is usage based and may bill in arrears.
   - Marketplace cancellation may require cloud-provider console steps.

## Direct Redis Cloud Cancellation

1. Delete every database in the subscription:
   - Open Redis Cloud Console.
   - Go to Databases.
   - For each database, open configuration, then Danger Zone, then Delete Database.
2. Cancel the subscription:
   - Go to Subscriptions.
   - Select the subscription.
   - Open Overview.
   - Select Cancel Subscription.
   - Confirm the cancellation dialog.
3. Verify:
   - Subscription no longer appears as active.
   - No databases remain under the subscription.
   - Billing status and remaining invoices are understood.

## Marketplace Cancellation

AWS Marketplace:

- Add a direct payment method in Redis Cloud before disconnecting if databases must continue running.
- Remove the AWS Marketplace mapping as appropriate.
- If this is the last AWS Marketplace-linked Redis account, unsubscribe through AWS Marketplace subscriptions.
- Contact Redis Support if mapping removal or billing state is unclear.

GCP Marketplace:

- Add a direct payment method in Redis Cloud before canceling if databases must continue running.
- Unsubscribe in Google Cloud Console, Marketplace, Your Orders.
- If this is the last GCP Marketplace-linked Redis account, warn that databases may be suspended or deleted unless direct payment is configured.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Cancel Subscription button missing | Databases still exist or unpaid balance remains | Delete databases and pay outstanding invoices. |
| Cancellation blocked | Outstanding invoices | Use Billing & Payments, Pay now. |
| Still billed after canceling | Subscription deletion was not completed | Verify subscription status under Subscriptions. |
| Redis UI cannot cancel marketplace subscription | AWS/GCP marketplace controls billing | Follow cloud marketplace cancellation path. |
| Pay Now missing | Auto-retry cycle active | Wait for retry cycle or contact Support. |

## Escalation Packet

Collect:

- Redis Cloud account and subscription ID/name.
- Subscription type and billing channel.
- Whether databases remain under the subscription.
- Outstanding invoice status.
- Marketplace account or order reference, if applicable.
- Cancellation attempt timestamp and exact error or missing UI state.
