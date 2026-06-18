---
name: redis-cloud-delete-database
description: "Safely guide Redis Cloud database deletion and related billing cleanup. Use when the user asks to delete a Redis Cloud database, remove a database from the console, automate deletion through API or Terraform, delete a subscription after deleting databases, stop billing, troubleshoot missing Delete Database buttons, or handle AWS/GCP Marketplace-linked subscriptions."
---

# Redis Cloud Delete Database

Use this skill for Redis Cloud database deletion. Deletion is permanent; keep diagnosis, owner handoff, confirmation, and final delete instructions as separate states.

## Safety Rules

- Confirm the exact account, subscription, database name, and database ID before deletion.
- Require a backup/export decision before deletion.
- Do not treat database deletion as subscription cancellation.
- Do not collect full payment card data while troubleshooting billing cleanup.
- Do not tell any user or Account Owner to delete, click `Delete Database`, or perform deletion until the explicit confirmation gate is satisfied.
- Treat `FLUSHDB` and `FLUSHALL` as destructive data-removal commands that require explicit confirmation.

## Required Deletion States

Follow these states in order. Do not skip ahead.

1. **Diagnosis and target review**
   - Collect account, subscription, database name, database ID, role, backup/export status, dependency status, and billing goal.
   - If the user lacks permission, explain the role blocker and prepare an owner review handoff.
   - Do not include final console paths or language like "have the owner delete" in this state.
2. **Owner handoff before confirmation**
   - Ask an Account Owner to review the target and confirm whether they are willing to authorize deletion.
   - Use wording like: "Please review database `<name>` / `<id>` in subscription `<subscription>` and confirm whether you accept permanent data loss. Do not delete yet."
   - If the goal is database deletion only, include that the subscription must remain active.
3. **Explicit confirmation gate**
   - Require a standalone confirmation before final instructions:
     - "I understand that deleting Redis Cloud database `<name>` / `<id>` is permanent data loss. The backup/export decision is complete, dependencies are cleared, and I authorize deletion of this database only."
   - If the user wants billing stopped, the confirmation must say whether subscription cancellation is also intended.
4. **Final delete instructions**
   - Only after the explicit confirmation gate is satisfied, provide the console, API, or Terraform deletion steps.
   - Verify the database disappears afterward and separately verify subscription or marketplace billing state when billing cleanup is in scope.

## Pre-Delete Checklist

1. Confirm the user has the Owner role or an Account Owner is available to review and explicitly authorize the action.
2. Confirm the database is the intended target, including environment and region.
3. Confirm applications, clients, jobs, dashboards, and alerts no longer depend on the database.
4. Export or back up data if there is any chance it will be needed later.
5. For Active-Active databases, confirm deletion will remove the database across all participating regions.
6. Confirm no region operation, maintenance task, or background change is currently in progress.
7. Ask whether the user also wants to delete the subscription to stop billing.

## Missing Delete Button Workflow

1. Confirm account, subscription, database name, database ID, and the user's role.
2. If the user is not an Owner or Account Owner, explain that deletion is blocked by role.
3. Send an owner review handoff that asks the Account Owner to validate the target and confirmation requirements.
4. Do not provide final deletion steps until the Account Owner or authorized operator gives the explicit confirmation statement.
5. If an Account Owner also cannot see the button, check active maintenance, region operations, background changes, and escalation data.

## Post-Confirmation Console Deletion Workflow

Use this workflow only after the explicit confirmation gate is satisfied.

1. Open Redis Cloud Console.
2. Go to `Databases`.
3. Select the database.
4. In the `Configuration` tab, scroll to `Danger Zone`.
5. Choose `Delete Database`.
6. Review the confirmation dialog.
7. If this is the only database in the subscription and the user wants billing stopped, choose the subscription deletion option if presented.
8. Confirm deletion only after the user has explicitly accepted the permanent data loss.
9. Verify the database no longer appears in the database list.

## API or Terraform Deletion

Use automation only for controlled teardown workflows.

Before running automation:

- Confirm Account Owner API key scope.
- Confirm the target subscription and database ID.
- Confirm backup/export status.
- Confirm state management for Terraform so the deletion is tracked correctly.
- Record the deletion request and result.

## Subscription and Account Cleanup

| Goal | Required action |
| --- | --- |
| Delete one database only | After explicit confirmation, delete the database; subscription may continue billing. |
| Stop billing for a subscription | After explicit confirmation, delete all databases, then delete/cancel the subscription. |
| Cancel marketplace billing | Cancel or unlink through AWS or GCP Marketplace as required. |
| Close Redis Cloud account | Delete databases/subscriptions, remove extra users, pay invoices, remove payment methods, then submit the privacy/account closure request. |

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Delete button is missing | User is not Account Owner or a maintenance/region operation is blocking deletion. |
| Delete button is disabled | Background operation is active; wait and retry after it completes. |
| Subscription still bills after database deletion | Subscription was not deleted or marketplace billing remains linked. |
| Cannot delete subscription | Databases remain or unpaid invoices block closure. |
| Database stuck deleting | Maintenance or background operation; refresh after waiting and escalate if it does not clear. |
| User only wants to empty data | Consider `FLUSHDB` or `FLUSHALL` only after explicit confirmation and backup decision. |

## Escalation Packet

Collect:

- Account, subscription, database name, and database ID.
- User role and whether an Account Owner attempted deletion.
- Backup/export status.
- Active-Active participation and regions.
- Current maintenance or region operation status.
- Error text or console/API response.
- Whether billing is Redis-direct, AWS Marketplace, GCP Marketplace, or another integration.
- Whether the goal is database deletion, subscription cancellation, or full account closure.
