---
name: redis-insight-install-config
description: "Install and configure Redis Insight across desktop, Docker, Kubernetes, OpenShift, and AWS EC2. Use when the user asks to install Redis Insight, run `redis/redisinsight`, expose port 5540, add Docker persistence, deploy with Kubernetes YAML or Helm, port-forward Redis Insight, configure team preloaded connections, secure multi-user access with VPN or firewall, find Redis Insight logs, or troubleshoot startup, TLS, host/port, and network errors."
---

# Redis Insight Install Config

Use this skill when a user needs to install, deploy, configure, or troubleshoot Redis Insight itself.

## Current-State Rule

Redis Insight packages, images, Helm charts, and supported OS versions change. Verify current official download and install docs when the exact package or version matters.

## Deployment Options

| Platform | Guidance |
| --- | --- |
| Desktop | Use official installer for Windows, macOS, or Linux package format. |
| Docker | Run `redis/redisinsight` and persist `/data` if connections/settings should survive container recreation. |
| Kubernetes/OpenShift | Use official manifests or Helm chart; decide ephemeral versus persistent storage. |
| AWS EC2 or VM | Run Docker or supported package on a dedicated instance; restrict network access. |

## Docker Quick Start

Without persistence:

```bash
docker run -d --name redisinsight -p 5540:5540 redis/redisinsight:latest
```

With persistence:

```bash
docker run -d --name redisinsight -p 5540:5540 \
  -v redisinsight:/data \
  redis/redisinsight:latest
```

Open:

```text
http://localhost:5540
```

## Kubernetes Pattern

1. Review the official Redis Insight Kubernetes manifest or Helm chart for the current version.
2. Decide whether storage should be persistent.
3. Apply manifests:

   ```bash
   kubectl apply -f redisinsight.yaml
   ```

4. Expose safely through an internal Service, ingress, VPN, or port-forward:

   ```bash
   kubectl port-forward deployment/redisinsight 5540:5540
   ```

5. Restrict access to trusted users/networks.

## Initial Configuration

- Add database connections with host, port, auth, and TLS settings.
- For Redis Cloud, retrieve endpoint, credentials, TLS settings, and allowlist/private connectivity from Cloud Console.
- For Redis Software, retrieve endpoint from Admin Console or `rladmin status databases`.
- Use labels/tags to organize many connections.
- Use preconfigured JSON or environment-based connection setup for teams.

## Security and Operations

- Restrict Redis Insight port `5540` with firewall, VPN, private network, reverse proxy, or identity-aware access.
- Do not expose Redis Insight openly to the internet.
- Redis Insight is not a full RBAC system; enforce access through network and Redis ACLs.
- Keep Redis Insight updated for security and feature fixes.
- Monitor CPU and RAM for large datasets.
- Avoid production `KEYS *` and large blocking operations; use filters, SCAN-based tools, and Database Analysis.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| App will not start | OS, CPU architecture, package type, container logs, and resource limits. |
| Cannot open UI | Port 5540 mapping, firewall, Service, ingress, or port-forward. |
| Connection fails | Host, port, credentials, Redis status, allowlists, firewalls, and routes. |
| TLS error | CA/client certs, key paths, SNI, expiry, and database TLS mode. |
| Docker data lost | Missing persistent volume mapped to `/data`. |
| Kubernetes state lost | Ephemeral storage used instead of persistent volume. |

Log locations:

- macOS/Linux: `~/.redis-insight`
- Windows: user profile `.redis-insight` directory.
- Docker: `/data/logs`

Debug mode:

```bash
DEBUG=ioredis*
```

## Escalation Packet

Collect:

- Redis Insight version and deployment mode.
- OS, container image, or Kubernetes manifests/Helm values.
- Port exposure method and URL.
- Persistence configuration.
- Startup logs or `/data/logs`.
- Target Redis product and connection error.
- TLS mode and cert source, with secrets redacted.
