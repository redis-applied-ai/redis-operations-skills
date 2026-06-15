---
name: redis-cloud-aws-marketplace-disconnect
description: "Safely disconnect Redis Cloud from AWS Marketplace billing. Use when the user asks to unmap AWS Marketplace from Redis Cloud, disconnect AWS Marketplace payment, cancel Redis Cloud AWS Marketplace subscription, handle a grayed-out Disconnect button, move subscriptions to direct billing, avoid database deletion after AWS unsubscribe, or troubleshoot AWS Marketplace contract and pay-as-you-go billing overlap."
---

# Redis Cloud AWS Marketplace Disconnect

Use this skill when moving a Redis Cloud account away from AWS Marketplace billing. The goal is billing continuity without accidental subscription or database deletion.

## Safety Rules

- Only a Redis Cloud Account Owner can disconnect the AWS Marketplace integration.
- Require a backup/export decision before billing changes that could affect subscriptions.
- Add and assign a fallback payment method before any AWS Marketplace unsubscribe.
- Do not collect full card numbers, AWS credentials, or payment secrets.
- Verify current AWS Marketplace cancellation UI and contract terms when guiding urgent billing actions.

## Preflight Checklist

1. Confirm Redis Cloud Account Owner role.
2. Identify whether AWS Marketplace maps to multiple Redis Cloud accounts or only this account.
3. Add a fallback payment method in Redis Cloud: valid card or approved wire transfer.
4. Reassign every Redis Cloud subscription from AWS Marketplace to the fallback payment method.
5. Clear outstanding invoices and open balances.
6. Back up databases before making billing changes.
7. Confirm whether marketplace credits, private offers, or contracts are in use.

## Disconnect Decision Tree

| Situation | Correct path |
| --- | --- |
| More than one Redis Cloud account is mapped to AWS Marketplace | Self-serve disconnect in Redis Cloud after moving subscriptions to fallback payment. |
| This is the last mapped Redis Cloud account | Cancel/unsubscribe from AWS Marketplace after subscriptions use fallback payment. |
| `Disconnect` is grayed out | Treat it as likely last-account handling; use AWS Marketplace cancellation flow. |
| User wants full Redis Cloud account deletion | Follow account deletion workflow after marketplace billing is disconnected. |
| User sees both contract and pay-as-you-go billing | Audit subscription mapping before disconnecting. |

## Self-Serve Disconnect Workflow

Use when more than one Redis Cloud account remains mapped to AWS Marketplace.

1. In Redis Cloud, open `Billing & Payments` then `Payment Methods`.
2. Add direct payment if one is not already available.
3. Move every subscription to the direct payment method.
4. Select `Disconnect` next to AWS Marketplace.
5. Verify the AWS Marketplace banner or payment method no longer appears.
6. Verify every subscription still shows active under the new payment method.

## Last Account Unsubscribe Workflow

Use when the Redis Cloud account is the final account mapped to AWS Marketplace.

1. In Redis Cloud, move every subscription to fallback direct billing.
2. Verify no active subscription remains tied to AWS Marketplace.
3. In AWS Console, open Marketplace managed subscriptions.
4. Find the Redis Cloud subscription and cancel/unsubscribe.
5. Return to Redis Cloud and verify the Marketplace payment option is gone.
6. Confirm databases and subscriptions remain active under fallback payment.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `Disconnect` option is grayed out | This may be the last mapped account; unsubscribe through AWS Marketplace. |
| Databases deleted after AWS unsubscribe | Fallback payment was not assigned before unsubscribe; escalate with timestamps and account IDs. |
| AWS cancel button missing | Outstanding invoices, active Marketplace-linked databases, permissions, or contract constraints. |
| Still billed after unmapping | Verify cancellation in AWS and payment method on every Redis Cloud subscription. |
| Credits or private offer expected to transfer | AWS Marketplace credits/contracts do not transfer to Redis Cloud direct billing. |
| Pay-as-you-go and contract billing both appear | Mapping issue; audit subscription billing account assignments. |

## Escalation Packet

Collect:

- Redis Cloud account ID and subscription IDs.
- AWS account ID, without credentials.
- Whether this is the last mapped account.
- Current payment method on each subscription.
- Outstanding invoice status.
- AWS Marketplace subscription status.
- Screenshots or text of grayed-out buttons or billing errors with sensitive data redacted.
- Timeline of fallback payment assignment, disconnect, and AWS cancellation attempts.
