---
name: redis-n8n-integration
description: "Connect n8n workflows to Redis for caching, sessions, pub/sub, vector search, semantic cache, RAG, and AI agent memory. Use when the user asks to configure n8n Redis credentials, split host and port fields, troubleshoot TLS, ECONNREFUSED, IP allow lists, dynamic n8n Cloud egress IPs, too many clients, missing Redis Vector Store node, NOPERM ACL errors, vector dimensions and distance metrics, or Redis Cloud and Redis Software connectivity."
---

# Redis n8n Integration

Use this skill when connecting n8n to Redis Cloud, Redis Software, Redis Stack, or Redis OSS for workflow state, caching, messaging, or vector search.

## Current-State Rule

n8n node availability, Redis Vector Store features, Redis Cloud TLS behavior, and plan limits change. Verify the current n8n version and Redis plan before promising a specific node, TLS setting, or connection limit.

## Connection Inputs

In n8n Redis credentials, keep fields separate:

- Host: Redis hostname only, no port suffix.
- Port: Redis database port.
- Username: `default` or a dedicated ACL user.
- Password: Redis password.
- Database: usually `0`.
- SSL/TLS: enable only when supported and required by the Redis deployment.

Common mistake: putting `host:port` in the Host field causes connection failures.

## Network Checklist

| Deployment | Check |
| --- | --- |
| n8n Cloud | Egress IPs may not be static; Redis Cloud allow lists can block it. |
| Self-hosted n8n | Use stable egress IP, NAT gateway, VPN, VPC peering, PrivateLink, or equivalent private path. |
| Redis Cloud | Confirm endpoint, port, credentials, TLS, and CIDR/IP access rules. |
| Redis Software | Confirm endpoint, port, firewall, DNS, TLS certs, and routing. |

For strict allow-list environments, prefer self-hosted n8n in a controlled network or a static-IP proxy/NAT path.

## Setup Workflow

1. Confirm Redis deployment type and connection details.
2. Confirm n8n deployment type: Cloud, Docker, Kubernetes, or other self-hosted.
3. Verify network path from n8n to Redis.
4. Create Redis credentials in n8n.
5. Test connection.
6. Add Redis nodes for cache, session, pub/sub, queue, or vector store workflow.
7. Configure connection pooling or execution concurrency to avoid connection-limit pressure.
8. Store credentials only in n8n credential manager and sanitize exported workflows.

## Vector Store Workflow

Use Redis Vector Store only when the n8n version and Redis deployment support it.

Confirm:

- Redis Search and Query capability is enabled.
- Vector dimension matches the embedding model.
- Distance metric matches the application: cosine, L2, or inner product.
- Index type fits scale:
  - FLAT for small/exact search.
  - HNSW-style approximate index for larger datasets.
- ACL user can run required Search and JSON commands.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| TLS error | TLS enabled in n8n but unsupported or cert trust mismatch | Verify plan/TLS support and CA/client cert configuration. |
| `ECONNREFUSED` from n8n Cloud | Redis Cloud IP allowlist blocks dynamic egress | Use self-hosted n8n or static egress proxy. |
| Too many clients | Connection limit or excessive workflow concurrency | Pool connections, reduce concurrency, or upgrade capacity. |
| Redis Vector Store node missing | n8n version or feature set lacks node | Upgrade or verify current n8n availability. |
| `NOPERM` | ACL user lacks command or key permissions | Grant least-privilege commands and key patterns. |
| Connection test fails | Host/port mixed, wrong credentials, blocked network, or TLS mismatch | Check fields and network path. |

## Security Practices

- Use dedicated ACL users where possible.
- Restrict Redis access by network path and CIDR where supported.
- Prefer TLS for production.
- Do not export workflows with secrets embedded.
- Confirm data residency and retention for managed n8n and Redis deployments.

## Escalation Packet

Collect:

- n8n version and deployment type.
- Redis product, plan, endpoint, port, and TLS mode.
- Whether n8n Cloud or self-hosted is used.
- Redis Cloud allowlist/private connectivity settings.
- Exact error text.
- ACL username and permission summary, without secrets.
- Vector node configuration: dimension, metric, index, and embedding model if relevant.
