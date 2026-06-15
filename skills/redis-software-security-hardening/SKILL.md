---
name: redis-software-security-hardening
description: Use when hardening Redis Software security, including private network deployment, HTTPS-only UI/API, RBAC, ACLs, LDAP, deactivating the default user, strong database passwords, TLS, CA-signed certificates, mTLS, cipher suites, certificate rotation, antivirus exclusions, remote syslog, audit logging, failed-login alerts, or CVE/security-advisory routing.
---

# Redis Software Security Hardening

Use this skill as a production security checklist for Redis Software. For CVEs, vulnerabilities, security advisories, patch status, or support-window claims, verify current official Redis security sources before answering.

## Security Layers

Harden in this order:

1. Network exposure and firewalling.
2. Control-plane access for UI and API.
3. Database user access and ACLs.
4. TLS and certificate trust.
5. LDAP or identity integration.
6. Logging, auditing, alerting, and retention.
7. Operational host exclusions and monitoring.

## Network And Control Plane

- Deploy Redis Software in a private trusted network.
- Do not expose management UI, REST API, or database endpoints directly to the public internet.
- Require HTTPS for UI and API access.
- Disable unencrypted API endpoints when current version and policy allow.
- Restrict database users from cluster-control access.
- Use firewall rules and routing controls to limit management access.

## Users, RBAC, And ACLs

- Use RBAC for admin console and API access.
- Use ACLs for database users and reusable data-access policies.
- Assign least privilege by role.
- Test access with representative users.
- Deactivate the default database user only after alternative users and application credentials are confirmed working.
- Audit user and role assignments regularly.

## Database Passwords

- Enforce strong passwords according to the organization's policy.
- Rotate database credentials.
- Use a password manager or secrets manager.
- Avoid sharing application credentials with human operators.
- Monitor failed authentication attempts.

## TLS And Certificates

- Enable TLS for client, proxy, node-to-node, sync, and replication paths where supported and required.
- Use CA-signed certificates for production when organizational policy requires it.
- Monitor certificate expiration.
- Rotate certificates on a planned schedule.
- Enable mTLS when mutual authentication is required.
- Validate cipher suite and protocol choices against compliance requirements.

Before certificate changes, confirm SANs, chain, private key match, and client trust-store impact.

## LDAP And Identity

- Use LDAP integration when organization policy centralizes identities there.
- Map LDAP groups to Redis Software RBAC roles.
- Confirm Redis Software nodes can reach LDAP hosts and ports.
- Test a non-admin and admin login path before enforcement.

## Auditing And Logs

- Enable auditing for logins, role changes, configuration changes, and failed authentication.
- Forward logs to remote syslog or centralized log storage.
- Alert on suspicious login failures, privilege changes, and certificate or LDAP errors.
- Keep local and remote retention aligned with policy.

## Host Operations

If antivirus or endpoint protection runs on Redis Software nodes, configure exclusions for Redis Software installation, binary, configuration, library, and provisioning directories according to current Redis guidance and organizational policy.

## Response Pattern

Answer with:

1. The relevant security layer.
2. Current state to verify.
3. Concrete hardening action.
4. Validation command or test.
5. Current official source check when the topic is CVEs, patches, support windows, or version-specific security behavior.
