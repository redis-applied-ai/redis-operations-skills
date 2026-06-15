---
name: redis-software-windows-server-dns-setup
description: Use when setting up Windows Server DNS for Redis Software clusters, including DNS Manager delegation, parent zones, Redis cluster FQDN, immutable cluster name, temporary IP-based delegation, node A records, delegated-zone NS records, glue cleanup, port 53 checks, nslookup validation, and database endpoint FQDN resolution.
---

# Redis Software Windows Server DNS Setup

Use this skill when configuring Windows Server DNS for Redis Software cluster node names and generated database endpoints.

## Planning Checks

Confirm:

- Windows Server DNS administrative access
- parent DNS zone, such as `example.com`
- intended Redis cluster subdomain, such as `mycluster.example.com`
- Redis node names and IP addresses
- DNS port `53` reachability
- whether Redis Software is being installed or already exists

The Redis cluster FQDN is set during installation and should be treated as immutable for normal operations.

## Setup Workflow

1. Choose the Redis cluster FQDN.
2. Enter that FQDN during Redis Software installation.
3. In Windows DNS Manager, create a delegation from the parent zone for the cluster subdomain.
4. Use temporary IP-based delegation if the wizard requires an initial name server.
5. Create `A` records for Redis nodes.
6. Replace placeholder or IP-based NS entries with node FQDNs.
7. Remove old glue records if prompted and no longer needed.
8. Refresh the zone and validate resolution.

## Record Shape

Node records:

```text
node1.mycluster.example.com A <node-1-ip>
node2.mycluster.example.com A <node-2-ip>
node3.mycluster.example.com A <node-3-ip>
```

Delegation NS targets:

```text
mycluster.example.com NS node1.mycluster.example.com
mycluster.example.com NS node2.mycluster.example.com
mycluster.example.com NS node3.mycluster.example.com
```

## Validation

Use:

```text
nslookup node1.mycluster.example.com
nslookup redis-12000.mycluster.example.com
```

Also test from Redis nodes and application networks that must connect to Redis endpoints.

## Troubleshooting

- Node FQDNs do not resolve: check A records, spelling, and zone placement.
- Cluster FQDN not reachable: verify delegation, propagation, and DNS port `53`.
- Delegation wizard fails: use temporary IP-based delegation, then replace with node FQDNs after A records exist.
- Reverse DNS warning: PTR records are usually not required for Redis cluster DNS.
- Wrong FQDN after install: plan reinstall or support-guided remediation; do not assume it can be changed in place.

## Response Pattern

Answer with:

1. Cluster FQDN and parent zone.
2. Delegation flow in Windows DNS Manager.
3. A and NS record plan.
4. Validation commands.
5. Immutable-FQDN and reverse-DNS caveats.
