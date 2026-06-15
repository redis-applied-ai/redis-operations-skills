---
name: redis-software-endpoint-flapping
description: "Diagnose and resolve Redis Software endpoint flapping and intermittent database connectivity. Use when endpoints alternate between available and unavailable, DNS resolution changes rapidly, clients see intermittent connection failures, maintenance or failover caused endpoint churn, `rladmin status endpoints` shows unexpected state, proxy policy rebinding is needed, or logs such as dmcproxy.log and event_log.log show repeated connects or disconnects."
---

# Redis Software Endpoint Flapping

Use this skill when Redis Software database endpoints rapidly change availability or clients intermittently fail to connect through FQDNs.

## Safety Rules

- Do not make direct-IP connection strings a permanent fix; they can bypass failover behavior.
- Do not disable production firewalls as a casual test. Use controlled allowlist checks or temporary changes with approval.
- Treat endpoint rebinds and proxy-policy changes as production-impacting changes.
- Preserve logs before disruptive recovery when flapping is active.

## Triage Workflow

1. Verify endpoint registration and database health:

   ```bash
   rladmin status endpoints
   rladmin status databases
   ```

   Confirm the endpoint is present, active, and mapped to a healthy database.

2. Identify the exact database endpoint from the database `ENDPOINT` column.
3. Test DNS from the client:

   ```bash
   dig <database-endpoint>
   nslookup <database-endpoint>
   ```

4. Test DNS from a Redis cluster node. If cluster nodes resolve but clients do not, focus on client resolver, corporate DNS, or network path.
5. If the endpoint is publicly resolvable, compare trusted resolvers:

   ```bash
   dig @8.8.8.8 <database-endpoint>
   dig @1.1.1.1 <database-endpoint>
   dig @9.9.9.9 <database-endpoint>
   ```

6. Trace custom FQDN delegation:

   ```bash
   dig +trace <fqdn>
   ```

7. Test Redis connectivity through FQDN, then direct IP only as a diagnostic comparison:

   ```bash
   redis-cli -h <fqdn> -p <port>
   redis-cli -h <ip-address> -p <port>
   ```

8. Review logs for endpoint churn:
   - `dmcproxy.log`
   - `event_log.log`

## Root Cause Checks

| Area | What to check |
| --- | --- |
| DNS delegation | NS, A, CNAME, or ALIAS records match current topology. |
| TTL and caches | TTLs are not too long for maintenance; clients do not cache DNS indefinitely. |
| Maintenance or failover | Endpoint removal/rebind did not happen before DNS TTL and client caches expired. |
| Network controls | Port 53 and Redis database ports are allowed through firewalls, security groups, proxies, NAT, and load balancers. |
| Proxy policy | Endpoint policy is appropriate for the database and topology. |
| TLS or mTLS | Certificate chain, SANs, expiry, and intermediates are valid for the endpoint. |
| Buffers | Output or replica buffer pressure is not causing repeated disconnects. |

## Proxy Policy Commands

Inspect endpoints:

```bash
rladmin status endpoints
```

Rebind only after confirming the intended policy and maintenance impact:

```bash
rladmin bind db db:<db-id> endpoint <endpoint-id> policy <single|all-master-shards|all-nodes>
```

For replica buffer issues, tune only with evidence:

```bash
rladmin tune db <db-name> slave_buffer <size>
```

## Mitigation Patterns

- Correct stale DNS records to match current cluster topology.
- Lower inappropriate client DNS cache settings for runtimes that cache aggressively.
- Increase rebind grace period when endpoint changes outrun DNS TTL expiration.
- Fix firewall or security group rules for DNS and Redis database ports.
- Correct TLS trust chain or expired certificates.
- Roll back recent topology, proxy, or networking changes if they triggered flapping.

## Escalation Packet

Collect:

- Database name, ID, endpoint, endpoint ID, and proxy policy.
- `rladmin status endpoints` and `rladmin status databases`.
- DNS results from client and cluster node.
- `dig +trace` output for custom FQDNs.
- Direct-IP comparison result, if tested.
- Maintenance/failover timeline.
- Relevant `dmcproxy.log` and `event_log.log` snippets.
- TLS error text and certificate metadata if applicable.
- Support package from involved nodes or all participating clusters for CRDB/geo-replication.
