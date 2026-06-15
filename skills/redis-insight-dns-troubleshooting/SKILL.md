---
name: redis-insight-dns-troubleshooting
description: Use when Redis Insight cannot connect because of DNS resolution issues, ENOTFOUND, NXDOMAIN, ETIMEDOUT, endpoint lookup failures, failover DNS TTL behavior, FQDN versus IP confusion, Redis Insight Docker DNS, ioredis debug logs, or when DNS works from one machine but not from the Redis Insight runtime.
---

# Redis Insight DNS Troubleshooting

Use this skill when Redis Insight cannot resolve or reach a Redis endpoint. Always test DNS from the environment where Redis Insight actually runs: desktop host, container, VM, or Kubernetes pod.

## Classify The Error

- `ENOTFOUND` or `NXDOMAIN`: hostname does not resolve from the Redis Insight runtime.
- `ETIMEDOUT`: hostname may resolve, but network path or Redis service is unreachable.
- Certificate or TLS hostname error: DNS resolves, but endpoint name and certificate/SNI may not align.
- Failover issue: cached DNS or long TTL may point clients at an old endpoint.

## First Checks

Run from the Redis Insight runtime environment:

```text
dig <database-endpoint>
nslookup <database-endpoint>
```

For Docker, exec into the Redis Insight container when possible and test there. For Kubernetes, test from the pod or a debug pod in the same namespace/network context.

Then test connection from Redis Insight with the same host and port.

## Logs And Debugging

Check Redis Insight logs for `ENOTFOUND`, `DNS resolve failed`, `ETIMEDOUT`, or TLS errors.

Common log locations:

- Docker: `/data/logs`
- macOS: `~/.redis-insight`
- Linux: `/home/<username>/.redis-insight`
- Windows: `C:\Users\<username>\.redis-insight`

Enable ioredis debug output where appropriate:

```text
DEBUG=ioredis* <start Redis Insight>
```

Use the operating-system-specific launch method for the user's environment.

## Network Checks

Confirm:

- DNS UDP/TCP port `53` is reachable from the Redis Insight runtime.
- Redis database port is reachable from the same runtime.
- corporate DNS, VPN, proxy, or container DNS settings are not overriding lookup.
- Redis Enterprise or Redis Cloud endpoint is the intended FQDN.
- local DNS cache is not stale after failover or endpoint changes.

Prefer FQDNs over raw IPs for production so failover and endpoint updates can work.

## Resolution Patterns

- Resolves on server but not client: fix client-side DNS resolver, search domains, VPN, or forwarding.
- Resolves on host but not in Docker: fix container DNS configuration or Docker network.
- Resolves but times out: check firewall, route, allowlist, security group, or Redis service state.
- Works by IP but not FQDN: DNS issue; do not use IP as a long-term production workaround.
- Fails after failover: flush DNS caches if needed and verify TTL strategy.

## Response Pattern

Answer with:

1. The likely class: DNS, network reachability, or TLS hostname.
2. Commands to run from the Redis Insight runtime.
3. Logs to inspect.
4. Environment-specific fix path.
5. Why FQDN is preferred for production connections.
