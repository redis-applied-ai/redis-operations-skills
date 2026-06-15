---
name: redis-software-rhel-firewall-dns
description: "Diagnose and fix Redis Software node UNREACHABLE or degraded status after RHEL/CentOS installation or upgrade caused by DNS, firewalld, security groups, or blocked node-to-node traffic. Use when nodes are unreachable after provisioning, `rladmin status` shows missing/not OK nodes, DNS lookups fail, port 53 is blocked, peer hostnames resolve incorrectly, or RHEL firewalld blocks required Redis Enterprise intra-cluster communication."
---

# Redis Software RHEL Firewall DNS

Use this skill for Redis Software clusters on RHEL/CentOS when cluster formation, health, or upgrades are blocked by DNS or internal network policy.

## Current-State Rule

Do not hardcode a Redis Software port list from memory. Use the official Redis Software network port configuration matrix for the deployed version and environment before requesting firewall/security-group changes.

## Triage Workflow

1. Confirm symptoms:
   - Nodes show `UNREACHABLE` shortly after provisioning.
   - Cluster degraded while services are running.
   - `rladmin status` shows nodes missing or not OK.
   - Connectivity tests fail between nodes.
   - Hostnames resolve to wrong IPs.
2. Identify connection model:
   - URL/FQDN-based client and cluster DNS.
   - IP-based client access with still-required node reachability.
3. Validate DNS before tuning Redis:
   - Cluster FQDN, NS delegation, and node A records.
   - `/etc/hosts` entries, if used.
   - Each node resolves peer node names to correct IPs.
4. Validate DNS reachability:

   ```bash
   getent hosts <peer-hostname>
   nc -vzu <node_ip> 53
   ```

5. Validate node-to-node traffic:
   - Use ping only as a routing check.
   - Test required TCP/UDP ports from the official port matrix.
   - Include control plane, database/shard traffic, DNS, metrics, and internal services as applicable.
6. Recheck cluster health:

   ```bash
   rladmin status
   ```

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Peer name resolves to wrong IP | Bad DNS record or stale `/etc/hosts` | Fix records and retest from every node. |
| DNS lookup times out | DNS traffic blocked or port conflict | Allow DNS traffic and check port 53 conflicts. |
| Ping works but cluster is degraded | Required TCP/UDP ports blocked | Validate against official Redis Software port matrix. |
| Nodes on different network segments fail | VLAN/security-group restrictions | Add appropriate inter-node allow rules for the segment design. |
| RHEL firewalld blocks traffic | Default zone denies required ports | Configure firewalld with Redis-supported services/settings for the version. |
| Stateful firewall drops traffic | Connection tracking or stateful rule behavior | Review firewall state handling and iptables/firewalld rule design. |

## Key Guidance

- Reverse DNS/PTR is not required for Redis Software cluster operation.
- New database endpoint ports may need to be opened; the cluster may not validate external firewall state for those ports.
- DNS and internal allowlists are common root causes for immediate post-provisioning `UNREACHABLE` nodes.
- Fix DNS and connectivity before pursuing Redis database configuration changes.

## Escalation Packet

Collect:

- Redis Software version and OS version.
- `rladmin status` output.
- Connection model: FQDN/URL-based or IP-based.
- Cluster FQDN and node record plan.
- `getent hosts <peer-hostname>` from each node.
- DNS port reachability tests.
- Failed TCP/UDP tests from the official port matrix.
- firewalld zone/rules and cloud security-group/network-policy rules.
