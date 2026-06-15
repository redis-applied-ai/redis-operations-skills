---
name: redis-software-azure-dns-setup
description: Use when setting up Azure DNS for Redis Software clusters, including Azure DNS Zones, delegated cluster subdomains, parent-zone NS records, Redis node A records, public versus private DNS zone constraints, immutable cluster FQDN during install, DNS propagation, port 53, and load balancer fallback tradeoffs.
---

# Redis Software Azure DNS Setup

Use this skill when configuring Azure DNS for Redis Software cluster hostnames. Redis Software cluster FQDN choices are foundational and may be difficult or impossible to change after installation, so validate the DNS plan before cluster creation.

## Planning Checks

Confirm:

- Azure subscription and DNS Zone permissions
- registered domain or delegated subdomain
- intended Redis cluster FQDN
- Redis node hostnames and IP addresses
- public versus private resolution requirements
- parent-zone or registrar access
- whether Azure Public DNS, Azure Private DNS, or an external DNS provider is appropriate

Verify current Azure DNS delegation behavior before assuming private-zone support for the desired delegation pattern.

## Setup Workflow

1. Choose the Redis cluster subdomain, such as `cluster1.example.com`.
2. Create or confirm the parent DNS zone.
3. Create a DNS zone for the Redis cluster subdomain.
4. Add `NS` records in the parent zone to delegate the cluster subdomain.
5. Add `A` records in the cluster zone for each Redis node.
6. Use the Redis cluster FQDN during Redis Software installation.
7. Validate resolution from Redis nodes and intended clients.

## Example Record Shape

Delegation in parent zone:

```text
cluster1.example.com. NS node1.cluster1.example.com.
cluster1.example.com. NS node2.cluster1.example.com.
cluster1.example.com. NS node3.cluster1.example.com.
```

Node records in cluster zone:

```text
node1.cluster1.example.com. A <node-1-ip>
node2.cluster1.example.com. A <node-2-ip>
node3.cluster1.example.com. A <node-3-ip>
```

Adapt names and values to the actual deployment.

## Validation Commands

```text
dig <node-fqdn>
dig NS <cluster-zone>
nslookup <node-fqdn>
```

Also test from the Redis node network, not only from an administrator laptop.

## Load Balancer Fallback

If DNS delegation is not feasible, an Azure Load Balancer may provide a client access path, but it can limit transparent failover and dynamic endpoint behavior. Prefer correct DNS design for Redis Software cluster identity and endpoint generation.

## Troubleshooting

- DNS does not resolve: verify parent-zone `NS` records and cluster-zone `A` records.
- Private-zone delegation fails: verify current Azure DNS support and consider public or external DNS design.
- `REFUSED`: inspect firewall, network security groups, and DNS query source.
- FQDN is wrong after install: plan for reinstall or support-guided options; do not assume it can be changed in place.
- New node unreachable: add or update the node `A` record.
- Propagation delay: inspect TTL and resolver cache.

## Response Pattern

Answer with:

1. The cluster FQDN plan.
2. Parent and cluster zone records.
3. Public/private DNS design checks.
4. Validation commands.
5. Load balancer caveats if DNS cannot be implemented.
