---
name: redis-insight-connect-database
description: "Connect Redis Insight to Redis Cloud, Redis Software, Redis Open Source, or Kubernetes-hosted Redis databases and troubleshoot connection failures. Use when the user mentions Redis Insight manual add, Open with Redis Insight, TLS or mTLS certificates, SNI, Kubernetes ingress passthrough, Redis Insight preconfigured databases, `RI_REDIS_HOST0`, `RI_PRE_SETUP_DATABASES_PATH`, authentication errors, INFO permission problems, or Redis Insight connection logs."
---

# Redis Insight Connect Database

Use this skill when helping a user add a database connection to Redis Insight or troubleshoot why Redis Insight cannot connect.

## Connection Workflow

1. Identify deployment type:
   - Redis Cloud.
   - Redis Software.
   - Redis Open Source.
   - Kubernetes/OpenShift ingress or route.
2. Gather connection details:
   - Host/FQDN and port.
   - Username and password or ACL user.
   - TLS requirement.
   - CA certificate, client certificate, and client key for mTLS if required.
   - IP allowlist/firewall status.
3. Choose connection method:
   - Manual Add for explicit host/port/TLS/auth.
   - Cloud Launch from Redis Cloud using Open with Redis Insight where available.
   - Auto-discovery for local or supported managed instances.
   - Preconfiguration for containers/team deployments.
4. Test connection before saving.
5. If connected, verify data browsing, Workbench, CLI, profiler, and slow log access as needed.

## Redis Cloud Path

1. Open database Configuration/Security in Redis Cloud.
2. Copy endpoint, port, username, and password.
3. Open Redis Insight.
4. Add Redis Database.
5. Enter endpoint and credentials.
6. Enable TLS when required.
7. Add CA/client certs when mTLS is enabled.
8. Test and save.

## Redis Software / OSS Path

1. Get endpoint from Cluster Manager or:

   ```bash
   rladmin status extra all
   ```

2. Determine TLS and ACL requirements.
3. Prepare proxy/server CA certificates and client cert/key if mTLS is required.
4. Add database in Redis Insight using FQDN/port and credentials.
5. For Kubernetes/OpenShift ingress, confirm route host/port, SNI, and TLS passthrough.

## Automated Preconfiguration

For Redis Insight containers or repeatable team setup:

- Use `RI_REDIS_HOST0`, `RI_REDIS_PORT0`, and related variables for simple preloaded connections.
- Use `RI_PRE_SETUP_DATABASES_PATH` to point at a JSON file defining multiple databases.
- Include TLS variables or certificate mounts when needed.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Failed to connect | Endpoint, port, client IP allowlist, firewall, and credentials. |
| TLS/SSL error | CA/client certs, mTLS settings, SNI, certificate expiry, and Redis Insight version. |
| Authentication error | Username/password, ACL role, and required command permissions. |
| Cluster connection fails | Access to all relevant cluster nodes and cluster API path. |
| Kubernetes protocol error | SNI and TLS passthrough on ingress/route. |
| Connections drop | Resource limits, firewall timeouts, and expensive commands such as broad key scans/deletes. |
| 429 errors | Excessive retries or scripted login/connect attempts. |
| INFO blocked | Upgrade Redis Insight or adjust ACLs if the workflow requires INFO. |

## Logs and Debugging

Common log locations:

- macOS/Linux: `~/.redis-insight`
- Windows: `C:\Users\<username>\.redis-insight`
- Docker: `/data/logs`

Enable detailed client traces when appropriate:

```bash
DEBUG=ioredis*
```

## Safety Checks

- Do not ask users to paste passwords, private keys, or full client certificates into chat.
- Avoid using broad key operations like `KEYS` or large `DEL` during connection validation.
- For production Kubernetes ingress, confirm TLS/SNI changes with the platform owner before editing routes.
