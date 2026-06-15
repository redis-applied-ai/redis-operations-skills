---
name: redis-cloud-inactivity-deletion-prevention
description: "Assess and prevent Redis Cloud database deletion due to inactivity for Free, Trial, Evaluation, Heroku, or marketplace free tiers. Use when the user asks whether a paid Redis Cloud database can be deleted for inactivity, how to keep a free database active, what counts as activity, how to handle seasonal workloads, whether console login counts, or how to respond to inactivity warning emails."
---

# Redis Cloud Inactivity Deletion Prevention

Use this skill to classify inactivity-deletion risk and recommend durable prevention.

## Core Rules

- Paid Redis Cloud commercial subscriptions such as Essentials, Pro, Flex, and paid marketplace plans are not deleted due to inactivity alone as long as the subscription and billing remain active.
- Free, Trial, Evaluation, promotional, or platform free add-on databases may be deleted after an inactivity window. Verify the current policy window in Redis Cloud terms or console notices before making exact-date commitments.
- Console login, viewing metrics, or leaving a database provisioned is not the same as Redis command activity. Successful Redis commands such as `GET` or `SET` count as database activity.
- Important data should not live only in a free/evaluation database.

## Risk Classification

| Situation | Inactivity deletion risk | Guidance |
| --- | --- | --- |
| Paid Essentials/Pro/Flex/marketplace-paid | No inactivity deletion alone | Keep billing active and monitor subscription status. |
| Free/Trial/Evaluation Redis Cloud | Yes | Upgrade or back up externally; optional keepalive is only a short-term mitigation. |
| Heroku or platform free add-on | Yes, plus platform policy risk | Upgrade tier or export regularly. |
| Redis Software or self-hosted Redis | No Redis Cloud inactivity deletion | Check infrastructure lifecycle and backup policies instead. |

## Prevention Workflow

1. Identify the plan/subscription type in Redis Cloud Console.
2. Check warning emails for inactivity, empty subscription, or pending deletion notices.
3. If the data matters, move to a paid subscription:
   - Create or upgrade to a paid plan.
   - Export/replicate/restore data.
   - Update application endpoints.
   - Verify application reads/writes.
4. If staying free temporarily, automate a lightweight command and alert on failure:

   ```text
   SET keepalive:<env> "<timestamp>"
   GET keepalive:<env>
   ```

5. Maintain external backups for anything that cannot be lost.

## Seasonal Workload Options

| Goal | Option |
| --- | --- |
| Keep data ready with no restore next season | Maintain a minimal paid database year-round and scale up before peak. |
| Minimize idle cost | Export to external storage, delete the database/subscription, recreate and restore later. |
| Keep free tier during idle season | Not recommended for important data; use keepalive and external backups if temporary. |

Deleting only a database may not stop billing. Confirm whether the subscription also needs deletion when the goal is to stop charges.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Free database disappeared | Inactivity cleanup, empty subscription, or platform maintenance cleanup | Check warning emails and backups; restore into a new paid database if possible. |
| Inactivity warning received | Free/trial database at risk | Run a successful command immediately, take/export backup, and upgrade if important. |
| Paid Flex database idle | No inactivity deletion; charges continue | No keepalive needed; delete subscription only if intentionally stopping service and billing. |
| Console activity did not prevent deletion | No Redis commands reached the database | Use real Redis command keepalive if staying free temporarily. |
| Heroku add-on removed | Free/promotional tier policy or maintenance | Check platform notices and restore from backup if available. |

## Escalation Packet

Collect:

- Redis Cloud account and subscription name.
- Plan type and whether it is free/trial/evaluation/paid.
- Database ID/name and last known active date.
- Warning email subjects and timestamps.
- Backup/export availability.
- Platform provider details if Heroku or marketplace add-on.
- Whether any successful Redis commands were sent during the inactivity window.
