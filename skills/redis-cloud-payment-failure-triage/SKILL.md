---
name: redis-cloud-payment-failure-triage
description: Use when Redis Cloud payment fails, invoices remain unpaid, Pay Now is unavailable or disabled, a new card does not charge, marketplace billing is disconnected, an account is blocked for non-payment, database access fails due to billing restrictions, India RBI recurring-payment behavior is involved, or Support needs invoice and payment confirmation details.
---

# Redis Cloud Payment Failure Triage

Use this skill to help a Redis Cloud user resolve billing and payment failures without collecting sensitive card data. Verify current Redis Cloud billing behavior and regional payment rules before quoting time windows or policy commitments.

## Classify The Billing Path

First identify:

- credit card billing
- AWS Marketplace billing
- Google Cloud Marketplace billing
- manual payment through Pay Now or payment link
- blocked or restricted account due to overdue invoices
- regional payment behavior, such as recurring-payment restrictions

## Intake Checklist

Ask for non-sensitive evidence only:

- account email or account ID if appropriate for support routing
- subscription ID
- invoice number
- invoice status in Billing History
- payment method type, not full card details
- whether the card is assigned to the affected subscription
- whether marketplace billing connection is active
- whether Pay Now is visible, disabled, or failing
- approximate time payment was attempted
- payment confirmation or receipt ID if already paid

Do not ask for full card number, CVV, bank credentials, or screenshots containing sensitive payment details.

## Triage Flow

1. Check Billing History for unpaid, pending, failed, or paid invoices.
2. Confirm the active subscription has a valid assigned payment method.
3. If card payments fail, have the user verify expiration, billing address, bank fraud block, supported card type, and available funds with their bank.
4. If marketplace billing is used, verify the cloud marketplace connection is still active and associated with the intended Redis Cloud account.
5. If Pay Now is disabled or missing, verify billing permissions, subscription payment method assignment, UI cache, and current Redis Cloud billing retry behavior.
6. If the account is blocked, pay all open balances and then verify whether access restores; escalate if restrictions remain.

## Common Situations

- Paid but still blocked: verify invoice shows Paid, refresh session, then open support with invoice number and payment confirmation.
- New card added but invoice still pending: verify the card is assigned to the subscription and allow current retry processing; use Pay Now when available.
- Card repeatedly declined: use another card or resolve with the issuing bank.
- Cannot delete or modify subscription: settle open balances first; billing restrictions can block admin actions.
- Database auth or access unexpectedly fails: check whether account restrictions were applied due to unpaid invoices.
- Regional recurring payments fail: use the current Redis Cloud-supported manual payment path and verify region-specific payment rules.

## Support Escalation

Escalate when:

- invoice is paid but account remains blocked
- Pay Now should be available but is missing or disabled
- marketplace billing appears linked but charges fail
- invoice remains pending after confirmation
- regional payment behavior does not match the current documented policy

Provide invoice number, subscription ID, payment confirmation, payment timestamp, and a redacted screenshot of Billing History if needed.

## Response Pattern

Answer with:

1. The likely billing path and failure type.
2. The portal checks to perform.
3. The non-sensitive evidence to collect.
4. Whether the next action is assign/update card, use manual payment, verify marketplace billing, contact bank, or open support.
