---
name: redis-cloud-okta-saml-sso-troubleshooting
description: Use when Redis Cloud SAML SSO with Okta fails during activation or login, including redisAccountMapping attribute problems, account owner requirement, lowercase role values, DNS domain verification, X.509 certificate formatting, Okta Profile Editor mapping, dummy ACS/metadata bootstrap URLs, user assignment, or Redis Cloud role provisioning failures.
---

# Redis Cloud Okta SAML SSO Troubleshooting

Use this skill to diagnose Redis Cloud SAML SSO activation or login failures when Okta is the identity provider.

## Safety Rules

- Treat SAML traces, HAR files, cookies, assertions, certificates, and user attributes as sensitive.
- Do not ask for IdP admin credentials, private keys, full SAML assertions, or unredacted HAR files in chat.
- Keep at least one verified Redis Cloud owner recovery path until SAML is proven working.
- Verify current Redis Cloud SAML documentation before asserting exact UI labels or supported role names.

## First Questions

Collect:

- Redis Cloud account ID and verified domain status
- Redis Cloud role of the user trying to activate SAML
- Okta app assignment status for that user
- exact activation or login error
- whether failure occurs during setup save, first IdP login, or later user login
- whether the Okta Profile Editor custom attribute was added and mapped into the SAML assertion

## Activation Prerequisites

Confirm these before debugging deeper:

1. The Redis Cloud account domain is verified.
2. The activating Redis Cloud user is an account owner.
3. Okta has a SAML app assigned to the activating user.
4. Okta sends the required Redis Cloud account mapping attribute.
5. The X.509 certificate was copied in the format Redis Cloud expects.

If the activating user is not mapped as owner for the target account, activation can fail even if the user is an Okta admin.

## Required Okta Attribute

Okta must send `redisAccountMapping` in the SAML assertion. It maps Redis Cloud account IDs to Redis Cloud roles.

Example shape:

```text
<account-id>=owner
<account-id>=viewer
```

Checks:

- account IDs match real Redis Cloud account IDs
- the activating account uses `owner`
- role values are lowercase
- no extra spaces, smart quotes, or copied formatting are present
- the Profile Editor attribute exists and is included in the SAML app attribute statements
- the assigned Okta user or group actually receives the value

Common failure: the attribute exists in Okta but is not passed in the SAML assertion because it was not added to the SAML app attribute statements.

## Certificate And Metadata Checks

Validate:

- Redis Cloud has the current Okta signing certificate.
- Certificate text is pasted exactly in the format the Redis Cloud UI requests.
- Expired or rotated Okta certificates have been updated in Redis Cloud.
- Entity ID and ACS URL match the Redis Cloud generated service provider metadata after setup.

Do not add or remove certificate boundary lines unless the Redis Cloud UI explicitly asks for that format.

## Okta Bootstrap Flow

Some Okta setup flows start with temporary ACS or metadata URLs so Redis Cloud can generate service provider metadata later.

If the user is stuck during this stage:

- confirm they followed the Redis Cloud setup sequence in order
- verify they replaced temporary Okta values with the Redis Cloud generated values when prompted
- ensure the Okta app is assigned to the activating user before the first login test
- retry in a clean browser session after changes to avoid stale SSO cookies

## Domain Verification

Redis Cloud SAML activation requires domain ownership verification.

Check:

- the DNS TXT record was created in the correct zone
- the value matches Redis Cloud exactly
- DNS propagation has completed
- the Redis Cloud Console shows the domain as verified before enabling SAML

If domain verification is blocked, solve DNS first; SAML troubleshooting will be misleading until the domain is verified.

## Login Failure Triage

| Symptom | Likely Cause | Next Check |
| --- | --- | --- |
| Activation fails to save | missing or malformed `redisAccountMapping` | inspect Okta assertion attributes |
| Activation user rejected | mapped role is not `owner` | map target account ID to `owner` |
| User logs in but has no access | account ID or role missing from assertion | verify user/group attribute assignment |
| Authorization fails | role casing or value mismatch | use lowercase role values |
| Certificate or metadata error | copied certificate or SP metadata mismatch | refresh Okta certificate/SP settings |
| SSO redirect loop | stale browser session or app assignment issue | test private browser and Okta assignment |
| Domain verification failure | TXT record missing or wrong | fix DNS and reverify in Redis Cloud |

## Evidence To Collect

Use redacted artifacts:

- Redis Cloud account ID and expected role
- screenshot or text of Redis Cloud domain verification status, without secrets
- Okta SAML attribute statement names and non-secret shape
- sanitized SAML trace showing `redisAccountMapping` presence and role value casing
- certificate issuer/expiration metadata, not private keys
- exact Redis Cloud error message and timestamp
- Okta sign-in event outcome for the same timestamp

## Response Shape

When answering, provide:

1. The most likely failure class.
2. The exact Okta or Redis Cloud field to verify.
3. Whether the activating user has the required owner mapping.
4. The next safe test.
5. What evidence to collect if Redis Support or the IdP admin must be involved.
