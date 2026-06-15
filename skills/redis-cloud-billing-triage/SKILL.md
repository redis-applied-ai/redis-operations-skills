---
name: redis-cloud-billing-triage
description: "Classify Redis Cloud billing questions and route them to the right billing workflow. Use when the user asks a broad Redis Cloud billing question, mentions payment failures, invoices, payment links, billing history, cost reports, payment information, credit card retries, data transfer charges, or unexpected Redis Cloud bill line items."
---

# Redis Cloud Billing Triage

Use this skill as a first-pass router for Redis Cloud billing cases. It helps choose the correct focused workflow and identify the evidence needed before escalation.

## Triage Workflow

1. Classify the billing issue:
   - Payment failure or declined card.
   - Credit card retry behavior.
   - Invoice lookup, payment link, PDF, or amount due.
   - Payment method or payment information.
   - Cost report download, visualization, or Cost Report API issue.
   - New network/data-transfer charge or unexpected bill line item.
2. Gather core identifiers:
   - Redis Cloud account.
   - Subscription.
   - Billing period or invoice number.
   - Payment method type when relevant.
   - Exact error, charge label, or missing artifact.
3. Route to the narrowest available skill or workflow:
   - Invoice lookup/payment links: use a focused invoice lookup workflow.
   - 429 or automation issues with billing APIs: use a rate-limit/automation workflow.
   - Marketplace billing: use the relevant AWS, GCP, or private-offer workflow.
   - Payment failures: use a payment-failure workflow.
   - Cost reports: use a cost-report download or API troubleshooting workflow.
4. If no narrow workflow exists yet, answer with a concise billing-support triage response and collect an escalation packet.

## Issue Map

| User symptom | Likely workflow |
| --- | --- |
| "I need my invoice" or "where is the payment link?" | Invoice lookup and billing history. |
| "My card was declined" or "payment failed" | Payment failure and retry handling. |
| "Where do I find payment info?" | Payment-method lookup and billing profile guidance. |
| "I need usage/cost data" | Cost report download, visualization, or Cost Report API. |
| "Why is there a data transfer charge?" | Network/data-transfer charge explanation and usage evidence. |
| "Marketplace credits are not used" | Marketplace account mapping and billing connection. |

## Safety Checks

- Do not ask for full credit card numbers, CVV, or sensitive tax identifiers.
- Do not promise refunds, invoice merges, or charge reversals; route those to Support or billing operations.
- For current pricing, fees, tax rules, support windows, or cloud marketplace behavior, verify live Redis or cloud-provider documentation before stating details as current.

## Escalation Packet

Collect:

- Redis Cloud account and subscription.
- Invoice number, billing period, or charge date.
- Payment method type, without sensitive card details.
- Exact portal/API error or bill line item.
- Whether the account uses direct Redis billing, AWS Marketplace, GCP Marketplace, Heroku, Vercel, or another integrated marketplace.
- Recent account changes: upgrade, downgrade, cancellation, private offer, marketplace mapping, or ownership transfer.
