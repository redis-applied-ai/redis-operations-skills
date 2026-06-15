---
name: redis-cloud-privacy-deletion-request
description: Use when a Redis Cloud user wants permanent personal-data erasure, GDPR or CCPA account deletion, privacy deletion form guidance, final Redis Cloud account erasure after cleanup, or help resolving blockers such as remaining databases, subscriptions, users, API keys, payment methods, unpaid balances, missing owner permissions, or no deletion confirmation email.
---

# Redis Cloud Privacy Deletion Request

Use this skill for the final privacy/data-erasure request after a Redis Cloud account has already been cleaned up. For resource cleanup before erasure, use `redis-cloud-delete-account`.

## Scope Boundary

- Privacy deletion is not the same as canceling one subscription.
- Privacy deletion is not complete until Redis confirms the erasure request.
- Only the Account Owner should submit the request for an account.
- Do not request secrets, full payment card numbers, CVV, passwords, or API key values.
- Redis may retain required billing or operational records according to legal obligations; do not promise deletion of legally retained records.

## Pre-Request Checklist

Before directing the user to submit a privacy request, confirm:

1. All databases are deleted or intentionally retained elsewhere.
2. All subscriptions are deleted or canceled as appropriate.
3. Other users have been removed from the account.
4. User and account API keys have been deleted.
5. Outstanding invoices or unpaid balances are resolved.
6. Payment methods and marketplace links have been removed or disconnected.
7. The requester is the Account Owner.

If any item is not true, route back to `redis-cloud-delete-account` or the relevant billing/marketplace skill before submitting the privacy request.

## Request Workflow

1. Have the Account Owner review the current Redis Privacy Policy.
2. Open the official Redis privacy request form.
3. Select account deletion or data erasure as the request type.
4. Provide non-secret identifiers that help locate the account:
   - primary account email
   - alternate emails that may have been used
   - account ID if available
   - organization or team name
5. Submit the request and watch for email confirmation.
6. If Redis asks for cleanup or billing follow-up, resolve those blockers and reply through the privacy workflow.
7. Keep the final confirmation email as the completion record.

## Common Blockers

| Symptom | Likely blocker | Guidance |
| --- | --- | --- |
| Request is rejected | Databases, subscriptions, users, or API keys remain. | Complete account cleanup first. |
| Form cannot be submitted | Requester is not the Account Owner or required fields are incomplete. | Use the owner account or resolve account access first. |
| Deletion is delayed | Unpaid invoices or active billing relationship remain. | Clear balances and disconnect payment or marketplace links. |
| User only wants their seat removed | They are not trying to erase the whole account. | Ask an Account Owner to remove the user from Access Management. |
| No confirmation email | Request may still be under review or email filtering hid it. | Check spam/junk, then contact Redis Support if several business days pass. |

## Response Pattern

When responding, state:

1. Whether this is subscription cancellation, account closure, or privacy deletion.
2. Which prerequisites still need to be cleared.
3. Who must take the next action.
4. What non-secret identifiers are appropriate for the privacy request.
5. What confirmation or rejection signal to expect next.
