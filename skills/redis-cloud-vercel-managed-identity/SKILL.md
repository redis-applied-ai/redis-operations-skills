---
name: redis-cloud-vercel-managed-identity
description: "Troubleshoot Redis Cloud accounts created through the Vercel integration where email, team access, roles, billing, or notifications are controlled by Vercel. Use when Access Management or Add user is missing in Redis Cloud, email is read-only, Continue with Vercel is required, a Vercel email change is not reflected, a user switched Vercel accounts and lost access, or billing and plan changes route through Vercel Marketplace."
---

# Redis Cloud Vercel Managed Identity

Use this skill when the Redis Cloud subscription was created through the Vercel integration. In this flow, Redis Cloud receives identity and access from Vercel; do not use the normal Redis Cloud email-change or team-management workflow unless the subscription is direct Redis Cloud.

## Core Rule

For Vercel-integrated Redis Cloud accounts:

- Email shown in Redis Cloud is read-only because it comes from Vercel sign-in.
- Team membership and role changes are managed in the Vercel team that installed the Redis integration.
- Missing Redis Cloud `Access Management`, `Team`, or `Add user` controls can be expected.
- Billing and plan changes follow Vercel Marketplace or integration controls.
- Redis Support cannot directly override Vercel identity for a user who cannot access the Vercel account.

## Triage Workflow

1. Confirm this is a Vercel-integrated subscription:
   - User signs in with `Continue with Vercel`.
   - Redis Cloud account or database was created from Vercel Marketplace or Vercel integration.
   - Redis Cloud team-management controls are missing or limited.
2. Identify the requested change:
   - update displayed email
   - regain access after switching Vercel accounts
   - add or remove users
   - adjust roles
   - fix notification email routing
   - manage billing or plan changes
3. Have the user check the owning Vercel team:
   - Which Vercel team installed the Redis integration?
   - Is the current Vercel login a member or owner of that same team?
   - Is the intended email verified in Vercel?
4. Route the action:
   - Email display: update and verify the email in Vercel, then sign out of Redis Cloud and sign back in with `Continue with Vercel`.
   - New email identity: add the new account or email to the same Vercel team, then authenticate through Vercel.
   - User or role management: perform the change in Vercel team settings.
   - Billing or plan management: use the Vercel Marketplace or integration billing path.
5. Refresh Redis Cloud state:
   - Sign out of Redis Cloud.
   - Sign back in with `Continue with Vercel`.
   - Verify the expected email, team access, databases, and notifications.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Email is read-only in Redis Cloud | Vercel provides the identity | Change and verify the email in Vercel, then re-authenticate in Redis Cloud. |
| `Access Management`, `Team`, or `Add user` is missing | Vercel owns team access | Manage users and roles in the Vercel team that owns the integration. |
| User switched Vercel accounts and lost Redis Cloud access | New account is not in the installing Vercel team | Add the new Vercel account to that same team, then sign in again with Vercel. |
| Notifications still go to the old email | Redis Cloud still sees the old Vercel identity or session | Verify the new email in Vercel, remove stale email aliases if appropriate, and re-authenticate. |
| Cannot add or remove Vercel team members | Vercel plan or permission limitation | Verify current Vercel team permissions and plan behavior in Vercel before advising upgrade or role changes. |
| No access to the old email or Vercel login | Identity recovery is controlled by Vercel | Recover the Vercel account or team access through Vercel Support. |

## Direct Redis Cloud Contrast

Use direct Redis Cloud workflows only after confirming the subscription is not Vercel-integrated:

| Action | Vercel-integrated path | Direct Redis Cloud path |
| --- | --- | --- |
| Change displayed account email | Vercel account settings, then re-authenticate | Redis Cloud access migration or account email-change workflow |
| Add or remove users | Vercel team management | Redis Cloud Access Management |
| Change roles | Vercel team roles | Redis Cloud Access Management roles |
| Billing and plan changes | Vercel Marketplace or integration billing | Redis Cloud Billing |

## Safety Checks

- Do not tell the user to edit Redis Cloud email directly for Vercel-integrated subscriptions.
- Do not remove an old Vercel identity until the new Vercel identity can access the same team and Redis Cloud databases.
- Do not promise exact Vercel plan capability, billing behavior, or UI labels without checking current Vercel and Redis Cloud state.
- Do not ask for passwords, recovery codes, API keys, or payment details.

## Escalation Packet

Collect non-secret details:

- Redis Cloud organization or subscription name.
- Confirmation that sign-in uses `Continue with Vercel`.
- Owning Vercel team name.
- Old and new Vercel email identities.
- Current Vercel team membership and role.
- Exact missing control, error text, or stale email symptom.
- Whether the issue is access, notification delivery, role management, or billing.
