---
name: redis-cloud-billing-permissions
description: "Verify Redis Cloud account ownership and billing permissions for subscription cancellation, downgrade, or billing changes. Use when the user cannot see or cancel a subscription, is unsure which Redis Cloud login owns it, has multiple organizations, signed in with Google, GitHub, email/password, or SSO, needs Owner/Admin/Billing Admin role checks, must recover access, or purchased through AWS, GCP, Azure, Heroku, or Vercel."
---

# Redis Cloud Billing Permissions

Use this skill when a user cannot find, cancel, downgrade, or manage billing for a Redis Cloud subscription.

## Core Rule

Billing actions require the correct Redis Cloud organization, the correct owning identity, and the required role: Owner, Admin, or Billing Admin. Billing email alone is a clue, not proof of ownership.

## Key Concepts

| Term | Meaning |
| --- | --- |
| Owning account | Redis Cloud identity under which the subscription was created or upgraded. |
| Purchasing identity | User/sign-in provider that completed checkout or upgrade. |
| Billing contact | Email receiving invoices; may be a shared mailbox or forwarding alias. |
| Sign-in method | Email/password, Google, GitHub, or SSO can represent different identities even with similar email addresses. |
| Organization | Redis Cloud container where the subscription lives; users may belong to multiple orgs. |

## Verification Workflow

1. Ask what billing action is needed: cancel, downgrade, payment update, invoice access, or ownership transfer.
2. Identify the likely owning identity:
   - Who completed the upgrade/purchase?
   - Which email receives invoices?
   - Which organization contains the subscription?
3. Check invoice or receipt clues:
   - Company name.
   - Plan or subscription name.
   - Invoice ID.
   - Charge date and amount.
   - Last four digits of payment method, if shown.
4. Sign in using the original provider used at purchase time:
   - Email/password.
   - Google.
   - GitHub.
   - SSO.
5. Switch to the correct Redis Cloud organization.
6. Open `Organization` then `Members`.
7. Confirm the user has Owner, Admin, or Billing Admin role.

## Access Recovery

| Situation | Action |
| --- | --- |
| Email/password account | Use password reset for the owning login email. |
| SSO-managed org | Contact IdP/SSO admin for group assignment or account restoration. |
| Another Owner exists | Ask them to cancel/downgrade or grant billing permissions. |
| User cannot see owners | Use receipts/invoices and support escalation with proof of relationship. |
| Same email, wrong login method | Try the original auth provider used to create or upgrade the subscription. |

## Third-Party Purchase Routing

If purchased externally, cancellation/downgrade may happen outside Redis Cloud:

| Channel | Where to manage |
| --- | --- |
| AWS Marketplace | AWS Marketplace and AWS account billing. |
| Google Cloud Marketplace | GCP Marketplace and GCP billing account. |
| Microsoft Azure managed Redis offerings | Azure Portal billing/subscription area. |
| Heroku add-on | Heroku add-on billing and plan controls. |
| Vercel integration | Vercel Marketplace/integration billing. |

## Common Failure Modes

- User is logged in with a different sign-in provider than the purchasing identity.
- User is viewing the wrong organization.
- User is in the right organization but lacks Owner/Admin/Billing Admin role.
- Billing receipts go to a shared alias, not the login identity.
- Marketplace purchase must be managed through the provider.

## Escalation Packet

Collect:

- Subscription ID or name.
- Redis Cloud organization name.
- Billing email/contact.
- Invoice ID, charge date, and amount.
- Login methods tried.
- User's current role in the organization.
- External purchase channel, if any.
- Marketplace account or provider billing context, without credentials or payment secrets.
