---
name: redis-insight-data-management
description: "Use Redis Insight to explore, debug, and manage Redis data safely. Use when the user asks to browse keys, inspect JSON, hashes, streams, or sorted sets, run Workbench or CLI commands, use Profiler, Slow Log, Database Analysis, bulk actions, troubleshoot Redis Insight connection or TLS errors, avoid KEYS in production, use SCAN or UNLINK, or find Redis Insight logs."
---

# Redis Insight Data Management

Use this skill when helping a user inspect and manage Redis data through Redis Insight after a database connection exists or connection details are available.

## Safety Rules

- Do not ask users to paste passwords, private keys, or client certificates into chat.
- Treat bulk delete, `DEL`, `UNLINK`, and key cleanup as destructive actions requiring explicit confirmation.
- Avoid `KEYS *` in production; use filtered browsing or `SCAN`-based workflows.
- Use Profiler cautiously on busy production systems because command capture can be noisy and sensitive.
- Redis Insight does not provide its own RBAC; rely on Redis ACLs, TLS, and network controls.

## Connection Checks

For Redis Cloud:

- Get endpoint, port, username/password, TLS setting, and certificates from the Cloud console.
- Confirm IP allowlists, private connectivity, or VPC peering allow the Redis Insight host.

For Redis Software:

- Get endpoint and port from the admin console or `rladmin`.
- Import enterprise-issued or self-signed certificates when TLS is enabled.

## Exploration Workflow

1. Open the database connection in Redis Insight.
2. Use Browser list or namespace/tree view to narrow keys.
3. Filter by prefix, pattern, or data type before inspecting large datasets.
4. Inspect values with an appropriate renderer such as JSON, HEX, ASCII, MessagePack, or Protobuf.
5. For CRUD edits, confirm the target key and expected serialization format.
6. For cleanup, select a filtered key set and confirm destructive bulk actions with the user.

## Command Workflows

| Tool | Use for |
| --- | --- |
| Workbench | Multi-line queries, search/vector examples, command editing, and repeatable snippets. |
| CLI | Quick one-off commands with helper/autocomplete. |
| Profiler | Real-time command visibility during a controlled troubleshooting window. |
| Slow Log | Identifying slow commands without broad command capture. |
| Database Analysis | Memory/type distribution and largest-key inspection; expect sampling or key-count limits. |

## Advanced Operations

Redis Insight can also help with:

- Streams and consumer groups.
- Pub/Sub channel inspection.
- Search index creation and queries.
- Vector search experiments.
- Redis Data Integration pipeline visibility when configured.
- Connection tags and preconfigured connection files for teams.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Failed to connect | Endpoint, port, credentials, allowlist, firewall, private networking, or database status. |
| TLS error | CA certificate, client certificate/key, SNI, certificate expiry, and Redis Insight version. |
| Latency or timeouts | Long-running commands, large scans, plan limits, network path, or resource saturation. |
| Bulk action incomplete | Filter scope, scan limit, namespace pattern, and whether keys changed during scan. |
| CLI and Workbench differ | Database context, ACL user permissions, selected connection, and network latency. |

## Debug Evidence

If Redis Insight itself is failing, ask for logs with sensitive values redacted.

Common log locations:

- macOS/Linux: `~/.redis-insight`
- Windows: user profile `.redis-insight` directory.
- Docker: `/data/logs`

For ioredis debugging, launch with:

```bash
DEBUG=ioredis*
```

## Escalation Packet

Collect:

- Redis Insight version and installation type.
- Redis deployment type: Cloud, Software, or OSS.
- Endpoint, port, TLS mode, and network path with secrets redacted.
- Error text or screenshot with credentials redacted.
- Whether Browser, Workbench, CLI, Profiler, Slow Log, or Database Analysis is affected.
- Approximate key count, largest key symptoms, and command being attempted.
- Relevant Redis Insight logs.
