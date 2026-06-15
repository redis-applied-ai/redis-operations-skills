---
name: redis-insight-onboarding
description: "Onboard new Redis Insight users through first launch, first database connection, and initial settings. Use when the user asks how to start Redis Insight, access it on desktop, Docker, Kubernetes, or EC2, add a Redis Cloud or Redis Enterprise database, configure host, port, username, password, TLS certificates, test connection, tune scan limits, avoid KEYS in production, or fix first-time connection refused, auth, TLS handshake, and timeout errors."
---

# Redis Insight Onboarding

Use this skill for first-time Redis Insight setup and connection guidance.

## Safety Rules

- Do not ask users to paste passwords, private keys, or certificates into chat.
- Recommend TLS for production connections.
- Avoid `KEYS` in production; use filtered browsing or `SCAN`.
- For shared Redis Insight deployments, rely on network controls, reverse proxy, and Redis ACLs because Redis Insight is not a full multi-tenant RBAC layer.

## First Launch

| Deployment | Access pattern |
| --- | --- |
| Desktop | Launch from Applications, Start Menu, or installed app launcher. |
| Docker | Open the mapped Redis Insight port, commonly `http://<host>:5540`. |
| Kubernetes | Open the service, ingress, or port-forwarded URL. |
| EC2 or VM | Open the instance DNS/IP and mapped Redis Insight port, after security group/firewall checks. |

## Add First Database

1. Open Redis Insight.
2. Choose `Add Database`.
3. Enter host and port:
   - Redis OSS often uses `6379`.
   - Redis Cloud and Redis Software commonly use product-specific endpoints and ports.
4. Enter username and password if required.
5. Enable TLS when the database requires it.
6. Import CA/client certificates if mutual TLS or custom trust is required.
7. Choose `Test Connection`.
8. Add the database only after the test succeeds.

For Redis Cloud, get endpoint, username, password, and TLS settings from the database security or connection settings in Redis Cloud Console.

For Redis Software, use the database endpoint from Admin Console or `rladmin status databases`.

## First-Use Workflow

- Use Browser to inspect keys and data types.
- Use Workbench for multi-line commands and examples.
- Use CLI for quick commands.
- Use Slow Log and Profiler for performance troubleshooting.
- Use Database Analysis for memory and key distribution.
- Use tags or preloaded connection files to organize team databases.

## First-Time Settings

- Enable TLS by default for production workflows.
- Lower scan limits for very large datasets to reduce UI and server pressure.
- Use environment variables or JSON preloaded connections for team consistency.
- Keep Redis Insight updated for security and feature fixes.
- Prefer `UNLINK` over `DEL` for large key deletion after explicit confirmation.

## Connection Troubleshooting

| Symptom | Check |
| --- | --- |
| Connection refused | Redis service is running, host/port are correct, and firewall allows traffic. |
| Authentication error | Username/password, ACL user, and selected database endpoint. |
| TLS handshake failed | CA certificate, client cert/key, SNI, expiry, and TLS mode. |
| Timeout | VPC, VPN, allowlist, security group, route table, firewall, or private endpoint path. |
| Redis Cloud connection fails | IP allowlist, private connectivity, endpoint, TLS, and credentials from Cloud Console. |
| Redis Software connection fails | Database endpoint, port, DNS, TLS, and proxy path. |

## Escalation Packet

Collect:

- Redis Insight version and deployment type.
- Target Redis product: OSS, Redis Cloud, or Redis Software.
- Host, port, TLS mode, and network path with secrets redacted.
- Exact connection error.
- Whether Test Connection fails or later operations fail.
- Firewall, allowlist, VPN, VPC, or security group context.
- Redis Insight logs if the application itself fails.
