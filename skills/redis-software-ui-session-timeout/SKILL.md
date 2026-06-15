---
name: redis-software-ui-session-timeout
description: "Configure and troubleshoot Redis Enterprise Software Cluster Manager automatic UI logout/session timeout. Use when the user asks how to change `cm_session_timeout_minutes`, adjust auto logout, find the session timeout UI path, use `rladmin` or REST API to update timeout, verify the setting, or debug users being logged out too soon."
---

# Redis Software UI Session Timeout

Use this skill to change or verify the Redis Enterprise Software Cluster Manager UI inactivity timeout.

## Requirements

- Admin privileges on the Redis Enterprise Software cluster.
- Cluster version, because UI paths vary by release.
- A security-approved timeout value in minutes.

## UI Paths

| Redis Software version | Path |
| --- | --- |
| 7.4 and later | `Cluster -> Security -> Preferences`, then edit `Session timeout`. |
| Older UI versions | `Settings -> Preferences -> Session timeout` or equivalent legacy preferences page. |

If the UI path is not visible, use the CLI or REST API method.

## CLI Method

Set the timeout:

```bash
rladmin cluster config cm_session_timeout_minutes <minutes>
```

Verify:

```bash
rladmin info cluster | grep cm_session_timeout_minutes
```

## REST API Method

```bash
curl -k -u <admin-email>:<password> \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{"cm_session_timeout_minutes": <minutes>}' \
  https://<cluster-host>:9443/v1/cluster
```

Handle credentials securely. Do not paste real passwords into shared logs.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| User logs out before configured timeout | Browser cookies/cache, incognito test, another browser, local sleep/network interruptions. |
| Setting does not change | Confirm admin privileges and that UI changes were saved. |
| CLI/API appears successful but UI differs | Verify with `rladmin info cluster`; refresh/relogin to the UI. |
| Timeout still inconsistent | Collect browser details, cluster version, configured value, timestamps, and relevant Cluster Manager logs. |

## Response Pattern

1. Ask for the cluster version and desired timeout.
2. Give the version-appropriate UI path.
3. Provide CLI/API fallback.
4. Include the verification command.
5. Mention browser/session troubleshooting only if the verified cluster setting is correct but behavior still looks wrong.
