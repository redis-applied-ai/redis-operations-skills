---
name: redis-software-socket-location
description: "Plan, configure, and troubleshoot Redis Software Unix socket file locations. Use when the user asks where Redis Enterprise socket files live, how to set socket path during install, whether socket paths can be changed after bootstrap, how to handle post-upgrade socket path mismatches, or errors such as `Failed opening Unix socket: bind: No such file or directory`."
---

# Redis Software Socket Location

Use this skill for Redis Software socket-file path questions and migrations.

## Core Rules

- Redis Software versions before 5.2.2 default socket files to `/tmp`.
- Redis Software 5.2.2 and later default socket files to `/var/opt/redislabs/run`.
- Upgrades from pre-5.2.2 do not automatically migrate socket paths.
- Set a custom socket path during installation when possible.
- Changing socket path after cluster bootstrap is not directly supported.
- Do not use deprecated `rlutil` socket-path changes.

## Fresh Install Workflow

1. Choose the socket path before installation.
2. Ensure the target directory exists.
3. Ensure it is writable by `redislabs`.
4. Install Redis Software with:

   ```bash
   sudo ./install.sh -s /path/to/socket/files
   ```

5. Verify sockets are created in the expected directory after install.

## Existing Cluster Decision Tree

If a bootstrapped cluster needs a different socket path, choose a supported migration:

| Situation | Recommended approach |
| --- | --- |
| Need same cluster with changed path | Replace nodes one by one using new installs with the desired `-s` path. |
| Can create a new cluster | Build a new cluster with the desired socket path and migrate using Replica Of. |
| Post-upgrade mismatch | Verify current paths and plan node replacement or supported migration. |
| PDNS or cluster errors reference invalid socket path | Check logs and socket path consistency, then plan remediation or migration. |

## Node Replacement Path

1. Install Redis Software on a new node using `install.sh -s <path>`.
2. Add the new node to the cluster.
3. Migrate workload off an old node.
4. Remove the old node.
5. Repeat until all nodes use the desired socket path.

## Replica Of Migration Path

1. Create a new Redis Software cluster with the desired socket path.
2. Configure Replica Of from the old cluster to the new cluster.
3. Validate data replication.
4. Shift production traffic.
5. Decommission the old cluster after validation.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `Failed opening Unix socket: bind: No such file or directory` | Directory exists, socket path configured consistently, service can write to path. |
| Socket file missing | Confirm service status and expected path for the installed version. |
| Permission denied | Confirm `redislabs:redislabs` ownership and write permissions. |
| Nodes disagree on socket path | Compare install/config history and plan node replacement or migration. |
| Errors after upgrade | Remember upgrade does not automatically migrate pre-5.2.2 socket locations. |

## Safety Checks

- Do not recommend directly editing socket paths on existing bootstrapped nodes as a normal procedure.
- Do not recommend deprecated `rlutil` path changes.
- Before migration, ask about production traffic, endpoint migration, backups, and rollback plan.

## Escalation Packet

Collect:

- Redis Software version and upgrade history.
- Current socket path per node.
- Desired socket path.
- Relevant logs containing socket errors.
- Ownership and permissions for the socket directory.
- Chosen migration method: node replacement or Replica Of.
