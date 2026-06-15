---
name: redis-software-cluster-license
description: "Apply, verify, renew, monitor, and troubleshoot Redis Software cluster licenses outside the Kubernetes REC workflow. Use when the user mentions Redis Enterprise license keys, cluster FQDN mismatch, trial vs production license, license expiry, shard or memory entitlement limits, `GET /v1/license`, `PUT /v1/license`, UI license upload, or configuration changes blocked by an expired license."
---

# Redis Software Cluster License

Use this skill for Redis Software cluster licensing through Cluster Manager UI or REST API.

## Core Model

- A Redis Software license is tied to the cluster FQDN/name.
- The cluster FQDN is set during cluster creation and is immutable.
- Production licenses enforce expiration, shard limits, memory/flash limits, and module entitlements.
- After applying a production license, the cluster cannot revert to trial mode.
- Expired licenses leave databases online but block configuration changes such as new DBs, resizing, or scaling.

## Safety Rules

- Treat license text as sensitive commercial configuration.
- Do not paste full license content into chat or logs unless secure handling is approved.
- Verify the cluster FQDN before requesting or applying a production license.
- Preload renewed licenses before expiration when possible.

## Apply or Update License

UI:

1. Open Cluster Manager.
2. Go to Cluster, Configuration, License.
3. Select Change.
4. Paste or upload the license string.
5. Save and verify status.

REST API:

```http
PUT /v1/license
{
  "license": "<license-content>"
}
```

CLI with curl:

```bash
curl -k -u <admin-user> \
  -H "Content-Type: application/json" \
  -X PUT https://<cluster>:9443/v1/license \
  -d '{"license":"<license-content>"}'
```

## Verify and Monitor

```http
GET /v1/license
```

Also check:

- UI: Cluster, Configuration, License.
- Prometheus-compatible metrics such as shard limits and shard usage.
- Alerting/email configuration for expiration notifications.
- Support package or API export for audit evidence.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| License rejected | FQDN in license does not match cluster name | Request corrected license for the exact cluster FQDN. |
| Cannot create or scale databases | Shard, memory, flash, or entitlement limit reached | Remove unused DBs, reduce usage, or upgrade license. |
| UI/configuration changes blocked | License expired | Upload renewed license. |
| User wants trial mode back | Production license was already applied | Use a new cluster for re-evaluation. |
| DR cluster uses same production license | Simultaneous reuse unsupported | Request a dedicated DR or migration license. |

## New Cluster Setup Reminder

During first setup:

1. Install Redis Software.
2. Open `https://<node>:8443/`.
3. Set admin credentials.
4. Set cluster FQDN.
5. Upload the license that exactly matches that FQDN.

## Escalation Packet

Collect:

- Cluster FQDN/name.
- License type: trial, production, temporary, DR, migration.
- License status and expiration.
- `GET /v1/license` output with sensitive license content redacted.
- Current shard/memory/flash usage versus licensed limits.
- Exact UI/API error text.
- Whether this is production, staging, DR, or migration.
