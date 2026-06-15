---
name: redis-software-host-port
description: "Find and validate Redis Software database host and port values. Use when the user asks where to get a Redis Enterprise Software endpoint, how to connect to a database, why port 8443, 6379, or 6380 does not work, how to read the ENDPOINT column from `rladmin status databases`, whether to use public endpoints, how proxy-managed endpoints work, or how TLS, firewall, DNS, CRDB regional endpoints, and OSS Cluster API affect connection strings."
---

# Redis Software Host Port

Use this skill when a user needs the correct host and port for a Redis Software database connection.

## Source of Truth

Use the database endpoint shown in the Admin Console or `rladmin status databases`. Do not infer the port from Redis OSS defaults.

## Admin Console Workflow

1. Open the Admin Console:

   ```text
   https://<cluster-fqdn>:8443
   ```

2. Go to `Databases`.
3. Select the database.
4. Find the database endpoint under the general or endpoint section.
5. Use the endpoint host and port in the client connection string.

Important: port `8443` is for the Admin Console UI, not database traffic.

## rladmin Workflow

From a Redis Software cluster node:

```bash
rladmin status databases
```

Use the `ENDPOINT` column. It contains the database host and port, for example:

```text
redis-12000.example.cluster:12000
```

## Connection Rules

- Redis Software database ports are assigned from Redis Software reserved database port ranges, not arbitrary ports.
- Do not assume `6379` or `6380`; those are common OSS defaults, not Redis Software defaults.
- Port assignment happens at database creation and generally should be treated as fixed.
- Clients should use the database endpoint, not direct shard or node addresses.
- Use `rediss://` or client TLS settings when TLS is enabled.
- Public endpoints exist only when public access was enabled and configured.

## Client Mode Guidance

| Database mode | Client guidance |
| --- | --- |
| Default proxy-based database | Use a normal standalone Redis client connection to the endpoint. |
| OSS Cluster API enabled | Use a cluster-aware client and verify current endpoint behavior for the deployment. |
| Active-Active CRDB | Use the local region's proxy endpoint for lower latency. |

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Host unreachable | DNS, network segmentation, VPC/subnet routing, firewall, and endpoint spelling. |
| Port inaccessible | Security group, host firewall, load balancer, and whether the database port is open. |
| TLS error | Use `rediss://`, correct CA/client certs, SNI, and matching database TLS config. |
| Database endpoint missing | Database is not active, provisioning is incomplete, or user is viewing the wrong database. |
| Client uses `CLUSTER SLOTS` and fails | OSS Cluster API may not be enabled or client mode is wrong. |
| User connects to node IP directly | Use the database endpoint instead; direct shard/node access is not the normal supported client path. |

## Validation Commands

```bash
rladmin status databases
dig <database-host>
nc -vz <database-host> <database-port>
redis-cli -h <database-host> -p <database-port> PING
```

Add TLS and ACL flags to `redis-cli` as required without exposing credentials in shell history.

## Escalation Packet

Collect:

- Cluster FQDN and database name/ID.
- Endpoint shown in Admin Console or `rladmin`.
- Redis Software version.
- Client connection string with secrets redacted.
- TLS enabled or disabled.
- Public/internal endpoint expectation.
- DNS and port test results.
- CRDB region or OSS Cluster API status if relevant.
