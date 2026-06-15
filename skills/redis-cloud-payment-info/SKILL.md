---
name: redis-cloud-payment-info
description: "Find Redis Cloud payment information, invoices, payment links, wire instructions, and consumption reports. Use when the user asks for Pay Now links, unpaid invoices, billing PDFs, Billing and Payments access, missing or expired payment links, Stripe payment links from Support, wire transfer details, monthly contract usage reports, marketplace contract reporting, or billing access denied for non-admin users."
---

# Redis Cloud Payment Info

Use this skill when a user needs Redis Cloud invoices, payment links, wire instructions, or contract consumption reports.

## Safety Rules

- Do not ask for full card numbers, bank credentials, or payment secrets.
- Billing pages require Owner, Admin, or Billing Admin access.
- Treat invoices and consumption reports as sensitive financial documents.
- If account access is lost, Redis Support may provide a standalone payment link; do not attempt to bypass account security.

## Find Invoices and Pay Now Links

1. Sign in to Redis Cloud Console or Customer Portal.
2. Open `Billing & Payments`.
3. Open `Billing History`.
4. Find the invoice by date, status, or invoice number.
5. Download the invoice PDF if needed.
6. If the invoice is unpaid, look for a `Pay Now` button or payment link.
7. If no payment link appears, contact Redis Support to request a payment link.

## Wire Transfer Information

For contracted or wire-transfer accounts:

- Payment instructions are usually included in the invoice email.
- Billing contacts receive invoices after each billing cycle.
- If the wire instructions are missing or unclear, use the invoice reference and request help from Redis Support or the billing contact.

## Monthly Consumption Reports

Contracted customers, including marketplace contracts, may receive monthly usage/consumption reports for the prior month.

Reports may go to:

- Account admins.
- Billing admins.
- Users with billing emails enabled.
- Other configured billing distribution lists.

Use reports to review current-period usage, accumulated contract consumption, and allocation by account, contract, subscription, or database where available.

## Contract and Marketplace Notes

- Contract details are visible from subscription overview or billing areas when the user has access.
- Marketplace behavior can differ by provider.
- Reconcile marketplace invoices with the cloud provider billing portal when charges do not match Redis Cloud views.
- Verify current provider-specific contract behavior before advising on purchases or eligibility.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Payment link not visible | Confirm invoice is unpaid; request a payment link from Redis Support. |
| Payment link expired | Ask Support or billing contact for a new link. |
| Invoice not found | Filter by date range, status, subscription, or invoice number. |
| Access denied | Use Owner/Admin/Billing Admin account or request billing access. |
| Account access lost | Contact Support for standalone payment help. |
| Wire instructions missing | Check invoice email and billing contacts; escalate with invoice reference. |
| Marketplace bill differs | Compare Redis report with AWS/GCP marketplace billing portal. |

## Escalation Packet

Collect:

- Redis Cloud account ID.
- Invoice number or invoice date.
- Subscription ID if known.
- User role and access status.
- Whether payment is card, wire, direct contract, AWS Marketplace, or GCP Marketplace.
- Payment link state: missing, expired, or failing.
- Billing contact email visibility, without sharing sensitive payment data.
