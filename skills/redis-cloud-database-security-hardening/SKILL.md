---
name: redis-cloud-database-security-hardening
description: Use when securing Redis Cloud database access with TLS, rediss URLs, FQDN certificate validation, Redis Cloud root CA trust, RBAC, Data ACLs, named users, ACL DRYRUN, Redis 8 ACL category changes, key patterns, CIDR allow lists, BYOC subscription allow lists, VPC peering, PrivateLink, Transit Gateway, or disabling public endpoints.
---

# Redis Cloud Database Security Hardening

Use this skill to harden Redis Cloud database access with encryption, least privilege, and network restrictions. Verify current plan capabilities, Redis version behavior, and console options before making availability claims.

## Hardening Order

1. Enable TLS and validate encrypted client connectivity.
2. Replace broad data access with named users, roles, and least-privilege ACLs.
3. Restrict network access with database-level CIDR allow lists.
4. Use private connectivity where available, then disable public endpoints when the architecture supports it.
5. Re-test access after Redis version upgrades or role changes.

## TLS Checklist

- Enable TLS in the Redis Cloud database security settings.
- Use `rediss://` or client-specific TLS options.
- Use the FQDN from the Console, not a raw IP address.
- Confirm the client or SDK supports TLS.
- Install or trust the Redis Cloud CA when required by the client environment.
- For `redis-cli`, verify it has TLS support.

Troubleshoot:

- handshake failure: check `rediss://`, FQDN, port, client TLS support, and CA trust.
- toggle appears unchanged: confirm edit/save flow and wait for configuration update.
- certificate hostname error: stop using raw IPs and use the endpoint hostname.

## RBAC And ACL Workflow

Use Redis Cloud Data Access Control through UI or supported API. Do not manage Redis Cloud users directly with `ACL SETUSER` or `ACL DELUSER` unless official guidance for the environment says so.

For custom roles:

- prefer named users
- scope with key patterns
- keep built-in roles unchanged
- use least privilege
- test with `ACL DRYRUN`

Example dry run:

```text
ACL DRYRUN <username> <command> [arg ...]
```

## Redis 8 ACL Category Review

When Redis 8 is involved, retest custom roles because ACL categories may include module commands such as Query Engine, JSON, time series, and probabilistic data structures.

Check:

- whether `@read` grants Search read commands
- whether `@write` grants JSON or other module writes
- whether `+@all -@write` blocks module writes as intended
- whether Redis 7-era explicit `FT.*` allowances are still needed or now redundant

Do not assume Redis 7 and Redis 8 ACL behavior is identical.

## CIDR And Private Connectivity

Database-level CIDR allow lists:

- add only trusted IPs or CIDR ranges
- confirm application egress IPs
- test before removing old ranges
- remember private and public network controls may both apply

Subscription-level allow lists:

- verify whether the subscription type supports them.

Private connectivity:

- use VPC peering, PrivateLink, Transit Gateway, or equivalent supported options where available
- validate routing, DNS, and security groups
- disable public endpoints only after private connectivity is proven

## Response Pattern

Answer with:

1. Current exposure and target security posture.
2. TLS connection changes.
3. RBAC/ACL design and `ACL DRYRUN` checks.
4. CIDR/private networking controls.
5. Redis version and plan capability checks that must be verified.
