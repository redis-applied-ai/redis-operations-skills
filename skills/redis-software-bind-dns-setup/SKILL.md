---
name: redis-software-bind-dns-setup
description: Use when setting up BIND DNS for Redis Software cluster DNS, including zone delegation, Redis node FQDNs, A records, NS records, glue records, RFC-compliant hostnames, named.conf or named.conf.local configuration, zone-file validation, DNS port 53, resolver testing from Redis nodes, and troubleshooting node discovery failures.
---

# Redis Software BIND DNS Setup

Use this skill when configuring BIND as authoritative DNS for Redis Software cluster hostnames. Focus on correct delegation and Redis node FQDN resolution before cluster initialization.

## Prerequisites

Confirm:

- registered domain or delegated subdomain for the Redis cluster
- domain registrar or parent-zone access
- BIND server access
- IP addresses and intended FQDNs for all Redis nodes
- Linux DNS server environment
- DNS port `53` open for UDP and TCP where needed

## Redis-Specific Rules

- Use FQDNs when initializing Redis Software clusters.
- Hostnames must follow RFC-compliant hostname rules.
- Do not rely on raw IP addresses for production cluster identity.
- Do not run multiple competing DNS servers on Redis cluster nodes.
- Avoid mDNS for production; reserve it for development or testing.

## Configuration Workflow

1. Define the Redis cluster DNS zone in BIND configuration.
2. Create the zone file for the Redis cluster domain.
3. Add `A` records for Redis node hostnames.
4. Add `NS` records for authoritative name servers.
5. Add glue records in the parent zone or registrar when needed.
6. Validate zone syntax before restart.
7. Restart or reload BIND.
8. Test DNS resolution from Redis nodes and client networks.

## Validation Commands

Use environment-appropriate equivalents:

```text
named-checkconf
named-checkzone <zone> <zone-file>
systemctl status named
systemctl status bind9
dig <node-fqdn>
dig @<dns-server-ip> <node-fqdn>
nslookup <node-fqdn> <dns-server-ip>
```

Check logs through the OS logging path for BIND zone or startup errors.

## Troubleshooting

- DNS queries fail: confirm BIND service is running, firewall allows port `53`, and clients use the intended resolver.
- Wrong IP returned: inspect `A` records, serial number, reload state, and DNS cache.
- Redis nodes cannot discover each other: verify delegation, NS records, glue records, and node FQDNs.
- Zone fails to load: run zone validation and inspect BIND logs.
- Propagation does not happen: verify parent zone or registrar delegation.

## Response Pattern

Answer with:

1. The Redis cluster DNS zone and node FQDN plan.
2. Parent-zone delegation and glue requirements.
3. BIND validation commands.
4. Resolver tests from Redis nodes.
5. Redis-specific constraints before cluster initialization.
