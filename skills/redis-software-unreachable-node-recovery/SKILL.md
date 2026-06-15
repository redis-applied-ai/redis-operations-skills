---
name: redis-software-unreachable-node-recovery
description: "Recover or replace an UNREACHABLE node in a Redis Enterprise Software cluster. Use when `rladmin status` shows a node not OK, UNREACHABLE, shards show `ERROR: stale info`, Redis services are down, `rlcheck` fails, node connectivity to 9443 is broken, disk/memory/time sync is unhealthy, or the user needs a safe node replacement decision."
---

# Redis Software Unreachable Node Recovery

Use this skill when a Redis Enterprise Software node is marked `UNREACHABLE` or not `OK`.

## Core Rule

Fix node health before retrying database, shard, migration, or maintenance operations. An unreachable node usually indicates OS, service, storage, or network failure.

## Identify Scope

```bash
rladmin status
rladmin status shards
```

Record:

- Node ID and IP.
- Whether the node is `UNREACHABLE`, not `OK`, or intermittently reachable.
- Shards hosted on the node.
- Any `ERROR: stale info` shard state.
- Whether cluster quorum is at risk.

## Node OS Checks

SSH to the node if possible:

```bash
df -h
free -m
timedatectl
```

Check:

- Disk is not full or near exhaustion.
- Memory pressure is not severe.
- Time sync is correct.
- Recent OS patching, reboot, firewall, storage, or hardware events.

## Redis Service Checks

```bash
supervisorctl status
rlcheck
```

All critical Redis Enterprise services should be running. Resolve `rlcheck` failures before continuing.

## Connectivity Checks

From another healthy node:

```bash
ping <node-ip>
curl -k https://<node-ip>:9443
```

Also verify relevant cluster ports and firewall rules if recent network changes occurred.

## Recovery Decision

| Finding | Action |
| --- | --- |
| Network route/firewall failure | Restore connectivity and revalidate cluster status. |
| Redis service stopped | Restart/fix service dependencies, then run `rlcheck`. |
| Disk full | Free space or restore storage, then restart affected services if needed. |
| OS/hardware unstable | Plan node replacement. |
| Node inaccessible | Treat as failed and plan replacement. |
| Shards stale after node returns | Recheck shard status and logs before forcing operations. |

## Replace Node Path

If recovery is not fast or safe:

1. Provision a replacement node with the same compatible Redis Enterprise version.
2. Join it to the cluster using the official cluster join process.
3. Migrate or restore shard placement according to cluster state.
4. Remove the failed node only after confirming replacement capacity and quorum.

Require explicit confirmation before removing a node from the cluster.

## Verification

After recovery or replacement:

```bash
rladmin status
rladmin status shards
rlcheck
```

Confirm:

- Node is `OK`.
- Shards are healthy.
- No stale info remains.
- Cluster operations are unblocked.
- Application connectivity has recovered.

## Evidence To Collect

- `rladmin status` and `rladmin status shards`.
- Node OS health output.
- `supervisorctl status`.
- `rlcheck` output.
- Connectivity test results.
- Recent changes and node logs.
