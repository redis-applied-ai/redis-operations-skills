---
name: redis-software-saml-sso-troubleshooting
description: Use when Redis Software SAML SSO login, activation, JIT provisioning, role mapping, IdP metadata, X.509 certificate validation, ACS or Entity ID matching, NameID email mapping, redisRoleMapping, firstName, lastName, email attributes, 400 GENERAL NONSUCCESS, login redirects, or SSO lockout recovery must be diagnosed.
---

# Redis Software SAML SSO Troubleshooting

Use this skill to diagnose SAML SSO failures in Redis Software. Most failures are caused by missing assertion attributes, role UID mapping errors, certificate or metadata drift, or IdP configuration mismatches.

## Safety And Access

- Keep at least one local Redis Software admin account that can sign in without SSO.
- Do not disable local recovery paths until SSO is proven working.
- Treat SAML traces and HAR files as sensitive; redact tokens, assertions, cookies, and personal data before sharing.
- Work with the IdP administrator for user assignment, attributes, and certificate metadata.

## First Classification

Classify the symptom:

- redirected back to login page
- HTTP 400 or generic SAML failure
- invalid certificate or signature validation error
- new JIT users are not created
- login succeeds but user has no access
- SSO stopped working suddenly after IdP change or certificate rotation
- users are locked out after SSO enforcement

## Required Assertion Checks

Use a SAML tracing tool to verify:

- SAML response is signed
- `firstName` is present and non-empty
- `lastName` is present and non-empty
- `email` is present and non-empty
- `NameID` contains the user email in the expected format
- `NameID` email matches the Redis Software username or email for existing users
- for new JIT users, `redisRoleMapping` is present and contains valid role UIDs

## Role Mapping Rules

- `redisRoleMapping` should contain role UIDs, not display names.
- Role UIDs are case-sensitive.
- It can contain multiple role UIDs when multiple roles should be assigned.
- It applies to new JIT-provisioned users.
- Existing Redis Software users keep their assigned roles; changing the assertion alone may not update them.

If an existing user logs in but lacks access, inspect their role assignment in Redis Software directly.

## Metadata And Certificate Checks

Validate:

- IdP X.509 certificate is pasted exactly as provided
- certificate is not expired
- Redis Software has current IdP metadata after rotation
- ACS URL matches the Redis Software SSO configuration
- Entity ID matches the Redis Software SSO configuration
- IdP binding matches the expected flow
- attributes are assigned to users and to the SAML app

Refresh metadata after changing certificates, endpoints, or attributes.

## Browser Checks

Use:

- private or incognito browser session
- no request-modifying extensions
- cleared cookies for Redis Software and IdP domains

This helps separate browser state from SAML assertion or metadata problems.

## Support Evidence

Collect:

- Redis Software version
- IdP type
- exact UI error
- sanitized SAML trace
- sanitized HAR capture if requested
- SSO configuration values, excluding secrets
- whether the user is new JIT or existing
- role UID values expected in `redisRoleMapping`

## Response Pattern

Answer with:

1. The most likely SAML failure class.
2. The exact assertion, role, metadata, or certificate check.
3. The fix in Redis Software or the IdP.
4. Local admin recovery guidance if SSO enforcement caused lockout.
5. Sanitized evidence to collect for Support if the failure persists.
