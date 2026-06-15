---
name: redis-cloud-backups
description: "Configure, monitor, and troubleshoot Redis Cloud database backups. Use when the user asks how to enable scheduled backups, run Backup Now, configure S3/GCS/Azure/FTP backup destinations, set backup frequency or retention, inspect backup status, fix permission errors, or understand plan-specific backup behavior in Redis Cloud."
---

# Redis Cloud Backups

Use this skill for Redis Cloud backup setup and troubleshooting.

## Current-State Rule

Backup capabilities, storage options, frequency, and retention controls can vary by plan and may change. Verify current Redis Cloud console/API behavior or documentation before stating plan limits as current fact.

## Configuration Workflow

1. Gather context:
   - Redis Cloud subscription and database.
   - Plan/tier.
   - Desired backup frequency and retention.
   - Remote storage provider: S3, GCS, Azure Blob, or FTP.
   - Whether an immediate on-demand backup is needed.
2. Open database settings:
   - Sign in to Redis Cloud.
   - Select subscription and database.
   - Open Configuration.
   - Find Durability.
3. Enable backups:
   - Toggle Enable Backups on.
   - Save configuration after setting destination and schedule.
4. Configure remote storage:
   - S3: bucket and policy allowing Redis Cloud to write objects.
   - GCS/Azure Blob: token or access configuration with write permissions.
   - FTP: host, username, password, and destination path.
5. Set schedule:
   - Essentials commonly uses fixed daily backups.
   - Pro can support configurable frequency and retention.
   - Verify current controls in the user's account.
6. Run on-demand backup:
   - Use Backup Now only after backups are enabled and saved.
7. Monitor:
   - Check database Activity tab.
   - Use Redis Cloud API when automation or audit is needed.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Backup Now is disabled | Backups are enabled, destination is saved, and current plan supports on-demand backup. |
| No backup records appear | Remote storage configuration, network reachability, and Activity tab status. |
| Permission denied | IAM policy, bucket/container ACL, token scope, or FTP credentials. |
| Frequency control missing | Plan/tier may not support custom frequency; verify current plan behavior. |
| Backup fails after storage change | Validate path, credentials, object write permissions, and provider-side logs. |

## Safety Checks

- Do not ask users to paste storage secrets, FTP passwords, or access tokens into chat.
- Confirm backup target is customer-approved and meets data residency/security requirements.
- Do not treat backup configuration as a restore test; separately validate restore procedures where required.
- Before changing production backup schedules or retention, ask about recovery objectives and compliance requirements.

## Escalation Packet

Collect:

- Subscription and database ID/name.
- Plan/tier.
- Backup destination type.
- Backup schedule and retention settings.
- Last successful and failed backup timestamps.
- Exact error message.
- Storage-side permission or access logs, with secrets redacted.
