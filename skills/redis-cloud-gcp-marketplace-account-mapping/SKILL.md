---
name: redis-cloud-gcp-marketplace-account-mapping
description: Use when setting up, mapping, remapping, or disconnecting Redis Cloud billing through Google Cloud Marketplace, including GCP Billing Admin, Billing User, Consumer Procurement Order Admin, Redis Cloud Account Owner requirements, iSaaS versus 3PIC model differences, private offers, grayed-out accounts, missing Manage on Provider, in-progress mappings, billing-account transfer, multiple Redis accounts, fallback credit cards, or unsubscribe risk.
---

# Redis Cloud GCP Marketplace Account Mapping

Use this skill for Redis Cloud account setup and billing mapping through Google Cloud Marketplace. Marketplace model, IAM roles, credits, discounts, and billing behavior are time-sensitive; verify current Google Cloud and Redis Cloud billing state before quoting specifics.

## Required Access

Confirm:

- Redis Cloud Account Owner permissions
- correct Google Cloud project
- correct Google Cloud Billing Account
- Google billing or procurement permissions sufficient for Marketplace subscription management
- authority to make billing changes

If roles are missing, route to the Google Cloud billing administrator or Redis Cloud owner.

## Identify Marketplace Model

Determine whether the subscription is:

- iSaaS: current integrated SaaS model
- 3PIC: legacy third-party integration contract model

The model can affect private offers, account mapping, Essentials, Active-Active, multiple account support, credits, discounts, and overage. Verify model before troubleshooting feature availability.

## Setup Flow

1. Start or confirm the Redis Cloud subscription in Google Cloud Marketplace.
2. Use the Marketplace setup or provider management flow to map the subscription to the intended Redis Cloud account.
3. Confirm Redis Cloud Billing & Payments shows GCP Marketplace as the active payment method.
4. Confirm entitlement or subscription mapping has completed before creating production databases.
5. Verify first invoice or marketplace line items after billing begins.

## Troubleshooting

- Signup loop or redirects: clear browser cache/cookies and restart from Google Cloud Marketplace.
- Private offer accepted but UI still shows on-demand: verify billing in Redis Cloud and Google Cloud before assuming failure.
- Cannot complete mapping: confirm project, billing account, and required IAM/procurement roles.
- Redis account greyed out: confirm Redis Cloud Account Owner status.
- Manage on Provider missing: switch to the original Google Cloud project and billing account used for the subscription.
- Mapping stuck in progress: open Redis Support with account and marketplace details.
- Move to a new billing account: do not unsubscribe first; coordinate remapping through Redis Support.
- 3PIC limitation suspected: verify model and request migration to iSaaS if needed for the desired features.

## Disconnect Or Unsubscribe Guardrail

Before unsubscribing or disconnecting:

1. Add a fallback payment method in Redis Cloud if required.
2. Move every active subscription to the fallback payment method.
3. Confirm no production database depends on Marketplace billing.
4. Only then unsubscribe or disconnect through Google Cloud Marketplace.

Warn clearly that unsubscribing without an active replacement billing method can put databases and subscriptions at risk.

## Support Evidence

Collect:

- Redis Cloud account ID or account email
- Google Cloud billing account ID, if safe through the support channel
- Google Cloud project ID
- Marketplace entitlement or order details
- offer type or contract model, if known
- affected Redis Cloud subscription IDs
- screenshots of mapping status with sensitive billing data redacted

## Response Pattern

Answer with:

1. The mapping goal: setup, remap, private offer, model migration, disconnect, or billing dispute.
2. Required Redis Cloud and Google Cloud permissions.
3. Marketplace model to verify.
4. Safe next step.
5. Fallback-payment warning for disconnects.
