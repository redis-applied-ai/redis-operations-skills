---
name: redis-cloud-cost-report-analysis
description: "Download, interpret, and visualize Redis Cloud Cost Report CSV files. Use when the user asks for Redis Cloud cost reports, Billing and Payments Cost Report download, Owner or Billing Admin access, Google Sheets or Excel pivot tables, BI dashboards, Essentials versus Pro cost rows, database usage windows, network cost lines, tags for cost allocation, marketplace invoice mismatch, blank or slow report downloads, or FinOps analysis."
---

# Redis Cloud Cost Report Analysis

Use this skill when a user needs to download, interpret, visualize, or troubleshoot the Redis Cloud Cost Report.

## Current-State Rule

Cost reporting, network line behavior, and API availability can change. Verify current Redis Cloud console/docs behavior before making claims about automation, GA status, or exact report fields.

## Access Requirements

- User must have Redis Cloud Owner or Billing Admin role.
- Viewer roles do not have billing report access.
- Report data is sensitive financial information; do not ask users to paste full account exports unless needed and approved.

## Download Workflow

1. Sign in to Redis Cloud Console.
2. Open `Billing & Payments`.
3. Select `Cost Report`.
4. Wait for CSV generation and download.
5. For large accounts, wait for generation to finish before retrying.

Current-month reports may show costs up to the report generation time and may not include finalized month-end adjustments.

## Report Interpretation

| Area | How to interpret |
| --- | --- |
| Essentials subscriptions | Usually one monthly row per subscription with fixed plan details. |
| Pro or flexible subscriptions | Multiple rows can appear by database, region, usage window, and intra-month changes. |
| Network charges | May appear as subscription-level line items; database-level granularity may not be available. |
| Tags | Useful for cost allocation when configured and supported for the subscription type. |
| List price | CSV may show Redis list price; discounts, credits, taxes, and marketplace adjustments can appear elsewhere. |
| Marketplace billing | Reconcile with AWS/GCP billing portals for total cost. |

## Spreadsheet Workflow

1. Import the CSV into Google Sheets or Excel.
2. Create a pivot table.
3. Suggested dimensions:
   - Rows: database name, subscription name, region, or tag.
   - Columns: month or billing period.
   - Values: total cost.
   - Filters: plan, subscription, region, HA, tags, or RBU type.
4. Add charts for spend by database, subscription, region, or tag over time.
5. Keep raw CSV data on a separate tab for auditability.

## BI Workflow

- Load the CSV into Tableau, Power BI, Looker, or an internal warehouse.
- Join with cloud provider billing exports when using AWS/GCP Marketplace.
- Normalize subscription IDs, database IDs, tags, and billing months.
- Separate Redis usage, network charges, discounts, credits, and marketplace charges.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Report missing or privileged access error | User is not Owner or Billing Admin. |
| Blank report | No usage history, wrong account, permissions, or browser/session issue. |
| Slow generation | Large account or long date range; wait and avoid repeated clicks. |
| Network line missing for recent month | Month-end costs may not be finalized; retry after finalization window. |
| Older months show zero network cost | Network reporting may not apply historically. |
| Tags missing | Tag support depends on subscription type and tag setup. |
| CSV differs from invoice | Invoice may include discounts, credits, taxes, or marketplace/provider charges. |
| Automation fails | Verify current report API support; UI-only flows can be blocked by browser security controls. |

## Escalation Packet

Collect:

- Redis Cloud account ID.
- User role.
- Billing month or date range.
- Whether billing is Redis-direct, AWS Marketplace, or GCP Marketplace.
- Report download error text or browser behavior.
- Whether the account has usage history.
- Whether network charges, tags, or specific databases are missing.
- Invoice or marketplace discrepancy summary, without sensitive payment details.
