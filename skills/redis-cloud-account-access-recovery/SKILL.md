---
name: redis-cloud-account-access-recovery
description: Use when a Redis Cloud user cannot access their account due to forgotten password, missing activation email, wrong social login provider, GitHub or Google account mismatch, SAML SSO issues, lost access to account email, unavailable account owner, user not invited, ownership transfer, or billing-based identity verification.
---

# Redis Cloud Account Access Recovery

Use this skill to route Redis Cloud account access issues to the correct recovery path. Account recovery is security-sensitive: do not promise account changes until ownership or identity has been verified.

## First Classify The Login Method

Ask which method created the account:

- email and password
- Google social login
- GitHub social login
- SAML SSO

If the user is unsure, ask whether a password reset works, whether Google or GitHub creates an empty account, and whether their organization uses SSO.

## Recovery Paths

### Email And Password

If the user still controls the account email:

1. Use the password reset flow.
2. Check inbox, spam, and junk folders.
3. Confirm the account activation email was completed if the account is new or unverified.
4. Retry login after activation and password reset.

If no reset email arrives, collect non-sensitive account details and escalate.

### Social Login

If the account was created with GitHub or Google:

- use the same provider originally used
- confirm the browser is signed into the intended provider account
- avoid switching providers, which can create a separate empty account
- recover the provider account through that provider if access is lost

If account merge or provider switch is requested, explain that identity verification is required and that merge or transfer may not always be possible.

### SAML SSO

For SAML users:

- Redis Cloud access is controlled by the identity provider
- the user must work with their IdP or IT administrator
- verify user is active and has required group or role assignments
- Redis Support cannot bypass the IdP or force-create SAML users

Only account owners can change SAML settings in Redis Cloud.

### Not A User Or Owner Unavailable

If the user is not listed on the account:

- ask an existing owner or admin to invite them
- if the owner is unavailable, escalate with business justification and ownership evidence

Do not claim Redis can add users without verifying ownership and security context.

## Ownership Evidence

For support escalation, request only the minimum appropriate non-secret evidence:

- account email or organization name
- business justification
- billing address or account name on file
- recent invoice or transaction reference
- last payment amount
- last four digits of the payment card if needed for support verification

Never request full card number, CVV, full bank details, identity documents, or provider passwords.

## Browser Issues

If social login spins or redirects fail:

- allow third-party cookies, pop-ups, and redirects for Redis Cloud and the identity provider
- disable tracking protection or ad blockers temporarily
- try private browsing, another browser, or another network

## Response Pattern

Answer with:

1. The likely authentication path.
2. The first recovery action for that path.
3. What evidence is safe to collect if Support is needed.
4. Security boundaries: SSO and ownership changes require the appropriate administrator or verified ownership.
