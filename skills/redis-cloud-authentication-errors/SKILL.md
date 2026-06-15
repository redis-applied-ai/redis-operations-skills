---
name: redis-cloud-authentication-errors
description: Use when Redis Cloud clients fail with `WRONGPASS`, `AUTH failed`, invalid username-password pair, generic failed-to-connect after auth, stale credentials after password rotation, ACL user versus default user mismatch, disabled ACL user or missing role, passwordless database rejecting AUTH, TLS-required database receiving plaintext, wrong endpoint or port, passwords with special characters in Redis URIs, billing or subscription suspension causing auth failures, or Redis Insight/manual tool auth mismatch.
---

# Redis Cloud Authentication Errors

Use this skill when Redis Cloud is reachable but authentication or protocol setup fails.

## Safety Rules

- Never ask users to paste passwords, API secrets, private keys, or full connection strings with credentials.
- Prefer redacted config snippets showing field names, not secret values.
- Be careful with `MONITOR`, packet captures, and logs because they may expose credentials or customer data.
- Distinguish authentication errors from TLS, endpoint, and account-state failures before rotating passwords.

## First Classification

Identify which mode the database expects:

| Mode | Client behavior |
| --- | --- |
| Default user with password | Client sends password only or implicit `default` user. |
| ACL/Data Access Control user | Client sends both username and password. |
| Passwordless default user | Client must not send `AUTH`. |
| TLS-enforced database | Client must use TLS and the correct TLS port/CA config before AUTH. |

Also confirm the client is using the endpoint and port copied from the intended database and subscription.

## Common Causes

- stale password after rotation
- client sends default-user auth while database expects ACL username/password
- ACL user is disabled or lacks a role for the target database
- passwordless database receives an `AUTH` command
- client connects without TLS to a TLS-required database
- wrong host, port, subscription, or database endpoint
- shell or URI parsing breaks passwords with special characters
- account or subscription is suspended or restricted by billing/account status

## Redis CLI Validation

TLS with default user:

```bash
redis-cli -h <host> -p <port> --tls -a '<password>'
```

TLS with ACL user:

```bash
redis-cli -h <host> -p <port> --tls --user <username> --pass '<password>'
```

Non-TLS:

```bash
redis-cli -h <host> -p <port>
```

Then authenticate according to the expected mode and run:

```redis
PING
```

Use `--user` and `--pass` with shell quoting for passwords containing characters such as `@`, `%`, `!`, `&`, `$`, or spaces. If a URI is required, URL-encode the password portion.

## TLS Versus AUTH

| Symptom | Likely class | Action |
| --- | --- | --- |
| Timeout or immediate disconnect before Redis error | TLS/plaintext mismatch, blocked port, or certificate failure | Verify TLS mode, port, CA trust, and network path. |
| `WRONGPASS` after connection succeeds | Username/password/auth mode mismatch | Verify default versus ACL user and secret stores. |
| `AUTH failed` for all clients suddenly | Rotation, account restriction, or subscription issue | Check recent credential changes and Redis Cloud account status. |
| Passwordless database fails only when client auths | Client still sends AUTH | Remove username/password from client config. |

## Rotation And Secret Store Checks

If credentials changed recently, update every consumer:

- Kubernetes/OpenShift Secrets
- environment variables
- Vault or other secrets managers
- CI/CD variables
- Redis Insight saved connection
- worker and scheduled-job configs

Restart or redeploy clients that only read credentials at startup.

## ACL User Checks

In Redis Cloud Data Access Control:

- user is enabled
- user has a role
- role includes the target database
- ACL permits required commands and key patterns

Use `redis-cloud-rbac-acl` for detailed role or `NOPERM` analysis.

## Persistent Investigation

If CLI succeeds but application fails:

- compare exact client host, port, TLS, username, and password fields
- inspect client logs with secrets redacted
- briefly use `MONITOR` only in a controlled low-traffic window if required to confirm whether clients send `AUTH`
- use packet capture only to verify TLS negotiation shape, not to expose payloads

## Escalation Packet

Collect:

- database ID, endpoint, and port with credentials removed
- authentication mode expected by the database
- TLS required or not
- redacted client config field names
- `redis-cli` test result
- recent password, ACL, TLS, endpoint, billing, or subscription changes
- exact error text and timestamp
- whether all clients fail or only a subset
