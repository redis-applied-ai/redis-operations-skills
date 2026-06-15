---
name: redis-cloud-free-inactivity-deletion
description: "Explain and triage Redis Cloud Free database deletion due to inactivity. Use when a Free 30 MB Redis Cloud database disappeared, the user logged into the console but sent no Redis commands, data is missing with no backups, an empty Free subscription blocks creating a new Free database, Heroku or Vercel integrations leave an empty subscription, or the user needs keepalive activity to avoid 14-day inactivity deletion."
---

# Redis Cloud Free Inactivity Deletion

Use this skill when a Redis Cloud Free database disappeared or the user asks why a free database was deleted.

## Core Rule

A Redis Cloud Free 30 MB database can be deleted after 14 consecutive days with no Redis read or write commands reaching the database. Console login, viewing metrics, or opening configuration does not count as activity.

## Confirmation Workflow

Ask:

1. Was the database on the Free 30 MB tier?
2. Did approximately 14 days pass with no Redis commands such as `GET`, `SET`, or application traffic?
3. Does the database no longer appear in Redis Cloud Console?
4. Did the user receive any inactivity warning email? This helps confirm but is not required.

If the first three answers are yes, explain that deletion was expected Free-tier inactivity behavior.

## Recovery Reality

- Deleted Free databases and their data are permanently removed.
- Free databases do not have backup or restore options.
- Redis Support cannot restore a deleted Free database.
- Paid databases are not deleted for inactivity; if a paid database is missing, investigate billing, account deletion, or owner/admin actions instead.

## Next Steps

| Situation | Action |
| --- | --- |
| User wants another Free database | Delete any empty Free subscription, then create a new Free database. |
| Empty Free subscription remains | Delete it in Redis Cloud Console or ask Redis Support to remove it if the UI cannot. |
| Heroku or Vercel integration left an empty subscription | Remove the empty Redis Cloud subscription before creating a new Free database. |
| User needs durable dev/staging data | Use a paid plan with durability and backup options. |
| User says commands were active recently | Collect activity evidence and contact Redis Support for confirmation. |

## Prevention

Ensure at least one Redis command reaches each Free database within every 14-day window. A scheduled keepalive can be:

```redis
SET keepalive_key "active" EX 60
```

Run it from cron, Cloud Scheduler, CI, or another reliable scheduler. The command must reach the actual database; console access does not reset inactivity.

## Escalation Packet

Collect only when deletion is disputed or an empty subscription cannot be removed:

- Redis Cloud account ID.
- Subscription ID.
- Database name.
- Free versus paid tier confirmation.
- Approximate deletion date.
- Approximate timestamps of recent Redis command activity, if any.
- Integration source such as Heroku or Vercel.
- Error shown when trying to delete the empty subscription.
