---
name: redis-cloud-gcp-private-offer
description: "Guide Redis Cloud customers through accepting, activating, mapping, and verifying a Google Cloud Marketplace private offer. Use when the user mentions Redis Cloud GCP private offers, Google Cloud Marketplace orders, Manage on Provider, Marketplace billing, GCP billing account mapping, private-offer activation failures, or Marketplace credits not being consumed."
---

# Redis Cloud GCP Private Offer

Use this skill to help a user complete or troubleshoot Redis Cloud private-offer activation through Google Cloud Marketplace. Keep the guidance focused on billing-account alignment, Marketplace order status, Redis Cloud account mapping, and verification.

## Workflow

1. Confirm the commercial context before giving steps:
   - The user has a Redis Cloud private-offer link or an existing GCP Marketplace order.
   - The intended Google Cloud billing account is known.
   - The target Redis Cloud account is known.
   - The user understands that mapping the contract changes how Redis Cloud usage is billed going forward.
2. Check required permissions:
   - Google Cloud: `Billing Administrator`, or `Billing User` plus `Consumer Procurement Order Admin`.
   - Redis Cloud: Owner access to the target account.
3. Accept the offer in Google Cloud Marketplace:
   - Open the private-offer link while signed in to the correct Google account.
   - Go to Cloud Marketplace, then Your Orders.
   - Select the intended billing account.
   - Wait for the order to become Active.
   - Open the order and confirm the offer details.
4. Select the Redis Marketplace listing and project:
   - Choose the Redis product listing from Your Orders.
   - Select a Google Cloud project associated with the same billing account used for the offer.
   - If the project is missing, create or select a project tied to that billing account before continuing.
5. Map the contract to Redis Cloud:
   - Use Manage on Provider to open Redis Cloud.
   - Sign in to the Redis Cloud account that should consume the Marketplace agreement.
   - Select the Redis Cloud account or accounts to associate with the Marketplace contract.
   - Enable the Marketplace payment checkbox.
6. Verify the mapping in Redis Cloud:
   - Open Billing & Payments, then Payment Methods.
   - Confirm Google Cloud Marketplace appears as a payment method.
   - Confirm the Marketplace order reference and connected billing relationship are visible.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Private offer cannot be accepted | Confirm the signed-in Google account and required billing/procurement permissions. |
| Order does not become Active | Confirm the billing account is valid and procurement permissions are assigned. |
| Manage on Provider is missing | Confirm the selected GCP project is tied to the same billing account used for the private offer. |
| Redis Cloud does not show Marketplace billing | Confirm the Marketplace payment checkbox was enabled during account mapping. |
| Charges do not consume Marketplace credits | Confirm the Redis Cloud account is mapped to the Marketplace contract under Billing & Payments. |

## Safety Checks

- Do not tell the user to activate or map a contract if the target Redis Cloud account or GCP billing account is uncertain.
- Treat multiple Redis Cloud accounts and multiple GCP billing accounts as high-risk for misbilling. Ask the user to verify the exact account and project before mapping.
- For current GCP Marketplace UI labels, permissions, or billing behavior that may have changed, verify live Google Cloud or Redis Cloud documentation before presenting it as current fact.

## Escalation Packet

When activation fails and basic checks do not resolve it, collect:

- GCP billing account name or ID.
- GCP project selected from the Marketplace listing.
- Marketplace order status.
- Redis Cloud account name or ID selected during mapping.
- Whether Manage on Provider appeared.
- Whether Google Cloud Marketplace appears under Redis Cloud payment methods.
- Screenshots or exact error text from Google Cloud Marketplace and Redis Cloud.
