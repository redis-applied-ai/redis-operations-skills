---
name: redis-cloud-heroku-downgrade-errors
description: "Resolve Redis Cloud subscription downgrade errors for Heroku add-ons. Use when Heroku says an add-on partner update failed, a Redis Cloud Heroku downgrade may have succeeded despite an error, the plan is stuck in Modifying or Pending, memory or feature limits block a downgrade, or Heroku and Redis Cloud show conflicting add-on tiers."
---

# Redis Cloud Heroku Downgrade Errors

Use this skill when a Redis Cloud Heroku add-on downgrade fails, appears inconsistent, or may have completed despite an error message.

## Core Principle

Heroku and Redis Cloud are separate control planes. A transient add-on partner API error in Heroku can appear even when Redis Cloud completed the subscription change. Verify state in both places before retrying.

## Immediate Verification

1. In Heroku:
   - Open the app.
   - Go to `Resources`.
   - Check the Redis Cloud add-on plan/tier.
   - Note any recent billing or add-on activity timestamp.
2. In Redis Cloud:
   - Open the linked Redis Cloud Console subscription.
   - Check the subscription plan size.
   - Check database memory limits.
   - Confirm the subscription is not `Modifying` or `Pending`.
3. If the target tier appears in either control plane, wait a few minutes, refresh both UIs, and restart app dynos/workers if the application needs to refresh connections or environment state.

## Retry Decision Matrix

| State | Action |
| --- | --- |
| Both Heroku and Redis Cloud show target tier | Treat downgrade as complete; verify billing and app connectivity. |
| Heroku showed an error but Redis Cloud shows target tier | Wait briefly, refresh Heroku, and avoid repeated downgrade attempts. |
| Plan unchanged and no operation is active | Wait 3-5 minutes, check Heroku and Redis status pages, then retry. |
| Subscription is `Modifying` or `Pending` | Do not retry; wait for the active operation to finish. |
| Redis Cloud and Heroku still disagree after 30 minutes | Escalate with evidence from both control planes. |

## Downgrade Blocker Checks

Before retrying, confirm the target plan can support the current database:

1. Check memory usage in Redis Cloud metrics or with:

   ```text
   INFO memory
   ```

2. Confirm `used_memory` is below the target plan capacity with practical headroom.
3. Check whether the lower plan supports current features:
   - Replication.
   - Persistence.
   - Backups.
   - Modules or capabilities.
   - Shard/database sizing.
4. Confirm the user has owner/admin permissions in Heroku and sufficient Redis Cloud permissions.
5. Verify billing is active and invoices are not past due.

## Prevention Guidance

- Avoid repeated rapid plan changes.
- Schedule resizes during lower traffic periods.
- Take a backup or export before reducing capacity.
- Reduce dataset size before attempting a smaller plan.
- Check Heroku and Redis Cloud status pages before retrying a failed change.

## Escalation Packet

Collect:

- Heroku app name.
- Redis Cloud subscription ID.
- Database ID.
- Current plan and intended target plan.
- Exact Heroku error text.
- Timestamp and timezone of the downgrade attempt.
- Current Heroku Resources view state.
- Current Redis Cloud subscription view state.
- Whether the action was attempted from Heroku Dashboard, Heroku CLI, or Redis Cloud Console.
- Memory usage and enabled features that could affect the target plan.

## Completion Criteria

The downgrade is complete when:

- Redis Cloud shows the new tier.
- Database memory limits reflect the target tier.
- Heroku add-on displays the target plan.
- No active `Modifying` or `Pending` operation remains.
- Billing reflects the updated tier.
- Application connectivity is healthy after any required dyno/worker restart.
