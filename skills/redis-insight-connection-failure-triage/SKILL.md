---
name: redis-insight-connection-failure-triage
description: Use when Redis Insight cannot connect to Redis Cloud, Redis Software, Redis Open Source, OSS Cluster, Sentinel, Docker, Kubernetes, or OpenShift deployments, including failed connection tests, wrong endpoint or port, IP/CIDR allowlist, private endpoint access, TLS or self-signed certificate errors, SNI issues, INFO permission failures, Redis Insight debug logs, CLI works but Redis Insight fails, cluster node reachability, or dropped Redis Insight connections.
---

# Redis Insight Connection Failure Triage

Use this skill when Redis Insight connection setup fails or an existing Redis Insight connection drops.

## Triage Order

1. Verify endpoint, port, username, password, TLS, and certificates.
2. Test network and DNS from the runtime where Redis Insight actually runs: desktop host, Docker container, VM, or Kubernetes pod.
3. Test with `redis-cli` using the same host, port, TLS, username, and password.
4. Compare Redis Insight behavior against CLI behavior.
5. Enable Redis Insight debug logging only after basic connection details are confirmed.
6. Check database/server health and resource limits.

## First Checks

Confirm:

- Host is the database FQDN or supported endpoint, not a stale private IP.
- Port matches the database endpoint and TLS setting.
- Client IP or network is allowed in Redis Cloud or firewall rules.
- Private endpoints are reachable from the Redis Insight runtime network.
- Username/password or ACL user is correct.
- The connected user can run required commands such as `INFO` when Redis Insight needs them.
- TLS/mTLS CA, client certificate, and client key are supplied when required.

## CLI Comparison

Non-TLS:

```bash
redis-cli -h <host> -p <port> -a <password>
```

TLS:

```bash
redis-cli -h <host> -p <port> --tls --cacert <ca-cert-file>
```

If CLI fails, fix endpoint, network, TLS, or auth before debugging Redis Insight. If CLI works but Redis Insight fails, focus on Redis Insight TLS/SNI configuration, local proxy/firewall behavior, or Redis Insight logs.

## Network And DNS Checks

Run from the Redis Insight runtime:

```bash
dig <hostname>
telnet <host> <port>
ping <host>
```

Use `redis-insight-dns-troubleshooting` for DNS-specific failures such as `ENOTFOUND`, `NXDOMAIN`, or container DNS differences.

For cluster mode, verify Redis Insight can reach all required cluster nodes or endpoints, not just the seed endpoint.

## Debug Logging

Enable ioredis debug logs when needed:

```bash
DEBUG=ioredis*
```

Common log locations:

- Docker: `/data/logs`
- macOS: `~/.redis-insight`
- Windows: `C:\Users\<username>\.redis-insight`
- Linux: `/home/<username>/.redis-insight`

Redact passwords, private keys, tokens, endpoint secrets, and customer data before sharing logs.

## Common Failures

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Failed to connect | Wrong host/port, closed port, bad credentials, or allowlist block. | Recheck endpoint, auth, firewall, and CIDR allowlist. |
| TLS self-signed chain error | Redis Insight does not trust the CA. | Import or configure the correct CA bundle. |
| Kubernetes/OpenShift protocol error | TLS/SNI or route/ingress mismatch. | Verify SNI, TLS passthrough, route host, and current Redis Insight version support. |
| CLI works but Redis Insight fails | Client-side Redis Insight TLS/proxy/logging issue. | Compare exact settings and review debug logs. |
| OSS Cluster connection fails | Redis Insight cannot reach every cluster node. | Open required node traffic or use a supported endpoint path. |
| Connection drops after success | Redis resource pressure, firewall timeout, failover, or expensive commands. | Check CPU/RAM/disk, server logs, and avoid broad `KEYS` or large `DEL`. |

## Server Health Checks

For Redis Software:

```bash
rladmin status issues_only
```

Also check server CPU, memory, disk, open files, connection limits, and logs when connections drop after initial success.

## Escalation Packet

Collect:

- Redis Insight version and runtime environment
- Redis product and deployment type
- endpoint, port, TLS mode, and whether private networking is involved
- CLI test result using equivalent settings
- DNS and port reachability test from the Redis Insight runtime
- sanitized Redis Insight debug logs
- exact error text or screenshot with secrets redacted
- server health status and recent network, certificate, or ACL changes
