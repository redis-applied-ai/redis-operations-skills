---
name: redis-cloud-flex-vat-gst-error
description: "Fix generic Redis Cloud Flex database creation failures caused by VAT or GST ID formatting. Use when the user sees An error occurred while creating a Redis Cloud Flex database, has VAT/GST configured, needs to edit Account Settings Contacts and Business Information, remove spaces from tax IDs, shorten long VAT/GST values, or escalate provisioning failures after billing-profile validation."
---

# Redis Cloud Flex VAT GST Error

Use this skill when Redis Cloud Flex database creation fails with a generic error and the account has VAT or GST information configured.

## Safety Rules

- Do not ask the user to paste full tax IDs unless strictly needed; prefer asking whether spaces, punctuation, or excessive length are present.
- Treat VAT/GST values and billing profile screenshots as sensitive business information.
- If the issue does not involve VAT/GST configuration, switch to a general Redis Cloud provisioning triage path.

## Triage Trigger

Use this workflow when all are true:

- The user is creating a Redis Cloud Flex database.
- The UI shows a generic `An error occurred` message.
- The account has a VAT or GST ID configured in billing/contact information.

## Fix Workflow

1. Ask the user to open Redis Cloud Console.
2. Go to `Account Settings`.
3. Open `Contacts & Business Information`, then `Contact Information`.
4. Find the `VAT / GST ID` field.
5. Update the value:
   - Remove spaces.
   - Remove unnecessary separators.
   - Keep the required country code and alphanumeric ID.
   - Keep the value under the backend-friendly length, roughly 32 characters or less.
6. Save changes.
7. Refresh the browser session.
8. Retry Redis Cloud Flex database creation.

Example formatting:

```text
GB 123 456 789 -> GB123456789
```

## Permission Handling

If the user cannot edit contact information:

- They likely lack account or billing permissions.
- Ask the Account Owner, billing owner, or account administrator to update the VAT/GST field.
- Retry database creation after the billing profile change is saved.

## Verification

Confirm:

- Flex database creation completes.
- The database reaches active state.
- The generic error no longer appears.
- Basic connectivity works after creation.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Error persists after removing spaces | Confirm official country format and remove punctuation not required by the format. |
| VAT/GST value is very long | Shorten to the minimum valid country-specific representation. |
| User cannot edit field | Account permissions or billing-owner role missing. |
| Error persists with valid VAT/GST | Treat as a separate provisioning issue and escalate. |

## Escalation Packet

Collect:

- Redis Cloud account ID.
- Region, subscription, and intended Flex database settings.
- Timestamp of failed creation.
- Screenshot of the generic error with sensitive details redacted.
- Whether VAT/GST had spaces, punctuation, or excessive length.
- Confirmation that contact information was saved and browser refreshed.
- User role or permission level.
