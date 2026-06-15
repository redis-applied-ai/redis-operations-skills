---
name: redis-cloud-invoice-lookup
description: "Help Redis Cloud users find invoices, invoice amounts, payment links, downloads, and billing-history entries in the Redis Cloud portal. Use when the user mentions invoice numbers, missing invoices, amount due, billing history, payment links, invoice downloads, tax invoices, double charges, unpaid-invoice access issues, or failed card charges related to Redis Cloud billing."
---

# Redis Cloud Invoice Lookup

Use this skill for Redis Cloud billing portal cases where the user needs to find an invoice, payment link, billed amount, invoice download, or related billing-history record.

## Workflow

1. Confirm the billing object:
   - Invoice number, if known.
   - Redis Cloud account and subscription.
   - Billing period or charge date.
   - Whether the user needs the invoice amount, a payment link, a PDF, legal/tax details, or a resend.
2. Guide the user through the portal:
   - Sign in to Redis Cloud.
   - Open the subscription Overview tab.
   - Go to Invoices or Billing History.
   - Search by invoice number.
   - Open the invoice details.
   - Look for Total Amount, Amount Due, or equivalent billed amount.
   - Use Download or Print if a PDF copy is needed.
3. If the invoice is missing or incorrect, triage before escalating:
   - Check invoice-number format and typos.
   - Check all subscriptions under the account.
   - Ask whether there were recent subscription changes, upgrades, downgrades, migrations, or payment retries.
   - Try another browser for PDF/download failures.
4. Escalate to Support when portal self-service cannot resolve the billing record.

## Troubleshooting

| Symptom | Likely cause | Next action |
| --- | --- | --- |
| Invoice number is not found | Typo, format mismatch, migration, or portal sync issue | Confirm format and account/subscription; escalate for manual lookup if still missing. |
| Invoice shows zero amount | Trial flow, no expected charge, contractual exception, or upgrade/downgrade adjustment | Ask for billing context and escalate if explanation is needed. |
| Invoice PDF cannot be downloaded | Browser issue, PDF generation error, blank file, or server error | Retry another browser; escalate if repeatable. |
| Missing legal or tax fields | Proforma or incomplete invoice | Request the full VAT/tax-compliant invoice through Support. |
| Multiple invoices or double charges | Multiple subscriptions or split billing | Review all subscriptions; ask Support whether merge or billing clarification is needed. |
| No invoice email arrived | Billing contact mismatch or email delivery issue | Check notification settings and request manual resend. |
| User cannot access portal because of unpaid invoice | Circular payment/access issue | Open a support ticket and request invoice/payment assistance. |
| Card charge failed | Expired, declined, or blocked card | Update payment method, retry charge, or ask about wire-transfer options. |

## Safety Checks

- Do not infer billing liability from a portal screenshot alone. Ask for invoice number, subscription, billing period, and account context.
- Do not ask users to post full payment-card data or sensitive tax identifiers in chat.
- For current portal labels, billing-policy details, or tax requirements, verify live Redis Cloud documentation or Support guidance before presenting them as definitive.

## Escalation Packet

Collect these details before escalating:

- Redis Cloud account and subscription.
- Invoice number and billing period.
- Exact issue: missing, zero amount, failed download, missing tax details, duplicate charge, or email not received.
- Browser and approximate timestamp for download or portal errors.
- Any recent changes: upgrade, downgrade, migration, trial conversion, card update, or account transfer.
