---
name: redis-software-post-password-acl-change
description: Use when Redis Software clients fail after password rotation, password reset, named user changes, ACL or role updates, TLS or certificate changes, endpoint or DNS changes, secret-store updates, or zero-downtime rotation attempts, especially errors such as `WRONGPASS`, `NOAUTH`, `NOPERM`, connection timeouts, stale secrets, clients not restarted, or needing REST API password rotation overlap.
---

# Redis Software Post-Password Or ACL Change

Use this skill when Redis Software application connections fail after credential, ACL, TLS, endpoint, or DNS changes.

## Safety Rules

- Never ask users to paste passwords, private keys, or full connection strings with secrets.
- Confirm cluster health before making further authentication changes.
- Treat password and ACL changes as production changes unless the user proves the cluster is disposable.
- Use staged REST API rotation only after verifying the Redis Software version and user flow supports it.

## What Changed

Identify the triggering change:

- password rotation or reset
- named user created, disabled, or changed
- ACL or role update
- TLS/certificate change
- endpoint, DNS, or port change
- secret store or environment variable update
- application restart or redeploy missing after secret change

## Health Before Auth Changes

Run:

```bash
rladmin status
rlcheck
```

If the cluster, nodes, endpoints, or shards are unhealthy, fix or route that issue before continuing with authentication changes. Cluster or shard failures can look like auth or connection failures.

## Endpoint And DNS Checks

Use the database endpoint, not direct node IPs:

```bash
dig <endpoint>
nc -vz <endpoint> <port>
```

Direct node IPs can change after failover, scaling, endpoint movement, or maintenance.

## Authentication Validation

For named user:

```bash
redis-cli -h <host> -p <port> --user <username> --pass '<password>' PING
```

For TLS:

```bash
redis-cli -h <host> -p <port> --tls --cacert <ca-cert-file> --user <username> --pass '<password>' PING
```

If CLI succeeds, focus on stale application config, secret stores, and whether clients were restarted. If CLI fails, check current password, user enabled state, ACLs, TLS, endpoint, and cluster health.

## Error Classifier

| Error | Meaning | Action |
| --- | --- | --- |
| `WRONGPASS` | Wrong/stale password or wrong username/password mode | Update all secret sources and verify username. |
| `NOAUTH` | Client connected but did not authenticate | Fix client auth fields. |
| `NOPERM` | User authenticated but lacks permissions | Review ACL/role command and key permissions. |
| Timeout/disconnect | Endpoint, DNS, TLS, port, network, or cluster health issue | Validate protocol, network path, and `rladmin` health. |

## ACL And Role Checks

Use:

```redis
ACL LIST
```

Confirm:

- user exists and is enabled
- command permissions cover the workload
- key patterns cover the keys being accessed
- database or endpoint scope is correct
- TLS settings match the client

For ACL design, use the project’s Redis Software ACL guidance if available; otherwise follow Redis ACL least-privilege principles.

## Secret Synchronization

Update every consumer:

- application environment variables
- Kubernetes/OpenShift Secrets
- Vault or other secret managers
- CI/CD variables
- monitoring and automation jobs
- Redis Insight saved connections

Restart or reload clients that cache credentials at startup.

## Zero-Downtime Rotation

If zero-downtime rotation is required, use `redis-software-credential-certificate-rotation` to verify whether the staged REST API password rotation flow applies. Do not assume every user type supports overlapping passwords.

## Escalation Packet

Collect with secrets redacted:

- Redis Software version and database endpoint
- endpoint, port, and TLS setting
- authentication model: default password or named user
- exact error text
- same-path `redis-cli` result
- `rladmin status` and `rlcheck`
- ACL/role summary with secret material removed
- time of change and whether clients were restarted
