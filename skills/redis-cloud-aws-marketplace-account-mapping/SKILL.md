---
name: redis-cloud-aws-marketplace-account-mapping
description: Use when setting up, mapping, remapping, or disconnecting Redis Cloud billing through AWS Marketplace, including AWSMarketplaceFullAccess, Redis Cloud Account Owner requirements, private offers, Pay-As-You-Go mapping, annual contracts, contract credits, duplicate billing, multiple Redis accounts, fallback credit card requirements, unsubscribe risk, or moving billing to another AWS account.
---

# Redis Cloud AWS Marketplace Account Mapping

Use this skill for Redis Cloud account setup and billing mapping through AWS Marketplace. Marketplace terms, private-offer coverage, credits, and trial details are time-sensitive; verify current AWS Marketplace and Redis Cloud billing state before quoting them.

## Required Access

Confirm the user has:

- Redis Cloud Account Owner permissions
- AWS account access for the Marketplace subscription
- appropriate AWS Marketplace IAM permissions for subscribing and managing products
- authority to make billing changes

If either Redis Cloud ownership or AWS Marketplace permissions are missing, route to the relevant account owner or AWS administrator.

## Setup Flow

1. Start or confirm the Redis Cloud subscription in AWS Marketplace.
2. Use the Marketplace setup flow to map the AWS subscription to the intended Redis Cloud account.
3. Confirm mapping in Redis Cloud billing or payment methods.
4. Confirm the intended subscriptions use the marketplace payment method.
5. Verify invoices and marketplace line items after the first billing cycle.

## Troubleshooting

- Signup loop or redirects: clear browser cache/cookies, use a clean session, and restart from the AWS Marketplace product setup flow.
- PAYG still mapped after private offer: complete product setup and keep both mappings active until Redis Support or the Console confirms remap.
- Private offer mapping fails or accounts are greyed out: open Redis Support with AWS account, offer, and Redis Cloud account details.
- Need to move billing to another AWS account: do not unsubscribe first; open Redis Support to preserve data and remap safely.
- Multiple Redis Cloud accounts on one AWS subscription: use the supported Redis Cloud marketplace account add flow or request support assistance.
- Duplicate or unexpected invoices: compare Redis Cloud subscription payment method, AWS Marketplace line items, plan type, and network/data-transfer charges.

## Disconnect Or Unsubscribe Guardrail

Before disconnecting AWS Marketplace or unsubscribing:

1. Add a fallback payment method in Redis Cloud if required.
2. Reassign every active subscription to the fallback payment method.
3. Confirm no production database depends on the marketplace billing path.
4. Only then unsubscribe in AWS Marketplace.

Warn clearly that unsubscribing without an active replacement billing method can put databases and subscriptions at risk.

## Private Offer And Credits

Before answering private-offer questions, verify:

- offer acceptance status
- mapped Redis Cloud account
- plan types covered by the offer
- whether network/data-transfer charges are covered
- remaining credits or contract term
- what happens at contract end under the current terms

Do not assume Essentials, Pro, transfer charges, or overage behavior without current billing evidence.

## Support Evidence

Collect:

- Redis Cloud account ID or account email
- AWS account ID, if safe to share through the support channel
- Marketplace subscription or offer ID
- contract/private-offer name
- affected Redis Cloud subscription IDs
- screenshots of mapping status with sensitive billing data redacted
- invoice numbers or duplicate line items

## Response Pattern

Answer with:

1. The current mapping goal: setup, remap, private offer, disconnect, or billing dispute.
2. Required Redis Cloud and AWS permissions.
3. Safe next step.
4. Fallback-payment warning for disconnects.
5. Current-state verification needed for offer, credit, and billing terms.
