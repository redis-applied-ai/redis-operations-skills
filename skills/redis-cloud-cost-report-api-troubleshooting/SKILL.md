---
name: redis-cloud-cost-report-api-troubleshooting
description: Use when troubleshooting Redis Cloud Cost Report API generation or downloads, including FOCUS CSV or JSON reports, `/cost-report` async task flow, polling `/tasks/{taskId}`, downloading `/cost-report/{costReportId}`, `Forbidden` errors, Owner/Viewer versus Billing Admin API permissions, `startDate` and `endDate` validation, 40-day date windows, subscription/database/region/tag filters, empty reports, JSON versus CSV format, or report totals differing from invoices.
---

# Redis Cloud Cost Report API Troubleshooting

Use this skill when Redis Cloud Cost Report API calls fail or produce unexpected output. Cost reporting and API permissions can change, so verify current Redis Cloud API documentation before making final access or field claims.

## Sensitive Data Rule

Cost reports contain financial and usage data. Do not ask users to paste full reports unless needed and approved. Redact account names, subscription names, tags, invoice references, and payment details where possible.

## API Permission Check

The source baseline says Cost Report API generation requires Owner or Viewer API credentials and that Billing Admin credentials can receive `Forbidden` for this endpoint. This differs from some console billing-report workflows.

When diagnosing:

1. Confirm whether the request uses Console UI or REST API.
2. Confirm API credential role without asking for the secret.
3. Verify current role behavior in the live docs or account if possible.

## Required Async Flow

Use the three-step API workflow:

1. Generate report:

   ```text
   POST /cost-report
   ```

   Response should include a `taskId`.

2. Poll task:

   ```text
   GET /tasks/{taskId}
   ```

   Wait until the task status is complete, such as `processing-completed` in the source baseline.

3. Download report:

   ```text
   GET /cost-report/{costReportId}
   ```

Do not try to download before the task returns a report ID.

## Request Body Validation

Check:

- `startDate` and `endDate` are in `YYYY-MM-DD` format.
- Date range is within the current API maximum; the source baseline uses `<= 40 days`.
- `format` is explicit when downstream tooling expects CSV or JSON.
- Filters are valid and not overly broad:
  - `subscriptionIds`
  - `databaseIds`
  - `subscriptionType`
  - `regions`
  - `tags`
- Each tag filter includes both `key` and `value`.

Split longer reporting windows into multiple valid requests.

## Troubleshooting Matrix

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `Forbidden` | API role not accepted for Cost Report API. | Try Owner or Viewer credentials after verifying current role policy. |
| `400` or invalid request | Date format, date range, filter shape, or tag object is invalid. | Validate body fields and split the date range. |
| Report never appears | Task was not polled to completion. | Poll task until complete, then use the returned report ID. |
| Empty report | No matching usage, wrong date window, or filters too tight. | Loosen filters and verify actual usage exists. |
| Too broad report | Missing filters. | Add subscription, database, region, type, or tag filters. |
| Tag filter ignored | Missing tag `key` or `value`. | Send complete tag objects. |
| Expected CSV but got JSON | Format not explicit or client accepted default differently. | Set `format` explicitly. |
| Totals differ from invoice | API is list-price/usage-oriented; invoice includes discounts, credits, taxes, marketplace, or timing adjustments. | Reconcile with invoice or marketplace bill and rerun after finalization if needed. |

## Reconciliation Caveats

Cost report API output can differ from invoices because of:

- list price versus contracted discounts or credits
- taxes and marketplace/provider charges
- month-end timing and late network-cost finalization
- filters that exclude subscriptions, databases, regions, or tags

For invoice disputes or billing-impacting decisions, use the official invoice or marketplace bill as the financial source of truth.

## Escalation Packet

Collect:

- account ID and credential role, with secrets redacted
- request method and endpoint
- sanitized request body
- date range and filters
- `taskId`, task status, and `costReportId` if available
- exact error body and status code
- expected format and actual format
- invoice discrepancy summary without sensitive payment details
