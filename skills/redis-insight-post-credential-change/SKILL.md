---
name: redis-insight-post-credential-change
description: Use when Redis Insight stops connecting after database password rotation, ACL/RBAC user changes, TLS or CA updates, endpoint or port changes, saved connection profile drift, Redis Insight stale credentials, Redis Insight works differently than `redis-cli`, `NOPERM` due to missing `INFO`, Docker or Kubernetes Redis Insight logs, or users need to edit or recreate a Redis Insight saved database connection.
---

# Redis Insight Post-Credential Change

Use this skill when Redis Insight fails after a Redis database credential, ACL, TLS, endpoint, or port change.

## Core Rule

Redis Insight stores connection profiles. It does not automatically update saved host, port, username, password, TLS, or CA settings after the database changes. Edit or recreate the saved connection before assuming the database is unhealthy.

## Safety Rules

- Do not ask users to paste real passwords, private keys, or full connection strings.
- Redact logs and screenshots before sharing.
- Compare with `redis-cli` using placeholders or locally supplied secrets.

## What Changed

Ask which event happened immediately before failure:

- password rotation or reset
- ACL/RBAC user or role change
- username changed from default to named user
- TLS enabled, disabled, or certificate/CA changed
- endpoint or port changed
- Redis Insight container/pod redeployed with old preconfigured settings

## Update The Saved Connection

In Redis Insight, edit or recreate the database profile and confirm:

- host
- port
- username
- password
- TLS enabled/disabled
- CA certificate or client certificate/key if required
- SNI/hostname settings when using Kubernetes, OpenShift, or ingress

If the profile was preconfigured by environment variables or a mounted JSON file, update the deployment source and restart Redis Insight.

## CLI Comparison

Run a matching `redis-cli` test from a comparable network path:

```bash
redis-cli -h <host> -p <port> --user <username> --pass '<password>' PING
```

For TLS:

```bash
redis-cli -h <host> -p <port> --tls --cacert <ca-cert-file> --user <username> --pass '<password>' PING
```

If CLI succeeds but Redis Insight fails, the issue is likely the Redis Insight profile, TLS/CA import, SNI setting, runtime network, or cached/preconfigured connection. If CLI fails, troubleshoot the database connection itself with `redis-cloud-authentication-errors` or the product-specific connection skill.

## INFO Permission Check

Redis Insight may require `INFO` for connection validation and database metadata.

Test:

```bash
redis-cli -h <host> -p <port> --user <username> --pass '<password>' INFO
```

If `NOPERM` appears, update the ACL/role to allow the required command set, or use an appropriate user for Redis Insight.

## Logs

Container:

```bash
docker logs <container>
```

Kubernetes:

```bash
kubectl logs <pod> -n <namespace>
```

Look for authentication failures, permission errors, TLS validation errors, DNS errors, or timeouts. Redact sensitive values before sharing.

## Escalation Packet

Collect:

- Redis Insight version and runtime: desktop, Docker, or Kubernetes
- exact change and timestamp
- saved connection settings with secrets redacted
- `redis-cli` `PING` result with equivalent settings
- `INFO` permission test result
- TLS/CA/SNI details if applicable
- relevant Redis Insight logs
- whether editing or recreating the saved connection changed behavior
