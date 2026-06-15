---
name: redis-software-firewalld
description: "Configure and troubleshoot firewalld for Redis Software on CentOS/RHEL hosts. Use when the user asks about `redislabs` or `redislabs-clients` firewalld services, Redis Enterprise installation firewall prompts, opening client/database ports, custom Cluster Manager ports, RHEL 9 firewalld service XML permission issues, rules reverting after reboot, or client/node connectivity blocked by host firewall."
---

# Redis Software Firewalld

Use this skill for Redis Software host-level `firewalld` setup on CentOS/RHEL.

## Current-State Rule

Port requirements can vary by Redis Software version, custom port configuration, and database endpoint choices. Confirm the installed version and official network port matrix before finalizing firewall rules.

## Core Concepts

- `firewalld` uses zones and services; the default zone is often `public`.
- Redis Software installation creates built-in service XML files under `/etc/firewalld/services/`.
- `redislabs` covers internal cluster, management, replication, metrics, and related service traffic.
- `redislabs-clients` covers client-to-cluster database traffic.
- Installer auto-configuration may add `redislabs`, but client access often still requires adding `redislabs-clients`.
- Firewalld rules are not a full hardening model; use security groups, external firewalls, and OS hardening as appropriate.

## Setup Workflow

1. Confirm prerequisites:
   - Root or sudo access.
   - Redis Software installed or staged.
   - Correct firewalld zone.
   - Version-specific port matrix.
2. Check built-in Redis service definitions:

   ```bash
   ls -l /etc/firewalld/services/redislabs*.xml
   ```

3. Add internal cluster service to the correct zone:

   ```bash
   sudo firewall-cmd --permanent --zone=public --add-service=redislabs
   ```

4. Add client access service if applications connect through host firewall:

   ```bash
   sudo firewall-cmd --permanent --zone=public --add-service=redislabs-clients
   ```

5. Add custom ports if the deployment remaps management or database ports:

   ```bash
   sudo firewall-cmd --permanent --zone=public --add-port=<PORT>/tcp
   ```

6. Reload and verify:

   ```bash
   sudo firewall-cmd --reload
   sudo firewall-cmd --list-all
   ```

## Common Port Areas to Verify

Use the official matrix for the exact version, but commonly review:

- Database endpoint range.
- Cluster Manager UI port, especially if changed with `rladmin cluster config cm_port <new-port>`.
- Prometheus endpoint.
- Internal transport and HA ports.
- ICMP echo between nodes where required by network policy.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Clients cannot connect | `redislabs-clients` missing from zone or custom DB port not open | Add client service or explicit port. |
| Node join fails | Internal ports or ICMP blocked | Confirm `redislabs` service and inter-node reachability. |
| Web UI moved to custom port | New port not opened | Add the custom port permanently and reload. |
| RHEL 9 cannot add Redis service | XML permission issue in affected versions | Upgrade or ensure `/etc/firewalld/services/*.xml` is readable, for example mode `644`. |
| Nonstandard DB ports fail | Custom ports not in firewalld | Add each custom endpoint port. |
| Rules disappear after reboot | Rules were not permanent | Reapply with `--permanent` and reload. |
| Connectivity still fails | External firewall, security group, SELinux, antivirus, or resource pressure | Check layers beyond firewalld and review `/var/log/firewalld`. |

## Safety Checks

- Confirm the zone before adding services; do not assume `public` is correct.
- Do not open broad ranges externally without reviewing exposure and security controls.
- Document any custom port changes and ensure monitoring/backups include `/etc/firewalld/services/`.
- After firewall changes, verify Redis cluster health and client connection paths.

## Escalation Packet

Collect:

- OS version and Redis Software version.
- Active firewalld zone and `firewall-cmd --list-all`.
- Redis service XML permissions.
- Custom ports or changed Cluster Manager port.
- Client and node connectivity tests.
- `/var/log/firewalld` errors.
