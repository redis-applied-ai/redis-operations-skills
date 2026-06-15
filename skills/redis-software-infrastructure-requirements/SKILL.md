---
name: redis-software-infrastructure-requirements
description: Use when planning Redis Software infrastructure before installation or upgrade, including CPU and RAM sizing, node count, quorum, supported operating systems, OS patching, network throughput, required ports, swap, NTP or Chrony clock sync, rack-zone awareness, cluster size limits, Redis Flex or Redis on Flash sizing, and deployment review with Redis Support.
---

# Redis Software Infrastructure Requirements

Use this skill before installing or upgrading Redis Software on virtual machines or bare metal. Exact platform support and sizing guidance can change by Redis Software version, so verify current official Redis docs and release notes before finalizing a production plan.

## Predeployment Tracks

Evaluate these tracks in order:

1. Supported OS and Redis Software version.
2. CPU, RAM, storage, and network sizing.
3. Node count, quorum, and failure-domain layout.
4. OS tuning: swap, time sync, firewall, and ports.
5. Product-specific features such as Redis Flex or Redis on Flash.
6. Evidence packet for Redis Support review when the deployment is important or high risk.

## Hardware Sizing Starting Points

Use source-derived sizing as a planning baseline, then recalculate for the workload:

- CPU: at least a few cores per node; production commonly needs more.
- RAM: enough for data, replicas, overhead, and headroom.
- Shard planning: estimate shard count from operations per second, memory per shard, replication, and proxy overhead.
- Reserve headroom for non-database processes and failover.
- Confirm storage with `redis-software-supported-storage`.

Do not treat generic minimums as production sizing. Ask for dataset size, write rate, read rate, persistence mode, replication, modules/features, latency target, and growth expectations.

## OS And Version Checks

1. Identify the target Redis Software version.
2. Verify the exact supported OS list for that version from current Redis docs.
3. Confirm the OS is fully patched and still inside vendor support.
4. Before a Redis major-version upgrade, verify that the existing OS remains supported by the target Redis version.
5. If the OS is deprecated or no longer supported for the target release, plan OS migration before or as part of the Redis upgrade.

## Network And Ports

Confirm:

- low-latency node-to-node connectivity
- enough bandwidth for client traffic, replication, shard migration, persistence, and storage access
- required Redis Software ports are free and open between nodes
- client ingress paths to database endpoint ports are approved
- DNS and cluster FQDN design are complete before cluster creation

If installation fails due to ports already in use, identify the process using the port before changing Redis configuration.

## OS Optimization

For production:

- Disable or tightly control swap to avoid latency and eviction surprises.
- Configure NTP or Chrony on every node before cluster creation.
- Apply Redis-approved system tuning through the installer or managed hardening process.
- Keep firewall rules explicit and reviewed.
- Run `/opt/redislabs/bin/rlcheck` after host preparation and installation.

## Topology Rules

- Use at least three nodes for quorum and high availability.
- Prefer an odd number of nodes for quorum planning.
- Spread nodes across racks, zones, or failure domains and enable rack-zone awareness where appropriate.
- Avoid placing primaries and replicas in the same failure domain.
- Verify current maximum supported cluster size for the Redis Software release before designing very large clusters.

## Redis Flex And Flash Planning

When planning Redis 8/Flex or older Redis on Flash deployments:

- Verify which engine applies to the target Redis version.
- Revisit RAM-to-flash ratios during major-version upgrades.
- Use locally attached flash devices for Flex/flash tiers.
- Keep flash storage separate from persistence devices and I/O paths.
- Validate hot set, latency target, and failure behavior under load.

## Support Review Packet

For production deployment review, gather:

- Redis Software target version and install package.
- OS, kernel, patch level, and virtualization or bare-metal details.
- node count, CPU, RAM, NICs, disk layout, and failure-domain map.
- storage filesystems, mount points, and IOPS/latency expectations.
- port/firewall matrix and DNS/FQDN plan.
- swap, NTP/Chrony, and `rlcheck` status.
- expected database count, shard count, persistence mode, replication, and workload profile.
