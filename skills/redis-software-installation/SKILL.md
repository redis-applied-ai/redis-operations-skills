---
name: redis-software-installation
description: "Install Redis Software on prepared Linux nodes. Use when the user asks to run the Redis Enterprise Software installer, use `install.sh -y`, create an answer file, set `umask 0022`, handle swap, systune, NTP, firewall ports, rlcheck, redislabs user/group permissions, offline installation, supervisord logs, or validate required ports 8443, 9443, 10000-19999, and 20000-29999 before cluster creation."
---

# Redis Software Installation

Use this skill when installing Redis Software on nodes that have already met system, OS, storage, and network prerequisites.

## Current-State Rule

Installer behavior, supported OS versions, package names, and release-specific validation can change. Verify current official install docs and release notes when exact version behavior matters.

## Preflight Checklist

Confirm:

- Redis Software installation package came from an official Redis source.
- Package checksum or integrity was verified.
- Package is copied to every node.
- User has root or `sudo` access.
- `umask` is set to `0022`.
- Production swap policy is decided; disabling swap is usually preferred.
- Time synchronization is planned.
- Required ports are open between nodes.
- Security team has approved firewall behavior.

Do not reduce `redislabs:redislabs` directory permissions from supported values such as `750` to `700`.

## Install Workflow

Extract the package on each node:

```bash
tar vxf <installation-package>.tar
```

Run the installer from the extracted directory:

```bash
sudo ./install.sh -y
```

The `-y` flag accepts default recommended answers for most installs.

## Interactive Prompt Guidance

| Prompt area | Recommended handling |
| --- | --- |
| Swap enabled | Production should normally avoid swap; proceed only with an explicit decision. |
| Automatic OS tuning | Prefer yes unless the environment has a managed hardening/tuning process. |
| NTP/time sync | Ensure time sync is configured by installer or preconfigured manually. |
| Firewall ports | Open required Redis Software ports or configure custom rules manually. |
| `rlcheck` | Run during install or immediately after. |
| Existing `redislabs` user/group | Investigate prior/partial install before proceeding. |

## Silent Answer File

Use an answer file when defaults need to be controlled:

```text
ignore_swap=no
systune=yes
ntp=no
firewall=no
rlcheck=yes
ignore_existing_osuser_osgroup=no
```

Run:

```bash
sudo ./install.sh -c /path/to/answer-file
```

## Port Checklist

Common required ranges:

- `8443`: Cluster Manager UI.
- `9443`: REST API.
- `10000-19999`: Database endpoints.
- `20000-29999`: Database shards.

Validate inter-node reachability and client access according to the deployment design.

## Post-Install Validation

Run or review:

```bash
/opt/redislabs/bin/rlcheck
rladmin status
```

Check logs:

```bash
/opt/redislabs/log/supervisord.log
```

Confirm:

- `redislabs:redislabs` user/group exists.
- Permissions match supported expectations.
- Required services are running.
- Ports are reachable.
- CPU, RAM, and flash/storage resources are visible.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Permission errors | `umask 0022`, ownership, and supported permissions. |
| Service startup failure | CPU, RAM, flash/storage, supervisord logs, and system tuning. |
| Network failure | Required ports, firewalls, routes, DNS, and security groups. |
| Existing user/group warning | Prior install remnants or permission mismatch. |
| Offline environment issues | Use offline installation procedure and confirm dependencies. |
| Primary change API returns not acceptable | Verify target node is fully bootstrapped and healthy before retrying. |

## Next Step

After installing on all nodes, create a new cluster or join the node to an existing cluster using the supported cluster deployment workflow.

## Escalation Packet

Collect:

- Redis Software version/build and package name.
- OS and version.
- Install command and answer file if used.
- Installer output and `rlcheck` output.
- `/opt/redislabs/log/supervisord.log`.
- User/group permissions.
- Port/firewall validation.
- Whether install is online or air-gapped.
