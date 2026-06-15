---
name: redis-cli-windows-docker-wsl
description: Use when a Windows user needs redis-cli for Redis Cloud, Redis Software, or Redis Open Source operations through Docker or WSL, especially for CLIENT LIST, CLIENT KILL, TLS connections, max-client troubleshooting, Docker Desktop, redis:8 container usage, WSL redis-tools installation, endpoint rebind requests, or safe connection termination.
---

# redis-cli On Windows With Docker Or WSL

Use this skill when a Windows user needs `redis-cli` but does not have a native Redis client installed. Prefer Docker for quick one-off access and WSL for a persistent Linux client environment.

## Before Connecting

Collect:

- host and port
- ACL username, if not default
- password or token handling approach
- whether TLS is required
- CA certificate path if certificate validation is required
- whether the database is already at max connections
- network allowlist or firewall access from the Windows machine

Do not paste passwords into shared logs or recorded terminals. Prefer environment variables or interactive prompts over command-line passwords when possible.

## Docker Option

Use Redis 8 image by default:

```text
docker run --rm -it redis:8 redis-cli -h <host> -p <port>
```

With username:

```text
docker run --rm -it redis:8 redis-cli --user <username> -h <host> -p <port>
```

For TLS:

```text
docker run --rm -it redis:8 redis-cli --tls -h <host> -p <port>
```

If a CA file is needed, mount it read-only:

```text
docker run --rm -it -v <windows-ca-dir>:/certs:ro redis:8 \
  redis-cli --tls --cacert /certs/<ca-file> -h <host> -p <port>
```

Use `AUTH` interactively or environment handling according to the user's security policy.

## WSL Option

Inside WSL:

```text
sudo apt-get update
sudo apt-get install -y redis-tools
redis-cli -h <host> -p <port>
redis-cli --tls -h <host> -p <port>
```

If the distro package is too old for required TLS or command support, use Docker with `redis:8` or install a current Redis CLI through a supported package path.

## Managing Connections

Read-only inspection:

```text
CLIENT LIST
```

Connection termination is disruptive. Confirm exact targets before using:

```text
CLIENT KILL ID <id>
CLIENT KILL ADDR <ip:port>
CLIENT KILL USER <username>
```

Avoid broad filters unless the user intentionally wants to terminate many clients during a maintenance window.

## Max Connections Scenario

If the database has reached max connections, a new `redis-cli` connection may fail.

Recommended sequence:

1. Stop or scale down the client application creating excessive connections.
2. Reduce pool size, concurrency, reconnect loops, or idle connection retention.
3. Retry `redis-cli` once connections drop.
4. If connections remain stuck, escalate for endpoint rebind or provider-side assistance.

Endpoint rebind terminates active connections and should be used only in non-production or during an approved maintenance window.

## Response Pattern

Answer with:

1. Docker or WSL path recommendation.
2. TLS and credential-safe connection command.
3. Read-only `CLIENT LIST` step.
4. Precise `CLIENT KILL` guidance only after target confirmation.
5. Max-connection fallback path if new admin connections are rejected.
