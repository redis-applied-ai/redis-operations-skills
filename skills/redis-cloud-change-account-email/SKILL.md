---
name: redis-cloud-change-account-email
description: "Guide Redis Cloud account email changes by adding a new user, transferring ownership/access, updating billing and notifications, recreating MFA/API tokens/integrations, and safely downgrading or removing the old user. Use when the user asks to change an email address, replace an account owner, migrate Redis Cloud access to a new email, or recover from removing the old user too early."
---

# Redis Cloud Change Account Email

Use this skill when a Redis Cloud user wants to change the email address associated with account access. Redis Cloud does not directly edit an existing account email; the safe path is an access migration.

## Core Rule

Do not present this as a direct email-edit operation. The procedure is:

1. Add the new email as a user.
2. Grant the needed role, usually Owner for an owner replacement.
3. Validate access and billing.
4. Recreate security settings, tokens, and integrations.
5. Downgrade or remove the old user only after validation.

## Workflow

1. Confirm context:
   - Redis Cloud account and organization.
   - Old email and new email.
   - Whether the old user is an Owner.
   - Whether SSO/SAML controls identity.
   - Whether API tokens, service accounts, CI/CD, monitoring, or billing depend on the old user.
2. Add the new user:
   - Sign in as a user with Owner permissions.
   - Open Access Management, Team.
   - Add the new email and assign the correct role.
   - Use Owner if the new user replaces the current owner.
3. Complete invitation:
   - New user accepts invitation.
   - New user sets password and completes account setup.
4. Validate the new user:
   - Databases are visible.
   - Team management is available.
   - Billing settings are accessible.
   - Administrative actions work.
5. Update billing and notifications:
   - Update billing ownership if applicable.
   - Update notification, alert, and operational email destinations.
6. Recreate security and integrations:
   - Configure MFA.
   - Recreate API tokens.
   - Update service accounts or external integrations if needed.
   - Update CI/CD, monitoring, automation, and other external systems.
7. Remove or downgrade old user:
   - Prefer temporary downgrade for rollback safety.
   - Remove only after the validation checklist passes.

## Validation Checklist

Before removing the old user, verify:

- New user has Owner role when ownership is being transferred.
- Billing access and billing ownership are updated.
- All databases are visible and accessible.
- MFA is configured on the new account.
- API tokens and integrations have been recreated or updated.
- Alerts and notifications route to the new email.
- No automation, CI/CD, monitoring, or external systems depend on the old account.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| New user cannot access billing | Confirm Owner role and billing ownership/update state. |
| Integrations fail after migration | Recreate API tokens and update dependent systems. |
| Resources are missing | Confirm organization membership and assigned role. |
| Access lost after old user removal | Escalate to Redis Support with ownership and account evidence. |
| SSO/SAML user identity differs | Coordinate with the identity provider administrator before changing Redis Cloud users. |

## Safety Checks

- Do not remove the old user until the new user has been fully validated.
- Do not assume MFA, tokens, service accounts, or integrations transfer automatically.
- Do not ask for passwords, MFA recovery codes, or secret tokens in chat.

## Escalation Packet

Collect:

- Redis Cloud account/organization.
- Old and new email addresses.
- Current roles for both users.
- Whether SSO/SAML is enabled.
- Billing ownership state.
- What validation failed.
- Whether the old user was removed or downgraded.
