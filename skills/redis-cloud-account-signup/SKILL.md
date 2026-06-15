---
name: redis-cloud-account-signup
description: "Guide Redis Cloud account creation and troubleshoot signup, activation, social login, invitation, account-exists, AWS Marketplace signup, and Google Cloud Marketplace signup flows. Use when the user asks to create a Redis Cloud account, did not receive verification email, has an expired signup link, sees Account already exists, wants to use Google/GitHub login, or is signing up through AWS or GCP Marketplace."
---

# Redis Cloud Account Signup

Use this skill for Redis Cloud account onboarding before subscription and database creation.

## Current-State Rule

Signup URLs, social-login behavior, marketplace listing names, and cloud marketplace flows can change. Verify live Redis Cloud and marketplace UI if exact current steps matter.

## Direct Signup Workflow

1. Ask whether the user is creating a direct Redis Cloud account or signing up through AWS/GCP Marketplace.
2. For direct signup:
   - Open the Redis Cloud signup page.
   - Choose email/password or social login.
   - Submit name, email, and password if using email signup.
   - Verify the email using the activation message.
   - Open the Redis Cloud Console.
   - Continue to subscription and first database creation.

## Marketplace Signup Workflow

AWS Marketplace:

1. Subscribe to the Redis Cloud product through AWS Marketplace.
2. Follow the redirect to Redis Cloud.
3. Log in or create a Redis Cloud account.
4. Confirm the Redis Cloud account maps to the AWS Marketplace subscription.

Google Cloud Marketplace:

1. Subscribe from the Redis Cloud listing in Google Cloud Marketplace.
2. Continue to the Redis Cloud portal.
3. Create or select the Redis Cloud account.
4. Link it to the intended GCP billing/project context.

Use the dedicated AWS or GCP Marketplace skills for detailed billing mapping and troubleshooting.

## Account Behavior

- A direct Redis Cloud account is tied to one email address.
- The same email cannot create multiple independent direct accounts.
- Plus addressing can be used when the organization permits it.
- Invitations can override account creation: an invited email joins the existing account.
- Social login creates, joins, or logs into an account depending on whether the email is new, invited, or already registered.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Verification email missing | Check spam/junk; resend from signup if available. |
| Signup link expired | Restart signup from the current signup page. |
| Social login fails | Confirm permissions were accepted and the social account email matches the intended Redis Cloud identity. |
| Account already exists | Log in instead; use password reset if needed. |
| User joins existing account unexpectedly | Check whether that email had a pending invitation. |
| Marketplace mapping missing | Verify the marketplace subscription and account mapping path. |

## Safety Checks

- Do not ask for passwords or MFA codes.
- Confirm whether the user intends to create a new account or join an existing organization.
- For marketplace signup, verify the billing account/project before mapping to avoid billing the wrong entity.

## Handoff

After successful signup, guide the user to:

- Choose a subscription.
- Select provider/region.
- Create the first database.
- Configure team members, billing, and security settings.
