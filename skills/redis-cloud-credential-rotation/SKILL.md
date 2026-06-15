---
name: redis-cloud-credential-rotation
description: "Plan and troubleshoot Redis Cloud credential rotation for database passwords, ACL/RBAC users, API keys, cloud provider credentials, and TLS/mTLS certificates. Use when the user asks to rotate Redis Cloud passwords, API keys, client certificates, BYOC or marketplace credentials, update secrets managers, avoid downtime during rotation, investigate authentication failures after rotation, or handle suspected credential compromise."
---

# Redis Cloud Credential Rotation

Use this skill for Redis Cloud secure-access management and credential rotation.

## Safety Rules

- Never ask users to paste passwords, API secrets, private keys, or client certificates into chat.
- Use secrets managers or environment variables with restricted access.
- Schedule disruptive rotations during low-traffic windows unless using a dual-credential path.
- Rotate immediately after suspected compromise or staff turnover.
- Verify current Redis Cloud security features and plan support before promising zero-downtime behavior.

## Rotation Decision Tree

| Credential type | Preferred pattern |
| --- | --- |
| Default database password | Rotate in console/API, then update all clients; only one password may be active. |
| Custom ACL/RBAC users | Create/update least-privilege users and roll clients gradually when supported. |
| Redis Cloud API key | Create new key, update automation, then revoke old key. |
| mTLS client certificate | Add new cert while old remains valid, migrate clients, then remove old cert. |
| BYOC/marketplace cloud credentials | Rotate through Cloud Account settings or provider-specific managed flow. |
| SAML/SSO console password | Follow identity provider policy, not Redis Cloud password policy. |

## Database Password Rotation

1. Identify database, users, and all dependent clients.
2. Confirm whether default user or custom RBAC users are used.
3. For default user:
   - Open database Security.
   - Edit password.
   - Save.
   - Update client connection strings and secrets managers immediately.
   - Expect old connections to fail when they reauthenticate.
4. For lower disruption:
   - Prefer custom users and least-privilege RBAC roles where the environment supports staged migration.
   - Roll clients one group at a time.

## API Key Rotation

1. Open Account, API Keys.
2. Create a new API key and secret.
3. Store it in the approved secrets manager.
4. Update CI/CD, automation, Terraform, monitoring, and integrations.
5. Verify the new key works.
6. Revoke or delete the old key.

## mTLS Certificate Rotation

1. Add the new client certificate while the old certificate remains valid.
2. Deploy the new certificate/key to clients.
3. Restart or reload clients as needed.
4. Verify successful TLS handshakes.
5. Remove the old certificate after all clients are migrated.

## Cloud Provider Credential Rotation

- For managed integrations, check whether Redis Cloud rotates and validates credentials automatically.
- For customer-provided credentials, update them in Cloud Account settings according to internal security policy.
- Verify resource access after rotation.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Authentication fails after password rotation | Client still uses old password or wrong username. |
| API access denied | Automation still uses revoked/old API key. |
| Cloud resource credential invalid | Provider credential expired, revoked, or not updated in Redis Cloud. |
| Connections drop after password change | Clients must reauthenticate; rotation was not staged. |
| TLS handshake failure | Client cert/key/CA not updated or certificate trust mismatch. |

## Best Practices

- Use RBAC and per-user credentials instead of shared default credentials when possible.
- Enforce MFA or SAML SSO for console access.
- Use `rediss://` or equivalent TLS-enabled clients.
- Review CIDR/IP allowlists during rotation.
- Audit rotation events in Redis Cloud logs or a central SIEM.

## Escalation Packet

Collect:

- Credential type being rotated.
- Database/account/API integration affected.
- Rotation timestamp.
- Secret storage/update path.
- Clients or jobs updated versus still pending.
- Exact authentication/TLS/API error with secrets redacted.
- Whether compromise is suspected.
