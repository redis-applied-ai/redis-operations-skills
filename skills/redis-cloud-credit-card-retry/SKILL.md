---
name: redis-cloud-credit-card-retry
description: "Troubleshoot failed Redis Cloud credit card payments and retry behavior. Use when the user asks why a Redis Cloud payment failed, when automatic retries happen, why Pay Now is disabled, how India-based manual payments work, what happens after replacing a card, or what billing evidence to send Redis Support."
---

# Redis Cloud Credit Card Retry

Use this skill for Redis Cloud subscription payment failures involving credit cards. Do not collect full card numbers, CVV values, or payment credentials.

## Safety Rules

- Never ask for full payment card numbers, CVV, screenshots containing full card data, or bank credentials.
- Work with the invoice reference, subscription, failure date, region, and last four card digits only.
- Treat payment retry timing and regional rules as current-state facts to verify if the user is planning an urgent payment.
- Escalate to Redis Support when payment network, cross-border, or regulatory behavior blocks normal self-service.

## Triage Workflow

1. Confirm the affected Redis Cloud account, subscription, invoice reference, and failure date.
2. Ask the user to check the payment failure notification sent to the account Owner/Admin, Billing Admins, or users with Billing Emails enabled.
3. Identify the failure class without collecting sensitive card data.
4. Explain retry behavior:
   - Redis Cloud retries failed card payments automatically up to three times within the same month.
   - If an automatic retry succeeds, the invoice changes from failed to paid.
5. Check whether manual payment is available:
   - India-based customers: `Pay Now` is expected to be available for each billing cycle because recurring payments are not supported.
   - Other regions: `Pay Now` can be disabled during the first three days of the month to avoid duplicate charges, then available starting on the fourth day.
6. If the user replaced the card and assigned it to the subscription, explain that Redis Cloud should retry open balances within 24 hours.
7. If retries fail or self-service is blocked, prepare an escalation packet.

## Failure Actions

| Failure type | Action |
| --- | --- |
| Card declined | Ask the user to contact the bank, confirm funds, or use another payment method. |
| Invalid card details | Re-enter card number, expiration, CVV, and billing address in the portal. |
| Fraud or security block | Ask the bank to approve Redis Cloud charges and future attempts. |
| Retry limit reached | Use `Pay Now` when available or assign another payment method. |
| Browser or session error | Refresh, use a private browser window, clear autofill, or try another browser. |
| India payment prompt not confirmed | Retry and confirm the required pop-up before leaving the flow. |

## Pay Now Explanation

Use this wording:

- `Pay Now` may be hidden or disabled while automatic retries are still in progress.
- For non-India regions, it is normally unavailable during the first three days of the month and available from the fourth day through month end.
- For India-based billing, manual confirmation is required; if the confirmation prompt is closed or ignored, the payment remains incomplete.

## Escalation Packet

Collect:

- Account and subscription identifiers.
- Invoice reference.
- Failure timestamp.
- Region and billing country.
- Last four digits of the payment card only.
- Visible failure reason or bank decline category.
- Whether the card was replaced and assigned to the subscription.
- Whether `Pay Now` is visible and what happens when it is used.
- Browser/session symptoms, if any.
