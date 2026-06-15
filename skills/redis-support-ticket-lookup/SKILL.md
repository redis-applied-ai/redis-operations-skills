---
name: redis-support-ticket-lookup
description: "Help users find and respond to Redis Support tickets in the Redis Support Portal. Use when the user searches for a ticket number in Help Center, cannot find a Redis Support ticket, wants to check ticket status, reply to Redis Support, view My Requests, see requests they are CC'd on, or understand why teammate-created tickets are not visible."
---

# Redis Support Ticket Lookup

Use this skill when a user needs to find an existing Redis Support ticket or reply in the correct support thread.

## Core Rule

The Help Center search bar finds public support articles, not private support tickets. Tickets are visible only after signing in to the Redis Support Portal and opening `My Requests`.

## Lookup Workflow

1. Ask the user to sign in to the Redis Support Portal with the email address used to open the ticket.
2. Open `My Requests` from the support profile.
3. Search or scan for:
   - Ticket number.
   - Ticket subject.
   - Date opened.
   - Product or deployment mentioned.
   - Most recent Redis Support reply.
4. If the user was CC'd, check the requests CC tab.
5. Open the ticket to review status, latest reply, requested information, and next action.
6. Reply in the existing ticket thread instead of opening a duplicate ticket.

## Solved Versus Closed

Verify current Redis Support Portal behavior before promising exact timing, but use this lifecycle model when explaining status:

- `Solved`: the case is treated as resolved or waiting without recent activity. Replying usually reopens the same ticket.
- `Closed`: the original case can no longer be reopened directly. Replying usually creates a follow-up ticket linked to the original.

When a user still needs help:

- If the ticket is `Solved`, reply in the same ticket with a short update, new evidence, or when logs will be available.
- If the ticket is `Closed`, reply with a concise summary and the new evidence; expect a follow-up ticket that references the prior case.
- If artifacts may have expired or been omitted, attach fresh logs, support packages, screenshots, or timestamps as needed.
- If the issue is not resolved but the user is still gathering data, advise sending a brief status update before closure.

## Visibility Troubleshooting

| Problem | Likely cause | Action |
| --- | --- | --- |
| Ticket number search finds only articles | User searched Help Center, not My Requests. | Sign in and open My Requests. |
| Ticket is missing | User signed in with the wrong email. | Try the original submission email. |
| Teammate's ticket is not visible | User is not requester or CC. | Ask requester to add the user as CC. |
| User wants to reply | Reply belongs in the existing ticket thread. | Open ticket from My Requests and reply there. |
| Ticket is `Solved` | It may reopen on reply. | Reply with the update and requested evidence. |
| Ticket is `Closed` | Follow-up case may be created. | Include original ticket number and current impact. |
| User has only email notification | Use ticket number, subject, date, and requester email to locate it. |

## Privacy Boundaries

- Do not ask for logs, screenshots, or ticket contents unless they are needed for the task.
- If asking for a ticket number or subject, remind the user to redact sensitive customer data.
- Do not suggest bypassing ticket visibility rules; private tickets protect troubleshooting history and customer information.

## Escalation Packet

If the ticket still cannot be found, collect:

- Ticket number from email notification.
- Ticket subject.
- Email address used to submit the request.
- Whether the user is requester or CC.
- Date opened and product/deployment involved.
- Screenshot of the portal error or empty view with sensitive data redacted.
- Whether a teammate opened the request.
