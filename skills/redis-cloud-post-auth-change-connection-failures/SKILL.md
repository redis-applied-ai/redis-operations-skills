---
name: redis-cloud-post-auth-change-connection-failures
description: Use when Redis Cloud applications or tools fail after recent ACL, RBAC, password, default user, passwordless access, TLS, certificate, secret-store, endpoint, or authentication configuration changes, especially errors such as `WRONGPASS`, `NOAUTH`, `NOPERM`, auth failed, timeouts, immediate disconnects, stale Kubernetes/Vault/CI secrets, Redis Insight saved credentials, or clients not restarted after rotation.
---

# Redis Cloud Post-Auth-Change Connection Failures

Use this skill when a Redis Cloud connection failure begins immediately after an authentication, access-control, TLS, or secret-management change.

## First Question

Identify the exact change before troubleshooting symptoms:

- password rotation or reset
- RBAC/Data Access Control user update
- default user disabled or password removed
- passwordless access enabled
- TLS, certificate, CA, or port setting changed
- secret store, environment variable, connection string, or client config changed
- Redis Insight or monitoring tool connection profile updated

## Error Classifier

| Error | Meaning | First check |
| --- | --- | --- |
| `WRONGPASS` after password rotation | stale secret or wrong auth mode | Update every secret source and restart cached clients. |
| `WRONGPASS` after RBAC/user change | client may still send password-only auth | Configure username and password; verify user enabled and scoped to database. |
| `NOAUTH` | client did not send credentials or uses wrong auth field | Mirror a working `redis-cli` connection config. |
| `NOPERM` | auth succeeded but command/key/database access is insufficient | Use `redis-cloud-rbac-acl` to inspect role, ACL, key pattern, and command permissions. |
| timeout or disconnect | TLS, endpoint, port, CA trust, or network path mismatch | Verify protocol, port, and network reachability. |
| multiple databases fail | account, subscription, billing, or shared secret problem | Check account/subscription status before rotating again. |

## Same-Path Redis CLI Test

Run from the same runtime network as the failing app whenever possible.

TLS with ACL user:

```bash
redis-cli -h <host> -p <port> --tls --user <username> --pass '<password>' PING
```

TLS with default user:

```bash
redis-cli -h <host> -p <port> --tls -a '<password>' PING
```

If CLI succeeds, focus on application config, stale secret sources, connection-string encoding, Redis Insight saved settings, or a missing restart. If CLI fails, continue checking database auth mode, user state, role mapping, TLS, endpoint, and account status.

## Secret Synchronization Checklist

Update every consumer:

- environment variables
- Kubernetes/OpenShift Secrets
- Vault or other secret managers
- CI/CD variables
- Redis Insight saved connections
- monitoring and automation tools
- worker, scheduler, and one-off job configs

Restart or redeploy clients that only load credentials at startup.

## Auth Mode Validation

Confirm current database expectation:

- default user: password only or implicit `default`
- RBAC/database access user: username plus password
- passwordless: do not send `AUTH`
- TLS required: use TLS URI/settings and correct CA trust before AUTH

Use Redis Cloud Console as the source of truth for current endpoint, port, TLS requirement, user state, role assignment, and database access.

## Evidence Packet

Collect with secrets redacted:

- exact change and timestamp
- endpoint, port, and TLS setting
- authentication model before and after
- exact error text
- same-path `redis-cli` result
- whether clients were restarted or redeployed
- secret stores updated versus pending
- affected clients/tools and whether all databases or one database fails
- role/ACL details for `NOPERM` cases
