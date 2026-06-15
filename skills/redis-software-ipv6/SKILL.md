---
name: redis-software-ipv6
description: "Plan, configure, and troubleshoot IPv6 in Redis Software and Redis Enterprise for Kubernetes. Use when the user asks about Redis Software IPv6 support, internal cluster IPv6, `use_internal_ipv6`, Bootstrap REST API, `redisEnterpriseIPFamily`, IPv6-only or dual-stack Kubernetes, AAAA records, external IPv6 addresses, node join NodeBootstrapError, UI unreachable after disabling IPv6, SSO IPv6 issues, or changing node IPs within the same protocol family."
---

# Redis Software IPv6

Use this skill when planning or debugging IPv6 for Redis Software self-managed clusters or Redis Enterprise for Kubernetes.

## Current-State Rule

IPv6 support depends on Redis Software version, operator version, Kubernetes networking, and known release issues. Verify current official docs and release notes before pinning supported versions or promising feature behavior.

## Core Rules

- Decide internal IPv4 versus IPv6 before cluster creation.
- Internal cluster IP family cannot be switched in place after cluster creation.
- All nodes must match the chosen internal IP family.
- Internal node-to-node communication uses either IPv4 or IPv6, not both.
- Existing clusters can change an internal address only within the same protocol family.
- Do not edit CCS fields directly for IPv6 toggles; use supported `rladmin` or API paths.

## Self-Managed Cluster Preflight

Confirm:

- Redis Software version supports the intended IPv6 mode.
- OS IPv6 is enabled on every node.
- Every node has a valid unicast IPv6 interface.
- `/etc/hosts` includes `::1 localhost` on every node.
- DNS has appropriate records:
  - `A` for IPv4.
  - `AAAA` for IPv6.
  - Both for dual-stack external access.
- Firewalls and security groups allow required IPv6 traffic.

## Bootstrap Guidance

For a new self-managed IPv6 internal cluster, set IPv6 only during bootstrap through the supported REST API payload, including `use_internal_ipv6: true` for the first node.

Important:

- Use a valid host IPv6 address, not a CIDR prefix.
- When joining additional nodes, do not force a mismatched `use_internal_ipv6`; joining nodes inherit the cluster internal family.
- A node without IPv6 cannot join an IPv6 internal cluster.

## Kubernetes Guidance

For Redis Enterprise for Kubernetes:

- Use a Kubernetes version and CNI that support the intended IPv6 or dual-stack mode.
- Set the supported REC field for IP family selection when required by the operator/version.
- Validate Services, Ingress, Routes, and DNS from both application pods and external clients.
- Confirm whether SSO, IdP callbacks, proxies, and load balancers support IPv6 or dual-stack behavior.

## External Addresses

For multi-IP nodes, internal and external addresses can differ. Manage external addresses through supported commands:

```bash
rladmin node <id> external_addr add <ipv6-address>
rladmin node <id> external_addr set <ipv6-address>
rladmin node <id> external_addr remove <ipv6-address>
```

## Change Internal Address Within Same Protocol

Use only when changing an address within the same IP family:

1. Demote the node:

   ```bash
   rladmin node <id> enslave demote_node
   ```

2. Disable supervisor:

   ```bash
   systemctl disable rlec_supervisor
   ```

3. Change the OS IP and reboot.
4. From another node, update the Redis Software node address:

   ```bash
   rladmin node <id> addr set <new-ipv6-address>
   ```

5. Re-enable and start supervisor:

   ```bash
   systemctl enable rlec_supervisor
   systemctl start rlec_supervisor
   ```

6. Verify:

   ```bash
   rladmin status nodes
   ```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| UI unreachable after OS IPv6 disabled | Redis Software still has IPv6 enabled; use supported cluster config toggle. |
| Node join fails | Node lacks IPv6, cluster IP family mismatch, missing `::1 localhost`, or wrong bootstrap/join payload. |
| Kubernetes DNS fails | AAAA records, Service IP family, CoreDNS, CNI, route/ingress, and pod resolution. |
| SSO or UI redirect fails | IdP, proxy, callback URL, and DNS support for IPv6/dual-stack. |
| Cluster API 503 or connection errors | Partial support or known bug in older release; verify release notes. |
| AWS VPC DNS issue | AWS resolver behavior with IPv6 name servers; use supported resolver strategy. |

Use:

```bash
rladmin cluster config ipv6 enabled
rladmin cluster config ipv6 disabled
curl -6 <url>
dig AAAA <name>
```

## Escalation Packet

Collect:

- Redis Software and operator versions.
- Self-managed or Kubernetes deployment.
- Cluster creation IP family and whether it is new or existing.
- Node IPs, interfaces, and `/etc/hosts` status.
- DNS records and `dig A/AAAA` results.
- Bootstrap/join payload with secrets redacted.
- REC spec fields for Kubernetes.
- Error text such as `NodeBootstrapError`, UI 503, TLS, or SSO callback failures.
