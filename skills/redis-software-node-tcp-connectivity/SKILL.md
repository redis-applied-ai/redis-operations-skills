---
name: redis-software-node-tcp-connectivity
description: "Use when Redis Software node-to-node TCP connectivity fails, including `verify_tcp_connectivity` errors, `CCS ERROR: TIMEOUT`, endpoints marked missing, shards showing `ERROR: timed out`, failed `rlcheck`, blocked internode ports, source-to-destination node port testing with `nc`, host firewall or security group issues, custom Redis Software ports, incomplete cluster diagnostic bundles, or node-level `debuginfo` collection."
---

# Redis Software Node TCP Connectivity

Use this skill when Redis Software cluster nodes cannot reliably communicate over required TCP ports. Always compare failed ports with the official Redis Software port matrix for the deployed version, topology, custom port configuration, and Active-Active usage before requesting network-rule changes.

## Symptoms

Look for:

- `rlcheck` reports `verify_tcp_connectivity` failure from one node IP to another
- `rladmin status nodes` shows `CCS ERROR: TIMEOUT`
- `rladmin status extra all` shows endpoints as missing
- shards show `ERROR: timed out`
- cluster-wide diagnostics miss logs from the impacted node

Treat these first as inter-node communication problems. Do not start with database-level recovery unless node connectivity is already healthy.

## First Commands

```bash
rladmin status extra all
rladmin status extra all errors_only
rladmin status nodes
rlcheck
```

From the `verify_tcp_connectivity` output, record:

- source node IP
- destination node IP
- failed port list
- whether the same destination appears in multiple failures
- whether ports are default or custom configured

## Directional Connectivity Testing

Run tests from the source node to the destination node:

```bash
nc -vz <destination_node_ip> <port>
```

Then test the reverse direction:

```bash
nc -vz <source_node_ip> <port>
```

Repeat for every failed port. If the cluster has more than two nodes, validate required Redis Software ports across all relevant node pairs, not only the first failing pair.

Common source-derived failed ports include `3333`, `3340`, `3344`, `8001`, `8080`, and `9443`, but do not treat that list as complete for every deployment.

## What To Inspect When Tests Fail

| Layer | Checks |
| --- | --- |
| Host firewall | `firewalld`, `iptables`, `nftables`, endpoint security agents. |
| Cloud firewall | Security groups, network security groups, provider firewall rules. |
| Subnet controls | Network ACLs, route tables, VLAN policies. |
| Routing | Source and destination have valid paths both ways. |
| Redis custom ports | `cnm_http_port`, `cnm_https_port`, and other custom Redis Software port settings. |
| Services | `supervisorctl status` and impacted node logs. |

If a single destination node is consistently unreachable, focus on that node's host firewall, security group, route path, and security tooling first.

## Logs And Diagnostics

Review impacted-node logs:

```text
/var/opt/redislabs/log/event_log.log
/var/opt/redislabs/log/cluster_wd.log
/var/opt/redislabs/log/dmcproxy.log
```

If cluster-wide diagnostics are incomplete, collect node-level diagnostics directly:

```bash
/opt/redislabs/bin/debuginfo
```

Preserve logs before restarting services or changing network policy when possible.

## Post-Fix Validation

After firewall, route, ACL, or security-policy changes:

```bash
rladmin status
rladmin status extra all
rlcheck
```

Confirm:

- the affected node no longer shows `CCS ERROR: TIMEOUT`
- endpoints are no longer missing
- shard status can be collected and timeout errors clear
- `verify_tcp_connectivity` passes for the affected node pairs

## Escalation Packet

Collect:

- Redis Software version and whether custom ports are configured
- source node, destination node, and failed port list
- `rlcheck` output showing the failure
- `nc -vz` results in both directions
- `rladmin status extra all` and `errors_only`
- host firewall, cloud firewall, ACL, and route findings
- impacted-node log snippets
- whether cluster diagnostics missed the affected node and whether node-level `debuginfo` was collected
