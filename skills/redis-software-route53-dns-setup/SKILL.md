---
name: redis-software-route53-dns-setup
description: Use when setting up AWS Route 53 DNS for Redis Software clusters, including hosted zones, delegated subdomains, NS records, node A records, Elastic IPs, registrar name-server updates, public versus private hosted zones, FQDN validation, dig/nslookup checks, and troubleshooting Redis node discovery by DNS.
---

# Redis Software Route 53 DNS Setup

Use this skill when configuring AWS Route 53 DNS for Redis Software cluster hostnames. The goal is stable FQDN-based node identity and endpoint resolution.

## Planning Checks

Confirm:

- domain or subdomain to use for Redis Software
- public or private hosted zone requirement
- AWS account and Route 53 permissions
- registrar or parent-zone access
- Redis node hostnames and IP addresses
- whether nodes use public Elastic IPs or private VPC addresses
- which clients and Redis nodes must resolve the names

## Setup Workflow

1. Create the Route 53 hosted zone for the Redis domain or subdomain.
2. Record the generated Route 53 name servers.
3. Delegate the subdomain from the parent zone or registrar using `NS` records.
4. Create one `A` record per Redis node hostname.
5. Ensure record values point to the correct public or private IPs for the chosen zone type.
6. Wait for propagation or resolver cache expiry.
7. Validate resolution from Redis nodes and from intended clients.

## Record Guidance

- Use `A` records for Redis node hostnames that map directly to IPs.
- Use `NS` records for delegation boundaries.
- Avoid using CNAMEs for node identity unless current Redis Software guidance and the deployment design explicitly allow it.
- Use FQDNs when initializing or adding Redis Software nodes.

## Validation Commands

```text
dig <node-fqdn>
dig NS <delegated-zone>
dig @<route53-nameserver> <node-fqdn>
nslookup <node-fqdn>
whois <domain>
```

From inside AWS, also test from the VPC or host where Redis Software runs when using private zones.

## Troubleshooting

- DNS not propagating: verify parent-zone or registrar NS delegation and allow cache expiry.
- Wrong IP returned: inspect Route 53 record value and stale resolver cache.
- Redis nodes cannot resolve each other: test from the Redis node, not only from an admin laptop.
- Public/private mismatch: confirm clients are querying the correct public or private hosted zone.
- Port 53 blocked: confirm UDP and TCP DNS reachability.

## Response Pattern

Answer with:

1. Zone type and domain plan.
2. Delegation and records needed.
3. Node FQDN to IP mapping.
4. Validation commands.
5. Troubleshooting path for propagation or wrong-answer issues.
