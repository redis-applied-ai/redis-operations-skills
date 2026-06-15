---
name: redis-software-credential-certificate-rotation
description: "Plan and troubleshoot Redis Software credential and certificate rotation. Use when the user asks to rotate Redis Enterprise Software passwords, REST API credentials, database user credentials, TLS certificates, customer-managed internode certificates, fix TLS handshake failures, handle password expiration or lockout, or use `/v1/users/password` or `/v1/cluster/certificates/rotate`."
---

# Redis Software Credential Certificate Rotation

Use this skill for Redis Software credential, password, and certificate rotation planning. Treat rotation as a production change unless the user proves the cluster is disposable.

## Safety Rules

- Never ask users to paste passwords, API secrets, private keys, certificates, or keystores into chat.
- Verify the Redis Software version and current official API behavior before relying on version-specific behavior such as customer-managed internode certificates or forced disconnects.
- Use a maintenance window for certificate trust changes or any rotation that cannot be staged.
- Update applications, automation, monitoring, and secrets managers before removing old credentials or trust material.
- Keep rollback material available until all clients have proven they can authenticate and complete TLS handshakes.

## Rotation Decision Tree

| Situation | Workflow |
| --- | --- |
| User or API password rotation | Add new password, update clients, verify, then remove old password. |
| Default user password rotation | Confirm whether the staged REST flow is supported; default users cannot use the multi-password rotation flow. |
| Database user or ACL/RBAC change | Inventory roles, update least-privilege credentials, then roll clients by group. |
| Cluster/API/client certificate rotation | Add or rotate certificates, update client trust stores, verify, then retire old trust material. |
| Customer-managed internode certificates | Verify Redis Software 8+ support and required REST workflow before planning. |
| Password expiration or lockout | Reset through self-service, SSO identity provider, or an administrator; then update stored secrets. |
| Suspected compromise | Rotate immediately, revoke old credentials, preserve logs, and audit access. |

## Password Rotation Workflow

1. Inventory affected users, databases, client applications, monitoring jobs, CI/CD jobs, and secrets managers.
2. Confirm whether the user supports staged password rotation through the REST API.
3. Add the new password without invalidating the old one:

   ```http
   POST https://<cluster-host>:9443/v1/users/password
   Content-Type: application/json

   {
     "username": "<username>",
     "new_password": "<new-password>"
   }
   ```

4. Update secrets managers, application configs, automation, monitoring, and database clients.
5. Restart or reload clients that do not reread credentials dynamically.
6. Verify sign-in, API access, database connections, and automation.
7. Remove the old password after all consumers have moved:

   ```http
   DELETE https://<cluster-host>:9443/v1/users/password
   Content-Type: application/json

   {
     "username": "<username>",
     "old_password": "<old-password>"
   }
   ```

8. Record the rotation timestamp, operator, affected users, and validation evidence.

## Certificate Rotation Workflow

1. Identify the certificate scope: cluster UI/API, database endpoint, client authentication, replication, or internode traffic.
2. Verify certificate format, expiration, SANs, CA chain, cipher compatibility, and required extended key usage. For internode and client authentication, confirm TLS Web Client Authentication requirements.
3. Add or rotate certificates through the supported Redis Software REST API path, such as:

   ```http
   POST https://<cluster-host>:9443/v1/cluster/certificates/rotate
   ```

4. Update clients, trust stores, service meshes, sidecars, and monitoring probes before retiring old certificates.
5. Validate TLS handshakes from representative clients and automation.
6. Remove old certificates only after all client populations have been verified.
7. For scheduled rotation jobs, confirm the cron expression, pre-expiry trigger, notification path, and failure handling.

## Password Expiration Recovery

1. Confirm the symptom: expired-password message, repeated authentication failures, or multiple users blocked at the same time.
2. If SSO is enabled, reset through the identity provider.
3. If self-service reset is available, use the cluster sign-in password reset flow.
4. Otherwise, ask a cluster or organization administrator to reset or unlock the account.
5. Replace stale passwords in local keychains, config files, environment variables, CI/CD variables, and secrets managers.
6. Rerun failed jobs and verify interactive and non-interactive access.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Connections fail after password rotation | Client, script, or secrets manager still uses old credentials. |
| REST API returns 400 or 403 | Unsupported user flow, bad request body, wrong credentials, or cluster health issue. |
| TLS handshake failure | Expired, mismatched, untrusted, or wrong-scope certificate; verify CA chain, EKU, SANs, and cipher support. |
| Old connections remain open | Clients have not reauthenticated; verify version-specific disconnect behavior and restart clients if required. |
| Password reset works but automation still fails | CI/CD, monitoring, or service account secret was not updated. |
| Internode certificate plan is blocked | Redis Software version or certificate attributes do not support the requested flow. |

## Escalation Packet

Collect:

- Redis Software version and cluster name.
- Credential or certificate type being rotated.
- Affected users, databases, endpoints, and client groups.
- Rotation method: UI, REST API, automation, SSO, or admin reset.
- Timeline of add, client update, validation, and removal steps.
- Exact HTTP status, authentication error, or TLS error with secrets redacted.
- Certificate metadata: issuer, subject, SANs, expiration, EKU, and chain source.
- Whether compromise, expiration, or routine policy triggered the rotation.
