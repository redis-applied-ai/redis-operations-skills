---
name: redis-cloud-connect-database
description: "Connect clients, redis-cli, and Redis Insight to a Redis Cloud database and troubleshoot Redis Cloud connection failures. Use when the user asks for Redis Cloud endpoint credentials, the Connect wizard, `redis-cli -u rediss://...`, Redis Insight Web/Desktop, Python/Node/Java/Go/.NET connection code, IP allowlist issues, VPC peering/private endpoints, RBAC username/password, authentication failure, TLS/SSL errors, or local-vs-production network mismatch."
---

# Redis Cloud Connect Database

Use this skill for Redis Cloud-specific connection setup and troubleshooting.

## Current-State Rule

Verify the actual database version and security settings in the Redis Cloud Console before stating TLS defaults, username requirements, module availability, or connection-string behavior as current fact.

## Connection Workflow

1. Confirm database and environment:
   - Redis Cloud account, subscription, database.
   - Local machine, app server, CI, or production runtime.
   - Public endpoint, private endpoint, or VPC peering path.
2. Gather connection details from Redis Cloud:
   - Host and port.
   - Username: often `default`, unless RBAC/custom users are used.
   - Password.
   - TLS setting.
   - IP allowlist requirements.
3. Use the Connect wizard when available:
   - Open the database list.
   - Select Connect next to the endpoint.
   - Copy the redis-cli command or language-specific snippet.
4. Choose client method:
   - Redis Insight Web/Desktop for visual management.
   - `redis-cli` for quick validation.
   - Language client for application integration.
5. Test connectivity and verify `PING` or equivalent.

## redis-cli Pattern

TLS:

```bash
redis-cli -u rediss://<username>:<password>@<host>:<port>
```

Non-TLS only when the database is explicitly configured without TLS:

```bash
redis-cli -u redis://<username>:<password>@<host>:<port>
```

## Python Pattern

```python
import redis

r = redis.Redis(
    host="your-db-host.redis.cloud",
    port=12345,
    username="default",
    password="your-password",
    ssl=True,
)

print(r.ping())
```

Adjust `ssl` and username according to the actual database settings.

## Redis Insight Path

- Browser: use Launch Redis Insight Web when available.
- Desktop: add a database manually with host, port, username, password, and TLS settings.
- Use the Redis Insight connection troubleshooting skill for deeper GUI/log analysis.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Connection refused or timeout | IP allowlist, outbound IP, firewall, private endpoint routing, VPC peering. |
| Works locally but not production | Production outbound IP/range is not allowlisted or private route is missing. |
| Authentication failure | Username/password, case sensitivity, RBAC role, disabled default user. |
| TLS/SSL error | `rediss://` vs `redis://`, client SSL flag, certificate trust, and actual database TLS setting. |
| Private endpoint fails | VPC peering/private connectivity status and application route table. |
| Client code fails | Use wizard snippet for the language and verify client library version. |

## Safety Checks

- Do not ask users to paste real passwords or connection strings with live secrets.
- Prefer redacted examples in tickets and docs.
- Before changing allowlists, identify exact outbound IPs and avoid overly broad CIDR exposure.
- For production apps, do not rely on dynamic local IP allowlisting; prefer stable private networking where appropriate.

## Escalation Packet

Collect:

- Database ID/name, host, and port with secrets redacted.
- Redis version and TLS setting.
- Username type: default or RBAC custom user.
- Client environment and outbound IP/range.
- Public/private endpoint used.
- Exact error message.
- Whether redis-cli, Redis Insight, and application client behave differently.
