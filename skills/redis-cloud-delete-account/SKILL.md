---
name: redis-cloud-delete-account
description: "Guide Redis Cloud account deletion and personal data erasure readiness. Use when the user asks to delete or close a Redis Cloud account, remove all Redis Cloud resources, submit a privacy deletion request, clear account deletion blockers, remove users or API keys, handle SAML/SSO users, resolve unpaid invoices, or unlink AWS/GCP Marketplace billing before closure."
---

# Redis Cloud Delete Account

Use this skill when the goal is full Redis Cloud account closure, not just stopping one subscription. Account deletion is irreversible and requires the Account Owner.

## Safety Rules

- Confirm whether the user wants full account deletion or only subscription cancellation.
- Require backup/export decisions before deleting databases.
- Do not collect full payment card details, credentials, or API key secrets.
- Treat account closure and privacy erasure as irreversible.
- Do not promise deletion until all resources, billing blockers, and identity requirements are cleared.

## Account Closure Prerequisites

The Account Owner must clear the account in this order:

1. Delete all databases.
2. Delete all subscriptions.
3. Remove all users except the Account Owner.
4. Remove user and account API keys.
5. Pay outstanding invoices.
6. Remove payment methods and marketplace links.
7. Submit the Redis privacy request for final account and personal data erasure.

## Decision Tree

| User goal | Guidance |
| --- | --- |
| Stop billing for one environment | Cancel or delete the subscription; full account deletion is not required. |
| Delete all data and account access | Follow the full account closure prerequisite sequence. |
| SAML/SSO account cleanup | Remove users in the identity provider, then verify Redis Cloud users/API keys. |
| Marketplace-linked account | Unlink or cancel through AWS/GCP Marketplace before final closure. |
| Non-owner wants removal | They cannot close the account; an Account Owner or IT admin must act. |

## Resource Cleanup Workflow

1. Verify the signed-in user is the Account Owner.
2. Delete databases from each subscription after confirming backups.
3. Delete subscriptions only after all databases are gone.
4. Remove team members through `Access Management`.
5. For SAML/SSO accounts, coordinate user removal through the identity provider.
6. Delete all API keys manually, including automation keys.
7. Resolve outstanding invoices in billing.
8. Remove payment methods and marketplace billing links.
9. Submit the privacy/account erasure request.
10. Watch for confirmation email or rejection details listing remaining blockers.

## Common Blockers

| Blocker | Action |
| --- | --- |
| Databases still exist | Delete every database first. |
| Subscriptions still exist | Delete or cancel subscriptions after databases are removed. |
| User is not Owner | Log in as Account Owner or ask the Owner to perform closure. |
| Outstanding invoices | Pay balances in Billing and Payments. |
| Marketplace billing remains linked | Cancel or unlink in the provider marketplace portal. |
| SAML/SSO users remain | Remove users in the IdP and verify Redis Cloud state. |
| UI is locked by maintenance | Wait for maintenance or background operation to complete. |
| Suspended billing state | Clear payment issue before retrying closure steps. |

## Privacy Request Guidance

Only submit the privacy erasure request after the account is clear. Redis may retain required billing or operational records according to legal obligations, even after account closure.

## Escalation Packet

Collect:

- Account ID or account email.
- Confirmation that the requester is the Account Owner.
- Remaining databases and subscriptions, if any.
- User and API key cleanup status.
- Billing status and unpaid invoice references.
- Payment method or marketplace linkage.
- SAML/SSO identity provider involvement.
- Privacy request status or rejection reason.
