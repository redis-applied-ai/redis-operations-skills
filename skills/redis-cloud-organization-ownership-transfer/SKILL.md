---
name: redis-cloud-organization-ownership-transfer
description: Use when transferring Redis Cloud organization ownership to a new email, replacing an Owner, moving billing ownership, migrating owner access without deleting subscriptions or databases, inviting a new Owner, handling SSO-controlled owner changes, rotating user-scoped API or CLI tokens, recreating MFA/security keys, or preventing lockout before downgrading or removing the old Owner.
---

# Redis Cloud Organization Ownership Transfer

Use this skill when a Redis Cloud organization must remain intact while ownership moves from one email identity to another.

## Core Rule

Redis Cloud account email addresses are not directly edited in place. Ownership transfer is an identity migration:

1. Invite or provision the new email.
2. Promote the new identity to Owner.
3. Validate organization and billing access.
4. Recreate user-scoped security items.
5. Downgrade or remove the old Owner only after validation.

## What Carries Over

Organization-level resources remain with the organization:

- subscriptions
- databases
- organization settings
- billing configuration after billing ownership/contact update
- role-based permissions assigned to the new user

User-scoped items do not automatically transfer:

- MFA authenticators and recovery codes
- personal API or CLI tokens
- security keys
- user-authorized integrations
- personal notification preferences

## Transfer Workflow

1. Confirm the requester is a current Owner or has verified authority to request ownership transfer.
2. Confirm old email, new email, organization name, and whether SSO/SAML is enforced.
3. If SSO is enforced, provision the new identity in the identity provider before Redis Cloud role changes.
4. Invite the new email from Team or Access Management.
5. Have the new user accept the invitation and complete login, MFA, or SSO setup.
6. Promote the new user to Owner if it was not assigned during invitation.
7. Validate the new Owner can:
   - manage team members
   - access billing
   - modify subscriptions
   - view and manage databases
8. Update billing owner, billing contact, invoice email, and notification destinations.
9. Recreate user-scoped tokens, integrations, security keys, and MFA on the new account.
10. Rotate dependent application, CI/CD, automation, and monitoring credentials.
11. Downgrade or remove the old Owner only after all validation passes.

## Special Scenarios

| Scenario | Guidance |
| --- | --- |
| Old email still signed in but mailbox lost | Complete transfer immediately while the session is available; validate new Owner before ending the old session. |
| Cannot sign in as old Owner | Escalate to Redis Support with ownership and billing evidence. |
| SSO blocks invitation | Ask the IdP administrator to provision and assign Redis Cloud access, then validate role inside Redis Cloud. |
| Multiple organizations | Repeat owner and billing validation for each organization. |
| Multiple subscriptions or billing contacts | Update each billing owner/contact path, not only the organization role. |

## Lockout Prevention

Before old Owner removal, confirm:

- new email appears as Owner
- billing ownership and invoice routing are updated
- MFA is enabled for the new Owner
- API/CLI tokens have been recreated and dependent systems updated
- integrations have been reauthorized
- old email is no longer the only Owner

Do not ask users to share passwords, MFA recovery codes, full payment details, or secret token values.

## Escalation Packet

For Support-assisted transfer, collect only non-secret evidence:

- organization name
- old and new email addresses
- billing contact email
- recent invoice number or payment reference
- subscription IDs or names
- whether SSO/SAML is enforced
- what step is blocked and any exact error text
