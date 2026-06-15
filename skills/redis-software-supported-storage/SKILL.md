---
name: redis-software-supported-storage
description: Use when planning, validating, or troubleshooting Redis Software storage on virtual machines or bare metal, including persistent block storage, EXT4 or XFS filesystems, NFS or shared storage rejection, ephemeral disk usage, Redis Flex or Auto-Tiering flash storage, AOF/RDB persistence paths, backup destinations, mount stability, disk latency, IOPS, storage migration, or storage-related failover and startup failures.
---

# Redis Software Supported Storage

Use this skill to assess Redis Software storage layouts before installation, upgrades, maintenance, or incident recovery. Storage support can change by Redis Software version and deployment mode, so verify current official Redis docs when making final support claims.

## Storage Rules

- Production Redis Software requires persistent block storage for cluster metadata, logs, and database persistence files.
- Use supported local filesystems such as `EXT4` or `XFS` for persistent volumes.
- Do not use NFS, NAS, RWX, or shared filesystem storage for Redis Software persistence, even if benchmark results look acceptable.
- Never place AOF/RDB persistence on ephemeral storage.
- Keep persistent, ephemeral, and Flash/Flex storage on separate devices and I/O paths.
- Use maintenance mode for production storage migration, resizing, or node-level storage work.

## Storage Types

| Type | Use | Requirements | Avoid |
| --- | --- | --- | --- |
| Persistent storage | Cluster metadata, logs, AOF, RDB, backups if local backup paths are used | Dedicated block volume or virtual disk; stable mount; `EXT4` or `XFS`; `redislabs:redislabs` ownership | NFS, NAS, shared/RWX storage, ephemeral disks |
| Ephemeral storage | Temporary working files or non-critical logs | Local disk attached to the node | Persistence, backups, anything needed after reboot |
| Flash/Flex storage | Redis Flex or Auto-Tiering cold tier for large datasets | Locally attached SSD/NVMe dedicated to Redis Flex | Network-attached storage or shared physical devices with persistence |
| Backup destination | Recovery copy outside the database path | External object storage or isolated backup target | Same failure domain as the cluster |

## Preflight Checklist

Before install or storage changes:

1. Identify all mount points Redis Software will use.
2. Confirm persistent volumes are block devices with `EXT4` or `XFS`.
3. Confirm mounts are stable in `/etc/fstab` or equivalent and available before Redis services start.
4. Confirm path ownership:

   ```bash
   chown -R redislabs:redislabs <path>
   ```

5. Run Redis Software checks where available:

   ```bash
   /opt/redislabs/bin/rlcheck
   ```

6. Confirm IOPS and latency are adequate for the expected write load, AOF rewrite, snapshots, and backups.
7. Confirm disk utilization alerting, typically before disks reach high-utilization failure bands.
8. Test backup restore in staging before upgrades, topology changes, or storage migration.

## Troubleshooting

| Symptom | Likely cause | First checks |
| --- | --- | --- |
| Cluster fails to start or node cannot join | Unsupported shared storage, mount missing, or permissions wrong | `mount`, `df -h`, filesystem type, owner/group, `rlcheck`, supervisord logs. |
| Data missing after failover or reboot | Persistence stored on ephemeral disk or wrong path | Database persistence config, AOF/RDB path, mount history. |
| AOF rewrite slow or failing | Disk latency, low IOPS, or disk full | Disk metrics, AOF rewrite logs, free space, I/O queue depth. |
| Redis restarts after reboot | Mount point loaded late or not mounted | Boot logs, `fstab`, systemd mount dependencies. |
| Latency spikes on Flex database | Flash storage is remote/shared or contended | Confirm local NVMe/SSD, separation from persistence, and hot/cold ratio. |
| PVC or disk cleanup is risky | Redis processes or finalizers may still be active | Stop and collect current process, mount, and cluster state before cleanup. |

## Storage Change Workflow

For production changes:

1. Confirm recent backups and a tested restore path.
2. Place one node at a time into maintenance mode using `redis-software-node-maintenance-patching`.
3. Migrate or resize the storage.
4. Verify mounts, ownership, filesystem, and service startup.
5. Exit maintenance mode and confirm `rladmin status` is healthy.
6. Repeat for the next node only after the cluster is stable.

## Escalation Packet

Collect:

- Redis Software version and deployment mode.
- Storage type, filesystem, mount options, and path layout.
- `df -h`, `mount`, and filesystem-type output.
- `rlcheck` output.
- Relevant `/opt/redislabs/log/` entries.
- Database persistence mode and AOF/RDB paths.
- Disk latency, IOPS, utilization, and recent storage changes.
