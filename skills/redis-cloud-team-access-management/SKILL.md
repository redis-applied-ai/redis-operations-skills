---
name: redis-cloud-team-access-management
description: "Manage Redis Cloud team members, console roles, invitations, notification settings, MFA status, and user removal. Use when the user asks how to add or invite a Redis Cloud user, choose Owner/Manager/Member/Viewer roles, fix missing invitation emails, resend expired invites, edit roles, remove team members, or explain why a user cannot access billing, subscriptions, or databases."
---

# Redis Cloud Team Access Management

Use this skill for Redis Cloud Console account and organization access. Do not confuse console team roles with Redis database ACL users.

## Invite Workflow

1. Confirm the requester has permission to manage team access. In Redis Cloud, this is typically an Owner-level action.
2. In the Redis Cloud Console, open the account or organization and go to `Team` or `Team Management`.
3. Choose `Add Member`, `Add User`, or `Invite User`.
4. Enter the user's name, email address, role, and notification preferences.
5. Send the invitation.
6. Ask the invited user to accept the email link and complete signup.
7. Verify the user appears in the Team list with the intended role.

## Role Guide

| Task | Owner | Manager | Member | Viewer |
| --- | --- | --- | --- | --- |
| Manage team access | Yes | No | No | No |
| Manage account settings | Yes | No | No | No |
| Billing and payments | Yes | No | No | No |
| Create subscriptions | Yes | Yes | No | No |
| Create databases on Flexible plan | Yes | Yes | No | No |
| Edit databases with cost impact | Yes | Yes | No | No |
| Create databases on Essentials plan | Yes | Yes | Yes | No |
| Edit databases without cost impact | Yes | Yes | Yes | No |
| View subscriptions and databases | Yes | Yes | Yes | Yes |

Use the least-privilege role that supports the user’s task. Use Viewer for read-only access, Member for limited database operations, Manager for operational subscription/database management, and Owner for account, billing, and team administration.

## Editing Users

- Role, name, and notification preferences can be edited from the Team list.
- Email address changes are not a normal edit operation; use an invite for the correct email or follow the account email-change workflow if the user owns the account.
- MFA state is controlled by the individual user profile. The admin view can show MFA status, but an admin should instruct the user to enable MFA in their own profile.

## Removal Safety

Removing a team member is permanent. Before deletion:

1. Confirm the exact user email.
2. Confirm that the user should lose Redis Cloud console access.
3. Check whether they are the only Owner or responsible billing/admin contact.
4. Ask for explicit confirmation before selecting `Delete` or equivalent UI action.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Invitation email missing | Verify email spelling, check spam/junk, then resend from Team Management. |
| Invitation link expired | Resend the invitation. |
| User cannot accept invite | Check whether the email already belongs to another Redis Cloud organization or account state. |
| User cannot perform an action | Compare the action against the role guide and adjust role if appropriate. |
| MFA shows disabled | Instruct the user to enable MFA in their profile; then refresh the Team view. |
| Console issue looks stale | Log out/in, clear cache, or test another browser before escalation. |

## Escalation Packet

Collect:

- Account or organization name.
- Invited user's email address.
- Current role and intended role.
- Exact action the user cannot perform.
- Invitation status and timestamp.
- Error text or screenshots.
- Browser/cache troubleshooting already attempted.
