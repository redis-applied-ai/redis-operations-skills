---
name: redis-cloud-maintenance-notifications
description: "Configure and troubleshoot Redis Cloud Advanced Notifications for planned maintenance. Use when the user asks who receives maintenance emails, how to enable or opt out of Advanced Notifications, how 14-day maintenance notices work, how to skip or reschedule Redis Cloud maintenance, or why notifications stopped after changing maintenance-window mode."
---

# Redis Cloud Maintenance Notifications

Use this skill for Redis Cloud planned-maintenance notification questions, especially Advanced Notifications tied to manual maintenance windows.

## Core Rules

- Advanced Notifications are for planned maintenance such as scheduled upgrades and optimizations.
- Notices are sent 14 days before scheduled maintenance; the timing is not configurable.
- Urgent cluster-health fixes may proceed without advance notification.
- Advanced Notifications require a Manual Maintenance Window.
- Switching to Automatic Maintenance Window disables Advanced Notifications.
- Switching back to Manual requires enabling Advanced Notifications again.

## Workflow

1. Confirm subscription and role:
   - Redis Cloud subscription is known.
   - User has Owner or Admin role for maintenance-window changes.
   - Operational email addresses are configured for account users.
2. Determine the user objective:
   - Receive notifications.
   - Opt out.
   - Skip upcoming maintenance.
   - Reschedule routine maintenance.
   - Postpone beyond the self-service limits.
   - Troubleshoot missing emails.
3. Guide the relevant action:
   - To enable: open Subscriptions, then Maintenance Window; set the window to Manual and check Advanced Notifications.
   - To opt out: uncheck Advanced Notifications for the subscription.
   - To skip: use the Skip button in the Console.
   - To reschedule: update the subscription Maintenance Window.
   - For postponement longer than the self-service window: open a Support ticket.
4. Verify:
   - Maintenance Window mode is Manual.
   - Advanced Notifications is checked when notifications are expected.
   - Recipient users have operational email enabled.

## Decision Table

| User goal | Action | Constraint |
| --- | --- | --- |
| Receive maintenance notices | Set Manual Maintenance Window and enable Advanced Notifications | Requires Owner/Admin permissions. |
| Stop maintenance notices | Uncheck Advanced Notifications | Applies per subscription. |
| Skip upcoming planned maintenance | Use Skip in the Console | Limited to once per month and skips activities for the next 14 days. |
| Reschedule routine maintenance | Change the Maintenance Window | Applies on the next maintenance cycle. |
| Postpone more than 14 days | Open Support ticket | Requires Support approval. |
| Notifications missing | Check window mode, checkbox, user emails, and operational email settings | Automatic mode disables Advanced Notifications. |

## Safety Checks

- Do not promise that all maintenance can be postponed. Urgent health fixes may not have advance notice or postponement.
- Do not assume every account user receives notifications; check operational email configuration.
- For current limits, UI labels, or policy details, verify live Redis Cloud documentation or Support guidance before presenting them as definitive.

## Escalation Packet

When escalating notification or postponement issues, collect:

- Subscription ID or name.
- Maintenance Window mode and configured window.
- Whether Advanced Notifications is enabled.
- Intended recipient email addresses and whether operational emails are enabled.
- Scheduled maintenance date/time and activity type.
- Whether Skip was already used in the current month.
