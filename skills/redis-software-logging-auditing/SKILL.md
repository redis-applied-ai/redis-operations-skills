---
name: redis-software-logging-auditing
description: "Collect, interpret, and configure Redis Enterprise Software logs and audit events. Use when the user asks where Redis Software logs are stored, how to view Cluster Manager logs, how to enable database connection auditing, how to forward logs to syslog or SIEM, or how to troubleshoot missing audit logs, TLS handshake failures, failover events, authentication events, or shard logs."
---

# Redis Software Logging And Auditing

Use this skill to find the right Redis Enterprise Software log source, configure auditing, and build an evidence packet for operations, security, or support cases.

## Log Source Map

| Source | Access path | Use for |
| --- | --- | --- |
| Cluster Manager UI | `Cluster Manager -> Logs` | Event-log level view with filters for time, severity, and event type. |
| REST API | `GET /v1/logs` | Programmatic access to event-log content. |
| Node file system | `/var/opt/redislabs/log/` | Full process-specific logs, including shard, proxy, resource manager, and watchdog logs. |

Only a partial event-log view is available through the UI and REST API. Use node log files for detailed diagnosis.

## Primary Files

| File | Inspect for |
| --- | --- |
| `event_log.log` | User/system events, authentication attempts, configuration changes, high-latency alerts, import failures. |
| `cnm_exec.log` | Database lifecycle actions, failovers, migrations, topology changes. |
| `resource_mgr.log` | CPU/memory management, shard allocation, auto-rebalance decisions. |
| `redis-<ID>.log` | Shard-level Redis logs, replication messages, evictions, client errors. |
| `node_wd.log` | Local node watchdog health checks, process restarts, disk and memory pressure. |
| `cluster_wd.log` | Inter-node watchdog events, node death/recovery, quorum changes. |
| `dmcproxy.log` | Client proxy routing, endpoint assignment, connection failures, timeouts, TLS handshake failures. |

## Collection Workflow

1. Identify the incident type: security/authentication, database lifecycle, client connectivity, failover, resource pressure, or shard-level Redis behavior.
2. Capture the time window, timezone, affected database ID/name, endpoint, node IDs, shard IDs, and client source IPs.
3. Pull UI/API event logs first for timeline context:

   ```bash
   curl -k -u <username>:<password> \
     -H "Content-Type: application/json" \
     https://<cluster_fqdn>:9443/v1/logs | jq
   ```

4. Use `/var/opt/redislabs/log/` on relevant nodes for detailed evidence.
5. Map shard IDs from `rladmin status` to `redis-<ID>.log` when investigating shard-level behavior.
6. Preserve raw snippets with timestamps and avoid editing log content when preparing an escalation packet.

## Audit Logging

Database connection auditing captures connection attempts, authentication outcomes, and disconnections. It is disabled by default and is separate from the Cluster Manager Logs UI and `/v1/logs` API output.

Enable auditing with the cluster configuration command shape:

```bash
rladmin cluster config auditing db_conns \
  audit_protocol <TCP|local> \
  audit_address <address> \
  audit_port <port> \
  audit_reconnect_interval <seconds> \
  audit_reconnect_max_attempts <attempts>
```

Guidance:

- Prefer TCP export to an external SIEM or listener for production.
- Use local output only for constrained diagnostics or lab environments.
- Omit `audit_port` when using local output.
- Verify the destination is reachable and writable before assuming Redis audit generation failed.

## Common Diagnoses

| Symptom | Check |
| --- | --- |
| No audit logs appear | Confirm auditing is enabled with `rladmin cluster config`; verify protocol, address, port, file permissions, and listener reachability. |
| Logs do not reach SIEM | Check network path, firewall, rsyslog/listener status, hostname, and port. |
| TLS handshake failures | Inspect `dmcproxy.log`; verify client certificate, CA trust, TLS versions, and ciphers. |
| Failover or migration timeline unclear | Correlate `event_log.log`, `cnm_exec.log`, `cluster_wd.log`, and shard logs by timestamp. |
| Need slow command evidence | Use database slowlog tooling rather than assuming it appears in Cluster Manager event logs. |
| User asks for ACL LOG | In Redis Enterprise Software, use auditing for connection/authentication review instead of relying on OSS-only `ACL LOG`. |

## Log Retention And Forwarding

- Redis log files normally rotate daily.
- Most logs keep fewer historical copies than watchdog logs; confirm the active logrotate policy on the node.
- Check `/opt/redislabs/config/logrotate.conf` and `/etc/logrotate.d/redislabs` before changing retention.
- Use `rsyslog` or a compatible forwarder to send Redis log files to syslog/SIEM.

## Escalation Packet

Collect:

- Redis Enterprise Software version.
- Affected database and endpoint.
- Node IDs, shard IDs, and relevant `rladmin status` output.
- Incident time window and timezone.
- Event log/API output for the window.
- Relevant process log snippets from `/var/opt/redislabs/log/`.
- Audit configuration and listener status if auditing is involved.
- TLS certificate and CA details for handshake failures.
