---
name: redis-software-google-cloud-dns-setup
description: Use when setting up Google Cloud DNS for Redis Software clusters, including choosing an immutable cluster FQDN, Cloud DNS managed zones, NS delegation to Redis nodes, A records for node public IPs, RFC-compliant hostnames, generated database endpoints, DNS propagation checks, mDNS avoidance, CNAME/private DNS caveats, and load balancer fallback tradeoffs.
---

# Redis Software Google Cloud DNS Setup

Use this skill when configuring Google Cloud DNS for Redis Software cluster hostnames and generated database endpoints. Validate DNS before cluster finalization because the Redis cluster FQDN becomes a long-lived identifier.

## Planning Checks

Confirm:

- Google Cloud project and Cloud DNS permissions
- existing managed zone or parent domain
- intended Redis cluster FQDN
- node hostnames and IP addresses
- public versus private resolution requirements
- whether Redis nodes will act as authoritative DNS servers for the delegated subdomain
- client networks that must resolve database endpoints

## Setup Workflow

1. Choose a cluster FQDN, such as `mycluster.example.com`.
2. Enter the FQDN during Redis Software installation.
3. In Cloud DNS, add an `NS` record for the Redis cluster subdomain.
4. Add the Redis node FQDNs as NS targets.
5. Add `A` records mapping each Redis node hostname to its IP.
6. Wait for TTL and propagation.
7. Validate node FQDNs and generated Redis database endpoint FQDNs.

## Example Record Shape

Delegation:

```text
mycluster.example.com. NS node1.mycluster.example.com.
mycluster.example.com. NS node2.mycluster.example.com.
mycluster.example.com. NS node3.mycluster.example.com.
```

Node records:

```text
node1.mycluster.example.com. A <node-1-ip>
node2.mycluster.example.com. A <node-2-ip>
node3.mycluster.example.com. A <node-3-ip>
```

Adapt to the real managed zone and IP layout.

## Validation Commands

```text
dig <node-fqdn>
dig NS <cluster-fqdn>
host <database-endpoint-fqdn>
nslookup <node-fqdn>
```

Test from the Redis node network and from intended clients.

## Caveats

- The Redis cluster FQDN is not a casual setting; changing it later may require reinstall or support-guided remediation.
- Do not use mDNS for production Redis Software clusters.
- Avoid CNAME patterns that conflict with Google Cloud private DNS behavior or Redis Software expectations.
- Do not run multiple competing authoritative DNS services on Redis nodes.
- A load balancer can provide access when DNS delegation is impossible, but it may reduce transparent failover and dynamic endpoint capabilities.

## Troubleshooting

- DNS not resolving: recheck NS and A records.
- TTL delay: wait for resolver cache expiry or lower TTL before cutover.
- Node updates break DNS: add, remove, or update node A/NS records.
- Generated database endpoint not resolving: validate cluster subdomain delegation and node authority.
- Private DNS issue: test from the same VPC and verify Cloud DNS zone visibility.

## Response Pattern

Answer with:

1. The cluster FQDN plan.
2. NS and A records needed in Cloud DNS.
3. Validation commands.
4. Production DNS caveats.
5. Load balancer tradeoff if DNS delegation is not possible.
